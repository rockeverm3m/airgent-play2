"""
Core: TTS generation + AirPlay push + device discovery.
"""

import asyncio
import subprocess
import os
import sys
import tempfile
import time
from pathlib import Path

# ─── TTS: CosyVoice 3.0 (optional dependency) ───

def _cosyvoice_available():
    try:
        sys.path.insert(0, CosyVoice._REPO)
        sys.path.append(os.path.join(CosyVoice._REPO, "third_party", "Matcha-TTS"))
        from cosyvoice.cli.cosyvoice import AutoModel
        return True
    except Exception:
        return False


class CosyVoice:
    """Lazy-loaded CosyVoice 3.0 TTS engine."""

    _REPO = "/tmp/CosyVoice"
    _MODEL = "/tmp/CosyVoice/pretrained_models/Fun-CosyVoice3-0.5B"
    _PROMPT_AUDIO = "/tmp/CosyVoice/asset/zero_shot_prompt.wav"
    _PROMPT_TEXT = "You are a helpful assistant.<|endofprompt|>今天天气真不错，阳光温暖，微风徐徐，适合出去走走。"
    _instance = None

    @classmethod
    def get(cls):
        if cls._instance is None:
            sys.path.insert(0, cls._REPO)
            sys.path.append(os.path.join(cls._REPO, "third_party", "Matcha-TTS"))
            from cosyvoice.cli.cosyvoice import AutoModel
            cls._instance = AutoModel(model_dir=cls._MODEL)
        return cls._instance

    @classmethod
    def generate(cls, text: str, output_path: str = None, voice_prompt_audio: str = None):
        """
        Generate speech from text. Returns path to WAV file.

        Args:
            text: The text to speak.
            output_path: Optional output path. Auto-generated if None.
            voice_prompt_audio: Reference audio for voice cloning.
                               Uses default Xiaoxiao clone if None.
        """
        import torchaudio
        model = cls.get()

        prompt_audio = voice_prompt_audio or cls._PROMPT_AUDIO
        prompt_text = cls._PROMPT_TEXT

        # If using custom prompt audio with default prompt text, 
        # user should provide matching prompt_text via the voice config
        wav_path = output_path or tempfile.mktemp(suffix=".wav", prefix="airgent_")

        for i, j in enumerate(model.inference_zero_shot(
            text, prompt_text, prompt_audio, stream=False
        )):
            torchaudio.save(wav_path, j["tts_speech"], model.sample_rate)
            return wav_path

        return None


# ─── Push: AirPlay via pyatv RAOP ───

def _ensure_wav_44100(filepath: str) -> str:
    """Convert audio to 44100Hz WAV (required by AirPlay RAOP)."""
    # Check if already correct
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "stream=sample_rate",
         "-of", "csv=p=0", filepath],
        capture_output=True, text=True
    )
    if result.stdout.strip() == "44100" and filepath.endswith(".wav"):
        return filepath

    cache = tempfile.mktemp(suffix=".wav", prefix="airgent_44100_")
    subprocess.run(
        ["ffmpeg", "-y", "-i", filepath, "-ar", "44100", "-ac", "2", cache],
        capture_output=True
    )
    return cache


def _push_airplay(filepath: str, device_name: str = "Genelec") -> bool:
    """Push audio to an AirPlay device via pyatv RAOP."""
    from pyatv import connect, scan
    from pyatv.const import Protocol

    wav_path = _ensure_wav_44100(filepath)

    async def _push():
        devices = await scan(loop=asyncio.get_event_loop(), timeout=5)
        target = None
        for d in devices:
            if device_name.lower() in d.name.lower():
                target = d
                break
        if not target:
            # Try first available AirPlay device
            for d in devices:
                for s in d.services:
                    if "RAOP" in str(s.protocol):
                        target = d
                        break
                if target:
                    break

        if not target:
            print(f"⚠️  No AirPlay device found matching '{device_name}'")
            return False

        atv = await connect(target, loop=asyncio.get_event_loop(), protocol=Protocol.RAOP)
        await atv.stream.stream_file(wav_path)
        atv.close()
        return True

    return asyncio.run(_push())


# ─── Public API ───

def speak(text: str, device: str = None, voice_prompt_audio: str = None):
    """
    Generate TTS audio and push to speaker.

    Args:
        text: Notification text to speak.
        device: Device name keyword (e.g. "JBL", "Genelec", "HomePod").
                Uses first available AirPlay device if not specified.
        voice_prompt_audio: Path to WAV file for voice cloning.
    """
    # Default device from env or auto-detect
    device = device or os.environ.get("AIRGENT_DEVICE")
    
    print(f"🔊 {text[:80]}")
    wav = CosyVoice.generate(text, voice_prompt_audio=voice_prompt_audio)
    if not wav:
        print("❌ TTS generation failed")
        return False

    if device:
        ok = _push_airplay(wav, device)
    else:
        ok = _push_airplay(wav, "Genelec")

    # Cleanup
    try:
        os.unlink(wav)
    except:
        pass

    if ok:
        print(f"✅ Pushed → {device or 'auto-detected'}")
    return ok


def notify(text: str, device: str = None):
    """Alias for speak(). Compatible with most agent notification patterns."""
    return speak(text, device)


def list_devices():
    """Discover all AirPlay-capable devices on the network."""
    from pyatv import scan

    async def _scan():
        devices = await scan(loop=asyncio.get_event_loop(), timeout=5)
        results = []
        for d in devices:
            protocols = [s.protocol.name for s in d.services]
            results.append({
                "name": d.name,
                "address": str(d.address),
                "protocols": protocols,
            })
        return results

    return asyncio.run(_scan())


# ─── CLI ───

def main():
    import argparse
    p = argparse.ArgumentParser(
        prog="airgent-play2",
        description="Push agent voice notifications via AirPlay 2",
        epilog="Example: airgent-play2 'Download complete' --device JBL",
    )
    p.add_argument("text", nargs="*", help="Notification text. Use '-' to read from stdin.")
    p.add_argument("-d", "--device", default=None,
                   help="Target device (e.g. JBL, Genelec, HomePod). Auto-detect if omitted.")
    p.add_argument("--list", action="store_true", help="List available AirPlay devices")
    p.add_argument("-v", "--version", action="version", version=f"airgent-play2 {__version__}")
    args = p.parse_args()

    if args.list:
        devices = list_devices()
        if not devices:
            print("No AirPlay devices found.")
        for d in devices:
            proto_str = ", ".join(d["protocols"])
            print(f"  {d['name']:40s} {d['address']:15s} [{proto_str}]")
        return

    if args.text:
        if args.text == ["-"]:
            text = sys.stdin.read().strip()
        else:
            text = " ".join(args.text)
    else:
        p.print_help()
        return

    if not text:
        print("⚠️  Empty text, nothing to speak.")
        return

    speak(text, args.device)


if __name__ == "__main__":
    main()
