from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class CompactPointModel(nn.Module):
    def __init__(
        self,
        num_classes: int,
        param_dim: int,
        hidden_dim: int,
        global_dim: int,
        instance_dim: int,
        k_neighbors: int,
        instance_modulation_scale: float,
    ):
        super().__init__()
        self.k_neighbors = k_neighbors
        self.instance_modulation_scale = instance_modulation_scale
        self.point_encoder = nn.Sequential(
            nn.Linear(6, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
        )
        self.local_mlp = nn.Sequential(
            nn.Linear((2 * hidden_dim) + 6, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
        )
        self.global_proj = nn.Sequential(
            nn.Linear(2 * hidden_dim, global_dim),
            nn.ReLU(),
        )
        fused_dim = (2 * hidden_dim) + global_dim
        self.classifier = nn.Sequential(
            nn.Linear(fused_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, num_classes),
        )
        self.param_head = nn.Sequential(
            nn.Linear(fused_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, param_dim),
        )
        self.boundary_head = nn.Sequential(
            nn.Linear(fused_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )
        self.instance_class_proj = nn.Linear(num_classes, fused_dim)
        self.instance_head = nn.Sequential(
            nn.Linear(fused_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, instance_dim),
        )

    def forward(self, points: torch.Tensor, normals: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        features = self.point_encoder(torch.cat([points, normals], dim=-1))
        neighbor_idx = knn_indices(points, self.k_neighbors)
        neighbor_feat = gather_neighbors(features, neighbor_idx)
        neighbor_points = gather_neighbors(points, neighbor_idx)
        neighbor_normals = gather_neighbors(normals, neighbor_idx)
        center_feat = features.unsqueeze(2).expand_as(neighbor_feat)
        rel_points = neighbor_points - points.unsqueeze(2)
        rel_normals = neighbor_normals - normals.unsqueeze(2)
        edge_feat = torch.cat([center_feat, neighbor_feat - center_feat, rel_points, rel_normals], dim=-1)
        local_feat = self.local_mlp(edge_feat).max(dim=2).values
        global_max = local_feat.max(dim=1, keepdim=True).values
        global_mean = local_feat.mean(dim=1, keepdim=True)
        global_feat = self.global_proj(torch.cat([global_max, global_mean], dim=-1))
        fused = torch.cat([features, local_feat, global_feat.expand(-1, points.size(1), -1)], dim=-1)
        logits = self.classifier(fused)
        params = self.param_head(fused)
        boundary = self.boundary_head(fused).squeeze(-1)
        class_context = self.instance_class_proj(F.softmax(logits, dim=-1))
        instance_input = fused + (self.instance_modulation_scale * class_context)
        instance = F.normalize(self.instance_head(instance_input), dim=-1)
        return logits, params, boundary, instance


def knn_indices(points: torch.Tensor, k: int) -> torch.Tensor:
    num_points = points.size(1)
    if num_points <= 1:
        return torch.zeros((points.size(0), num_points, 1), dtype=torch.long, device=points.device)
    k = max(1, min(k, num_points - 1))
    with torch.no_grad():
        dist = torch.cdist(points, points)
        _, indices = dist.topk(k + 1, dim=-1, largest=False)
    return indices[:, :, 1:]


def gather_neighbors(x: torch.Tensor, indices: torch.Tensor) -> torch.Tensor:
    batch_size, num_points, channels = x.shape
    k = indices.size(-1)
    batch_idx = torch.arange(batch_size, device=x.device).view(batch_size, 1, 1).expand(-1, num_points, k)
    return x[batch_idx, indices]
