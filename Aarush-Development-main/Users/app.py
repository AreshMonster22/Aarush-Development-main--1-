from flask import Flask, render_template
from supabase import create_client

import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL") 
supabase_key = os.getenv("SUPABASE_KEY")

supabase = create_client(supabase_url, supabase_key)

@app.route("/")
def index():
    response = supabase.table("users").select("*").execute()
    counting = len(response.data)
    print(f"Successfully fetches {counting} rows!")
    return str(response.data)

if __name__ == "__main__":
    app.run()