from app import app, db, User

# Define admin credentials
admin_username = 'nani'
admin_password = 'vin'  # Ensure to hash passwords in a real application

with app.app_context():
    # Create tables if they don't exist
    db.create_all()

    # Check if the admin user already exists
    admin_user = User.query.filter_by(username=admin_username).first()
    if not admin_user:
        # Add admin user
        admin_user = User(username=admin_username, password=admin_password)
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user created with username: {admin_username}")
    else:
        print("Admin user already exists")
