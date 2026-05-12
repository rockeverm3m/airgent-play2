---
name: airgent-play2
description: "Voice notifications via AirPlay 2 + DLNA. Let your claw speak through any speaker in your house."
version: 0.1.0
homepage: "https://github.com/rockeverm3m/airgent-play2"
tags:
  - audio
  - notifications
  - airplay
  - tts
  - smart-home
platforms:
  - macos
dependencies:
  - pyatv
  - ffmpeg
  - torch
  - torchaudio
---

# Airgent Play 2

Give your claw a voice. When a task finishes, your claw speaks the result through any AirPlay 2 or DLNA speaker in your house. No phone, no text — just a voice in the room.

## Install

```bash
pip install airgent-play2
```

Or from source:

```bash
git clone https://github.com/rockeverm3m/airgent-play2.git
cd airgent-play2
pip install -e .
```

## Usage

### From any claw command

```bash
airgent-play2 "Z-Lib download complete: 6 books"
```

### List available speakers

```bash
airgent-play2 --list
```

### Target a specific speaker

```bash
airgent-play2 "Task done" --device JBL
```

### Set default speaker

```bash
export AIRGENT_DEVICE="Genelec"
```

### As a Python module

```python
from airgent_play2 import notify
notify("Model training finished — 97.3% accuracy")
```

## What claw tasks need this

Any long-running task your claw handles:
- Cron jobs (downloads, monitoring, reports)
- Model training / dataset processing
- System alerts (disk full, CPU spike)
- Remux / media notifications

Just add `airgent-play2 "summary"` at the end of the task.

## Supported Devices

Any AirPlay 2 or DLNA speaker. Tested with JBL BAR 1300, Genelec G2, HomePod Mini, Apple TV 4K, Xiaomi TV, and more.

## Voice

Uses CosyVoice 3.0 for local Chinese TTS with zero-shot voice cloning. Falls back to macOS `say` if CosyVoice is not installed.
