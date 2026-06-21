from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from app.utils import get_ip_info, get_whois_info, get_dns_records, search_username, analyze_website
from app.osint_search import osint_searcher
from app.optimizer import optimizer
from app.tools import get_tools_status
import time
import logging
import json

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ==================== MAIN ROUTES ====================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    # Simple health check used by Render
    return jsonify({"status": "ok"}), 200

@app.route('/ip-lookup')
def ip_lookup():
    return render_template('ip_lookup.html')

@app.route('/domain-lookup')
def domain_lookup():
    return render_template('domain_lookup.html')

@app.route('/identity-lookup')
def identity_lookup():
    return render_template('identity_lookup.html')

@app.route('/name-search')
def name_search():
    return render_template('name_search.html')

@app.route('/phone-lookup')
def phone_lookup():
    return render_template('phone_lookup.html')

@app.route('/email-search')
def email_search():
    return render_template('email_search.html')

@app.route('/image-search')
def image_search():
    return render_template('image_search.html')

@app.route('/company-search')
def company_search():
    return render_template('company_search.html')

@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/tools')
def tools_page():
    return render_template('tools.html')

# ==================== IP LOOKUP API ====================

@app.route('/api/ip/<ip>')
def api_ip(ip):
    try:
        logger.info("IP lookup for %s", ip)
        time.sleep(0.3)
        data = get_ip_info(ip)
        return jsonify({
            "success": True,
            "data": data,
            "timestamp": time.time()
        })
    except Exception as e:
        logger.exception("Error in api_ip")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ==================== DOMAIN LOOKUP API ====================

@app.route('/api/domain/<domain>')
def api_domain(domain):
    try:
        logger.info("Domain lookup for %s", domain)
        time.sleep(0.3)
        whois_data = get_whois_info(domain)
        dns_data = get_dns_records(domain)
        return jsonify({
            "success": True,
            "data": {
                "whois": whois_data,
                "dns": dns_data
            },
            "timestamp": time.time()
        })
    except Exception as e:
        logger.exception("Error in api_domain")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ==================== USERNAME SEARCH API ====================

@app.route('/api/username/<username>')
def api_username(username):
    try:
        logger.info("Username search for %s", username)
        time.sleep(0.3)
        data = osint_searcher.search_username(username)
        return jsonify({
            "success": True,
            "data": data,
            "timestamp": time.time()
        })
    except Exception as e:
        logger.exception("Error in api_username")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ==================== NAME SEARCH API ====================

@app.route('/api/name-search', methods=['POST'])
def api_name_search():
    try:
        data = request.get_json()
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        location = data.get('location', '').strip()
        
        if not first_name or not last_name:
            return jsonify({
                "success": False,
                "error": "First name and last name are required"
            }), 400
        
        logger.info("Name search for %s %s, location: %s", first_name, last_name, location)
        time.sleep(0.5)
        
        results = osint_searcher.search_name(first_name, last_name, location)
        
        return jsonify({
            "success": True,
            "data": results,
            "timestamp": time.time()
        })
    except Exception as e:
        logger.exception("Error in api_name_search")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ==================== PHONE LOOKUP API ====================

@app.route('/api/phone-search', methods=['POST'])
def api_phone_search():
    try:
        data = request.get_json()
        phone_number = data.get('phone_number', '').strip()
        
        if not phone_number:
            return jsonify({
                "success": False,
                "error": "Phone number is required"
            }), 400
        
        logger.info("Phone search for %s", phone_number)
        time.sleep(0.5)
        
        results = osint_searcher.search_phone(phone_number)
        
        return jsonify({
            "success": True,
            "data": results,
            "timestamp": time.time()
        })
    except Exception as e:
        logger.exception("Error in api_phone_search")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ==================== EMAIL SEARCH API ====================

@app.route('/api/email-search', methods=['POST'])
def api_email_search():
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        
        if not email:
            return jsonify({
                "success": False,
                "error": "Email address is required"
            }), 400
        
        if '@' not in email:
            return jsonify({
                "success": False,
                "error": "Invalid email format"
            }), 400
        
        logger.info("Email search for %s", email)
        time.sleep(0.5)
        
        results = osint_searcher.search_email(email)
        
        return jsonify({
            "success": True,
            "data": results,
            "timestamp": time.time()
        })
    except Exception as e:
        logger.exception("Error in api_email_search")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ==================== IMAGE SEARCH API ====================

