"""Unit tests for ClayDirector."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from clay_director.blender_scene import DEFAULT_NEUTRAL_GRAY
from clay_director.cli import main as cli_main
from clay_director.media_utils import build_ffmpeg_encode_command
from clay_director.prompt_builder import build_shot_prompt
from clay_director.storyboard import load_sequence, validate_sequence

DEMO_JSON = ROOT / "examples" / "demo_sequence.json"


class TestClayDirector(unittest.TestCase):
    def test_load_and_validate_demo_sequence(self) -> None:
        seq = load_sequence(DEMO_JSON)
        self.assertEqual(seq.fps, 24)
        self.assertEqual(len(seq.shots), 3)
        self.assertAlmostEqual(seq.total_duration_sec, 13.0)
        self.assertEqual(seq.total_frames, 312)
        self.assertEqual(validate_sequence(seq), [])

    def test_build_shot_prompt(self) -> None:
        seq = load_sequence(DEMO_JSON)
        prompt = build_shot_prompt(seq, seq.shots[1])
        self.assertIn("DEMO-02", prompt)
        self.assertIn("85mm, f/2.0", prompt)
        self.assertIn("Prop_Ceramic_Teacup", prompt)

    def test_ffmpeg_command_builder(self) -> None:
        seq = load_sequence(DEMO_JSON)
        cmd = build_ffmpeg_encode_command(
            "renders/frame_%04d.png", "exports/DEMO-01.mp4", seq.shots[0], seq.render_settings
        )
        joined = " ".join(cmd)
        self.assertIn("-framerate 24", joined)
        self.assertIn("-frames:v 96", joined)
        self.assertIn("scale=1280:720:flags=lanczos", joined)

    def test_neutral_gray_constant(self) -> None:
        self.assertEqual(DEFAULT_NEUTRAL_GRAY[0], DEFAULT_NEUTRAL_GRAY[1])
        self.assertEqual(DEFAULT_NEUTRAL_GRAY[1], DEFAULT_NEUTRAL_GRAY[2])

    def test_cli_smoke(self) -> None:
        self.assertEqual(cli_main(["validate", str(DEMO_JSON)]), 0)
        self.assertEqual(cli_main(["build-prompt", str(DEMO_JSON), "--shot", "DEMO-02"]), 0)
        self.assertEqual(cli_main(["plan-encode", str(DEMO_JSON)]), 0)


if __name__ == "__main__":
    unittest.main()
