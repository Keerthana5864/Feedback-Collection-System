import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_password_reset_phone():
    print("--- Testing Password Reset (Phone) ---")
    # Step 1: Request OTP
    payload_step1 = {
        "email": "student@demo.com",
        "phone": "9876543210" # This matches the feedback I just submitted for this student account? 
        # Wait, the student_id in feedback was 'student@demo.com''s ID.
    }
    try:
        response = requests.post(f"{BASE_URL}/forgot-password-phone", json=payload_step1)
        print(f"Step 1 Status: {response.status_code}")
        data = response.json()
        if data['status'] == 'success':
            otp = data['otp']
            print(f"Generated OTP: {otp}")
            
            # Step 2: Reset Password
            payload_step2 = {
                "email": "student@demo.com",
                "new_password": "newpassword123"
            }
            response2 = requests.post(f"{BASE_URL}/reset-password-phone", json=payload_step2)
            print(f"Step 2 Status: {response2.status_code}")
            print(f"Reset Result: {response2.text}")
        else:
            print(f"Error in Step 1: {data['message']}")
            
    except Exception as e:
        print(f"Error during password reset test: {e}")

if __name__ == "__main__":
    test_password_reset_phone()
