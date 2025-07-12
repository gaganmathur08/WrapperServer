# 🔐 Encrypted News API Wrapper (FastAPI)

This is a lightweight FastAPI-based wrapper server that enables secure, encrypted communication between a client (e.g., a Flutter app) and the [NewsAPI.org](https://newsapi.org) service.

It demonstrates:
- AES-256-CBC encryption with PKCS7 padding
- Encrypted requests/responses over HTTPS

---

## 🚀 Features

- Accepts encrypted JSON input from client
- Forwards decrypted request to NewsAPI
- Encrypts the NewsAPI response and returns it securely
- Compatible with Flutter-based mobile client

---

## 🛠 Requirements

- Python 3.8+
- `pip` or `venv` for package management
- [NewsAPI.org](https://newsapi.org) API key (free)

---

## 📦 Installation (Local Setup)

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/encrypted-news-wrapper.git
cd encrypted-news-wrapper

python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate.bat   # Windows

pip install -r requirements.txt

uvicorn wrapper_server:app --host 0.0.0.0 --port 8000
```
## 🔐 Run with HTTPS using `mkcert` (for IP-based SSL testing)
To create a locally trusted SSL certificate for your **local IP address** (e.g. `192.168.1.101`) — ideal for mobile device testing:

### ✅ Step 1: Install `mkcert`
```bash
brew install mkcert
brew install nss  # optional, needed for Firefox support
mkcert -install
```

### ✅ Step 2: Generate Cert and Key for Your IP
Replace 192.168.1.101 with your machine’s actual local IP:
```bash
mkcert 192.168.1.101
```

### ✅ Step 3: Run FastAPI with SSL
```bash
uvicorn wrapper_server:app --host 0.0.0.0 --port 8000 \
  --ssl-keyfile=192.168.1.101-key.pem \
  --ssl-certfile=192.168.1.101.pem
```
