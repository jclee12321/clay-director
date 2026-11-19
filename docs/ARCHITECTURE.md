# ClayDirector Software Architecture

## 1. Design Goals

ClayDirector separates **creative direction data** (storyboards, timing, camera geometry, references) from **execution engines** (Blender, FFmpeg, and external video generation backends):

1. **Zero Lock-In**: All sequence definitions are stored in plain version-controlled JSON.
2. **Deterministic Timeline Math**: Every shot is validated against an exact frame rate (default `24fps`) so downstream editing and previs clips stay frame-accurate.
3. **Runtime Isolation**: Blender helpers (`blender_scene.py`) degrade gracefully when imported in standard Python environments, allowing full CI and unit testing without requiring a Blender GUI process.
4. **Composable CLI**: Each pipeline step (`validate`, `build-prompt`, `plan-encode`) is callable independently or chained in automation scripts.

---

## 2. Core Modules

| Module | Responsibility |
|---|---|
| `models.py` | Immutable dataclasses for `CameraSpec`, `ShotSpec`, `RenderSettings`, and `SequenceSpec`. |
| `storyboard.py` | Loads sequence JSON and checks duplicate IDs, duration bounds, frame alignment, and missing references. |
| `blender_scene.py` | Generic `bpy` utilities for neutral blocking materials, camera focal length/DOF configuration, and safe collection keyframing. |
| `prompt_builder.py` | Compiles structured shot fields into clean, repeatable text prompts for any downstream video model. |
| `media_utils.py` | Generates standardized FFmpeg H.264 encoding commands for PNG render sequences. |
| `cli.py` | Unified command-line interface. |

---

## 3. Planned Extension Points

- **Timeline Bridges**: Exporters/importers for OpenTimelineIO (`.otio`) and CMX 3600 EDL.
- **Provider Plugins**: Abstract base class for submitting render jobs, polling status, and logging metadata across multiple video backends.
- **Automated Verification**: Post-render FFprobe metadata checks and pluggable vision-model QA hooks.
