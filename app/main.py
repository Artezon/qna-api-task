import os
from fastapi import FastAPI
import uvicorn
from routes.questions import questions_api

app = FastAPI()

app.include_router(questions_api)

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("SERVER_HOST"), port=os.getenv("SERVER_PORT"))
