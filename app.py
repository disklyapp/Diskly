

from flask import Flask, render_template, request, redirect, url_for, session, flash, Response, make_response
import os
import requests
import time
import json
import uuid
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
UPLOAD_FOLDER = 'static/uploads'
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "pASSWORD11212121")

API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:3000").rstrip('/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def home():
    return render_template("index.html")
@app.route("/app-ads.txt")
def app_ads():
    return Response(
        "google.com, pub-2241901350003769, DIRECT, f08c47fec0942fa0",
        mimetype="text/plain"
    )
@app.route('/admin/upload', methods=['GET'])
def upload():
    if 'token' not in session:
        return redirect('/admin/login')

    return render_template("admin/upload.html", token=session['token'], api_base_url=API_BASE_URL)

import time
from flask import make_response

@app.route('/admin/videos')
def videos_page():
    # ✅ Always check session first
    if 'token' not in session:
        return redirect('/admin/login')
    print("=== /videos HIT ===", flush=True)

    token = session.get('token')
    print("TOKEN:", token, flush=True)

    if not token:
        print("NO TOKEN → redirecting", flush=True)
        return redirect('/admin/login')
    
    api_url = f"{API_BASE_URL}/api/admin/videos?_={int(time.time())}"
    print("BEFORE API CALL", flush=True)
    headers = {
        "Authorization": f"Bearer {session['token']}",
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    }

    try:
        response = requests.get(api_url, timeout=20, headers=headers)

        print("Status:", response.status_code, flush=True)

        if response.status_code == 200:
            videos = response.json()
            print("Data:", videos, flush=True)
        else:
            videos = []
            try:
                flash(response.json().get("error", "Could not load videos."))
            except:
                flash("Could not load videos.")

    except Exception as e:
        print("Videos Error:", e)
        videos = []
        flash("Server connection failed.")

    # ✅ Prevent browser caching
    resp = make_response(render_template("admin/videos.html", videos=videos))
    resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    print("BEFORE API CALL")
    return resp

@app.route('/admin/videos/<int:video_id>', methods=['DELETE', 'PUT'])
def modify_video(video_id):
    if 'token' not in session:
        return {"error": "Unauthorized"}, 401
    
    api_url = f"{API_BASE_URL}/api/admin/videos/{video_id}"
    headers = {"Authorization": f"Bearer {session['token']}"}
    try:
        if request.method == 'DELETE':
            res = requests.delete(api_url, headers=headers)
        elif request.method == 'PUT':
            res = requests.put(api_url, headers=headers, json=request.json)
            
        if res.status_code in [200, 204]:
            return {"message": "Success"}, 200
        else:
            return {"error": res.json().get("error", "Action failed")}, res.status_code
    except Exception as e:
        return {"error": "Server connection failed"}, 500

@app.route('/admin/telegram')
def telegram():
    if 'token' not in session:
        return redirect('/admin/login')
    return render_template('admin/telegram.html', api_base_url=API_BASE_URL)

@app.route('/contact')
def contact():
    return render_template('contactus.html')

@app.route('/privacy-policy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms-and-condition')
def terms():
    return render_template('terms.html')

@app.route('/why-choose-us')
def why():
    return render_template('why.html')

@app.route('/admin/ads')
def ads():
    if 'token' not in session:
        return redirect('/admin/login')
    return render_template('admin/ads.html')

@app.route('/dmca')
def dmca():
    return render_template('dmca.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/social')
def social():
    return render_template('social.html')
@app.route('/trending')
def trending():
    return render_template('trending.html')
@app.route('/feature')
def feature():
    return render_template('feature.html')


@app.route('/admin/analytics')
def analytics():
    if 'token' not in session:
        return redirect('/admin/login')
    return render_template('admin/analytics.html')
@app.route('/admin/logout')
def logout():
    session.clear()
    return render_template('index.html')


@app.route('/.well-known/assetlinks.json')
def asset_links():
    data = [
  {
    "relation": ["delegate_permission/common.handle_all_urls"],
    "target": {
      "namespace": "android_app",
      "package_name": "com.starwish.diskly",
      "sha256_cert_fingerprints": [
          "C5:A7:66:3C:74:1B:A4:4F:F8:43:0B:6F:B3:2A:56:16:25:07:F8:A2:8A:EB:DC:4C:79:E6:41:35:6E:AF:96:41",
          "58:E0:0A:EB:35:E1:2F:37:B0:6B:AD:B1:19:27:65:E2:9B:B6:2A:C9:02:E8:68:B1:5E:D0:12:20:B1:C4:51:C1",
          "C5:A7:66:3C:74:1B:A4:4F:F8:43:0B:6F:B3:2A:56:16:25:07:F8:A2:8A:EB:DC:4C:79:E6:41:35:6E:AF:96:41",
          "C5:A7:66:3C:74:1B:A4:4F:F8:43:0B:6F:B3:2A:56:16:25:07:F8:A2:8A:EB:DC:4C:79:E6:41:35:6E:AF:96:41",
          "78:A4:E1:E6:86:46:47:14:07:C1:CE:66:67:B7:A4:0A:46:95:BE:2A",
        "24:5E:C1:5F:01:10:24:30:30:D6:F9:46:A8:C8:88:BA:C7:4F:11:87:E7:67:AD:1C:CE:B1:3D:89:6C:AA:68:F5"
      ]
    }
  }
]
    return Response(
        json.dumps(data),
        mimetype='application/json'
    )
