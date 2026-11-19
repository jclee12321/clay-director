"""Command-line interface for ClayDirector."""

from __future__ import annotations

import argparse
from pathlib import Path
import shlex
import sys

from .media_utils import build_ffmpeg_encode_command
from .prompt_builder import build_shot_prompt
from .storyboard import load_sequence, validate_sequence


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="clay-director",
        description="Open-source 3D previs and generative video pipeline CLI.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_val = sub.add_parser("validate", help="Validate storyboard JSON and 24fps alignment.")
    p_val.add_argument("sequence", help="Path to sequence JSON file.")

    p_prompt = sub.add_parser("build-prompt", help="Assemble structured shot prompt(s).")
    p_prompt.add_argument("sequence", help="Path to sequence JSON file.")
    p_prompt.add_argument("--shot", help="Optional single shot_id.")

    p_enc = sub.add_parser("plan-encode", help="Print FFmpeg H.264 encoding commands.")
    p_enc.add_argument("sequence", help="Path to sequence JSON file.")
    p_enc.add_argument("--frames-dir", default="./renders", help="Directory containing PNG frames.")
    p_enc.add_argument("--out-dir", default="./exports", help="Output directory for MP4 clips.")

    args = parser.parse_args(argv)
    seq = load_sequence(args.sequence)

    if args.command == "validate":
        issues = validate_sequence(seq)
        print(
            f"Sequence '{seq.sequence_id}' ({seq.project_name}): "
            f"{len(seq.shots)} shots, {seq.total_duration_sec:.1f}s ({seq.total_frames} frames @ {seq.fps}fps)"
        )
        for shot in seq.shots:
            print(
                f"  - {shot.shot_id} | {shot.duration_sec:.1f}s ({shot.frame_count(seq.fps)}f) | "
                f"{shot.camera.focal_length_mm:.0f}mm f/{shot.camera.f_stop:.1f} ({shot.camera.movement})"
            )
        if issues:
            for msg in issues:
                print(f"  {msg}")
            return 1 if any(m.startswith("[ERROR]") for m in issues) else 0
        print("Validation passed with 0 issues.")
        return 0

    if args.command == "build-prompt":
        targets = [s for s in seq.shots if not args.shot or s.shot_id == args.shot]
        if not targets:
            print(f"Shot '{args.shot}' not found.", file=sys.stderr)
            return 2
        for idx, shot in enumerate(targets):
            if idx > 0:
                print("\n" + "-" * 60 + "\n")
            print(build_shot_prompt(seq, shot))
        return 0

    if args.command == "plan-encode":
        frames_dir = Path(args.frames_dir)
        out_dir = Path(args.out_dir)
        start = 1
        for shot in seq.shots:
            cmd = build_ffmpeg_encode_command(
                frame_pattern=frames_dir / "frame_%04d.png",
                output_mp4=out_dir / f"{shot.shot_id}.mp4",
                shot=shot,
                settings=seq.render_settings,
                start_number=start,
            )
            print(f"# {shot.shot_id} ({shot.title})")
            print(" ".join(shlex.quote(part) for part in cmd))
            start += shot.frame_count(seq.fps)
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
