from database import supabase
import sys

def check_db():
    print("--- Supabase Diagnostic ---")
    try:
        # Check if users table exists by selecting 1 row
        res = supabase.table('users').select('*').execute()
        print("[SUCCESS] 'users' table access")
        print(f"Total users: {len(res.data)}")
        for i, user in enumerate(res.data):
            print(f"User {i+1}: Email='{user.get('email')}', Role='{user.get('role')}'")
    except Exception as e:
        print(f"[FAILED] 'users' table access")
        print(f"Error: {e}")

    try:
        # Check if feedback table exists
        res = supabase.table('feedback').select('*').limit(1).execute()
        print("[SUCCESS] 'feedback' table access")
    except Exception as e:
        print("[FAILED] 'feedback' table access")
        print(f"Error: {e}")

if __name__ == "__main__":
    check_db()
