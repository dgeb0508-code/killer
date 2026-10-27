"""narration.py의 문장으로 나레이션 음성(voice/*.mp3)과 길이표(voice/durations.json)를 만든다.

실행: python make_voice.py   (edge-tts 필요, 네트워크 사용)
"""
import asyncio
import json
import subprocess
from pathlib import Path

import edge_tts

from narration import LINES, VOICE

OUT = Path(__file__).parent / "voice"


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


async def main():
    OUT.mkdir(exist_ok=True)
    durations = {}
    for key, text in LINES:
        path = OUT / f"{key}.mp3"
        await edge_tts.Communicate(text, VOICE).save(str(path))
        durations[key] = round(duration(path), 3)
        print(key, durations[key])
    (OUT / "durations.json").write_text(json.dumps(durations, indent=1))


if __name__ == "__main__":
    asyncio.run(main())
