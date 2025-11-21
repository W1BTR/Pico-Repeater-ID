# 2025 W1BTR https://bigtimeradio.us
# BASED ON 2021 Kattni Rembor PICOMP3 Project - Modified for repeater ID
# SPDX-License-Identifier: MIT
# Requires Pico Board to be flashed with Adafruit's CircuitPy for Pico.

import board
import audiomp3
import audiopwmio
import time
import random

# --- Configuration ---

MODE = "CW"  # "CW" or "MP3"
CW_TEXT = "W1BTR" # Text to play in CW mode (only a-z, 0-9, '.', ' ', and '#' (special sound) are supported)
ENABLE_RANDOM_MP3 = True # Set to True to enable 1 in X chance of playing alternative file (Works on CW and MP3 Mode)
RANDOM_MP3_ODDS = 50 # If ENABLE_RANDOM_MP3 is True, this is the 'X' in '1 in X' chance
DEFAULT_MP3_FILE = "Repeater ID.mp3" # Default MP3 file to play in MP3 mode
# Setup audio output on GP0
audio = audiopwmio.PWMAudioOut(board.GP0)
# 15 minutes in seconds
INTERVAL = 15 * 60  # 900 seconds
# List of alternative media files
alternative_files = [
    "Funny Version.mp3",
    "Voice Welcome.mp3",
]

# --- End Configuration ---


def play_audio_file(filename):
    print("Attempting to play:", filename)
    try:
        decoder = audiomp3.MP3Decoder(open(filename, "rb"))
        audio.play(decoder)
        print("Playing", filename, "at", time.monotonic(), "seconds")
        # Wait for playback to complete
        while audio.playing:
            pass
        print("Playback complete.")
        return True
    except OSError as e:
        print(f"Error: Could not find {filename} file! {e}")
        return False

print("Repeater ID Player Starting...")
print(f"Mode: {MODE}")
if MODE == "CW":
    print(f"CW Text: {CW_TEXT}")
else: # MODE == "MP3"
    print(f"Default MP3 File: {DEFAULT_MP3_FILE}")
    print(f"Random MP3 enabled: {ENABLE_RANDOM_MP3}")
    if ENABLE_RANDOM_MP3:
        print(f"With a 1 in {RANDOM_MP3_ODDS} chance of playing an alternative file.")

# Play immediately on startup, then every 15 minutes
while True:
    if MODE == "CW":
        print(f"Entering CW Mode for text: {CW_TEXT}")
        played_random_alternative = False

        # Check if we should play a random alternative INSTEAD of CW
        if ENABLE_RANDOM_MP3 and random.randint(1, RANDOM_MP3_ODDS) == 1:
            alternative_file = random.choice(alternative_files)
            print("Special alternative file chosen:", alternative_file)
            if play_audio_file(alternative_file):
                played_random_alternative = True

        if played_random_alternative:
            print("Played random alternative instead of CW. Waiting 15 minutes...")
        else:
            for char in CW_TEXT:
                char_lower = char.lower()
                if 'a' <= char_lower <= 'z':
                    filename = f"alphabet/{char_lower}.mp3"
                    if not play_audio_file(filename):
                        print(f"Failed to play {filename}, skipping character.")
                    time.sleep(0.4) # Short delay between letters
                elif '0' <= char_lower <= '9':
                    filename = f"alphabet/{char_lower}.mp3"
                    if not play_audio_file(filename):
                        print(f"Failed to play {filename}, skipping character.")
                    time.sleep(0.4) # Short delay between digits
                elif char_lower == '.':
                    filename = "alphabet/period.mp3"
                    if not play_audio_file(filename):
                        print(f"Failed to play {filename}, skipping period.")
                    time.sleep(0.4) # Short delay for period
                elif char_lower == '#':
                    filename = "alphabet/hashtag.mp3"
                    if not play_audio_file(filename):
                        print(f"Failed to play {filename}, skipping hashtag.")
                    time.sleep(0.4) # Short delay for hashtag
                elif char_lower == ' ':
                    time.sleep(1.0) # Longer delay for space
                else:
                    print(f"Skipping unsupported character: {char}")
            print("CW playback finished. Waiting 15 minutes...")

    elif MODE == "MP3":
        file_to_play = DEFAULT_MP3_FILE

        # Check for the 1 in X chance if random is enabled
        if ENABLE_RANDOM_MP3 and random.randint(1, RANDOM_MP3_ODDS) == 1:
            # Choose a random file from the alternative list
            file_to_play = random.choice(alternative_files)
            print("Special alternative file chosen:", file_to_play)

        if not play_audio_file(file_to_play):
            if file_to_play == DEFAULT_MP3_FILE:
                print(f"Please ensure {DEFAULT_MP3_FILE} is available.")
            else:
                print("Please ensure alternative files are available.")
            print("Retrying in 60 seconds...")
            time.sleep(60)
            continue
        print("MP3 playback finished. Waiting 15 minutes...")

    # Wait for x time
    time.sleep(INTERVAL)
