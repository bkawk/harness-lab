from __future__ import annotations

from typing import TYPE_CHECKING

import torch
import torch.nn.functional as F

if TYPE_CHECKING:
    from harness_lab.science_config import ScienceConfig


def compute_instance_loss(instance_embed: torch.Tensor, labels: torch.Tensor, instance_ids: torch.Tensor, margin: float) -> torch.Tensor:
    valid = instance_ids >= 0
    if not valid.any():
        return instance_embed.new_zeros(())
    similarity = torch.matmul(instance_embed, instance_embed.transpose(1, 2))
    same_instance = (instance_ids.unsqueeze(2) == instance_ids.unsqueeze(1)) & valid.unsqueeze(2) & valid.unsqueeze(1)
    same_class = labels.unsqueeze(2) == labels.unsqueeze(1)
    eye = torch.eye(labels.size(1), device=labels.device, dtype=torch.bool).unsqueeze(0)
    positive_mask = same_instance & ~eye
    negative_mask = same_class & ~same_instance & valid.unsqueeze(2) & valid.unsqueeze(1)
    total = instance_embed.new_zeros(())
    positive = (1.0 - similarity)[positive_mask]
    if positive.numel() > 0:
        total = total + positive.mean()
    negative = F.relu(similarity - margin)[negative_mask]
    if negative.numel() > 0:
        total = total + negative.mean()
    return total


def compute_loss(
    logits: torch.Tensor,
    param_pred: torch.Tensor,
    boundary_logits: torch.Tensor,
    instance_embed: torch.Tensor,
    batch: dict[str, torch.Tensor],
    *,
    param_scale: torch.Tensor,
    cfg: ScienceConfig,
) -> tuple[torch.Tensor, dict[str, float]]:
    cls_loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), batch["labels"].reshape(-1))
    scale = param_scale.view(1, 1, -1)
    param_error = F.smooth_l1_loss(param_pred / scale, batch["params"] / scale, reduction="none")
    param_loss = (param_error * batch["param_mask"]).sum() / batch["param_mask"].sum().clamp(min=1.0)
    boundary_pos = batch["boundary"].mean().clamp(min=1e-3, max=1.0 - 1e-3)
    pos_weight = ((1.0 - boundary_pos) / boundary_pos).detach()
    boundary_loss = F.binary_cross_entropy_with_logits(boundary_logits, batch["boundary"], pos_weight=pos_weight)
    instance_loss = compute_instance_loss(instance_embed, batch["labels"], batch["instance_ids"], cfg.instance_margin)
    # Keep the existing loss recipe, but modestly strengthen transfer-sensitive terms
    # when the batch actually contains sparse boundary structure and valid instances.
    boundary_focus = (1.0 + 0.25 * (1.0 - boundary_pos)).detach()
    valid_instance_fraction = (batch["instance_ids"] >= 0).float().mean().clamp(min=0.0, max=1.0)
    instance_focus = (1.0 + 0.15 * valid_instance_fraction).detach()
    loss = (
        cls_loss
        + cfg.param_loss_weight * param_loss
        + cfg.boundary_loss_weight * boundary_focus * boundary_loss
        + cfg.instance_loss_weight * instance_focus * instance_loss
    )
    return loss, {
        "loss": float(loss.detach().item()),
        "cls_loss": float(cls_loss.detach().item()),
        "param_loss": float(param_loss.detach().item()),
        "boundary_loss": float(boundary_loss.detach().item()),
        "instance_loss": float(instance_loss.detach().item()),
    }
