import streamlit as st
from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip
from google.cloud import speech, texttospeech
import openai
import os

# Initialize OpenAI and Google APIs
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "https://internshala.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"
openai.api_key = '22ec84421ec24230a3638d1b51e3a7dc'

# Function to transcribe audio using Google's Speech-to-Text API
def transcribe_audio(audio_path):
    client = speech.SpeechClient()
    
    with open(audio_path, 'rb') as audio_file:
        content = audio_file.read()
    
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)
    
    transcription = ""
    for result in response.results:
        transcription += result.alternatives[0].transcript
    
    return transcription

# Function to correct transcription using GPT-4
def correct_transcription(transcription):
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=f"Please correct the following transcription: {transcription}",
        max_tokens=500
    )
    return response.choices[0].text.strip()

# Function to generate audio from corrected text using Google's Text-to-Speech API
def generate_audio(text, output_audio_file):
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-J",  # Journey model or equivalent
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    with open(output_audio_file, 'wb') as out:
        out.write(response.audio_content)
    
    return output_audio_file

# Streamlit UI
st.title("Video Audio Correction with GPT-4 and Google Cloud")

# File uploader for video
video_file = st.file_uploader("Upload a video file", type=["mp4", "mkv", "mov"])
if video_file is not None:
    st.video(video_file)

    # Save video to local
    video_path = "uploaded_video.mp4"
    with open(video_path, "wb") as f:
        f.write(video_file.read())
    
    # Extract audio from video
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_path = "extracted_audio.wav"
    audio_clip.write_audiofile(audio_path)

    # Transcribe audio
    st.write("Transcribing audio...")
    transcription = transcribe_audio(audio_path)
    st.write("Original Transcription:")
    st.text(transcription)

    # Correct transcription using GPT-4
    st.write("Correcting transcription with GPT-4...")
    corrected_transcription = correct_transcription(transcription)
    st.write("Corrected Transcription:")
    st.text(corrected_transcription)

    # Generate corrected audio
    st.write("Generating new audio with Text-to-Speech...")
    output_audio_path = "corrected_audio.wav"
    generate_audio(corrected_transcription, output_audio_path)
    st.audio(output_audio_path)

    # Replace original audio in the video
    st.write("Replacing audio in the original video...")
    final_video = video_clip.set_audio(AudioFileClip(output_audio_path))
    final_video_path = "final_video_with_corrected_audio.mp4"
    final_video.write_videofile(final_video_path)

    st.write("Here is your video with corrected audio:")
    st.video(final_video_path)
