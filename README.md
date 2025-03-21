# Folder Synchronizer

A Python script to synchronize two folders (source and replica).

*Developed by Gabriel Lemos.*

(in due development)
## Usage
```bash
python sync_folders.py [source_path] [replica_path] [interval_seconds] [log_file_path]
```

## Command-Line Arguments

The script requires the following arguments to be passed via the command line:

| Argument           | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| `source_path`      | Path to the source folder (original files).                                 |
| `replica_path`     | Path to the replica folder (will mirror the source folder).                 |
| `interval_seconds` | Synchronization interval in seconds (e.g., `60` for 1 minute).              |
| `log_file_path`    | Path to the log file where operations will be recorded (e.g., `sync.log`).  |

### Example
```bash
python sync_folders.py ./source_folder ./replica_folder 120 ./sync.log
