from gpiozero import Button
from signal import pause
from transcribe import transcribe, translate
from encode import playback
import subprocess
import os
import signal
import time

PIN = 17
recording_process = None

record_command = [
    'arecord',
    '-D', 'plughw:3,0',
    '-f', 'S16_LE',
    '-r', '16000',
    '-t', 'wav',
    'original.wav'
]
play_command = [
    'aplay', '-D', 'plughw:3,0',
    '-v', 'output.wav'
]
encoding_command = [
    'ffmpeg', '-i', 'output.mp3', 'output.wav', '-y'
]

def cleanup(signum, frame):
    global recording_process
    if recording_process and recording_process.poll() is None:
        recording_process.terminate()
        recording_process.wait()
    print("Exiting cleanly.")
    exit(0)

def start_recording():
    global recording_process
    if not recording_process or recording_process.poll() is not None:
        try:
            recording_process = subprocess.Popen(
                record_command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("Recording started.")
        except Exception as e:
            print(f"Error starting recording: {e}")

def stop_recording():
    global recording_process
    if recording_process and recording_process.poll() is None:
        try:
            recording_process.terminate()
            recording_process.wait()
        except subprocess.CalledProcessError as e:
            print(f"Error terminating recording process: {e}")

        print("Recording stopped.\n")
        if os.path.exists('original.wav'):
            print("Generating transcription...")
            try:
                original = transcribe()
                translation = translate(original)
                print(original)
                print("\n\nGenerating Translation...")
                time.sleep(1)
                playback(translation)
                print(translation)
                print("----------")

                encode_and_playback()
            except Exception as e:
                print(f"Error processing file: {e}")
        else:
            print("Recording file not found. Skipping transcription.")

def encode_and_playback():
    try:
        subprocess.run(encoding_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(play_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error during encoding/playback: {e}")

signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)

btn = Button(PIN, bounce_time=0.1)
btn.when_pressed = start_recording
btn.when_released = stop_recording

pause()