@app.context_processor
def inject_google_client_id():
    return dict(google_client_id=os.environ.get("GOOGLE_CLIENT_ID", ""))

@app.route('/admin/google-login', methods=['POST'])
def google_login():
    req_data = request.json
    id_token = req_data.get('idToken') if req_data else None
    if not id_token:
        return {"error": "Missing Google ID Token"}, 400

    api_url = f"{API_BASE_URL}/api/admin/google-login"
    try:
        response = requests.post(api_url, json={"idToken": id_token})
        if response.status_code == 200:
            data = response.json()
            session['token'] = data['token']
            session['admin_email'] = data['admin']['email']
            return {"success": True}, 200
        else:
            try:
                err_msg = response.json().get("error", "Google login failed")
            except:
                err_msg = "Google login failed"
            return {"error": err_msg}, response.status_code
    except Exception as e:
        return {"error": "Server connection failed"}, 500


@app.route('/admin/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        api_url = f"{API_BASE_URL}/api/admin/login"

        payload = {
            "email": username,
            "password": password
        }

        response = requests.post(api_url, json=payload)

        if response.status_code == 200:

            data = response.json()

            # Save everything in session
            session['token'] = data['token']
            session['admin_email'] = data['admin']['email']

            return render_template("admin/login_success.html", token=data['token'])

        else:
            try:
                flash(response.json().get("error", "Invalid username or password"))
            except:
                flash("Invalid username or password")

    return render_template("admin/login.html")

@app.route('/admin/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        api_url = f"{API_BASE_URL}/api/admin/register"
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post(api_url, json=payload)
        
        if response.status_code == 200:
            flash("Signup successful! Please login.")
            return redirect('/admin/login')
        else:
            try:
                flash(response.json().get("error", "Signup failed"))
            except:
                flash("Signup failed")
                
    return render_template("admin/signup.html")

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'token' not in session:
        return redirect('/admin/login')
    
    headers = {"Authorization": f"Bearer {session['token']}"}
    data = {}
    reports_data = {}
    
    try:
        # Fetch Dashboard Stats
        res_dash = requests.get(f"{API_BASE_URL}/api/admin/dashboard", headers=headers)
        if res_dash.status_code == 200:
            data = res_dash.json()
            
        # Fetch Reports Data
        res_rep = requests.get(f"{API_BASE_URL}/api/admin/reports", headers=headers)
        if res_rep.status_code == 200:
            reports_data = res_rep.json()
            
    except Exception as e:
        flash("Server connection failed.")
        
    return render_template("admin/dashboard.html", data=data, reports=reports_data)

@app.route('/admin/account')
def admin_account():
    if 'token' not in session:
        return redirect('/admin/login')
    
    headers = {"Authorization": f"Bearer {session['token']}"}
    account_data = {}
    try:
        res = requests.get(f"{API_BASE_URL}/api/admin/account", headers=headers)
        if res.status_code == 200:
            account_data = res.json()
    except:
        pass
        
    return render_template("admin/account.html", account=account_data, token=session['token'], api_base_url=API_BASE_URL)

@app.route('/superadmin/login', methods=['GET', 'POST'])
def superadmin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        api_url = f"{API_BASE_URL}/api/superadmin/login"
        response = requests.post(api_url, json={"username": username, "password": password})
        if response.status_code == 200:
            data = response.json()
            session['superadmin_token'] = data['token']
            return redirect('/superadmin/dashboard')
        else:
            try:
                flash(response.json().get("error", "Invalid superadmin credentials"))
            except:
                flash("Invalid superadmin credentials")
    return render_template("superadmin/login.html")

@app.route('/superadmin/dashboard')
def superadmin_dashboard():
    if 'superadmin_token' not in session:
        return redirect('/superadmin/login')
        
    headers = {"Authorization": f"Bearer {session['superadmin_token']}"}
    data = {}
    reports_data = {}
    
    try:
        res_dash = requests.get(f"{API_BASE_URL}/api/superadmin/dashboard", headers=headers)
        if res_dash.status_code == 200:
            data = res_dash.json()
            
        res_rep = requests.get(f"{API_BASE_URL}/api/superadmin/reports", headers=headers)
        if res_rep.status_code == 200:
            reports_data = res_rep.json()
            
    except Exception as e:
        flash("Server connection failed.")
        
    return render_template("superadmin/dashboard.html", data=data, reports=reports_data)

@app.route('/superadmin/videos', methods=['GET'])
def superadmin_videos():
    if 'superadmin_token' not in session:
        return redirect('/superadmin/login')
    
    api_url = f"{API_BASE_URL}/api/superadmin/videos"
    headers = {"Authorization": f"Bearer {session['superadmin_token']}"}
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            videos_data = response.json()
        else:
            videos_data = []
            flash(response.json().get("error", "Failed to load videos."))
    except Exception as e:
        videos_data = []
        flash("Server connection failed.")
    return render_template("superadmin/videos.html", videos=videos_data)

@app.route('/superadmin/admins', methods=['GET'])
def superadmin_admins():
    if 'superadmin_token' not in session:
        return redirect('/superadmin/login')
    
    api_url = f"{API_BASE_URL}/api/superadmin/admins"
    headers = {"Authorization": f"Bearer {session['superadmin_token']}"}
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            admins_data = response.json()
        else:
            admins_data = []
            flash(response.json().get("error", "Failed to load admins."))
    except Exception as e:
        admins_data = []
        flash("Server connection failed.")
    return render_template("superadmin/admins.html", admins=admins_data)

@app.route('/superadmin/admins/limits', methods=['PUT'])
def superadmin_admins_limits():
    if 'superadmin_token' not in session:
        return Response(json.dumps({"error": "Unauthorized"}), status=401, mimetype='application/json')
    
    api_url = f"{API_BASE_URL}/api/superadmin/admins/limits"
    headers = {"Authorization": f"Bearer {session['superadmin_token']}"}
    try:
        response = requests.put(api_url, headers=headers, json=request.json)
        return Response(response.text, status=response.status_code, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"error": "Server connection failed"}), status=500, mimetype='application/json')

