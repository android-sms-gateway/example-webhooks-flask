# 📱 Example SMS Webhook Processor (Flask)

[![Example](https://img.shields.io/badge/Type-Example%20Project-orange.svg)](https://github.com/android-sms-gateway/example-webhooks-flask)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.9%2B-brightgreen.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask-%23000000.svg)](https://flask.palletsprojects.com/)

> **⚠️ Example Project Notice**  
> Not intended for production use without proper security review and modifications.

## 📋 Table of Contents
- [📱 Example SMS Webhook Processor (Flask)](#-example-sms-webhook-processor-flask)
  - [📋 Table of Contents](#-table-of-contents)
  - [✨ About The Project](#-about-the-project)
    - [🛠️ Built With](#️-built-with)
    - [⚠️ Important Notes](#️-important-notes)
  - [🚀 Getting Started](#-getting-started)
    - [📦 Prerequisites](#-prerequisites)
    - [⚡ Installation](#-installation)
  - [⚙️ Configuration](#️-configuration)
  - [🖥️ Usage](#️-usage)
  - [📚 API Reference](#-api-reference)
    - [`POST /webhook/sms-received`](#post-webhooksms-received)
  - [🤝 Contributing](#-contributing)
  - [📜 License](#-license)

## ✨ About The Project

**Example Project Features**:
- 🧩 Demonstrates webhook registration/deregistration lifecycle
- 🔐 Example HMAC signature validation implementation
- 📝 Sample payload validation using Pydantic models
- 🔄 Synchronous Flask implementation

### 🛠️ Built With

- 🚀 [Flask](https://flask.palletsprojects.com/) - Lightweight Python web framework
- ✔️ [Pydantic](https://pydantic.dev/) - Data validation and settings management
- 🌐 [HTTPX](https://www.python-httpx.org/) - Synchronous HTTP client

### ⚠️ Important Notes

**This example intentionally omits**:

- Production-grade error handling
- Rate limiting
- Persistent storage integration
- Advanced security features

**Recommended for**:

- 🧪 Testing SMS Gate webhook integration
- 🎓 Learning Flask webhook implementations

## 🚀 Getting Started

### 📦 Prerequisites

- Python 3.9+ (development environment)
- Valid SSL certificate ([project's CA](https://docs.sms-gate.app/services/ca/) available) or reverse proxy (like [ngrok](https://ngrok.com/))
- SMS Gate credentials

### ⚡ Installation

1. Clone the example repository:
    ```bash
    git clone https://github.com/android-sms-gateway/example-webhooks-flask.git
    cd example-webhooks-flask
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create environment file:
    ```bash
    cp .env.example .env
    ```

## ⚙️ Configuration

**Example `.env` configuration**:
```ini
# 🔑 Example SMS Gate API Credentials
FLASK_SMS_GATE_API_URL="https://api.sms-gate.app/3rdparty/v1" # API root endpoint (optional)
FLASK_SMS_GATE_API_USERNAME="test_user"                       # API username
FLASK_SMS_GATE_API_PASSWORD="test_password"                   # API password

# 🔒 Example Webhook Security
FLASK_WEBHOOK_SECRET="your_test_secret_here"                      # signing key (optional)
FLASK_WEBHOOK_URL="https://localhost:8443/webhook/sms-received"   # current server endpoint

# 🛡️ SSL Configuration
FLASK_SSL_CERT_PATH="./certs/server.crt"  # SSL certificate (optional)
FLASK_SSL_KEY_PATH="./certs/server.key"   # SSL private key (optional)
```

## 🖥️ Usage

**Run the server**:
```bash
python app.py
```

**Expected output**:
```plaintext
Registered webhook ID: 6GlbDer5u83MLiupOKXxf
 * Serving Flask app 'main'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://10.10.0.2:8080
Press CTRL+C to quit
Received SMS:
SIM: 1
From: 6505551212
Message: Android is always a sweet treat!
Received at: 2025-04-15 15:50:56+07:00
127.0.0.1 - - [15/Apr/2025 15:50:59] "POST /webhook/sms-received HTTP/1.1" 200 -
^CUnregistered webhook ID: 6GlbDer5u83MLiupOKXxf
```

## 📚 API Reference

### `POST /webhook/sms-received`

**Example Request**:
```bash
curl -X POST https://localhost:8443/webhook/sms-received \
  -H "X-Signature: abc123..." \
  -H "X-Timestamp: 1690123456" \
  -d @sample_payload.json
```

**Example Response**:
```json
{
  "status": "ok"
}
```

## 🤝 Contributing

This example project welcomes contributions to:

- Improve documentation
- Demonstrate additional features
- Enhance example security implementations

## 📜 License

This example code is released under [Apache License 2.0](LICENSE).
