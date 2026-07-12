import os
from dotenv import load_dotenv

load_dotenv()

PRATILIPI_BASE_URL = os.getenv("PRATILIPI_BASE_URL")
PRATILIPI_GRAPHQL_URL = os.getenv("PRATILIPI_GRAPHQL_URL")
USER_AGENT = os.getenv("USER_AGENT")
PRATILIPI_TOKEN = os.getenv("PRATILIPI_TOKEN")

if not all([PRATILIPI_BASE_URL, PRATILIPI_GRAPHQL_URL, USER_AGENT, PRATILIPI_TOKEN]):
    raise RuntimeError("Missing one or more required env vars: PRATILIPI_BASE_URL, PRATILIPI_GRAPHQL_URL, USER_AGENT, PRATILIPI_TOKEN")
