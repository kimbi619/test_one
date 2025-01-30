from mongoengine import connect
from app import User  

connect('test_one_db')

def clear_database():
    try:
        User.objects.delete()
        print("Database cleared successfully!")
    except Exception as e:
        print(f"An error occurred while clearing the database: {str(e)}")

if __name__ == "__main__":
    clear_database() 