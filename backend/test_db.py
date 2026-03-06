from database import supabase
try:
    res = supabase.table('users').select('count', count='exact').execute()
    print(f"Success! Users count: {res.count}")
except Exception as e:
    print(f"Error: {e}")
