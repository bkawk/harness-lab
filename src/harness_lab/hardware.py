from __future__ import annotations

import os
import platform
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
            "environment_hint": self.environment_hint,
        }


def hardware_profile_path(memory_dir: Path) -> Path:
    return memory_dir / "hardware_profile.json"


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
