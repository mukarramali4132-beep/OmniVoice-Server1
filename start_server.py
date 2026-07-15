import subprocess
import sys
import time
import requests
import os
import signal

SERVER_URL = "http://127.0.0.1:8000/health"

print("=" * 70)
print("OmniVoice Server Startup")
print("=" * 70)

# ---------------------------------------------------------
# Kill previous launcher
# ---------------------------------------------------------

try:
    if os.name == "nt":
        subprocess.run(
            "taskkill /F /IM python.exe",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        subprocess.run(
            "pkill -f launcher.py",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
except Exception:
    pass

# ---------------------------------------------------------
# Start Server
# ---------------------------------------------------------

print("Starting FastAPI...")

process = subprocess.Popen(
    [sys.executable, "launcher.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
)

# ---------------------------------------------------------
# Wait Until Ready
# ---------------------------------------------------------

TIMEOUT = 300

START = time.time()

READY = False

while True:

    line = process.stdout.readline()

    if line:
        print(line.rstrip())

    try:

        response = requests.get(
            SERVER_URL,
            timeout=2,
        )

        if response.status_code == 200:

            data = response.json()

            if data.get("success"):

                READY = True

                break

    except Exception:
        pass

    if process.poll() is not None:

        print("\nServer exited unexpectedly.")

        sys.exit(1)

    if time.time() - START > TIMEOUT:

        print("\nStartup timeout.")

        process.kill()

        sys.exit(1)

    time.sleep(2)

print()

print("=" * 70)
print("SERVER READY")
print("=" * 70)

print(response.json())

print()

print(
    "Now start Cloudflare in another terminal:"
)

print()

if os.name == "nt":

    print(
        "cloudflared tunnel --url http://127.0.0.1:8000"
    )

else:

    print(
        "./cloudflared tunnel --url http://127.0.0.1:8000"
    )

print()

process.wait()