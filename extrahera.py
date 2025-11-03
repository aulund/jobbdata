import os
import shutil
import zipfile
import tarfile
import gzip
import tempfile
from pathlib import Path

# === Fråga användaren ===
source_dir = input("📂 Ange sökvägen till mappen med arkiv: ").strip('" ')
target_dir = input("📁 Ange sökvägen till mål-mappen (dit allt ska flyttas): ").strip('" ')

# === Hjälpfunktioner ===
def safe_move(src_path: Path, dst_dir: Path, existing_files: set) -> Path:
    """Flytta fil till dst_dir och hantera namn-krockar med _1, _2, ..."""
    dst_dir.mkdir(parents=True, exist_ok=True)
    base = src_path.stem
    ext = "".join(src_path.suffixes)
    dst_name = f"{base}{ext}"
    i = 1
    while dst_name in existing_files:
        dst_name = f"{base}_{i}{ext}"
        i += 1
    dst_path = dst_dir / dst_name
    existing_files.add(dst_name)
    shutil.move(src_path, dst_path)
    return dst_path

def extract_zip(zpath: Path, outdir: Path):
    print(f"[ZIP] Extraherar: {zpath.name}")
    with zipfile.ZipFile(zpath, 'r') as zf:
        zf.extractall(outdir)

def extract_tar(tpath: Path, outdir: Path):
    print(f"[TAR] Extraherar: {tpath.name}")
    with tarfile.open(tpath, 'r:*') as tf:
        tf.extractall(outdir)

def extract_gz(gzpath: Path, outdir: Path):
    # Hanterar enkel gzip (t.ex. .fastq.gz -> .fastq)
    print(f"[GZ] Packar upp: {gzpath.name}")
    out_name = gzpath.name[:-3] if gzpath.name.lower().endswith('.gz') else gzpath.stem
    out_path = outdir / out_name
    with gzip.open(gzpath, 'rb') as f_in, open(out_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out, length=1024*1024)  # 1MB buffer

# === Körning ===
src = Path(source_dir)
dst = Path(target_dir)
dst.mkdir(parents=True, exist_ok=True)

if not src.exists():
    print(f"❌ Fel: källmappen '{src}' finns inte.")
    exit(1)

archives = list(src.iterdir())
found_any = False
# Pre-build set of existing filenames for faster collision detection
existing_files = {f.name for f in dst.iterdir() if f.is_file()} if dst.exists() else set()

print(f"\n🔍 Letar arkiv i: {src}\n")

for item in archives:
    if item.is_dir():
        continue

    # Quick file extension check before expensive operations
    suffix_lower = item.suffix.lower()
    name_lower = item.name.lower()
    
    # Skip files that definitely aren't archives based on extension
    # We support: .zip, .tar, .tar.gz, .tar.bz2, .tar.xz, .tgz, and standalone .gz files
    if suffix_lower not in {'.zip', '.tar', '.gz', '.tgz', '.bz2', '.xz'}:
        continue
    
    # Identifiera arkivtyp - check extension first for speed
    is_zip = False
    is_tar = False
    is_gz = False
    
    if suffix_lower == '.zip':
        is_zip = zipfile.is_zipfile(item)
    elif suffix_lower in {'.tar', '.tgz'} or name_lower.endswith(('.tar.gz', '.tar.bz2', '.tar.xz')):
        # TAR files (possibly compressed) - tarfile.open with 'r:*' auto-detects compression
        try:
            is_tar = tarfile.is_tarfile(item)
        except Exception:
            pass
    elif suffix_lower == '.gz' and not name_lower.endswith('.tar.gz'):
        # Simple gzip file (not tar.gz)
        is_gz = True
    else:
        # Fallback for ambiguous cases (.bz2, .xz without .tar prefix)
        # Try tar first, then fall back to zip check
        try:
            is_tar = tarfile.is_tarfile(item)
        except Exception:
            pass
        if not is_tar:
            is_zip = zipfile.is_zipfile(item)

    if not (is_zip or is_tar or is_gz):
        continue

    found_any = True
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        try:
            if is_zip:
                extract_zip(item, tmpdir_path)
            elif is_tar:
                extract_tar(item, tmpdir_path)
            elif is_gz:
                extract_gz(item, tmpdir_path)

            moved = 0
            for root, dirs, files in os.walk(tmpdir_path):
                for f in files:
                    src_path = Path(root) / f
                    safe_move(src_path, dst, existing_files)
                    moved += 1

            print(f"  → Flyttade {moved} filer till {dst}\n")

        except Exception as e:
            print(f"⚠️ Fel vid extrahering av {item.name}: {e}")

if not found_any:
    print("❌ Inga zip/tar/gz-arkiv hittades i mappen.")
else:
    print("✅ Klart! Alla arkiv extraherade och filer flyttade.")
