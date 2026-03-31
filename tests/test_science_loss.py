import torch

from harness_lab.science_backend import ScienceConfig
from harness_lab.science_loss import compute_instance_loss, compute_loss


def test_compute_instance_loss_returns_zero_when_no_valid_instances():
    instance_embed = torch.randn(1, 4, 8)
    labels = torch.tensor([[0, 1, 1, 0]])
    instance_ids = torch.full((1, 4), -1)

    loss = compute_instance_loss(instance_embed, labels, instance_ids, margin=0.35)

    assert loss.item() == 0.0


def test_compute_loss_returns_component_metrics():
    cfg = ScienceConfig()
    logits = torch.randn(1, 3, 4)
    param_pred = torch.randn(1, 3, 2)
    boundary_logits = torch.randn(1, 3)
    instance_embed = torch.randn(1, 3, cfg.instance_dim)
    batch = {
        "labels": torch.tensor([[1, 2, 0]]),
        "params": torch.randn(1, 3, 2),
        "param_mask": torch.ones(1, 3, 2),
        "boundary": torch.tensor([[0.0, 1.0, 0.0]]),
        "instance_ids": torch.tensor([[0, 1, -1]]),
    }

    loss, metrics = compute_loss(
        logits,
        param_pred,
        boundary_logits,
        instance_embed,
        batch,
        param_scale=torch.ones(2),
        cfg=cfg,
    )

    assert loss.ndim == 0
    assert metrics.keys() == {"loss", "cls_loss", "param_loss", "boundary_loss", "instance_loss"}
    assert metrics["loss"] >= 0.0
