import argparse
import sys
import os

from .generator import generate_logs, write_logs
from .config import LOG_LINES, OUT_PATH, OUT_FILE_NAME, MOCK_COUNT


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Generate fake nginx log entries")
    
    parser.add_argument(
        "--lines", "-l",
        type=int,
        default=LOG_LINES,
        help=f"Number of log lines to generate (default: {LOG_LINES})"
    )
    
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default=OUT_PATH,
        help=f"Directory to write logs to (default: {OUT_PATH})"
    )
    
    parser.add_argument(
        "--filename", "-f",
        type=str,
        default=OUT_FILE_NAME,
        help=f"Filename to write logs to (default: {OUT_FILE_NAME})"
    )

    parser.add_argument(
        "--mocks", "-m",
        type=int,
        default=MOCK_COUNT,
        help=f"Number of mocks to generate for remote_addr, user, user_agent, uri_path, and referer to simular real data"
    )
    
    return parser.parse_args(args)


def main(args=None):
    args = parse_args(args)
    
    print(f"Generating {args.lines} log entries...")
    logs = generate_logs(args.lines)
    
    full_path = write_logs(logs, args.output_dir, args.filename)
    print(f"Logs written to {full_path}")
    print(f"Log size: {os.path.getsize(full_path)} bytes")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())