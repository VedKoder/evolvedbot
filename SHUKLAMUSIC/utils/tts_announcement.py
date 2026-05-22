"""
TTS Announcement Utility
Generates a voice announcement before music starts in VC.
Announces: "Music is going to start. The music is {title} by {artist}. Enjoy it!"
"""

import asyncio
import os
import tempfile
import time

from SHUKLAMUSIC import LOGGER


async def generate_announcement_tts(title: str, artist: str = None) -> tuple:
    """
    Generate a TTS announcement audio file.
    Returns (file_path, duration_in_seconds).
    Falls back gracefully on any error.
    """
    try:
        from gtts import gTTS

        # Build the announcement text
        if artist and artist.strip() and artist.lower() not in ["unknown", "n/a", ""]:
            text = (
                f"Music is going to start. "
                f"The music is {title} by {artist}. "
                f"Enjoy it!"
            )
        else:
            text = (
                f"Music is going to start. "
                f"Now playing {title}. "
                f"Enjoy it!"
            )

        # Generate TTS file
        tts = gTTS(text=text, lang="en", slow=False)

        tmp_dir = tempfile.gettempdir()
        tts_path = os.path.join(tmp_dir, f"tts_intro_{int(time.time())}_{os.getpid()}.mp3")

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, tts.save, tts_path)

        # Get duration using pydub
        duration = await _get_audio_duration(tts_path)

        LOGGER(__name__).info(f"TTS announcement generated: {tts_path} ({duration:.1f}s)")
        return tts_path, duration

    except Exception as e:
        LOGGER(__name__).warning(f"TTS generation failed: {e}")
        return None, 0


async def _get_audio_duration(file_path: str) -> float:
    """Get duration of an audio file in seconds."""
    try:
        loop = asyncio.get_event_loop()

        def _get_dur():
            try:
                from pydub import AudioSegment
                audio = AudioSegment.from_file(file_path)
                return len(audio) / 1000.0
            except Exception:
                # Fallback: estimate ~4-6 words per second for TTS
                return 5.0

        return await loop.run_in_executor(None, _get_dur)
    except Exception:
        return 5.0


def cleanup_tts_file(file_path: str):
    """Delete TTS temp file after use."""
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        pass
