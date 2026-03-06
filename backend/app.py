from flask import Flask, request, jsonify
from flask_cors import CORS
from database import supabase
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    print(f"[LOGIN] Attempt for: {data.get('email')}")
    email = data.get('email', '').strip().lower()
    password = data.get('password')
    institution_id = data.get('institution_id')
    
    try:
        # Cast to int if it's a numeric string, otherwise keep as is
        try:
            search_id = int(institution_id) if institution_id else None
        except (ValueError, TypeError):
            search_id = institution_id

        query = supabase.table('users').select('*').eq('email', email)
        if search_id:
            query = query.eq('institution_id', search_id)
            
        response = query.single().execute()
        user = response.data
        
        if user and user['password'] == password:
            print(f"[LOGIN] Success for: {email}")
            return jsonify({
                "status": "success",
                "user": {
                    "id": user['id'],
                    "email": user['email'],
                    "role": user['role'],
                    "institution_id": user.get('institution_id')
                }
            })
        else:
            print(f"[LOGIN] Failed for: {email} (Invalid credentials)")
            return jsonify({"status": "error", "message": "Invalid email, password, or institution"}), 401
    except Exception as e:
        print(f"[LOGIN] Exception for {email}: {e}")
        return jsonify({"status": "error", "message": "User not found or database error"}), 500

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    print(f"\n[REGISTER REQUEST] Data: {data}")
    try:
        email = data.get('email', '').strip().lower()
        institution_id = data.get('institution_id')
        
        if not email:
            return jsonify({"status": "error", "message": "Email is required"}), 400
        if not institution_id:
            return jsonify({"status": "error", "message": "Institution ID is required"}), 400
            
        # Update data with normalized email
        data['email'] = email

        # Check existing in THIS institution
        existing = supabase.table('users').select('*').eq('email', email).eq('institution_id', institution_id).execute()
        if existing.data:
            print(f"[REGISTER] FAILED: {email} already exists in institution {institution_id}")
            return jsonify({"status": "error", "message": "Email already registered in this institution"}), 400
            
        print(f"[REGISTER] Inserting into Supabase: {email}")
        response = supabase.table('users').insert(data).execute()
        
        if response.data:
            print(f"[REGISTER] SUCCESS: Created user {email}")
            return jsonify({"status": "success", "data": response.data})
        else:
            print(f"[REGISTER] FAILED: Insert returned no data for {email}")
            return jsonify({"status": "error", "message": "Database insert failed"}), 500
            
    except Exception as e:
        print(f"[REGISTER] CRITICAL ERROR: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/institutions/register', methods=['POST'])
def register_institution():
    data = request.json
    try:
        # 1. Create Institution
        institution_data = {
            "name": data.get('name'),
            "slug": data.get('slug', data.get('name', '').lower().replace(' ', '-'))
        }
        inst_resp = supabase.table('institutions').insert(institution_data).execute()
        
        if not inst_resp.data:
            return jsonify({"status": "error", "message": "Failed to create institution"}), 500
            
        institution = inst_resp.data[0]
        
        # 2. Create Admin User for this institution
        admin_data = {
            "email": data.get('admin_email').strip().lower(),
            "password": data.get('admin_password'),
            "role": "admin",
            "institution_id": institution['id']
        }
        user_resp = supabase.table('users').insert(admin_data).execute()
        
        return jsonify({
            "status": "success",
            "institution": institution,
            "admin": user_resp.data[0] if user_resp.data else None
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    try:
        # Ensure institution_id is an integer for BigInt column
        if 'institution_id' in data:
            try:
                data['institution_id'] = int(data['institution_id'])
            except (ValueError, TypeError):
                pass
                
        # Expected fields: student_id, student_name, phone_number, subject, teacher, rating, comments
        response = supabase.table('feedback').insert(data).execute()
        return jsonify({"status": "success", "data": response.data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/admin/stats', methods=['GET'])
def get_stats():
    institution_id = request.args.get('institution_id')
    if not institution_id:
        return jsonify({"status": "error", "message": "Institution ID required"}), 400
        
    try:
        # Cast to int for BigInt column lookup
        try:
            search_id = int(institution_id)
        except (ValueError, TypeError):
            search_id = institution_id

        # Get feedback scoped to institution
        response = supabase.table('feedback').select('*').eq('institution_id', search_id).execute()
        feedback_list = response.data
        
        stats = {
            "total_feedback": len(feedback_list),
            "average_rating": sum(f['rating'] for f in feedback_list) / len(feedback_list) if feedback_list else 0,
            "feedback": feedback_list
        }
        return jsonify({"status": "success", "data": stats})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/admin/response', methods=['POST'])
def admin_response():
    data = request.json
    feedback_id = data.get('id')
    response_text = data.get('response')
    try:
        response = supabase.table('feedback').update({"admin_response": response_text}).eq('id', feedback_id).execute()
        return jsonify({"status": "success", "data": response.data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Faculty Management ---
@app.route('/api/faculties', methods=['GET'])
def get_faculties():
    institution_id = request.args.get('institution_id')
    try:
        response = supabase.table('faculties').select('*').eq('institution_id', int(institution_id)).execute()
        return jsonify({"status": "success", "data": response.data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/faculties', methods=['POST'])
def add_faculty():
    data = request.json
    try:
        response = supabase.table('faculties').insert(data).execute()
        return jsonify({"status": "success", "data": response.data[0]})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/faculties/<int:id>', methods=['PUT'])
def update_faculty(id):
    data = request.json
    try:
        response = supabase.table('faculties').update({"name": data.get('name')}).eq('id', id).execute()
        return jsonify({"status": "success", "data": response.data[0]})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/faculties/<int:id>', methods=['DELETE'])
def delete_faculty(id):
    try:
        supabase.table('faculties').delete().eq('id', id).execute()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Subject Management ---
@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    institution_id = request.args.get('institution_id')
    try:
        response = supabase.table('subjects').select('*').eq('institution_id', int(institution_id)).execute()
        return jsonify({"status": "success", "data": response.data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/subjects', methods=['POST'])
def add_subject():
    data = request.json
    try:
        response = supabase.table('subjects').insert(data).execute()
        return jsonify({"status": "success", "data": response.data[0]})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/subjects/<int:id>', methods=['PUT'])
def update_subject(id):
    data = request.json
    try:
        response = supabase.table('subjects').update({"name": data.get('name')}).eq('id', id).execute()
        return jsonify({"status": "success", "data": response.data[0]})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/subjects/<int:id>', methods=['DELETE'])
def delete_subject(id):
    try:
        supabase.table('subjects').delete().eq('id', id).execute()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    data = request.json
    email = data.get('email')

    try:
        # Check if user exists
        result = supabase.table('users').select('id, email').eq('email', email).execute()
        if not result.data:
            # Don't reveal if email exists or not (security best practice)
            return jsonify({"status": "success", "message": "If an account exists, a reset link has been sent."})

        # Send email using Gmail SMTP
        sender_email = os.environ.get('MAIL_USER')
        sender_password = os.environ.get('MAIL_PASS')
        reset_link = f"http://localhost:5500/frontend/reset.html?email={email}"

        msg = MIMEMultipart("alternative")
        msg['Subject'] = "Password Reset - Faculty Feedback System"
        msg['From'] = sender_email
        msg['To'] = email

        html_body = f"""
        <html><body style="font-family: Arial, sans-serif; max-width: 500px; margin: auto; padding: 30px;">
            <h2 style="color: #1e293b;">Password Reset Request</h2>
            <p>Hello,</p>
            <p>We received a request to reset your password for the <strong>Faculty Feedback System</strong>.</p>
            <a href="{reset_link}" style="display:inline-block; margin: 20px 0; padding: 12px 24px;
               background: #6366f1; color: white; text-decoration: none; border-radius: 8px; font-weight: bold;">
               Reset My Password
            </a>
            <p style="color: #64748b; font-size: 0.85rem;">If you did not request this, please ignore this email.</p>
        </body></html>
        """
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())

        return jsonify({"status": "success", "message": "Reset link sent successfully!"})
    except Exception as e:
        print(f"Password reset error: {e}")
        return jsonify({"status": "error", "message": "Failed to send reset email. Please try again."}), 500

# In-memory OTP store: { phone_number: otp }
otp_store = {}

@app.route('/api/forgot-password-phone', methods=['POST'])
def forgot_password_phone():
    import random
    data = request.json
    phone = data.get('phone', '').strip()
    email = data.get('email', '').strip()
    try:
        # Verify email exists in users table
        user_result = supabase.table('users').select('id, email').eq('email', email).execute()
        if not user_result.data:
            return jsonify({"status": "error", "message": "No account found with this email."}), 404
        # Verify phone exists in feedback table for this student
        student_id = user_result.data[0]['id']
        phone_result = supabase.table('feedback').select('phone_number').eq('student_id', student_id).limit(1).execute()
        if not phone_result.data or phone_result.data[0]['phone_number'] != phone:
            return jsonify({"status": "error", "message": "Phone number does not match our records."}), 404
        # Generate 6-digit OTP
        otp = random.randint(100000, 999999)
        otp_store[email] = otp  # Store by email
        print(f"[OTP] Email: {email} | OTP: {otp}")
        return jsonify({"status": "success", "otp": otp})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/reset-password-phone', methods=['POST'])
def reset_password_phone():
    data = request.json
    email = data.get('email', '').strip()
    new_password = data.get('new_password', '')
    try:
        # Update password directly by email in users table
        result = supabase.table('users').update({"password": new_password}).eq('email', email).execute()
        if result.data:
            otp_store.pop(email, None)
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": "Could not update password. Email not found."}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "success", "message": "Backend is running"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"Backend is running at http://localhost:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)
