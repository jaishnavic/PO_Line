import os
from dotenv import load_dotenv

load_dotenv()

FUSION_BASE_URL = os.getenv("FUSION_BASE_URL")
FUSION_USERNAME = os.getenv("FUSION_USERNAME")
FUSION_PASSWORD = os.getenv("FUSION_PASSWORD")