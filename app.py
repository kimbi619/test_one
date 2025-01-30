from flask import Flask, render_template, request
from datetime import datetime
from mongoengine import Document, IntField, StringField, DateTimeField, connect
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

connect('test_one_db')

class User(Document):
    
    id_number = IntField(required=True, unique=True)

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


def get_next_available_id():
    """Find the next available ID by getting the highest current ID and adding 1"""
    highest_user = User.objects.order_by('-id_number').first()
    if highest_user:
        return highest_user.id_number + 1
    return 1  # Start with 1 if no users exist


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
    next_id = get_next_available_id()
    return render_template('index.html', next_id=next_id)



@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form.get('name')

        surname = request.form.get('surname')

        requested_id = int(request.form.get('id_number'))

        date_of_birth_str = request.form.get('date_of_birth')

        form_data = {
            'name': name,
            'surname': surname,
            'id_number': requested_id,
            'date_of_birth': date_of_birth_str
        }

        # Validate name and surname
        if not validate_name(name) or not validate_name(surname):
            return render_template('index.html', 
                                error="Name and surname must contain only letters and spaces",
                                data=form_data,
                                next_id=get_next_available_id())

        # Validate date format
        date_of_birth = validate_date_format(date_of_birth_str)
        if not date_of_birth:
            return render_template('index.html', 
                                error="Invalid date format",
                                data=form_data,
                                next_id=get_next_available_id())

        next_id = get_next_available_id()
        

        if not is_id_available(requested_id):
            actual_id = next_id
            message = f"ID {requested_id} was already taken. Saved with ID: {actual_id}"
        else:
            actual_id = requested_id
            message = f"Data saved successfully with ID: {actual_id}"


        user = User(
            name=name,
            surname=surname,
            id_number=actual_id,
            date_of_birth=date_of_birth
        )
        user.save()
        

        next_id = get_next_available_id()
        return render_template('index.html', 
                            success=message,
                            next_id=next_id)

    except Exception as e:
        return render_template('index.html', 
                            error=f"An error occurred: {str(e)}",
                            data=form_data,
                            next_id=get_next_available_id())



# RUN THE APP
if __name__ == '__main__':
    app.run(debug=True) 