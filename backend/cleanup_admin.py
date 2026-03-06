from database import supabase

def delete_user(email):
    print(f"Attempting to delete user: {email}")
    try:
        res = supabase.table('users').delete().eq('email', email).execute()
        if res.data:
            print(f"SUCCESS: User {email} deleted.")
        else:
            print(f"INFO: User {email} not found.")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    delete_user('admin@gmail.com')