@app.route('/superadmin/admins/<int:admin_id>/status', methods=['PUT'])
def superadmin_admins_status(admin_id):
    if 'superadmin_token' not in session:
        return Response(json.dumps({"error": "Unauthorized"}), status=401, mimetype='application/json')
    
    api_url = f"{API_BASE_URL}/api/superadmin/admins/{admin_id}/status"
    headers = {"Authorization": f"Bearer {session['superadmin_token']}"}
    try:
        response = requests.put(api_url, headers=headers, json=request.json)
        return Response(response.text, status=response.status_code, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"error": "Server connection failed"}), status=500, mimetype='application/json')

@app.route('/superadmin/payouts', methods=['GET'])
def superadmin_payouts():
    if 'superadmin_token' not in session:
        return redirect('/superadmin/login')
    
    api_url = f"{API_BASE_URL}/api/superadmin/payouts"
    headers = {"Authorization": f"Bearer {session['superadmin_token']}"}
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            payouts_data = response.json()
        else:
            payouts_data = []
            flash(response.json().get("error", "Failed to load payouts."))
    except Exception as e:
        payouts_data = []
        flash("Server connection failed.")
    return render_template("superadmin/payouts.html", payouts=payouts_data)

@app.route('/superadmin/payouts/<int:payout_id>', methods=['PUT'])
def superadmin_payouts_update(payout_id):
    if 'superadmin_token' not in session:
        return Response(json.dumps({"error": "Unauthorized"}), status=401, mimetype='application/json')
    
    api_url = f"{API_BASE_URL}/api/superadmin/payouts/{payout_id}"
    headers = {"Authorization": f"Bearer {session['superadmin_token']}"}
    try:
        response = requests.put(api_url, headers=headers, json=request.json)
        return Response(response.text, status=response.status_code, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"error": "Server connection failed"}), status=500, mimetype='application/json')

@app.route('/superadmin/settings', methods=['GET', 'POST'])
def superadmin_settings():
    if 'superadmin_token' not in session:
        return redirect('/superadmin/login')
    
    api_url = f"{API_BASE_URL}/api/superadmin/settings"
    headers = {"Authorization": f"Bearer {session['superadmin_token']}"}
    
    if request.method == 'POST':
        try:
            earning_rate = float(request.form.get('earningRatePer1000Views', 0))
            telegram_enabled = request.form.get('telegramUploadEnabled') == 'on'
            min_payout = float(request.form.get('minimumPayoutThreshold', 0))
            
            payload = {
                "earningRatePer1000Views": earning_rate,
                "telegramUploadEnabled": telegram_enabled,
                "minimumPayoutThreshold": min_payout
            }
            
            response = requests.put(api_url, headers=headers, json=payload)
            if response.status_code == 200:
                flash("Settings updated successfully.")
            else:
                try:
                    flash(response.json().get("error", "Failed to update settings."))
                except:
                    flash("Failed to update settings.")
        except ValueError:
             flash("Invalid numeric value provided.")
        except Exception as e:
            flash("Server connection failed.")
        return redirect('/superadmin/settings')

    # GET request
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            settings_data = response.json()
        else:
            settings_data = {}
            try:
                flash(response.json().get("error", "Failed to load settings."))
            except:
                flash("Failed to load settings.")
    except Exception as e:
        settings_data = {}
        flash("Server connection failed.")
    return render_template("superadmin/settings.html", settings=settings_data)

@app.route('/superadmin/logout')
def superadmin_logout():
    session.pop('superadmin_token', None)
    return redirect('/superadmin/login')

@app.route('/app')
def apps():
    return redirect("https://play.google.com/store/apps/details?id=com.starwish.diskly")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

