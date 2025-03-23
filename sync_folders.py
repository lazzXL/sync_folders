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
    """Main synchronization loop with progress feedback and clear logging."""
    import os
    import shutil
    from datetime import datetime
    
    # Create replica root if it doesn't exist
    if not os.path.exists(replica):
        os.makedirs(replica)
        logger.info(f"Created replica root: {replica}")

    while True:
        try:
            # Phase 1
            logger.info("🔄 Scanning for changes...")
            sync_start = datetime.now()
            
            for root, dirs, files in os.walk(source):
                # Creates equivalent directory structure in replica
                relative_path = os.path.relpath(root, source)
                replica_dir = os.path.join(replica, relative_path)
                
                if not os.path.exists(replica_dir):
                    os.makedirs(replica_dir)
                    logger.info(f"📁 Created directory: {replica_dir}")

                # File synchronization logic
                for file in files:
                    src_path = os.path.join(root, file)
                    rep_path = os.path.join(replica_dir, file)
                
                    copy_needed = False
                    if not os.path.exists(rep_path):
                        copy_needed = True
                        reason = "new file"
                    else:
                        # Comparation of size and modification time
                        src_stat = os.stat(src_path)
                        rep_stat = os.stat(rep_path)
                        
                        if src_stat.st_size != rep_stat.st_size:
                            copy_needed = True
                            reason = "size difference"
                        elif src_stat.st_mtime > rep_stat.st_mtime:
                            copy_needed = True
                            reason = "modification time"

                    # copy if needed
                    if copy_needed:
                        shutil.copy2(src_path, rep_path)
                        logger.info(f"📄 Copied {reason}: {file}")

            # Phase 2
            logger.info("🧹 Cleaning up orphaned files...")
            for root, dirs, files in os.walk(replica):
                relative_path = os.path.relpath(root, replica)
                source_dir = os.path.join(source, relative_path)

                # Removes files not present in source
                for file in files:
                    rep_path = os.path.join(root, file)
                    src_path = os.path.join(source_dir, file)
                    
                    if not os.path.exists(src_path):
                        os.remove(rep_path)
                        logger.info(f"🗑️ Removed orphaned file: {file}")

                # Removes empty directories
                if not os.path.exists(source_dir):
                    shutil.rmtree(root)
                    logger.info(f"📁 Removed orphaned directory: {relative_path}")

            # Calculates sync duration
            sync_duration = datetime.now() - sync_start
            logger.info(f"✅ Sync completed in {sync_duration.total_seconds():.2f}s")
            logger.info(f"⏳ Next sync in {interval} seconds...\n")

        except Exception as e:
            logger.error(f"🚨 Synchronization error: {str(e)}")
            raise

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


