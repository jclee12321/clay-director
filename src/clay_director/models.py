"""Core data schemas for sequences, shots, cameras, and render settings."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CameraSpec:
    """Camera lens and motion metadata for a single shot."""

    focal_length_mm: float
    f_stop: float
    movement: str = "locked"
    focus_pull: str | None = None


@dataclass(frozen=True)
class RenderSettings:
    """Output video technical settings."""

    width: int = 1280
    height: int = 720
    aspect_ratio: str = "16:9"
    fps: int = 24


@dataclass(frozen=True)
class ShotSpec:
    """Structured metadata describing one shot in a storyboard sequence."""

    shot_id: str
    title: str
    duration_sec: float
    camera: CameraSpec
    visual_summary: str
    lighting: str
    action_beats: list[str]
    reference_assets: list[str] = field(default_factory=list)
    audio_notes: str = ""

    def frame_count(self, fps: int = 24) -> int:
        return int(round(self.duration_sec * fps))


@dataclass(frozen=True)
class SequenceSpec:
    """An ordered sequence of shots."""

    sequence_id: str
    project_name: str
    fps: int
    shots: list[ShotSpec]
    render_settings: RenderSettings = field(default_factory=RenderSettings)

    @property
    def total_duration_sec(self) -> float:
        return round(sum(s.duration_sec for s in self.shots), 3)

    @property
    def total_frames(self) -> int:
        return sum(s.frame_count(self.fps) for s in self.shots)
