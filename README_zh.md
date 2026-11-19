# ClayDirector 🎬

**开源 3D 预演与生成式视频管线工具骨架**

> English documentation: [README.md](README.md)

**ClayDirector** 是一个轻量级、模型无关的开源 Python 工具集，用于把结构化分镜数据、Blender 中性灰三维预演、FFmpeg 视频打包与可扩展的生成式视频接口串联为可复现的工程工作流。

## 核心模块

- **分镜与时间轴校验 (`storyboard.py`)**：统一管理镜头编号、24fps 帧数与参考资产清单。
- **Blender 场景辅助 (`blender_scene.py`)**：提供中性灰阻塞材质、相机焦段与景深配置等通用 `bpy` 工具函数。
- **模板化提示词装配 (`prompt_builder.py`)**：基于结构化 JSON 自动拼装镜头描述，减少手工出错。
- **媒体打包 (`media_utils.py`)**：自动生成标准 24fps H.264 FFmpeg 压制命令。

## 快速开始

```bash
pip install -e .
python -m clay_director.cli validate examples/demo_sequence.json
python -m clay_director.cli build-prompt examples/demo_sequence.json --shot DEMO-02
python -m unittest discover -s tests -v
```

## 开源协议

MIT License — 详见 [LICENSE](LICENSE)。
