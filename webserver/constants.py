import os

# List of directories in gitserver/bot-templates
# Deprecated. Use RepositoryTemplateName
VALID_REPO_TEMPLATES = ["python", "c-sharp", "golang"]

# Timeout for OAuth flow
AUTH_TIMEOUT = 15 * 60 * 1000

AUTH_TOKEN_SECRET = os.environ.get("AUTH_TOKEN_SECRET", "CHANGE-ME")