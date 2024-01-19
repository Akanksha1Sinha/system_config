import psutil
import speedtest
import platform
import socket
import wmi
import platform
import subprocess
import uuid
import subprocess

def get_installed_software():
    c = wmi.WMI()
    software_list = []

    for product in c.Win32_Product():
        software_list.append(product.Caption)

    return software_list

def get_internet_speed():
    try:
        result = subprocess.check_output(['speedtest-cli', '--simple'], text=True)
        lines = result.strip().split('\n')

        if len(lines) >= 2:
            download_speed = float(lines[0].split()[1]) / 10**6  # in Mbps
            upload_speed = float(lines[1].split()[1]) / 10**6  # in Mbps
            return download_speed, upload_speed
        else:
            return "Invalid output format from speedtest-cli"
    except FileNotFoundError:
        return "speedtest-cli not found. Please install it using: pip install speedtest-cli"
    except Exception as e:
        return f"Error: {e}"


def get_screen_resolution():
    try:
        import screeninfo
        screen = screeninfo.get_monitors()[0]
        return screen.width, screen.height
    except ImportError:
        return "Screeninfo library not installed"

def get_cpu_info():
    cpu_info = {
        "model": platform.processor(),
        "cores": psutil.cpu_count(logical=False),
        "threads": psutil.cpu_count(logical=True)
    }
    return cpu_info

def get_gpu_info():
    try:
        c = wmi.WMI()
        for gpu in c.Win32_VideoController():
            return gpu.Caption
        return "No GPU detected"
    except ImportError:
        return "wmi library not installed"

def get_ram_size():
    ram_info = psutil.virtual_memory()
    return ram_info.total // (2**30)  # Convert to GB

def get_screen_size():
    try:
        import screeninfo
        screen = screeninfo.get_monitors()[0]
        diagonal_size = ((screen.width ** 2) + (screen.height ** 2)) ** 0.5
        return round(diagonal_size / 25.4, 1)  # Convert to inches
    except ImportError:
        return "Screeninfo library not installed"

def get_mac_address(interface="Wi-Fi"):
    try:
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(5, -1, -1)])
        return mac_address
    except ImportError:
        return "uuid library not installed"

def get_public_ip_address():
    try:
        ip_address = socket.gethostbyname(socket.gethostname())
        return ip_address
    except socket.gaierror:
        return "Unable to retrieve public IP address"

def get_windows_version():
    return platform.version()

if __name__ == "__main__":
    print("Installed Software:")
    print(get_installed_software())

    print("\nInternet Speed:")
    speed_results = get_internet_speed()

    if isinstance(speed_results, tuple):
        download_speed, upload_speed = speed_results
        print(f"Download Speed: {download_speed:.2f} Mbps")
        print(f"Upload Speed: {upload_speed:.2f} Mbps")
    else:
        print(speed_results)

    print("\nScreen Resolution:")
    print(get_screen_resolution())

    print("\nCPU Information:")
    cpu_info = get_cpu_info()
    print(f"Model: {cpu_info['model']}")
    print(f"Number of Cores: {cpu_info['cores']}")
    print(f"Number of Threads: {cpu_info['threads']}")

    print("\nGPU Information:")
    print(get_gpu_info())

    print("\nRAM Size:")
    print(f"{get_ram_size()} GB")

    print("\nScreen Size:")
    print(f"{get_screen_size()} inches")

    print("\nMAC Address:")
    print(f"Wi-Fi MAC Address: {get_mac_address()}")

    print("\nPublic IP Address:")
    print(get_public_ip_address())

    print("\nWindows Version:")
    print(get_windows_version())

