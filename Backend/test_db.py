import psycopg2
try:
    conn = psycopg2.connect("postgresql://postgres:IAFITP_12026@db.erdynerdhojvzguhhaiv.supabase.co:5432/postgres")
    print("Connected successfully using direct connection!")
    conn.close()
except Exception as e:
    print(f"Direct Connection Error: {e}")

try:
    conn = psycopg2.connect("postgresql://postgres.erdynerdhojvzguhhaiv:IAFITP_12026@aws-1-us-east-1.pooler.supabase.com:6543/postgres")
    print("Connected successfully using pooler connection!")
    conn.close()
except Exception as e:
    print(f"Pooler Connection Error: {e}")
