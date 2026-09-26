from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
STORAGE_DIR = BASE_DIR / "storage"

SALARY_SLIP_DIR = STORAGE_DIR / "salary_slips"
PDF_DIR = STORAGE_DIR / "generated_pdfs"
TEMP_DIR = STORAGE_DIR / "temp"

for directory in [
    DATA_DIR,
    STORAGE_DIR,
    SALARY_SLIP_DIR,
    PDF_DIR,
    TEMP_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{DATA_DIR / 'tds_enterprise_master.sqlite'}"
)

APP_ENV = os.getenv("APP_ENV", "development")

MAX_UPLOAD_MB = int(
    os.getenv("MAX_UPLOAD_MB", "10")
)
