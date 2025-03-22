# Imports for later

import argparse
import logging
import time

"""
Probably will use this function just haven't decided on what algorithm to use yet
def file_hash(filepath):
    import hashlib
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()
"""


def setup_logger(log_file_path):
    """Not fully developed yet."""
    logger = logging.getLogger("FolderSync")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s'))

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s'))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

def sync_folders(source, replica, logger, interval):
    # TODO 
    while True:
        logger.info(f"Syncing {source} → {replica}")
        time.sleep(interval)

def parse_args(args=None):
    """Argument parsing logic."""
    parser = argparse.ArgumentParser(description="Synchronize two folders.")
    parser.add_argument("source_path", help="Path to the source folder")
    parser.add_argument("replica_path", help="Path to the replica folder")
    parser.add_argument("interval_seconds", type=int, help="Sync interval in seconds")
    parser.add_argument("log_file_path", help="Path to the log file")
    return parser.parse_args(args)

def main():
    args = parse_args()
    logger = setup_logger(args.log_file_path)
    sync_folders(args.source_path, args.replica_path, logger, args.interval_seconds)

if __name__ == "__main__":
    main()


