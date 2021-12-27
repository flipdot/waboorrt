import argparse
import sys

from sqlalchemy.exc import IntegrityError

from database import SessionLocal
from models import APIKeyModel

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["create-api-key"])
    parser.add_argument("--key")

    args = parser.parse_args()
    if args.command == "create-api-key":
        db = SessionLocal()
        if args.key:
            key = APIKeyModel(id=args.key)
        else:
            key = APIKeyModel()
        db.add(key)
        try:
            db.commit()
        except IntegrityError:
            print("IntegrityError. Seems like API key already exists")
            db.close()
            sys.exit()
        finally:
            db.close()
        db.refresh(key)
        db.close()
        print(key.id)
