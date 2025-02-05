# User Registration System Documentation

## System Requirements
- Python 3.8 or higher
- MongoDB 6.0 or higher
- Git (optional)

## Setup Instructions

### 1. Setting up a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
virtualenv venv
source venv/bin/activate
```

### 2. MongoDB Installation

#### Windows:
1. Download MongoDB Community Server from [MongoDB Download Center](https://www.mongodb.com/try/download/community)
2. Run the installer and follow the installation wizard
3. Add MongoDB to your system PATH if not done automatically
4. Create a directory for MongoDB data:
```bash
mkdir C:\data\db
```

#### macOS:
Using Homebrew:
```bash
brew tap mongodb/brew
brew install mongodb-community
```

#### Linux (Ubuntu):
```bash
# Import MongoDB public key
curl -fsSL https://pgp.mongodb.com/server-6.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg \
   --dearmor

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | \
   sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Update and install MongoDB
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start MongoDB service
sudo systemctl start mongod
sudo systemctl enable mongod
```

### 3. Application Setup

1. Create a new directory for your project:
```bash
mkdir user_registration_system
cd user_registration_system
```

2. Create the required files:
```bash
# Create server.py and index.html files
touch server.py index.html requirements.txt
```

3. Copy the provided code into the respective files:
- `server.py`: Copy the server code
- `index.html`: Copy the HTML code
- `requirements.txt`: Add the dependencies

4. Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 4. Database Setup

1. Start MongoDB service (if not already running):
```bash
# Windows
net start MongoDB

# macOS
brew services start mongodb-community

# Linux
sudo systemctl start mongod
```

2. The application will automatically create the database `test_one_db` when it first runs.

### 5. Running the Application

1. Start the server:
```bash
python server.py
```

2. Access the application:
- Open your web browser
- Navigate to `http://localhost:8000`

### 6. Using the Application

#### Adding a New User:
1. Fill in the registration form:
   - ID Number (will be pre-filled with next available ID)
   - Name (letters and spaces only)
   - Surname (letters and spaces only)
   - Date of Birth (use the date picker)
2. Click "POST" to submit
3. The form will show success or error messages

#### Viewing Records:
The current implementation doesn't include a view records page. To view records, you can use MongoDB Compass or the MongoDB shell:

1. Using MongoDB Shell:
```bash
mongosh
use test_one_db
db.users.find()
```

2. Using MongoDB Compass:
- Download and install [MongoDB Compass](https://www.mongodb.com/try/download/compass)
- Connect to `mongodb://localhost:27017`
- Navigate to `test_one_db` database
- View the `users` collection

## Troubleshooting

### Common Issues and Solutions

1. **MongoDB Connection Error**
```
Check if MongoDB service is running:
# Windows
net start MongoDB

# macOS
brew services list

# Linux
sudo systemctl status mongod
```

2. **Port Already in Use**
```
Change the port in server.py:
run_server(port=8001)  # or any other available port
```

3. **Permission Denied**
```bash
# Linux/macOS
sudo chmod +x server.py
```

### Security Notes

- This is a basic implementation and should not be used in production without additional security measures
- Consider adding:
  - Input sanitization
  - CSRF protection
  - SSL/TLS
  - User authentication
  - Rate limiting

## File Structure
```
user_registration_system/
├── server.py           # Main server implementation
├── index.html         # Frontend interface
└── requirements.txt   # Python dependencies
```

## Dependencies
- mongoengine==0.27.0
- pymongo==4.6.1

## Contributing
To contribute to this project:
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License
This project is open-source and available under the MIT License.
