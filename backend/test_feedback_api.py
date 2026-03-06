import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_feedback_submission():
    print("--- Testing Feedback Submission ---")
    # First, get a student_id from users table
    try:
        from database import supabase
        student = supabase.table('users').select('id, institution_id').eq('email', 'student@demo.com').single().execute().data
        if not student:
            print("Student user not found.")
            return

        payload = {
            "student_id": student['id'],
            "institution_id": student['institution_id'],
            "student_name": "Test Student",
            "roll_no": "12345",
            "phone_number": "9876543210",
            "subject": "Mathematics",
            "teacher": "Dr. Smith",
            "rating": 4,
            "comments": "Great teaching style!"
        }
        
        response = requests.post(f"{BASE_URL}/feedback", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error during feedback test: {e}")

if __name__ == "__main__":
    test_feedback_submission()
