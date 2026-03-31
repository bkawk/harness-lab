from __future__ import annotations

import os
import platform
import subprocess
from dataclasses import dataclass
from pathlib import Path

from harness_lab.memory import read_json
from harness_lab.workspace import write_json


@dataclass(frozen=True)
class HardwareProfile:
    hostname: str
    platform_name: str
    platform_release: str
    machine: str
    cpu_count: int
    load_average: tuple[float, float, float] | None
    memory_gb_estimate: float | None
    cuda_available: bool
    gpu_count: int
    gpu_name: str
    gpu_memory_total_gb: float | None
    gpu_memory_free_gb: float | None
    environment_hint: str

    def to_dict(self) -> dict:
        return {
            "hostname": self.hostname,
            "platform_name": self.platform_name,
            "platform_release": self.platform_release,
            "machine": self.machine,
            "cpu_count": self.cpu_count,
            "load_average": list(self.load_average) if self.load_average is not None else None,
            "memory_gb_estimate": self.memory_gb_estimate,
            "cuda_available": self.cuda_available,
            "gpu_count": self.gpu_count,
            "gpu_name": self.gpu_name,
            "gpu_memory_total_gb": self.gpu_memory_total_gb,
            "gpu_memory_free_gb": self.gpu_memory_free_gb,
            "environment_hint": self.environment_hint,
        }


def hardware_profile_path(memory_dir: Path) -> Path:
    return memory_dir / "hardware_profile.json"


def _detect_gpu_profile() -> tuple[bool, int, str, float | None, float | None]:
    try:
        import torch  # type: ignore

        if torch.cuda.is_available():
            device_index = torch.cuda.current_device()
            props = torch.cuda.get_device_properties(device_index)
            free_bytes, total_bytes = torch.cuda.mem_get_info(device_index)
            return (
                True,
                int(torch.cuda.device_count()),
                str(props.name),
                round(total_bytes / (1024**3), 2),
                round(free_bytes / (1024**3), 2),
            )
    except Exception:
        pass

    try:
        completed = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=name,memory.total,memory.free",
                "--format=csv,noheader,nounits",
            ],
            check=True,
            text=True,
            capture_output=True,
        )
        lines = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
        if lines:
            first = [part.strip() for part in lines[0].split(",")]
            name = first[0] if first else ""
            total_gb = round(float(first[1]) / 1024.0, 2) if len(first) > 1 and first[1] else None
            free_gb = round(float(first[2]) / 1024.0, 2) if len(first) > 2 and first[2] else None
            return (True, len(lines), name, total_gb, free_gb)
    except Exception:
        pass

    return (False, 0, "", None, None)


def detect_hardware_profile() -> HardwareProfile:
    load_average = os.getloadavg() if hasattr(os, "getloadavg") else None
    memory_gb_estimate: float | None = None
    if hasattr(os, "sysconf"):
        try:
            page_size = int(os.sysconf("SC_PAGE_SIZE"))
            total_pages = int(os.sysconf("SC_PHYS_PAGES"))
            memory_gb_estimate = round((page_size * total_pages) / (1024**3), 2)
        except (ValueError, OSError):
            memory_gb_estimate = None

    cuda_available, gpu_count, gpu_name, gpu_memory_total_gb, gpu_memory_free_gb = _detect_gpu_profile()

    system = platform.system().lower()
    if "darwin" in system:
        environment_hint = "local_macos"
    elif "linux" in system:
        environment_hint = "linux_or_remote"
    else:
        environment_hint = "unknown_environment"

    return HardwareProfile(
        hostname=platform.node(),
        platform_name=platform.system(),
        platform_release=platform.release(),
        machine=platform.machine(),
        cpu_count=os.cpu_count() or 0,
        load_average=tuple(round(value, 3) for value in load_average) if load_average is not None else None,
        memory_gb_estimate=memory_gb_estimate,
        cuda_available=cuda_available,
        gpu_count=gpu_count,
        gpu_name=gpu_name,
        gpu_memory_total_gb=gpu_memory_total_gb,
        gpu_memory_free_gb=gpu_memory_free_gb,
        environment_hint=environment_hint,
    )


def refresh_hardware_profile(memory_dir: Path) -> HardwareProfile:
    memory_dir.mkdir(parents=True, exist_ok=True)
    profile = detect_hardware_profile()
    write_json(hardware_profile_path(memory_dir), profile.to_dict())
    return profile


def read_hardware_profile(memory_dir: Path) -> dict:
    path = hardware_profile_path(memory_dir)
    if not path.exists():
        return {}
    return read_json(path)
