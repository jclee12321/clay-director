"""Standard FFmpeg command builder for PNG image sequences."""

from __future__ import annotations

from pathlib import Path

from .models import RenderSettings, ShotSpec


def build_ffmpeg_encode_command(
    frame_pattern: str | Path,
    output_mp4: str | Path,
    shot: ShotSpec,
    settings: RenderSettings,
    start_number: int = 1,
) -> list[str]:
    """Generate a clean H.264 FFmpeg command for one rendered shot."""
    frames = shot.frame_count(fps=settings.fps)
    return [
        "ffmpeg",
        "-y",
        "-framerate",
        str(settings.fps),
        "-start_number",
        str(start_number),
        "-i",
        str(frame_pattern),
        "-frames:v",
        str(frames),
        "-vf",
        f"scale={settings.width}:{settings.height}:flags=lanczos",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-crf",
        "18",
        "-movflags",
        "+faststart",
        str(output_mp4),
    ]
