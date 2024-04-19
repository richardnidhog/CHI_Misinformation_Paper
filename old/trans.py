from openai import OpenAI

client = OpenAI(api_key='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')

video_file_path = r"Snaptik.app_7145912890321554730.mp4"

def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
    return transcript

transcript = transcribe_audio(video_file_path)

transcript_file_path = r"transcript.txt"

with open(transcript_file_path, "w") as file:
    file.write(transcript)

print("Transcription complete. Transcript saved to:", transcript_file_path)