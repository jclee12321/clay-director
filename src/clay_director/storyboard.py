"""Storyboard JSON loader and 24fps timeline validator."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import CameraSpec, RenderSettings, SequenceSpec, ShotSpec


def load_sequence(path: str | Path) -> SequenceSpec:
    """Load a SequenceSpec from a JSON storyboard file."""
    raw: dict[str, Any] = json.loads(Path(path).read_text(encoding="utf-8"))
    rs_raw = raw.get("render_settings", {})
    render_settings = RenderSettings(**rs_raw) if rs_raw else RenderSettings()

    shots: list[ShotSpec] = []
    for item in raw["shots"]:
        cam = CameraSpec(**item["camera"])
        shots.append(
            ShotSpec(
                shot_id=item["shot_id"],
                title=item["title"],
                duration_sec=float(item["duration_sec"]),
                camera=cam,
                visual_summary=item["visual_summary"],
                lighting=item["lighting"],
                action_beats=list(item["action_beats"]),
                reference_assets=list(item.get("reference_assets", [])),
                audio_notes=item.get("audio_notes", ""),
            )
        )

    return SequenceSpec(
        sequence_id=raw["sequence_id"],
        project_name=raw["project_name"],
        fps=int(raw.get("fps", 24)),
        shots=shots,
        render_settings=render_settings,
    )


def validate_sequence(seq: SequenceSpec) -> list[str]:
    """Validate sequence metadata, frame alignment, and shot ID uniqueness."""
    issues: list[str] = []

    if seq.fps <= 0:
        issues.append(f"[ERROR] Invalid fps: {seq.fps}")

    seen: set[str] = set()
    for shot in seq.shots:
        if shot.shot_id in seen:
            issues.append(f"[ERROR] Duplicate shot_id: {shot.shot_id}")
        seen.add(shot.shot_id)

        if shot.duration_sec <= 0:
            issues.append(f"[ERROR] {shot.shot_id}: duration_sec must be positive.")

        exact_frames = shot.duration_sec * seq.fps
        if abs(exact_frames - round(exact_frames)) > 1e-4:
            issues.append(
                f"[WARN] {shot.shot_id}: duration {shot.duration_sec}s is not frame-aligned at {seq.fps}fps."
            )

        if not shot.action_beats:
            issues.append(f"[WARN] {shot.shot_id}: no action_beats defined.")

    return issues
