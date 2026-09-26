from pathlib import Path
from datetime import datetime
import shutil

from config.settings import DATA_DIR


def backup_database(db_path: Path):

    backup_dir = DATA_DIR / "backup"
    backup_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    destination = (
        backup_dir /
        f"tds_enterprise_master_{timestamp}.sqlite"
    )

    shutil.copy2(
        db_path,
        destination,
    )

    return destination
