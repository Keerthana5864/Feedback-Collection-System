from database import supabase

try:
    # Try to insert a dummy response to see if the column exists
    res = supabase.table('feedback').select('*').limit(1).execute()
    if res.data:
        test_id = res.data[0]['id']
        print(f"Testing update on feedback ID: {test_id}")
        update_res = supabase.table('feedback').update({"admin_response": "Test"}).eq('id', test_id).execute()
        print("Update successful!")
    else:
        print("No feedback found to test.")
except Exception as e:
    print(f"Error: {e}")
