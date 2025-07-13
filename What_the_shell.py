#!/bin/python3

from termcolor import colored
import argparse
import json
import urllib.parse
import base64
import ipaddress
import os


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


# Load payloads
with open("data/payloads.json") as f:
    PAYLOADS = json.load(f)

# Encoding helpers
def encode_payload(payload, encoding):
    if encoding == "url":
        return urllib.parse.quote_plus(payload)
    elif encoding == "base64":
        return base64.b64encode(payload.encode()).decode()
    return payload

# IP validation
def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

# Port validation
def is_valid_port(port):
    try:
        port = int(port)
        return 1 <= port <= 65535
    except ValueError:
        return False

# Render payload with variables
def render_payload(template, ip, port, shell):
    return template.replace("{ip}", ip).replace("{port}", str(port)).replace("{shell}", shell)

# Main logic
def main():
    parser = argparse.ArgumentParser(description="CLI Reverse Shell Generator (like revshells.com)")
    parser.add_argument("--ip", required=True, help="Attacker IP address")
    parser.add_argument("--port", required=True, type=int, help="Listening port")
    parser.add_argument("--os", required=True, choices=PAYLOADS.keys(), help="Target OS")
    parser.add_argument("--payload", required=False, help="Payload name (run with --list to view options)")
    parser.add_argument("--shell", default="/bin/bash", help="Shell to use for injection")
    parser.add_argument("--encode", choices=["none", "url", "base64"], default="none", help="Encoding option")
    parser.add_argument("--list", action="store_true", help="List available payloads for the selected OS")

    args = parser.parse_args()

    if not is_valid_ip(args.ip):
        print("[!] Invalid IP address")
        return
    if not is_valid_port(args.port):
        print("[!] Invalid port")
        return

    os_payloads = PAYLOADS.get(args.os, {})

    if args.list:
        print(f"\nAvailable payloads for {args.os}:")
        for name in os_payloads:
            print(f" - {name}")
        return

    if not args.payload or args.payload not in os_payloads:
        print("[!] Invalid or missing payload name. Use --list to see options.")
        return

    template = os_payloads[args.payload]
    rendered = render_payload(template, args.ip, args.port, args.shell)
    encoded = encode_payload(rendered, args.encode)

    print(colored(f"\n[+] Final Payload:\n{encoded}\n", 'green'))

if __name__ == "__main__":
    main()
