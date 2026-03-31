from __future__ import annotations

from harness_lab.hardware import HardwareProfile


def test_hardware_profile_serializes_gpu_fields():
    profile = HardwareProfile(
        hostname="lab-box",
        platform_name="Linux",
        platform_release="6.0",
        machine="x86_64",
        cpu_count=24,
        load_average=(1.0, 0.5, 0.25),
        memory_gb_estimate=91.3,
        cuda_available=True,
        gpu_count=1,
        gpu_name="RTX Test",
        gpu_memory_total_gb=7.62,
        gpu_memory_free_gb=1.25,
        environment_hint="linux_or_remote",
    )
    payload = profile.to_dict()
    assert payload["cuda_available"] is True
    assert payload["gpu_count"] == 1
    assert payload["gpu_name"] == "RTX Test"
    assert payload["gpu_memory_total_gb"] == 7.62
    assert payload["gpu_memory_free_gb"] == 1.25
