"""ClayDirector: Open-source 3D previs and generative video pipeline toolkit."""

from .models import CameraSpec, RenderSettings, SequenceSpec, ShotSpec
from .prompt_builder import build_shot_prompt
from .storyboard import load_sequence, validate_sequence

__all__ = [
    "CameraSpec",
    "RenderSettings",
    "SequenceSpec",
    "ShotSpec",
    "build_shot_prompt",
    "load_sequence",
    "validate_sequence",
]

__version__ = "0.1.0"
