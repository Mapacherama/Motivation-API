import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from openai import APIStatusError, OpenAI

# Load environment variables
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

print(API_KEY)
print(BASE_URL)

# Initialize OpenAI client for DeepSeek
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# Initialize FastAPI app
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to the DeepSeek Motivation API"}

@app.get("/quote")
def get_motivational_quote():
    """Fetches a motivational quote from DeepSeek AI."""
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a motivational AI. Provide an inspiring quote."},
                {"role": "user", "content": "Give me a motivational quote."},
            ],
            stream=False
        )
        return {"quote": response.choices[0].message.content}
    
    except APIStatusError as e:
        if e.status_code == 402:
            raise HTTPException(status_code=402, detail="Insufficient Balance. Please check your DeepSeek account.")
        else:
            raise HTTPException(status_code=500, detail="An error occurred while fetching the quote.")


@app.get("/movie-recommendation")
def get_motivational_movie():
    """Fetches a motivational movie recommendation."""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a film expert specializing in motivational movies."},
            {"role": "user", "content": "Recommend me a motivational movie with a short reason why."},
        ],
        stream=False
    )

    return {"movie": response.choices[0].message.content}

@app.get("/great-person")
def get_great_person():
    """Fetches a famous great person with their story."""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a historian who provides inspiring life stories."},
            {"role": "user", "content": "Tell me about a great person and why they inspire people."},
        ],
        stream=False
    )

    return {"person": response.choices[0].message.content}

# Run with: uvicorn main:app --reload
