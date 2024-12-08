from transcribe import client
from pathlib import Path

speech_file_path = Path(__file__).parent / "output.mp3"
def playback(transcription):
  response = client.audio.speech.create(
  model="tts-1",
  voice="alloy",
  input=transcription
)
  
  response.stream_to_file(speech_file_path)
  


