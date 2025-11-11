import socket
import argparse
import concurrent.futures
import ipaddress

def scan_port(ip, port, timeout=1):
    """
    Scans a single port on the given IP address to check if it's open.

    Args:
        ip (str): The IP address to scan.
        port (int): The port number to scan.
        timeout (float): Timeout for the connection attempt in seconds.

    Returns:
        tuple: (port, status) where status is 'Open' if the port is open, 'Closed' otherwise.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            return (port, 'Open')
        else:
            return (port, 'Closed')
    except socket.error:
        return (port, 'Error')

def scan_ports(ip, start_port, end_port, max_threads=100):
    """
    Scans a range of ports on the given IP address using multithreading.

    Args:
        ip (str): The IP address to scan.
        start_port (int): The starting port number.
        end_port (int): The ending port number.
        max_threads (int): Maximum number of threads to use.

    Returns:
        list: List of tuples (port, status) for each port scanned.
    """
    ports = range(start_port, end_port + 1)
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(scan_port, ip, port) for port in ports]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    # Sort results by port number
    results.sort(key=lambda x: x[0])
    return results

def display_results(results):
    """
    Displays the scan results in a clean table format.

    Args:
        results (list): List of tuples (port, status).
    """
    print(f"{'Port':<10} {'Status':<10}")
    print("-" * 20)
    for port, status in results:
        if status == 'Open':
            print(f"{port:<10} {status:<10}")

def validate_ip(ip):
    """
    Validates if the given string is a valid IP address.

    Args:
        ip (str): The IP address string to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def main():
    """
    Main function to parse arguments, perform the scan, and display results.
    """
    parser = argparse.ArgumentParser(description='Port Scanner Tool')
    parser.add_argument('ip', help='IP address to scan')
    parser.add_argument('start_port', type=int, help='Starting port number')
    parser.add_argument('end_port', type=int, help='Ending port number')
    parser.add_argument('--threads', type=int, default=100, help='Maximum number of threads (default: 100)')

    args = parser.parse_args()

    ip = args.ip
    start_port = args.start_port
    end_port = args.end_port
    max_threads = args.threads

    # Validate IP address
    if not validate_ip(ip):
        print(f"Error: Invalid IP address '{ip}'")
        return

    # Validate port range
    if start_port < 1 or end_port > 65535 or start_port > end_port:
        print("Error: Invalid port range. Ports must be between 1 and 65535, and start_port <= end_port.")
        return

    print(f"Scanning {ip} from port {start_port} to {end_port}...")

    try:
        results = scan_ports(ip, start_port, end_port, max_threads)
        open_ports = [result for result in results if result[1] == 'Open']

        if open_ports:
            print(f"\nOpen ports found:")
            display_results(open_ports)
        else:
            print(f"\nNo open ports found in the range {start_port}-{end_port}.")

    except Exception as e:
        print(f"Error during scanning: {e}")

if __name__ == "__main__":
    main()
