"""Generic Blender (bpy) helpers for neutral blocking materials and camera DOF.

Safe to import outside Blender so standard Python unit tests run cleanly in CI.
"""

from __future__ import annotations

from typing import Any

try:
    import bpy  # type: ignore
except ImportError:  # pragma: no cover - standard Python environment
    bpy = None


DEFAULT_NEUTRAL_GRAY = (0.5, 0.5, 0.5, 1.0)


def require_blender() -> Any:
    if bpy is None:
        raise RuntimeError(
            "Blender `bpy` is unavailable outside Blender. Run with `blender -b --python <script.py>`."
        )
    return bpy


def create_neutral_material(
    name: str = "NeutralBlockingMat",
    rgba: tuple[float, float, float, float] = DEFAULT_NEUTRAL_GRAY,
    roughness: float = 0.85,
) -> Any:
    """Create or update a simple matte neutral Principled BSDF material."""
    b = require_blender()
    mat = b.data.materials.get(name) or b.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf is not None:
        bsdf.inputs["Base Color"].default_value = rgba
        bsdf.inputs["Roughness"].default_value = roughness
    return mat


def configure_camera_dof(camera_obj: Any, focal_length_mm: float, f_stop: float, focus_distance_m: float) -> None:
    """Set camera focal length and physical depth-of-field parameters."""
    require_blender()
    cam = camera_obj.data
    cam.lens = focal_length_mm
    cam.dof.use_dof = True
    cam.dof.aperture_fstop = f_stop
    cam.dof.focus_distance = max(0.05, focus_distance_m)


def keyframe_collection_visibility(collection: Any, visible: bool, frame: int) -> None:
    """Safely keyframe collection object visibility by copying the live object list."""
    for obj in list(collection.all_objects):
        obj.hide_viewport = not visible
        obj.hide_render = not visible
        obj.keyframe_insert(data_path="hide_viewport", frame=frame)
        obj.keyframe_insert(data_path="hide_render", frame=frame)
