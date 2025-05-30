# Configuration file with security issues

# Security issue: hardcoded credentials
DATABASE_URL = "postgresql://admin:password123@localhost/myapp"
REDIS_URL = "redis://:redis_password@localhost:6379/0"

# Security issue: API keys in config
API_KEY = "sk-1234567890abcdef1234567890abcdef"
SECRET_TOKEN = "super-secret-token-that-should-not-be-here"
JWT_SECRET = "jwt-secret-key-123"

# Security issue: debug mode enabled
DEBUG = True
TESTING = True

# Security issue: weak encryption key
ENCRYPTION_KEY = "simple-key-123"

# Security issue: exposed internal endpoints
INTERNAL_API_ENDPOINT = "http://internal-api.company.com:8080"
ADMIN_PANEL_URL = "/secret-admin"

# Security issue: database credentials
DB_HOST = "192.168.1.100"
DB_PORT = 5432
DB_USER = "root"
DB_PASSWORD = "root123"
DB_NAME = "production_db"

# Security issue: AWS credentials (dummy but realistic looking)
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
AWS_REGION = "us-east-1"

# Security issue: payment gateway credentials
STRIPE_SECRET_KEY = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"
PAYPAL_CLIENT_ID = "AQkquBDf1zctJOWGKWUEtKXm6qVhueUEMvXO_-MCI4DQQ4-LWvkDLIN2fGsd"
PAYPAL_CLIENT_SECRET = "EL1tVxAjhT7cJimnz5-Nsx9k2reTKSVfErNQF-CmrwJgxRtylkGTKlU4RvrX"

# Security issue: email server credentials
SMTP_HOST = "smtp.company.com"
SMTP_PORT = 587
SMTP_USER = "notifications@company.com"
SMTP_PASSWORD = "email_password_123"

# Security issue: logging sensitive data
LOG_LEVEL = "DEBUG"
LOG_PASSWORDS = True
LOG_API_KEYS = True