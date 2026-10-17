"""
Download the three raw datasets for the NYC itinerary project into data/raw/.

Run from the project folder (VS Code terminal):
    python src/download_data.py

Files (already-downloaded files are skipped):
  1. Foursquare NYC check-ins (Yang et al., TSMC 2014)   -> dataset_TSMC2014_NYC.txt   (~25 MB unzipped)
  2. Google Local metadata, New York (UCSD McAuley Lab)  -> meta-New_York.json.gz      (large; a few minutes)
  3. Brooklyn Bridge Automated Pedestrian Counts (NYC)    -> Brooklyn_Bridge_Automated_Pedestrian_Counts.csv
"""
import gzip
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

GOOGLE_URL = "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/meta-New_York.json.gz"
BRIDGE_URL = "https://data.cityofnewyork.us/api/views/6fi9-q3ta/rows.csv?accessType=DOWNLOAD"
FOURSQUARE_DRIVE_ID = "1VE67jfSN-GV6fkCfuyBEQJzk_qy-SfOk"   # author's official Google Drive file (zip)

FOURSQUARE_MANUAL = """
  Manual download (either one works):
    a) Author's page: https://sites.google.com/site/yangdingqi/home/foursquare-dataset
       -> section '2. NYC and Tokyo Check-in Dataset' -> 'dataset here'. Unzip and put
          dataset_TSMC2014_NYC.txt into data/raw/
    b) Kaggle: https://www.kaggle.com/chetanism/foursquare-nyc-and-tokyo-checkin-dataset
       -> put dataset_TSMC2014_NYC.csv into data/raw/
"""


def download(url, dest):
    """Stream a URL to disk with a simple progress readout."""
    tmp = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (CSE487 course project)"})
    with urllib.request.urlopen(req, timeout=60) as r, open(tmp, "wb") as f:
        total = int(r.headers.get("Content-Length") or 0)
        done = 0
        while chunk := r.read(1 << 20):
            f.write(chunk)
            done += len(chunk)
            msg = f"{done / 1e6:,.1f} MB" + (f" / {total / 1e6:,.1f} MB" if total else "")
            print(f"\r    {msg}", end="", flush=True)
    print()
    tmp.replace(dest)


def get_foursquare():
    if list(RAW.rglob("dataset_TSMC2014_NYC.*")):
        print("[1/3] Foursquare: already present, skipping")
        return True
    print("[1/3] Foursquare: downloading from the author's Google Drive ...")
    zip_path = RAW / "dataset_tsmc2014.zip"
    try:
        import gdown
    except ImportError:
        print("    'gdown' is not installed (pip install gdown)." + FOURSQUARE_MANUAL)
        return False
    try:
        gdown.download(id=FOURSQUARE_DRIVE_ID, output=str(zip_path), quiet=False)
        with zipfile.ZipFile(zip_path) as z:
            member = next(m for m in z.namelist() if m.endswith("dataset_TSMC2014_NYC.txt"))
            with z.open(member) as src, open(RAW / "dataset_TSMC2014_NYC.txt", "wb") as dst:
                shutil.copyfileobj(src, dst)
        zip_path.unlink(missing_ok=True)
        print("    saved dataset_TSMC2014_NYC.txt")
        return True
    except Exception as e:  # Drive quota / network issues
        print(f"    automatic download failed ({e})." + FOURSQUARE_MANUAL)
        return False


def get_google():
    dest = RAW / "meta-New_York.json.gz"
    if dest.exists():
        print("[2/3] Google Local metadata: already present, skipping")
        return True
    print("[2/3] Google Local metadata (New York): downloading ...")
    try:
        download(GOOGLE_URL, dest)
        with gzip.open(dest, "rt", encoding="utf-8") as f:     # sanity check: first line is a JSON record
            assert f.readline().lstrip().startswith("{")
        return True
    except Exception as e:
        print(f"    failed ({e}). Download manually from:\n    {GOOGLE_URL}\n    and put it in data/raw/")
        return False


def get_bridge():
    dest = RAW / "Brooklyn_Bridge_Automated_Pedestrian_Counts.csv"
    if list(RAW.rglob("*rooklyn*ridge*.csv")):
        print("[3/3] Brooklyn Bridge counts: already present, skipping")
        return True
    print("[3/3] Brooklyn Bridge counts: downloading from NYC Open Data ...")
    try:
        download(BRIDGE_URL, dest)
        with open(dest, encoding="utf-8") as f:
            assert "hour_beginning" in f.readline().lower()
        return True
    except Exception as e:
        print("    failed ({}). Manual: https://data.cityofnewyork.us/Transportation/"
              "Brooklyn-Bridge-Automated-Pedestrian-Counts-Demons/6fi9-q3ta -> Export -> CSV".format(e))
        return False


if __name__ == "__main__":
    ok = [get_foursquare(), get_google(), get_bridge()]
    print("\nFiles in data/raw:")
    for p in sorted(RAW.rglob("*")):
        if p.is_file():
            print(f"  {p.relative_to(RAW)}  ({p.stat().st_size / 1e6:,.1f} MB)")
    if all(ok):
        print("\nAll three datasets ready. Open src/nyc_itinerary_phase1.ipynb and Run All.")
    else:
        print("\nSome downloads need to be done manually (see messages above).")
        sys.exit(1)
