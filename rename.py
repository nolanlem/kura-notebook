from pathlib import Path

TARGET_EXTENSIONS = {'.wav', '.npy', '.txt'}

def needs_insertion(stem: str) -> bool:
    parts = stem.split('_')
    return len(parts) >= 2 and parts[1] != 'n'

def insert_n_after_first_token(stem: str) -> str:
    parts = stem.split('_')
    parts.insert(1, 'n')
    return '_'.join(parts)

def rename_files(root: Path) -> None:
    for path in root.rglob('*'):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TARGET_EXTENSIONS:
            continue

        stem = path.stem
        if not needs_insertion(stem):
            continue

        new_stem = insert_n_after_first_token(stem)
        target = path.with_name(f"{new_stem}{path.suffix}")

        if target.exists():
            print(f"SKIP (exists): {path} -> {target}")
            continue

        print(f"RENAME: {path} -> {target}")
        path.rename(target)

if __name__ == "__main__":
    rename_files(Path('.').resolve())