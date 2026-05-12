# 🔉 Airgent Play 2

> **Let your AI agents talk to you. Through any speaker. In any room.**
>
> AirPlay 2 · DLNA · Local TTS. One command, every speaker.
>
> Task finished? Download done? Bug found? Your agent doesn't text you — it *speaks* to you.

---

<p align="center">
  <img src="https://img.shields.io/badge/protocol-AirPlay%202%2BDLNA-blue" alt="protocol">
  <img src="https://img.shields.io/badge/platform-macOS-lightgrey" alt="platform">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
</p>

---

[English](README.md) | [中文](README.zh-CN.md)

## What is this?

Your AI agents finish background tasks all the time — cron jobs, downloads, model training, data processing. But they can only *text* you. You have to check your phone, open Feishu, scroll through notifications.

Airgent Play2 gives agents a **voice**. When a task completes, your agent speaks the result through any AirPlay 2 speaker in your house.

Kitchen speaker: *"Z-Lib download done — six books."*
Living room soundbar: *"Dataset processing finished — 2.3 TB, zero errors."*
Study monitors: *"Remux found — Dune Part Two, 4K HDR, seeding now."*

## How it works

```
Agent finishes task
       │
       ▼
airgent-play2 "Download complete: 6 books"
       │
       ▼
CosyVoice 3.0 (local TTS) → WAV audio
       │
       ▼
pyatv RAOP → AirPlay 2 speaker
       │
       ▼
🎵 You hear it. No phone required.
```

## Quick Start

### Prerequisites

- macOS (Apple Silicon recommended)
- Python 3.12+
- [ffmpeg](https://ffmpeg.org) (`brew install ffmpeg`)
- One or more AirPlay 2 speakers on the same network

### Install

```bash
pip install airgent-play2
```

Or from source:

```bash
git clone https://github.com/rockeverm3m/airgent-play2.git
cd airgent-play2
pip install -e .
```

### First run

```bash
# List your AirPlay speakers
airgent-play2 --list

# Speak through the first available speaker
airgent-play2 "Hello, this is your agent speaking"

# Target a specific speaker
airgent-play2 "Download finished" --device JBL
```

---

## Agent Integration Guide

Airgent Play2 is designed to work with **any agent framework**. Pick your integration pattern:

### Pattern 1: Shell command (universal)

Any agent that can run shell commands:

```bash
airgent-play2 "Z-Lib download complete: 6 books"
```

Works with: **Claude Code, OpenAI Codex CLI, OpenCode, cron jobs, bash scripts.**

### Pattern 2: Python module

Agents or scripts with a Python runtime:

```python
from airgent_play2 import notify, speak

# Quick notification
notify("Model training finished — 97.3% accuracy")

# With specific device
speak("Server CPU at 95%", device="JBL")
```

Works with: **Hermes Agent, LangChain agents, custom Python scripts.**

### Pattern 3: Pipe from any process

Any script that produces output:

```bash
python train_model.py 2>&1 | tail -1 | airgent-play2 -
# or
echo "$(cat /tmp/result.txt)" | airgent-play2 -
```

Works with: **Any CLI tool, shell scripts, Makefiles.**

### Pattern 4: HTTP webhook (planned)

```bash
curl -X POST localhost:9876/speak -d '{"text": "Build failed"}'
```

*Coming in v0.2.0.*

### Setting the default speaker

```bash
# Per-session
export AIRGENT_DEVICE="Genelec"

# Permanent (add to ~/.zshrc)
echo 'export AIRGENT_DEVICE="Genelec"' >> ~/.zshrc
```

Now every `airgent-play2` call goes to that speaker.

### Agent prompt template

Copy this into your agent's system prompt or cron job description:

```
After completing a task, notify me via Airgent Play2:
  airgent-play2 "Brief summary of what was done (under 80 characters)"

Keep notifications short and factual. Example format:
  "Z-Lib: 6 books downloaded"
  "Dataset: FineWeb 12% complete, no errors"
  "Warning: proxy guard detected 7890 connection"
```

---

## Supported Devices

Tested and working:

| Device | Type | Protocol |
|--------|------|----------|
| JBL BAR 1300 | Soundbar | AirPlay + DLNA |
| Genelec G2 | Studio monitors | AirPlay + DLNA |
| HomePod Mini | Smart speaker | AirPlay |
| Apple TV 4K | Media center | AirPlay |
| Xiaomi TV S Pro | Smart TV | AirPlay + DLNA |
| Z9X PRO | Media player | AirPlay + DLNA |

Any AirPlay 2 compatible speaker should work. Run `airgent-play2 --list` to see yours.

---

## Voice Customization

Airgent Play2 uses **CosyVoice 3.0** for local TTS with zero-shot voice cloning.

### Using a custom voice

```python
from airgent_play2 import speak

# Clone any voice from a short WAV sample
speak("Your notification", voice_prompt_audio="/path/to/voice_sample.wav")
```

### Using the system voice (macOS only, fallback)

If CosyVoice is not installed, Airgent Play2 falls back to the macOS `say` command.

```bash
# Install CosyVoice (recommended for Chinese TTS)
# Automatic on first run OR:
airgent-play2 --setup-tts
```

---

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Any Agent   │ ──▶ │ Airgent Play2 │ ──▶ │  AirPlay 2  │
│ (shell/py)   │     │   ┌────────┐ │     │   Speaker   │
│              │     │   │ TTS    │ │     │             │
│  "Msg"  ─────┼────▶│   │CosyVoic│─┼────▶│  🎵 "Msg"   │
│              │     │   └────────┘ │     │             │
└─────────────┘     └──────────────┘     └─────────────┘
```

## FAQ

**Q: Does this steal my system audio?**
No. Airgent Play2 uses pyatv's RAOP protocol to stream directly to the speaker. Your Mac's audio output is unaffected.

**Q: What languages does TTS support?**
CosyVoice 3.0 supports Chinese natively. English and other languages work but quality varies. For English-only use cases, the macOS `say` fallback works well.

**Q: Does it work without internet?**
Yes. Everything runs locally — TTS generation, audio encoding, and AirPlay streaming.

**Q: Can multiple agents share it?**
Yes. The notification pipeline is stateless. Multiple agents or cron jobs can call `airgent-play2` simultaneously.

**Q: My speaker isn't showing up.**
Ensure the speaker is on the same Wi-Fi network and AirPlay is enabled. Run `airgent-play2 --list` to troubleshoot.

---

## Contributing

Bug reports and feature requests are welcome.

```bash
git clone https://github.com/rockeverm3m/airgent-play2.git
cd airgent-play2
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

---

## Roadmap

- [ ] Docker image for headless Linux servers
- [ ] HTTP webhook endpoint
- [ ] Multi-room simultaneous broadcast
- [ ] Voice preset library
- [ ] Windows support (DLNA fallback)

## License

MIT — see [LICENSE](LICENSE).

---

<p align="center">
  <sub>Built for agents that deserve to be heard.</sub>
</p>
