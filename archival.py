from datetime import datetime

BUCKET = 'retail-sales-data-wh'

RAW_SUBFOLDERS = ['customers', 'products', 'stores', 'sales']


def list_files(prefix):
    """List all CSV files under given S3 prefix"""
    s3_path = f"s3://{BUCKET}/{prefix}"
    try:
        files = dbutils.fs.ls(s3_path)
        csv_files = [
            f.path.replace(f"s3://{BUCKET}/", "")
            for f in files
            if f.path.endswith('.csv')  # only CSV, skip folders
        ]
        return csv_files
    except Exception as e:
        print(f" Error reading {s3_path}: {e}")
        return []


def extract_datetime(filepath):
    """
    Extract datetime from filename.
    Supports any prefix — takes LAST two underscore parts as date+time.
    
    Example: customers_src_20042026100105.csv
    Example: sales_transactions_src_20042026100107.csv
    
    Always: second-to-last part = DDMMYYYY, last part = HHMMSS
    """
    filename = filepath.split('/')[-1].replace('.csv', '')
    parts = filename.split('_')
    
    try:
        date_part = parts[-2]  # e.g. '20042026'
        time_part = parts[-1]  # e.g. '100105'
        
        dt = datetime.strptime(date_part + time_part, '%d%m%Y%H%M%S')
        
        # ✅ Debug print so you can verify parsing is correct
        print(f"    📅 Parsed: {filename} → {dt.strftime('%d %b %Y %H:%M:%S')}")
        
        return dt
        
    except Exception as e:
        print(f" Could not parse datetime from: {filename} → Error: {e}")
        return datetime.min  # treat unparseable as oldest


def archive_old_files(folder_name):
    """
    Keep only the NEWEST file in raw/folder/.
    Move all older files to archive/raw/folder/.
    """
    source_prefix  = f"raw/{folder_name}/"
    archive_prefix = f"archive/raw/{folder_name}/"

    print(f"\n{'─'*50}")
    print(f" Folder: {source_prefix}")

    files = list_files(source_prefix)

    if not files:
        print(" No files found — skipping")
        return 0

    print(f"  Found {len(files)} file(s):")
    for f in files:
        print(f"    → {f.split('/')[-1]}")

    if len(files) == 1:
        print(" Only 1 file — nothing to archive")
        return 0

    # ── Sort with debug ──────────────────────────────────────
    print("\n  Parsing datetimes:")
    files_with_dt = [(f, extract_datetime(f)) for f in files]

    # Sort ASCENDING first so we can clearly see order
    files_with_dt.sort(key=lambda x: x[1])

    print("\n  Sorted oldest → newest:")
    for f, dt in files_with_dt:
        print(f"    {f.split('/')[-1]}  →  {dt.strftime('%d %b %Y %H:%M:%S')}")

    # ── Newest = LAST item after ascending sort ──────────────
    latest_file = files_with_dt[-1][0]   #  LAST = newest
    old_files   = [f for f, dt in files_with_dt[:-1]]  # everything before last

    print(f"\n  KEEPING  (newest): {latest_file.split('/')[-1]}")
    print(f"  ARCHIVING {len(old_files)} old file(s):")

    archived = 0
    for file in old_files:
        filename     = file.split('/')[-1]
        source_path  = f"s3://{BUCKET}/{file}"
        archive_path = f"s3://{BUCKET}/{archive_prefix}{filename}"

        print(f"\n    Moving: {filename}")
        print(f"    From  : {source_path}")
        print(f"    To    : {archive_path}")

        try:
            dbutils.fs.cp(source_path, archive_path)   # copy to archive
            dbutils.fs.rm(source_path)                 # delete from raw
            print(f"  Done")
            archived += 1
        except Exception as e:
            print(f"  FAILED: {e}")

    return archived


def run_archival():
    print("=" * 50)
    print(" ARCHIVAL PROCESS STARTED")
    print(f"   Time: {datetime.now().strftime('%d %b %Y %H:%M:%S')}")
    print("=" * 50)

    total_archived = 0
    for folder in RAW_SUBFOLDERS:
        total_archived += archive_old_files(folder)

    print(f"\n{'='*50}")
    print(f" ARCHIVAL COMPLETE")
    print(f"   Total files archived: {total_archived}")
    print(f"{'='*50}")


# Run
run_archival()