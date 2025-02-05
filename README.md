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



### 3. Database Setup

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


### 4. Running the Application

1. Start the server:
```bash
python app.py
```

2. Access the application:
- Open your web browser
- Navigate to `http://127.0.0.1:5000`

### 5. Using the Application

#### Adding a New User:
1. Fill in the registration form:
   - ID Number (will be pre-filled with next available ID)
   - Name (letters and spaces only)
   - Surname (letters and spaces only)
   - Date of Birth (use the date picker)
2. Click "POST" to submit
3. The form will show success or error messages

#### Viewing Records
To view all registered users:
1. Start the application
2. Navigate to `http://127.0.0.1:5000/views` in your web browser
3. You will see a table displaying all registered users with their details

### Database Management
The application includes a utility script (`clear_db.py`) to manage the database:

1. To clear all records from the database:
```bash
python clear_db.py
```

This will:
- Connect to the `test_one_db` database
- Remove all user records
- Display a success message when complete

**Warning**: This action cannot be undone. Use with caution in production environments.

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
Change the port in app.py:
run_server(port=8001)  # or any other available port
```

3. **Permission Denied**
```bash
# Linux/macOS
sudo chmod +x app.py
```
