from datetime import datetime

BUCKET = 'retail-sales-data-wh'

# Source folders
RAW_SUBFOLDERS = [
    'customers',
    'products',
    'stores',
    'sales'
]


def list_files(prefix):
    """List all files under given S3 prefix"""
    s3_path = f"s3://{BUCKET}/{prefix}"

    try:
        files = dbutils.fs.ls(s3_path)

        return [
            f.path.replace(f"s3://{BUCKET}/", "")
            for f in files
            if not f.path.endswith('/')
        ]

    except Exception as e:
        print(f"Error reading {s3_path}: {e}")
        return []


def extract_datetime(filepath):
    """
    Extract datetime from filename:
    customers_src_06052026120000.csv
    """

    filename = filepath.split('/')[-1]

    try:
        parts = filename.replace('.csv', '').split('_')

        date_part = parts[-2]
        time_part = parts[-1]

        return datetime.strptime(
            date_part + time_part,
            '%d%m%Y%H%M%S'
        )

    except:
        return datetime.min


def archive_old_files(folder_name):

    source_prefix = f"raw/{folder_name}/"
    archive_prefix = f"archive/raw/{folder_name}/"

    print(f"\nChecking folder: {source_prefix}")

    files = list_files(source_prefix)

    if len(files) <= 1:
        print("Only latest file exists — nothing to archive")
        return 0

    # Sort newest first
    sorted_files = sorted(
        files,
        key=extract_datetime,
        reverse=True
    )

    latest_file = sorted_files[0]
    old_files = sorted_files[1:]

    print(f"Keeping latest: {latest_file}")

    archived = 0

    for file in old_files:

        filename = file.split('/')[-1]

        source_path = f"s3://{BUCKET}/{file}"
        archive_path = f"s3://{BUCKET}/{archive_prefix}{filename}"

        print(f"Archiving: {filename}")

        # Copy
        dbutils.fs.cp(source_path, archive_path)

        # Delete original
        dbutils.fs.rm(source_path)

        archived += 1

    return archived


def run_archival():

    print("=" * 60)
    print("ARCHIVAL STARTED")
    print("=" * 60)

    total_archived = 0

    for folder in RAW_SUBFOLDERS:

        total_archived += archive_old_files(folder)

    print("\n" + "=" * 60)
    print(f"TOTAL FILES ARCHIVED: {total_archived}")
    print("=" * 60)


# Run
run_archival()