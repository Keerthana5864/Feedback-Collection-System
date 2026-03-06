import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_admin_stats():
    print("--- Testing Admin Stats ---")
    try:
        # We know Institution ID 1001 exists
        params = {"institution_id": 1001}
        response = requests.get(f"{BASE_URL}/admin/stats", params=params)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        if data['status'] == 'success':
            stats = data['data']
            print(f"Total Feedbacks: {stats['total_feedback']}")
            print(f"Average Rating: {stats['average_rating']}")
            print(f"Latest Feedback: {stats['feedback'][-1]['student_name'] if stats['feedback'] else 'None'}")
        else:
            print(f"Error: {data['message']}")
            
    except Exception as e:
        print(f"Error during stats test: {e}")

if __name__ == "__main__":
    test_admin_stats()
