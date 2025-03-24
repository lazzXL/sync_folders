import os
import logging
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sync_folders import setup_logger, sync_folders, parse_args

# Test 1: Logger configuration
def test_setup_logger(tmpdir):
    """Test for if logger creates file and outputs to console."""
    log_file = tmpdir.join("test.log")
    logger = setup_logger(str(log_file))
    
    assert len(logger.handlers) == 2
    assert isinstance(logger.handlers[0], logging.FileHandler)
    assert isinstance(logger.handlers[1], logging.StreamHandler)

    logger.info("Test message")
    with open(log_file, 'r') as f:
        assert "[20" in f.read() 

# Test 2: Argument parsing
def test_arg_parsing():
    # Mock command-line arguments
    test_args = [
        "source_folder", 
        "replica_folder", 
        "60", 
        "sync.log"
    ]

    args = parse_args(test_args)
    
    assert args.source_path == "source_folder"
    assert args.replica_path == "replica_folder"
    assert args.interval_seconds == 60
    assert args.log_file_path == "sync.log"

# Test 3: Basic folder synchronization testing
def test_sync_basic_operations(tmpdir):
    """Test file creation/deletion with controlled sync cycles"""
    # Setup test folders
    source = tmpdir.mkdir("source")
    replica = tmpdir.mkdir("replica")
    log_file = tmpdir.join("sync.log")
    logger = setup_logger(str(log_file))

    # Test 1
    test_file = source.join("test.txt")
    test_file.write("Hello World")
    
    # Runs one cycle
    sync_folders(str(source), str(replica), logger, 1, max_cycles=1)
    assert os.path.exists(os.path.join(replica, "test.txt"))

    # Test 2
    test_file.remove()

    sync_folders(str(source), str(replica), logger, 1, max_cycles=1)
    assert not os.path.exists(os.path.join(replica, "test.txt"))

# Test 4: Nested directory creation
def test_nested_directory(tmpdir):
    """Test directory structure with controlled sync"""
    source = tmpdir.mkdir("source")
    replica = tmpdir.mkdir("replica")
    log_file = tmpdir.join("sync.log")
    logger = setup_logger(str(log_file))

    nested_dir = source.mkdir("subdir")
    test_file = nested_dir.join("file.txt")
    test_file.write("Content")

    sync_folders(str(source), str(replica), logger, 0.1, max_cycles=1)
    assert os.path.exists(os.path.join(replica, "subdir/file.txt"))