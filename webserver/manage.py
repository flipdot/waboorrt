import argparse

from database import SessionLocal
from models import APIKeyModel

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["create-api-key"])

    args = parser.parse_args()
    if args.command == "create-api-key":
        db = SessionLocal()
        key = APIKeyModel()
        db.add(key)
        db.commit()
        db.refresh(key)
        db.close()
        print(key.id)
