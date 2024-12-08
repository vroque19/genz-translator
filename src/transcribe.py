from openai import OpenAI
import dotenv
import os
dotenv.load_dotenv()
key = os.environ['OPENAI_API_TOKEN']
client = OpenAI(api_key=key)

def translate(text):
  try:
      response = client.chat.completions.create(
          model="gpt-4o-mini",  # not as advanced, but faster and cheaper
          messages=[
              {"role": "system", "content": "You are a helpful translation assistant that converts Gen Z slang into English for millenials and Gen X to easily understand. If there is no slang detected, the translation is simply the original message I provided you. Please only respond with the translation and nothing else."},
              {"role": "user", "content": f"Translate this into formal English: {text}"}
          ]
      )
      translation = response.choices[0].message.content
      # print(translation)
      return translation
  except Exception as e:
      print(f"An error occurred during translation: {e}")
      return ""

def transcribe():
  audio_file= open("original.wav", "rb")
  transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
  )

  return transcription.text

# translate(transcribe())



