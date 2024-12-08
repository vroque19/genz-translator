from pathlib import Path
from openai import OpenAI
import dotenv
import os
dotenv.load_dotenv()
key = os.environ['OPENAI_API_TOKEN']
client = OpenAI(api_key=key)

speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="alloy",
  input="Today is a wonderful day to build something people love!"
)

response.stream_to_file(speech_file_path)
