from pathlib import Path
for p in [Path('backend'), Path('backend/routers'), Path('data')]:
    p.mkdir(parents=True, exist_ok=True)
print('Directories created', [str(p) for p in [Path('backend'), Path('backend/routers'), Path('data')]])