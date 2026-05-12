# 🔉 Airgent Play 2

> **让你的 AI agent，在任何房间的智能音箱上，向你汇报工作。**
>
> AirPlay 2 · DLNA · 本地 TTS。一条命令，所有音箱。
>
> 下载完了？模型跑完了？出 bug 了？你的 agent 不用发文字——它直接开口说给你听。

---

<p align="center">
  <img src="https://img.shields.io/badge/协议-AirPlay%202%2BDLNA-blue">
  <img src="https://img.shields.io/badge/平台-macOS-lightgrey">
  <img src="https://img.shields.io/badge/许可证-MIT-green">
</p>

---

[English](README.md) | 中文

## 这是什么？

你的 AI agent 每天在后台跑一堆任务——定时下载、模型训练、数据处理。但它们只能发文字通知。你得拿起手机、打开飞书、翻消息。

Airgent Play2 给 agent 装了张嘴。任务一完成，agent 直接把结果念给你听——随便哪个房间的音箱都行。

厨房音箱：*「Z-Lib 下载完成，六本书。」*
客厅回音壁：*「数据集处理完毕，2.3TB，零错误。」*
书房监听：*「Remux 有货了——沙丘2，4K HDR，正在做种。」*

## 原理

```
Agent 完成任务
       │
       ▼
airgent-play2 "下载完成：6本书"
       │
       ▼
CosyVoice 3.0（本地 TTS）→ WAV 音频
       │
       ▼
pyatv RAOP 协议 → AirPlay 2 音箱
       │
       ▼
🎵 你听到了。不用看手机。
```

## 快速开始

### 环境要求

- macOS（推荐 Apple Silicon）
- Python 3.12+
- [ffmpeg](https://ffmpeg.org)（`brew install ffmpeg`）
- 同一局域网内至少一台 AirPlay 2 音箱

### 安装

```bash
pip install airgent-play2
```

或从源码安装：

```bash
git clone https://github.com/rockeverm3m/airgent-play2.git
cd airgent-play2
pip install -e .
```

### 第一次使用

```bash
# 列出你家的 AirPlay 音箱
airgent-play2 --list

# 推送到第一个可用的音箱
airgent-play2 "你好，我是你的 agent，现在可以说话了"

# 指定音箱
airgent-play2 "下载完成了" --device JBL
```

---

## Agent 集成指南

Airgent Play2 设计为**任何 agent 框架都能用**。四种集成方式，选你顺手的：

### 方式 1：Shell 命令（通用）

任何能执行 shell 命令的 agent：

```bash
airgent-play2 "Z-Lib 下载完成：6本书"
```

适用于：**Claude Code、OpenAI Codex CLI、OpenCode、cron 任务、bash 脚本。**

### 方式 2：Python 模块

有 Python 运行环境的 agent 或脚本：

```python
from airgent_play2 import notify, speak

# 快速通知
notify("模型训练完成——准确率 97.3%")

# 指定设备
speak("服务器 CPU 达到 95%", device="JBL")
```

适用于：**Hermes Agent、LangChain agent、自定义 Python 脚本。**

### 方式 3：管道输入

任何产出文本的脚本：

```bash
python train_model.py 2>&1 | tail -1 | airgent-play2 -
# 或
echo "$(cat /tmp/result.txt)" | airgent-play2 -
```

适用于：**任意 CLI 工具、shell 脚本、Makefile。**

### 方式 4：HTTP Webhook（计划中）

```bash
curl -X POST localhost:9876/speak -d '{"text": "构建失败"}'
```

*v0.2.0 上线。*

### 设置默认音箱

```bash
# 当前会话生效
export AIRGENT_DEVICE="Genelec"

# 永久生效（加入 ~/.zshrc）
echo 'export AIRGENT_DEVICE="Genelec"' >> ~/.zshrc
```

之后每次 `airgent-play2` 都默认推送到这台音箱。

### Agent 提示词模板

把这段写进你的 agent 系统提示词或 cron 描述里：

```
任务完成后，通过 Airgent Play2 语音通知我：
  airgent-play2 "简短的结果摘要（不超过80字）"

通知保持简洁、只讲事实。格式示例：
  "Z-Lib：已下载6本书"
  "数据集：FineWeb 完成12%，无错误"
  "告警：proxy guard 检测到7890连接"
```

---

## 支持的设备

已测试通过：

| 设备 | 类型 | 协议 |
|------|------|------|
| JBL BAR 1300 | 回音壁 | AirPlay + DLNA |
| Genelec G2 | 监听音箱 | AirPlay + DLNA |
| HomePod Mini | 智能音箱 | AirPlay |
| Apple TV 4K | 媒体中心 | AirPlay |
| 小米电视 S Pro | 智能电视 | AirPlay + DLNA |
| Z9X PRO | 播放器 | AirPlay + DLNA |

任何 AirPlay 2 兼容音箱理论上都能用。跑 `airgent-play2 --list` 看看你家的。

---

## 音色自定义

Airgent Play2 使用 **CosyVoice 3.0** 做本地 TTS，支持零样本音色克隆。

### 用自己的声音

```python
from airgent_play2 import speak

# 用一段简短 WAV 录音克隆音色
speak("你的通知内容", voice_prompt_audio="/path/to/voice_sample.wav")
```

### 系统音色兜底（仅 macOS）

如果 CosyVoice 没装，自动降级到 macOS `say` 命令。

```bash
# 安装 CosyVoice（推荐中文场景）
# 首次运行自动提示，或手动：
airgent-play2 --setup-tts
```

---

## 架构

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  任意 Agent   │ ──▶ │ Airgent Play2 │ ──▶ │  AirPlay 2  │
│ (shell/py)   │     │   ┌────────┐ │     │    音箱      │
│              │     │   │  TTS   │ │     │             │
│  "消息"  ────┼────▶│   │CosyVoic│─┼────▶│  🎵 "消息"  │
│              │     │   └────────┘ │     │             │
└─────────────┘     └──────────────┘     └─────────────┘
```

## 常见问题

**问：会抢占我电脑的音频输出吗？**
不会。Airgent Play2 用 pyatv 的 RAOP 协议直连音箱推流，Mac 的系统音频完全不碰。

**问：TTS 支持哪些语言？**
CosyVoice 3.0 原生支持中文。英文和其他语言也能用但质量不一。纯英文场景用 macOS `say` 兜底更稳。

**问：断网能用吗？**
能。全程本地运行——TTS 生成、音频编码、AirPlay 推流都不需要外网。

**问：多个 agent 能同时用吗？**
能。通知管线无状态，多个 agent 或 cron 任务可以同时调 `airgent-play2`。

**问：音箱搜不到？**
确保音箱在同一 Wi-Fi，AirPlay 已开启。跑 `airgent-play2 --list` 排查。

---

## 路线图

- [ ] Docker 镜像，支持无头 Linux 服务器
- [ ] HTTP Webhook 端点
- [ ] 多房间同步广播
- [ ] 音色预设库
- [ ] Windows 支持（DLNA 降级）

## 许可证

MIT — 详见 [LICENSE](LICENSE)。

---

<p align="center">
  <sub>为那些值得被听到的 agent 而建。</sub>
</p>
