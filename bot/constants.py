from dotenv import load_dotenv, find_dotenv
from os import environ as env

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

DISCORD_BOT_TOKEN = env.get("DISCORD_BOT_TOKEN")
