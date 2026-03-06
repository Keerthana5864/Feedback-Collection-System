from dotenv import load_dotenv
load_dotenv()
import os

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
print(f"URL: {url}")
print(f"KEY starts with: {key[:30] if key else 'None'}")

try:
    from supabase import create_client
    client = create_client(url, key)
    r = client.table('users').select('id').limit(1).execute()
    print("SUCCESS! Connected to Supabase.")
    print("Data:", r.data)
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
