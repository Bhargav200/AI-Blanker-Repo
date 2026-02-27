import requests
import time
import os
import json

BASE_URL = "http://localhost:8000"

def test_backend_up():
    print("\n--- Testing Backend Connection ---")
    url = f"{BASE_URL}/"
    for i in range(10):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("✅ Backend is UP!")
                return True
        except:
            print(f"Waiting for backend... ({i+1}/10)")
            time.sleep(2)
    print("❌ Backend failed to start.")
    return False

def test_full_redaction_flow():
    print("\n--- Testing Full Redaction Flow ---")
    
    # 1. Create a dummy file
    test_file_path = "test_redaction.txt"
    test_content = "My name is John Doe and my email is john.doe@example.com."
    with open(test_file_path, "w") as f:
        f.write(test_content)
    
    try:
        # 2. Start a redaction job
        print(f"Creating job with file: {test_file_path}")
        with open(test_file_path, 'rb') as f:
            files = {'files': f}
            data = {
                "redaction_mode": "Mask",
                "confidence_threshold": "0.5",
                "pii_categories": json.dumps(["PERSON", "EMAIL"])
            }
            response = requests.post(f"{BASE_URL}/jobs/create", files=files, data=data)
            if response.status_code != 200:
                print(f"❌ Failed to create job: {response.text}")
                return False
            
            job_data = response.json()
            job_id = job_data['job_id']
            print(f"✅ Job created successfully! ID: {job_id}")
            
        # 3. Wait for job to complete
        print("Waiting for job to complete...")
        max_retries = 30
        for _ in range(max_retries):
            status_res = requests.get(f"{BASE_URL}/jobs/{job_id}")
            job_status = status_res.json()
            if job_status['status'] == "Completed":
                print("✅ Job completed successfully!")
                break
            elif job_status['status'] == "Failed":
                print(f"❌ Job failed: {job_status.get('error_message')}")
                return False
            time.sleep(1)
        else:
            print("❌ Job timed out.")
            return False
        
        # 4. Verify file details and visual preview
        file_id = job_status['files'][0]['id']
        file_res = requests.get(f"{BASE_URL}/files/{file_id}")
        file_details = file_res.json()
        
        print(f"Checking file details for File ID: {file_id}")
        
        # Verify visual preview exists and is an image
        visual_res = requests.get(f"{BASE_URL}/files/{file_id}/visual")
        if visual_res.status_code == 200 and visual_res.headers.get('Content-Type', '').startswith('image/'):
            print("✅ Visual preview verified as an image.")
        else:
            print(f"❌ Visual preview check failed! Status: {visual_res.status_code}, Type: {visual_res.headers.get('Content-Type')}")
            return False
            
        raw = file_details.get('raw_content')
        redacted = file_details.get('redacted_content')
        
        if raw == test_content:
            print("✅ Raw content matches original text.")
        else:
            print(f"❌ Raw content mismatch! Expected: {test_content}, Got: {raw}")
            return False
            
        if redacted and "[REDACTED]" in redacted:
            print(f"✅ Redacted content verified: {redacted}")
        else:
            print(f"❌ Redacted content check failed: {redacted}")
            return False
            
        return True
        
    finally:
        # Cleanup
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

if __name__ == "__main__":
    if test_backend_up():
        if test_full_redaction_flow():
            print("\n🎉 All backend tests passed!")
        else:
            print("\n❌ Backend tests failed.")
