import os


class Config:
    def __init__(self):

        required_vars = [
            "REPO_PATH"
        ]

        missing_vars = [var for var in required_vars if var.upper() not in os.environ]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

        for key in os.environ:
            setattr(self, key.lower(), os.environ[key])

    def get(self, key):
        return getattr(self, key.lower(), None)