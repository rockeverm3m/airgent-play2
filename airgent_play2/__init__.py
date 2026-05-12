"""
Airgent Play 2 — Give your AI agents a voice.

Push voice notifications from any agent to any AirPlay 2 speaker.

Usage:
    # As a CLI tool (any agent that can run shell commands)
    airgent-play2 "Z-Lib download complete: 6 books"

    # As a Python module
    from airgent_play2 import notify
    notify("Dataset processing done")

    # Pipe from any script
    echo "Model training finished" | airgent-play2 -
"""

__version__ = "0.1.0"

from .core import notify, speak, list_devices

__all__ = ["notify", "speak", "list_devices"]
