import subprocess
import time
import sys
import os

def run_backend():
    print("Starting Backend (FastAPI)...")
    return subprocess.Popen([sys.executable, "-m", "uvicorn", "main:app", "--reload", "--port", "8000"])

def run_frontend():
    print("Starting Frontend (Streamlit)...")
    return subprocess.Popen([sys.executable, "-m", "streamlit", "run", "app.py"])

if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs("storage/input", exist_ok=True)
    os.makedirs("storage/output", exist_ok=True)
    os.makedirs("storage/logs", exist_ok=True)
    os.makedirs("storage/temp", exist_ok=True)
    os.makedirs("database", exist_ok=True)

    backend_proc = run_backend()
    time.sleep(5) # Wait for backend to start
    frontend_proc = run_frontend()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        backend_proc.terminate()
        frontend_proc.terminate()
