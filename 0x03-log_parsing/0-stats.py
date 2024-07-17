#!/usr/bin/python3

import sys

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

    try:
        for line in sys.stdin:
            line = line.strip()  # Remove leading/trailing whitespace
            parts = line.split()  # Split by whitespace
            
            if len(parts) < 10:
                # Skip lines that do not match the expected format
                continue
            
            # Extract parts
            ip_address = parts[0]
            date = parts[3].strip('[]')  # Remove brackets from date
            status_code = parts[-2]
            file_size = int(parts[-1])
            
            # Update metrics
            total_file_size += file_size
            if status_code in status_counts:
                status_counts[status_code] += 1
            
            line_counter += 1
            
            # Print metrics every 10 lines
            if line_counter == 10:
                print_metrics(status_counts, total_file_size)
                line_counter = 0

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl + C)
        pass

    # Print final metrics
    print_metrics(status_counts, total_file_size)

if __name__ == "__main__":
    main()

