"""Generic template-based structured prompt builder."""

from __future__ import annotations

from .models import SequenceSpec, ShotSpec


def build_shot_prompt(seq: SequenceSpec, shot: ShotSpec) -> str:
    """Assemble a clean structured shot description from storyboard metadata."""
    refs = ", ".join(shot.reference_assets) if shot.reference_assets else "None"
    cam = shot.camera
    cam_desc = f"{cam.focal_length_mm:.0f}mm, f/{cam.f_stop:.1f}, movement={cam.movement}"
    if cam.focus_pull:
        cam_desc += f", focus_pull={cam.focus_pull}"

    beats = "\n".join(f"  - {b}" for b in shot.action_beats)
    lines = [
        f"Shot: {shot.shot_id} — {shot.title}",
        f"Format: {seq.render_settings.aspect_ratio}, {shot.duration_sec:.1f}s @ {seq.fps}fps",
        f"Camera: {cam_desc}",
        f"References: {refs}",
        f"Visual Summary: {shot.visual_summary}",
        f"Lighting: {shot.lighting}",
        f"Action Beats:\n{beats}",
    ]
    if shot.audio_notes:
        lines.append(f"Audio Notes: {shot.audio_notes}")
    return "\n".join(lines)
