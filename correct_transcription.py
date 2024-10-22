import openai

def correct_transcription(transcript):
    openai.api_key = "22ec84421ec24230a3638d1b51e3a7dc"
    
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=f"Correct this transcript by removing any grammatical errors and filler words: {transcript}",
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    
    return response.choices[0].text.strip()
