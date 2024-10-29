import os

SECRET_KEY = os.environ.get("SECRET_KEY")
SERVER_HOST = os.environ.get("SERVER_HOST")
SERVER_PORT = os.environ.get("SERVER_PORT")
SERVER_DEBUG_MODE = os.environ.get("SERVER_DEBUG_MODE")
LLM_HOST = os.environ.get("LLM_HOST")
LLM_PORT = os.environ.get("LLM_PORT")
SESSION_TIMEOUT = os.environ.get("SESSION_TIMEOUT")