@app.route('/api/image-search', methods=['POST'])
def api_image_search():
    try:
        data = request.get_json()
        image_url = data.get('image_url', '').strip()
        
        if not image_url:
            return jsonify({
                "success": False,
                "error": "Image URL is required"
            }), 400
        
        # Basic URL validation
        if not image_url.startswith(('http://', 'https://')):
            return jsonify({
                "success": False,
                "error": "Image URL must start with http:// or https://"
            }), 400
        
        logger.info("Image search for %s", image_url)
        time.sleep(0.5)
        
        results = osint_searcher.search_by_image_url(image_url)
        
        return jsonify({
            "success": True,
            "data": results,
            "timestamp": time.time()
        })
    except Exception as e:
        logger.exception("Error in api_image_search")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ==================== COMPANY SEARCH API ====================

@app.route('/api/company-search', methods=['POST'])
def api_company_search():
    try:
        data = request.get_json()
        company_name = data.get('company_name', '').strip()
        
        if not company_name:
            return jsonify({
                "success": False,
                "error": "Company name is required"
            }), 400
        
        logger.info("Company search for %s", company_name)
        time.sleep(0.5)
        
        results = osint_searcher.search_company(company_name)
        
        return jsonify({
            "success": True,
            "data": results,
            "timestamp": time.time()
        })
    except Exception as e:
        logger.exception("Error in api_company_search")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ==================== WEBSITE ANALYSIS API ====================

@app.route('/api/analyze/<path:url>')
def api_analyze(url):
    try:
        logger.info("Analyze url %s", url)
        time.sleep(0.3)
        data = analyze_website(url)
        return jsonify({
            "success": True,
            "data": data,
            "timestamp": time.time()
        })
    except Exception as e:
        logger.exception("Error in api_analyze")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ==================== SYSTEM STATS API ====================

@app.route('/api/system-stats')
def api_system_stats():
    try:
        stats = optimizer.get_stats()
        return jsonify({
            "success": True,
            "data": stats,
            "timestamp": time.time()
        })
    except Exception as e:
        logger.exception("Error in api_system_stats")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ==================== TOOLS STATUS API ====================

@app.route('/api/tools-status')
def api_tools_status():
    try:
        statuses = get_tools_status()
        return jsonify({
            "success": True,
            "data": statuses,
            "timestamp": time.time()
        })
    except Exception as e:
        logger.exception("Error in api_tools_status")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ==================== OPTIMIZATION API ====================

@app.route('/api/optimize', methods=['POST'])
def api_optimize():
    try:
        msg = optimizer.optimize()
        return jsonify({
            "success": True,
            "message": msg,
            "stats": optimizer.get_stats(),
            "timestamp": time.time()
        })
    except Exception as e:
        logger.exception("Error in api_optimize")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ==================== STREAMING ENDPOINTS ====================

@app.route('/stream/stats')
def stream_stats():
    def event_stream():
        try:
            while True:
                stats = optimizer.get_stats()
                payload = json.dumps(stats)
                yield f"data: {payload}\n\n"
                time.sleep(1)
        except GeneratorExit:
            logger.info("SSE stats client disconnected")
    return Response(stream_with_context(event_stream()), mimetype='text/event-stream')

@app.route('/stream/tools')
def stream_tools():
    def event_stream():
        try:
            while True:
                statuses = get_tools_status(force=True)
                payload = json.dumps(statuses)
                yield f"data: {payload}\n\n"
                time.sleep(15)
        except GeneratorExit:
            logger.info("SSE tools client disconnected")
    return Response(stream_with_context(event_stream()), mimetype='text/event-stream')

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found_error(error):
    logger.warning("404 Error: %s", error)
    return jsonify({
        "success": False,
        "error": "Resource not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.exception("Server Error: %s", error)
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
