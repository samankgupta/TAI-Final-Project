"""Configuration settings for Resume Trust Lab System."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
env_file = Path(__file__).parent.parent / ".env"
load_dotenv(env_file)

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

# Data files
DATASET_PATH = "/Users/samankgupta/Downloads/TAI Final Project/dataset.csv"
JOB_DESC_PATH = DATA_DIR / "job_description.txt"

# Output files
STAGE_1_OUTPUT = OUTPUT_DIR / "stage_1.json"
STAGE_2_OUTPUT = OUTPUT_DIR / "stage_2.json"
STAGE_3_OUTPUT = OUTPUT_DIR / "stage_3.json"
STAGE_4_OUTPUT = OUTPUT_DIR / "stage_4.json"
STAGE_5_OUTPUT = OUTPUT_DIR / "stage_5.json"
METRICS_OUTPUT = OUTPUT_DIR / "metrics.json"
FAILURE_ANALYSIS_OUTPUT = OUTPUT_DIR / "failure_analysis.json"

# Ranking parameters
TOP_K_STAGE_2 = 50  # Keep top 50 from baseline
TOP_K_STAGE_3 = 50  # Keep top 50 from embedding
TOP_K_STAGE_4 = 5   # Keep top 5 from Gemini base
TOP_K_STAGE_5 = 5   # Keep top 5 from Improved Gemini

# Model names
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
GEMINI_MODEL_NAME = "gemini-3.1-flash-lite"

# API Settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Cache settings
USE_API_CACHE = True
CACHE_DIR = PROJECT_ROOT / ".cache"

# Default parameters
DEFAULT_TOP_K = 5
SIMILARITY_THRESHOLD = 0.0  # No threshold, rank all

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)
