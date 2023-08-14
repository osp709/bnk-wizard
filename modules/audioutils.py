"""
Module for utilities
"""

import tempfile
import subprocess
from pygame import mixer


def get_data_as_wem(new_file: str) -> bytes:
    """
    If wem data, return as is, else convert to wem and return
    """
    if new_file.endswith(".wem"):
        with open(new_file, "rb") as wem_file:
            return wem_file.read()

    new_wem_file = tempfile.gettempdir() + "\\temp.wem"
    try:
        subprocess.check_call(
            [
                r"modules\\vgmstream-win64\\vgmstream-cli.exe",
                "-o",
                new_wem_file,
                new_file,
            ]
        )
    except subprocess.CalledProcessError as err:
        print(err.output)

    with open(new_wem_file, "rb") as wem_file:
        return wem_file.read()


def play_wem_audio(wem_data: bytes):
    """
    Play the given wem audio
    """
    wem_filename = tempfile.gettempdir() + "\\temp.wem"
    with open(wem_filename, mode="wb") as wem_file:
        wem_file.write(wem_data.data)
    try:
        mixer.music.unload()
    finally:
        pass
    try:
        wav_filename = wem_filename.split(".wem")[0] + ".wav"
        subprocess.check_call(
            [
                r"modules\\vgmstream-win64\\vgmstream-cli.exe",
                "-o",
                wav_filename,
                wem_filename,
            ]
        )
        mixer.music.load(wav_filename)
        mixer.music.play()
    except subprocess.CalledProcessError as err:
        print(err.output)


def stop_wem_audio():
    """Stop if any audio is playing"""
    try:
        mixer.music.stop()
    finally:
        pass
