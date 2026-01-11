import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from app.main import app
import tempfile

client = TestClient(app)

def test_upload():
    print("Testing upload functionality...")
    
    # 1. Test if API is accessible
    response = client.get("/")
    print(f"1. API root: {response.status_code} - {response.json()}")
    
    # 2. Test stats endpoint
    response = client.get("/stats/")
    print(f"2. Stats endpoint: {response.status_code} - {response.json()}")
    
    # 3. Create a test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Test document content for DocSlim\n" * 100)
        temp_file = f.name
    
    # 4. Try to upload
    print(f"3. Attempting upload of {temp_file}...")
    with open(temp_file, 'rb') as file:
        files = {'file': ('test.txt', file)}
        response = client.post("/upload/", files=files)
        
    print(f"   Upload response: {response.status_code}")
    if response.status_code == 200:
        print(f"   Success: {response.json()}")
    else:
        print(f"   Error: {response.text}")
    
    # 5. Clean up
    os.unlink(temp_file)
    
    print("\n✅ Test completed")

if __name__ == "__main__":
    test_upload()