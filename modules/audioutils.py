"""
Module for utilities
"""

import tempfile
import subprocess
import logging
from pygame import mixer


def get_data_as_wem(new_file: str) -> bytes:
    """If wem data, return as is, else convert to wem and return"""
    try:
        if new_file.endswith(".wem"):
            with open(new_file, "rb") as wem_file:
                return wem_file.read()

        new_wem_file = tempfile.gettempdir() + "\\temp.wem"
        subprocess.check_call(
            [
                r"bin\\vgmstream-cli.exe",
                "-o",
                new_wem_file,
                new_file,
            ]
        )
    except IOError as err:
        logging.exception(err)
        return 0
    except subprocess.CalledProcessError as err:
        logging.exception(err)
        return 0
    except Exception as err:
        logging.exception(err)
        return 0
    with open(new_wem_file, "rb") as wem_file:
        return wem_file.read()


def save_wem_to_file(wem_data: bytes, aud_filename: str) -> int:
    """Write wem to file"""
    try:
        if aud_filename.endswith(".wem"):
            with open(aud_filename, "wb") as wem_file:
                wem_file.write(wem_data)
            return 1
        new_wem_filename = tempfile.gettempdir() + "\\temp.wem"
        with open(new_wem_filename, "wb") as new_wem_file:
            new_wem_file.write(wem_data)
        subprocess.check_call(
            [
                r"bin\\vgmstream-cli.exe",
                "-o",
                aud_filename,
                new_wem_filename,
            ]
        )
        return 1
    except IOError as err:
        logging.exception(err)
        return 0
    except subprocess.CalledProcessError as err:
        logging.exception(err)
        return 0
    except Exception as err:
        logging.exception(err)
        return 0


def play_wem_audio(wem_data: bytes):
    """Play the given wem audio"""
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
                r"bin\\vgmstream-cli.exe",
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
