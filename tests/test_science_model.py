import torch

from harness_lab.science_model import CompactPointModel, gather_neighbors, knn_indices


def test_knn_indices_handles_single_point():
    points = torch.zeros(2, 1, 3)

    indices = knn_indices(points, k=8)

    assert indices.shape == (2, 1, 1)
    assert torch.equal(indices, torch.zeros_like(indices))


def test_gather_neighbors_returns_expected_shape():
    x = torch.randn(2, 5, 4)
    indices = torch.tensor(
        [
            [[1, 2], [0, 2], [0, 1], [1, 2], [2, 3]],
            [[1, 2], [0, 2], [0, 1], [1, 2], [2, 3]],
        ]
    )

    gathered = gather_neighbors(x, indices)

    assert gathered.shape == (2, 5, 2, 4)


def test_compact_point_model_forward_shapes():
    model = CompactPointModel(
        num_classes=4,
        param_dim=3,
        hidden_dim=32,
        global_dim=48,
        instance_dim=8,
        k_neighbors=3,
        instance_modulation_scale=0.1,
    )
    points = torch.randn(2, 6, 3)
    normals = torch.randn(2, 6, 3)

    logits, params, boundary, instance = model(points, normals)

    assert logits.shape == (2, 6, 4)
    assert params.shape == (2, 6, 3)
    assert boundary.shape == (2, 6)
    assert instance.shape == (2, 6, 8)
