import os

# List of directories in gitserver/bot-templates
# Deprecated. Use RepositoryTemplateName
VALID_REPO_TEMPLATES = ["python", "csharp", "golang"]

# Timeout for OAuth flow
AUTH_TIMEOUT = 15 * 60 * 1000

# User session should be terminated if not used for X seconds
SESSION_EXPIRATION_TIME = 60 * 60 * 24 * 7  # 7 days

AUTH_TOKEN_SECRET = os.environ.get("AUTH_TOKEN_SECRET", "CHANGE-ME")

PG_HOST = os.environ.get("POSTGRES_HOST", "localhost")
PG_USER = os.environ.get("POSTGRES_USER", "waboorrt")
PG_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "change-me-in-production")
PG_DB_NAME = os.environ.get("POSTGRES_DB_NAME", PG_USER)

GITSERVER_HOST = os.environ.get("GITSERVER_HOST", "localhost")
GITSERVER_HTTP_PORT = os.environ.get("GITSERVER_HTTP_PORT", "2223")

SQL_DATABASE_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DB_NAME}"

OAUTH_PROVIDERS = {
    "RC3": {
        "CLIENT_ID": os.environ.get("RC3_CLIENT_ID"),
        # "REDIRECT_URI": os.environ.get("RC3_REDIRECT_URI"),
        "TOKEN_URI": os.environ.get("RC3_TOKEN_URI"),
        "CLIENT_SECRET": os.environ.get("RC3_CLIENT_SECRET"),
    }
}
