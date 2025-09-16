import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    # Test status endpoint
    print("Testing /api/status...")
    try:
        response = requests.get(f"{base_url}/api/status")
        print("Status:", response.status_code)
        print("Response:", response.json())
    except Exception as e:
        print("Error:", e)
    
    # Test ask endpoint
    print("\nTesting /api/ask...")
    try:
        payload = {
            "question": "Qu'est-ce que la loi d'Ohm?",
            "subject_filter": "physique"
        }
        response = requests.post(f"{base_url}/api/ask", json=payload)
        print("Status:", response.status_code)
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Error:", response.text)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_api()