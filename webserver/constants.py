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

OAUTH_PROVIDERS = {
    "RC3": {
        "client_id": os.environ.get("RC3_CLIENT_ID", "laxrXrJyOYbOLz4G3UmFllCev3ONYUcNP1KhcVvQ"),
        "redirect_uri": os.environ.get("RC3_REDIRECT_URI", "https://localhost/rc3/login"),
        "token_uri": os.environ.get("RC3_TOKEN_URI", "http://localhost/rc3/token"),
        "client_secret": os.environ.get("RC3_CLIENT_SECRET", (
            "sdsQamhx8ISB6cqywe96Yax4hjrcNo1vpJ14LxRK1kmst0Im3FA2sFARXjkg9obO"
            "d4hsaIrdw7GXFLh7xhVhsLDq1J8SfkTi38fxCKvRcUtSxbYn6VDfn7HfwB6VfUEC"
        )),
    }
}
