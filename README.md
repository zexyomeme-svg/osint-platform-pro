# OSINT Platform Pro

A comprehensive Open Source Intelligence (OSINT) platform built with Flask that provides tools for gathering, analyzing, and visualizing information from various sources across the internet.

## 🎯 Overview

OSINT Platform Pro is a professional-grade web application designed for security researchers, investigators, and analysts. It aggregates multiple OSINT tools and APIs into a single, user-friendly interface, enabling efficient information gathering from IP addresses, domains, usernames, and websites.

## ✨ Features

### Core OSINT Tools

1. **IP Lookup**
   - Geolocation and ISP information
   - Network details and organization info
   - Uses IP-API.com service

2. **Domain Lookup**
   - WHOIS information retrieval
   - Domain registration details
   - DNS record resolution (A, MX, NS, TXT records)
   - Certificate transparency search via crt.sh

3. **Identity/Username Lookup**
   - Cross-platform username search across major social networks
   - Checks: GitHub, Twitter, Instagram, Reddit, Pinterest, YouTube, TikTok
   - Identifies existing accounts and provides direct links

4. **Website Analysis**
   - HTTP status code analysis
   - Header extraction and analysis
   - Server identification
   - Content-Type detection

### System Features

- **Real-time System Statistics**
  - RAM usage monitoring
  - CPU usage tracking
  - Automatic resource optimization
  - Server-Sent Events (SSE) streaming for live updates

- **Tools Status Dashboard**
  - Monitor availability of external OSINT services
  - Health checks for API endpoints
  - TTL-based caching (30 seconds) to reduce overhead
  - Tracks: IP-API, ipwho.is, Google DNS, Cloudflare DNS, crt.sh, RDAP, Sherlock, ExifTool

- **Performance Optimization**
  - Garbage collection triggered on demand
  - RAM limit monitoring (configurable)
  - Resource usage alerting

## 📁 Project Structure

```
osint-platform-pro/
├── app/
│   ├── main.py                 # Flask app with routes
│   ├── utils.py                # OSINT lookup functions
│   ├── tools.py                # External tool status checking
│   ├── optimizer.py            # Resource optimization
│   └── templates/
│       ├── base.html           # Base template with navigation
│       ├── index.html          # Home/dashboard page
│       ├── ip_lookup.html      # IP lookup interface
│       ├── domain_lookup.html  # Domain lookup interface
│       ├── identity_lookup.html # Username search interface
│       ├── stats.html          # System statistics page
│       └── tools.html          # Tools status dashboard
├── run.py                      # Application entry point
├── requirements.txt            # Python dependencies
├── Procfile                    # Deployment configuration
├── .gitignore                  # Git ignore rules
└── README.md                   # This file

```

## 🛠️ Technology Stack

- **Backend**: Python 3.10+
- **Web Framework**: Flask 2.2.5
- **HTTP Client**: requests 2.31.0
- **DNS Resolution**: dnspython 2.4.2
- **WHOIS Lookup**: python-whois 0.7.7
- **System Monitoring**: psutil 5.9.5
- **Production Server**: Gunicorn 20.1.0
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)

## 📦 Dependencies

```
Flask==2.2.5              # Web framework
requests==2.31.0          # HTTP requests
python-whois==0.7         # WHOIS lookups
psutil==5.9.5             # System monitoring
gunicorn==20.1.0          # Production WSGI server
dnspython==2.4.2          # DNS resolution
```

## 🚀 Installation & Setup

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/zexyomeme-svg/osint-platform-pro.git
   cd osint-platform-pro
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000`

### Production Deployment (Render)

This repository is pre-configured for deployment on Render.

**Recommended Render Settings:**
- **Branch**: main
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app.main:app`
- **Python Runtime**: 3.10 or 3.11
- **Environment Variables** (for low-memory plans):
  ```
  GUNICORN_CMD_ARGS="--workers=1 --threads=2 --timeout=60"
  ```
- **Health Check**: HTTP: `/health`

**Deployment Steps:**
1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Apply the recommended settings above
4. Deploy!

**Note**: Some features like WHOIS and DNS queries may be rate-limited or fail on free-tier deployments due to outbound request restrictions.

## 🔌 API Endpoints

### Main Routes
- `GET /` - Home page
- `GET /health` - Health check (used by Render)
- `GET /ip-lookup` - IP lookup interface
- `GET /domain-lookup` - Domain lookup interface
- `GET /identity-lookup` - Username search interface
- `GET /stats` - System statistics page
- `GET /tools` - Tools status dashboard

### API Endpoints
- `GET /api/ip/<ip>` - Get IP geolocation data
- `GET /api/domain/<domain>` - Get domain WHOIS and DNS info
- `GET /api/username/<username>` - Search username across platforms
- `GET /api/analyze/<url>` - Analyze website headers and info
- `GET /api/system-stats` - Get real-time system statistics
- `GET /api/tools-status` - Get status of external OSINT tools
- `POST /api/optimize` - Trigger garbage collection

### Streaming Endpoints (SSE)
- `GET /stream/stats` - Stream system statistics (updates every 1 second)
- `GET /stream/tools` - Stream tools status (updates every 15 seconds)

## 📊 Usage Examples

### IP Lookup
```bash
curl http://localhost:5000/api/ip/8.8.8.8
```

### Domain Lookup
```bash
curl http://localhost:5000/api/domain/example.com
```

### Username Search
```bash
curl http://localhost:5000/api/username/johndoe
```

### Website Analysis
```bash
curl http://localhost:5000/api/analyze/example.com
```

## ⚙️ Configuration

### Resource Limits
Edit `app/optimizer.py` to adjust RAM limits:
```python
optimizer = ResourceOptimizer(ram_limit_mb=512)  # Default: 512 MB
```

### Tool Status Cache TTL
Edit `app/tools.py` to adjust cache duration:
```python
_cache = {
    'timestamp': 0,
    'ttl': 30,  # Change this value (in seconds)
    'data': []
}
```

## 🔐 Security Considerations

- **API Rate Limiting**: Be aware that external APIs have rate limits
- **Input Validation**: All user inputs should be validated before processing
- **HTTPS**: Use HTTPS in production environments
- **API Keys**: Some services may require API keys for higher rate limits (not included in basic version)
- **Data Privacy**: Ensure compliance with local laws when performing OSINT activities

## 📝 Notes

- The platform uses free, public OSINT services with no API keys required
- Rate limiting is applied to prevent excessive API calls
- Some services may block requests if rate limits are exceeded
- DNS and WHOIS queries may fail or be rate-limited in production environments

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

2. **DNS Resolution Fails**
   - Check internet connectivity
   - Verify DNS server availability
   - Some hosting providers may block DNS queries

3. **WHOIS Queries Timeout**
   - Increase timeout values in `app/utils.py`
   - Use alternative WHOIS services

4. **Memory Issues on Render**
   - Reduce `GUNICORN_CMD_ARGS` workers
   - Enable garbage collection optimization
   - Monitor usage via the `/stats` page

## 📄 License

This project is provided as-is. Please ensure you comply with all applicable laws and terms of service when using OSINT tools.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests to improve the platform.

## 📧 Contact & Support

For questions or issues, please open a GitHub issue in the repository.

---

**Version**: 1.0.0  
**Last Updated**: 2026-06-21  
**Status**: Active Development
