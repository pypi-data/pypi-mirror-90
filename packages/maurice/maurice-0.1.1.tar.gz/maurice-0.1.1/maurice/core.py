from pathlib import Path


CACHE_DIR = Path.cwd().joinpath(".maurice_cache").absolute()
CACHE_DIR.mkdir(parents=True, exist_ok=True)
