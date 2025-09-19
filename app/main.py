import os
from fastapi import FastAPI
import uvicorn
from app.utils import is_env_true
from app.routes.questions import questions_api
from app.routes.answers import answers_api

kwargs: dict = {}
if not is_env_true("API_DOCS"):
    kwargs = dict(docs_url=None, redoc_url=None, openapi_url=None, swagger_ui_oauth2_redirect_url=None)

app = FastAPI(**kwargs)

app.include_router(questions_api)
app.include_router(answers_api)

if __name__ == "__main__":
    host = os.getenv("SERVER_HOST")
    if not host:
        raise RuntimeError("SERVER_HOST environmental variable is not set")
    
    port = os.getenv("SERVER_PORT")
    if not port:
        raise RuntimeError("SERVER_PORT environmental variable is not set")
    try:
        port = int(port)
    except ValueError:
        raise RuntimeError("SERVER_PORT environmental variable must be a valid number")
    
    uvicorn.run(app, host=host, port=port)
