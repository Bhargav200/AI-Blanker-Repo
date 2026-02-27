import requests
import time

def test_backend():
    url = "http://localhost:8000/"
    for i in range(10):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("Backend is UP!")
                return True
        except:
            print(f"Waiting for backend... ({i+1}/10)")
            time.sleep(2)
    print("Backend failed to start.")
    return False

if __name__ == "__main__":
    test_backend()
