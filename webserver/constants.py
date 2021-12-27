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

SQL_DATABASE_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DB_NAME}"