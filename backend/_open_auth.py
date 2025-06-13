from pathlib import Path, PurePosixPath
print(Path(__file__).resolve())
text = Path('backend/auth.py').read_text()
print(text)