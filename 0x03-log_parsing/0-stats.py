#!/usr/bin/python3

import sys
import signal
import re

def print_metrics(status_counts, total_file_size):
    """
    Prints metrics: total file size and number of lines by status code.
    Args:
        status_counts (dict): Dictionary containing counts of status codes.
        total_file_size (int): Total accumulated file size.
    """
    print(f"Total file size: {total_file_size}")
    for code in sorted(status_counts.keys()):
        count = status_counts[code]
        if count > 0:
            print(f"{code}: {count}")

def handle_interrupt(signal, frame):
    """
    Signal handler function for SIGINT (Ctrl + C).
    Args:
        signal: The signal number.
        frame: The current stack frame (not used).
    """
    print("\nInterrupted. Printing current metrics:")
    print_metrics(status_counts, total_file_size)
    sys.exit(0)

def main():
    total_file_size = 0
    status_counts = {
        "200": 0,
        "301": 0,
        "400": 0,
        "401": 0,
        "403": 0,
        "404": 0,
        "405": 0,
        "500": 0
    }
    line_counter = 0

    # Set up signal handler for SIGINT (Ctrl + C)
    signal.signal(signal.SIGINT, handle_interrupt)

    try:
        for line in sys.stdin:
            line = line.strip()  # Remove leading/trailing whitespace
            
            # Define a regex pattern for matching expected line format
            pattern = r'^(\S+) - \[([^\]]+)\] "GET \/projects\/260 HTTP\/1\.1" (\d+) (\d+)$'
            match = re.match(pattern, line)
            
            if not match:
                # Skip lines that do not match the expected format
                continue
            
            # Extract parts from matched groups
            ip_address = match.group(1)
            date = match.group(2)
            status_code = match.group(3)
            file_size = int(match.group(4))
            
            # Update metrics
            total_file_size += file_size
            if status_code in status_counts:
                status_counts[status_code] += 1
            
            line_counter += 1
            
            # Print metrics every 10 lines
            if line_counter == 10:
                print_metrics(status_counts, total_file_size)
                line_counter = 0

    except Exception as e:
        # Handle other exceptions gracefully
        print(f"Error: {e}")

    finally:
        # Print final metrics before exiting
        print("\nFinal metrics:")
        print_metrics(status_counts, total_file_size)

if __name__ == "__main__":
    main()

