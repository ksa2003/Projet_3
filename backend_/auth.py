import hashlib
from backend_.supabase_client import supabase

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup_user(email, password, role):
    # Check if email exists
    existing_user = supabase.table("users").select("email").eq("email", email).execute()
    
    if existing_user.data:
        return {"success": False, "error": "Email already exists."}

    try:
        hashed_password = hash_password(password)
        response = supabase.table("users").insert({
            "email": email,
            "password": hashed_password,
            "role": role
        }).execute()

        return {"success": True, "data": response.data} if response.data else \
               {"success": False, "error": "Account creation failed."}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

def login_user(email, password):
    try:
        existing_user = supabase.table("users").select("*").eq("email", email).execute()
        
        if not existing_user.data:
            return {"success": False, "error": "Invalid email or password."}

        user = existing_user.data[0]
        hashed_password = hash_password(password)
        
        return {"success": True, "user": user} if user["password"] == hashed_password else \
               {"success": False, "error": "Invalid email or password."}

    except Exception as e:
        return {"success": False, "error": str(e)}