import argparse
import getpass
import sys
from core.database import SessionLocal, Base, engine
from core.security import validate_password_strength
from services.admin_service import admin_service
from db.models import User, RefreshToken, EmailVerificationToken, PasswordResetToken, SecurityAuditLog


def init_db():
    """Create all database tables."""
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables initialized successfully.")


def create_admin(email: str, name: str, password: str = None):
    """Create or elevate an admin user."""
    if not password:
        password = getpass.getpass("Enter administrator password: ")
        confirm_password = getpass.getpass("Confirm administrator password: ")
        if password != confirm_password:
            print("Error: Passwords do not match.", file=sys.stderr)
            sys.exit(1)

    is_valid, error = validate_password_strength(password)
    if not is_valid:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    db = SessionLocal()
    try:
        admin = admin_service.bootstrap_first_admin(db, email=email, password=password, name=name)
        print(f"Success: Administrator account '{admin.email}' is ready with role '{admin.role}'.")
    finally:
        db.close()


def show_users():
    """List existing registered users."""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"\nTotal users: {len(users)}")
        print(f"{'ID':<6} {'Role':<8} {'Active':<8} {'Verified':<10} {'Email':<30} {'Name'}")
        print("-" * 75)
        for u in users:
            print(f"{u.id:<6} {u.role:<8} {str(u.is_active):<8} {str(u.is_email_verified):<10} {u.email:<30} {u.full_name}")
        print()
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="JobPilot AI Auth Administration CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # init-db
    subparsers.add_parser("init-db", help="Create database tables")

    # create-admin
    admin_parser = subparsers.add_parser("create-admin", help="Bootstrap or elevate an administrator account")
    admin_parser.add_argument("--email", required=True, help="Admin email address")
    admin_parser.add_argument("--name", default="System Administrator", help="Admin display name")
    admin_parser.add_argument("--password", help="Admin password (will prompt securely if not provided)")

    # show-users
    subparsers.add_parser("show-users", help="List registered users")

    args = parser.parse_args()

    if args.command == "init-db":
        init_db()
    elif args.command == "create-admin":
        create_admin(args.email, args.name, args.password)
    elif args.command == "show-users":
        show_users()


if __name__ == "__main__":
    main()
