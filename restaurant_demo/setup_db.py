"""
Database Seeding Script - Populate initial data.
"""
from app import create_app
from app.seeds import seed_data


def seed_database():
    """Entry point for command line execution."""
    app = create_app()
    with app.app_context():
        seed_data()


if __name__ == '__main__':
    seed_database()
