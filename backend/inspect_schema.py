from database import supabase

def inspect_schema():
    print("--- Inspecting Tables ---")
    try:
        # Try to select from institutions
        try:
            res = supabase.table('institutions').select('*').limit(1).execute()
            print("Table 'institutions' exists.")
        except Exception as e:
            print(f"Table 'institutions' error/missing: {e}")

        # Check users columns
        try:
            res = supabase.table('users').select('*').limit(1).execute()
            if res.data:
                print(f"Table 'users' columns: {list(res.data[0].keys())}")
            else:
                print("Table 'users' exists but is empty.")
        except Exception as e:
            print(f"Table 'users' error: {e}")

        # Check feedback columns
        try:
            res = supabase.table('feedback').select('*').limit(1).execute()
            if res.data:
                print(f"Table 'feedback' columns: {list(res.data[0].keys())}")
            else:
                print("Table 'feedback' exists but is empty.")
        except Exception as e:
            print(f"Table 'feedback' error: {e}")

    except Exception as e:
        print(f"Global error: {e}")

if __name__ == "__main__":
    inspect_schema()
