from pathlib import Path
from typing import Generator

def get_logs_count(path: Path) -> int:
    """
    Count the number of log files in a given directory.

    The function searches for log files with extensions ".log.gz" or "latest.log" in the specified directory and its subdirectories.
    If a directory named "logs" exists within the specified path, it will only search within this directory.

    Parameters:
    path (Path): The path to the directory to search for log files.

    Returns:
    int: The total count of log files found.
    """

    path = Path(path)
    log_count: int = 0

    def get_count(path: Path) -> int:
        count = 0
        for file in path.iterdir():
            if file.name.endswith(".log.gz") or file.name.endswith("latest.log"):
                count += 1
        return count

    if Path(path, "logs").exists():
        log_count += get_count(Path(path, "logs"))
    else:
        log_count += get_count(path)

    return log_count

def get_logs(path: Path) -> set[str]:
    """
    Retrieve a set of log files from a given directory.

    This function searches for log files with extensions ".log.gz" or "latest.log" in the specified directory and its subdirectories.
    If a directory named "logs" exists within the specified path, it will only search within this directory.

    Parameters:
    path (Path): The path to the directory to search for log files.

    Returns:
    set[str]: A set containing the absolute paths of all log files found.
    """

    path: Path = Path(path)
    logs: set[str] = set()

    def get_logs_helper(path: Path) -> None:
        for file in path.iterdir():
            if file.is_file() and (file.name.endswith(".log.gz") or file.name.endswith("latest.log")):
                if "debug" not in file.name:
                    logs.add(str(file.name))

    if Path(path, "logs").exists():
        get_logs_helper(Path(path, "logs"))
    else:
        get_logs_helper(path)

    return logs

def get_instances(path: Path) -> set[str]:
    """
    Retrieve a set of instances from a given directory.

    This function scans the specified directory and its subdirectories for directories.
    Each directory name is considered an instance.

    Parameters:
    path (Path): The path to the directory to scan for instances.

    Returns:
    set[str]: A set containing the names of all instances found.
    """

    path: Path = Path(path)

    instances: set = set()

    for file in path.iterdir():
        if file.is_dir():
            instances.add(file.name)

    print(instances)

    return instances

def get_time_from_log(path: Path):

    log_lines: tuple = tuple()

    from gzip import open, BadGzipFile
    from managers.classes import TimeBlock
    from datetime import datetime

    def get_lines() -> tuple:
        if path.suffix == ".gz":
            try:
                with open(path, 'rt') as f:
                    return tuple(f.readlines())
            except BadGzipFile:
                print(f"Error: {path.name} is not a valid gzip file.")
                return ()
        else:
            try:
                with path.open('r') as f:
                    return tuple(f.readlines())
            except Exception as e:
                print(f"An error occurred while reading {path.name}: {e}")
                return ()

    def extract_timestamp(line: str) -> str:
        if line.startswith('['):
            end_index = line.find(']')
            if end_index != -1:
                return line[1:end_index]
        return ""

    def parse_timestamp(timestamp: str) -> datetime:
        # Attempt different formats, depending on the log type
        try:
            return datetime.strptime(timestamp, "%d%b%Y %H:%M:%S.%f")  # Forge example
        except ValueError:
            try:
                return datetime.strptime(timestamp, "%H:%M:%S")  # Fabric/Minecraft example
            except ValueError:
                return None

    def get_time_start(log_lines: tuple) -> datetime:
        for line in log_lines:
            timestamp = extract_timestamp(line)
            if timestamp:
                return parse_timestamp(timestamp)
        return None

    def get_time_end(log_lines: tuple) -> datetime:
        for line in reversed(log_lines):
            timestamp = extract_timestamp(line)
            if timestamp:
                return parse_timestamp(timestamp)
        return None

    log_lines = get_lines()

    if log_lines:
        start_time = get_time_start(log_lines)
        end_time = get_time_end(log_lines)

        if start_time and end_time:
            # Calculate the difference in seconds
            duration_seconds = int((end_time - start_time).total_seconds())
            
            # Create a TimeBlock from the duration
            duration = TimeBlock.from_seconds(duration_seconds)
            duration.normalize()

            #print(f"Start Time: {start_time}")
            #print(f"End Time: {end_time}")
            #print(f"Total Playtime: {duration}")
            return duration
        else:
            #print("Could not extract valid timestamps.")
            return None
    else:
        #print("No log lines to process.")
        return None