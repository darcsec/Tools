import subprocess
import ipaddress

def ping_sweep(ip_block, output_file=None):
    try:
        # Generate IP addresses in the given IP block
        network = ipaddress.ip_network(ip_block, strict=False)
        total_hosts = len(list(network.hosts()))
    except ValueError:
        print(f"Invalid IP block: {ip_block}")
        return

    if output_file is None:
        sanitized_ip_block = str(ip_block).replace('/', '_')
        output_file = f"live_hosts_{sanitized_ip_block}.txt"

    live_hosts = []

    for i, ip in enumerate(network.hosts(), start=1):
        # Execute the ping command
        result = subprocess.run(['ping', '-c', '1', '-W', '1', str(ip)], stdout=subprocess.DEVNULL)
        if result.returncode == 0:
            live_hosts.append(str(ip))
            # Print the IP in green
            print(f"\033[92m{ip} is up\033[0m")

        # Update status
        print(f"\033[95mProgress: {i}/{total_hosts}\033[0m", end='\r')  # Purple color code

    # Write live hosts to the output file
    with open(output_file, 'w') as file:
        for host in live_hosts:
            file.write(host + '\n')

    # Print summary
    num_live_hosts = len(live_hosts)
    print(f"\nTotal number of live hosts: \033[95m{num_live_hosts}\033[0m")
    print(f"Live hosts saved to: \033[95m{output_file}\033[0m")

if __name__ == "__main__":
    ip_block = input("Enter the IP or IP block (e.g., 192.168.1.0/24): ")
    output_file = input("Enter the output file name (press Enter to use default): ")
    ping_sweep(ip_block, output_file if output_file else None)
