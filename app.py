from flask import Flask, render_template, request, jsonify
from datetime import datetime
from mongoengine import Document, IntField, StringField, DateTimeField, connect
import re


app = Flask(__name__)
app.secret_key = 'dn??21//2&*fsdjiwi32ouh832oew32@#@$@#asdainfaiandal'

connect('test_one_db')

class User(Document):
    
    id_number = StringField(required=True, unique=True, max_length=13, min_length=13)

    name = StringField(required=True)

    surname = StringField(required=True)

    date_of_birth = DateTimeField(required=True)

    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'users',
        'indexes': ['id_number']
    }




def validate_name(name):
    """Validate name/surname to contain only letters and spaces"""
    return bool(re.match(r'^[A-Za-z\s]+$', name))


def validate_sa_id(id_number, date_of_birth):
    """Validate South African ID number"""
    try:
        if not re.match(r'^\d{13}$', id_number):
            return False, "ID Number must be exactly 13 digits"
        
        year = id_number[:2]
        month = id_number[2:4]
        day = id_number[4:6]
        
        dob_year = date_of_birth.strftime('%y')
        dob_month = date_of_birth.strftime('%m')
        dob_day = date_of_birth.strftime('%d')
        
        # Compare dates
        if (year != dob_year or 
            month != dob_month or 
            day != dob_day):
            return False, "ID Number does not match Date of Birth"
        
        gender_digits = int(id_number[6:10])
        if not (0 <= gender_digits <= 9999):
            return False, "Invalid gender digits in ID Number"
        
        # Validate citizenship digit (11)
        citizenship = int(id_number[10])
        if citizenship not in [0, 1]:
            return False, "Invalid citizenship digit in ID Number"
        
        return True, "Valid ID Number"
        
    except Exception as e:
        return False, f"Invalid ID Number format: {str(e)}"


def is_id_available(id_number):
    """Check if an ID is available"""
    return not User.objects(id_number=id_number).first()


def validate_date_format(date_str):
    """Validate date string format (DD/MM/YYYY)"""
    try:
        return datetime.strptime(date_str, '%d/%m/%Y')
    except ValueError:
        return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'GET':
        return {'success': True}
    
    try:
        name = request.form.get('name')
        surname = request.form.get('surname')
        id_number = request.form.get('id_number')
        date_of_birth_str = request.form.get('date_of_birth')

        form_data = {
            'name': name,
            'surname': surname,
            'id_number': id_number,
            'date_of_birth': date_of_birth_str
        }

        # Validate name and surname
        if not validate_name(name) or not validate_name(surname):
            return {'error': "Name and surname must contain only letters and spaces"}

        # Validate date format
        date_of_birth = validate_date_format(date_of_birth_str)
        if not date_of_birth:
            return {'error': "Invalid date format. Use DD/MM/YYYY"}

        # Validate ID number
        is_valid_id, id_message = validate_sa_id(id_number, date_of_birth)
        if not is_valid_id:
            return {'error': id_message}

        # Check for duplicate ID
        if not is_id_available(id_number):
            return {'error': f"ID Number {id_number} already exists in the database"}

        # Save user
        user = User(
            name=name,
            surname=surname,
            id_number=id_number,
            date_of_birth=date_of_birth
        )
        user.save()

        return {
            'success': "Data saved successfully",
            'id_number': id_number
        }

    except Exception as e:
        return {'error': f"An error occurred: {str(e)}"}
    


@app.route('/view')
def view_records():
    try:
        # Get all users, sorted by creation date
        users = User.objects.order_by('-created_at')
        return render_template('view_records.html', users=users)
    except Exception as e:
        return render_template('view_records.html', error=str(e))


if __name__ == '__main__':
    app.run(debug=True)