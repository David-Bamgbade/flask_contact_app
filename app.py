from flask import Flask

from flask import jsonify, request

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client.contactApp
contactDb = db.contactDb

app = Flask(__name__)


class Contact:
    def __init__(self):
        self.first_name = request.json['first_name']
        self.last_name = request.json['last_name']
        self.phone_number = request.json['phone_number']
        self.email = request.json['email']

    def get_phone_number(self):
        return self.phone_number

    def get_email(self):
        return self.email


class User:

    def __init__(self):
        self.list_of_contacts = []
        self.first_name = request.json['first_name']
        self.last_name = request.json['last_name']
        self.phone_number = request.json['phone_number']
        self.email = request.json['email']
        self.password = request.json['password']

    def get_list_of_contacts(self):
        return self.list_of_contacts

    def get_password(self):
        return self.password

    def get_email(self):
        return self.email


@app.route("/add", methods=['POST'])
def add_contact():
    data = request.json
    document = contactDb.find_one(data)
    if document is None:
        first_name = validate_first_name(data['first_name'].lower())
        last_name = validate_last_name(data['last_name'].lower())
        email = validate_email(data['email'].lower())
        phone_number = validate_phone_number(data['phone_number'])
        contactDb.insert_one(data)
        response = jsonify(" Contact Added Successfully")
        return response
    else:
        raise Exception("Contact Already Exist")


@app.route('/logout', methods=['POST'])
def logout():
    logged_in_user = None
    return jsonify({"message": "Logged out successfully"})


@app.route("/signup", methods=['POST'])
def sign_up():
    data = request.json
    user = User()
    document = contactDb.find_one(data)
    if document is None:
        user.first_name = validate_first_name(data['first_name'].lower())
        user.last_name = validate_last_name(data['last_name'].lower())
        user.email = validate_email(data['email'].lower())
        user.phone_number = validate_phone_number(data['phone_number'].lower())
        user.password = validate_password(data['password'].lower())
        user.get_list_of_contacts()
        contactDb.insert_one(data)
        response = jsonify("Sign up successful")
        return response
    else:
        raise Exception("User Already Exist")


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"})
    email = data['email']
    password = data['password']
    user = contactDb.find_one({"email": email})
    if user:
        if user['password'] == password:
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"error": "Invalid username or password"})


@app.route("/find_by_number", methods=["GET"])
def find_contact_by_phone_number():
    phone_number = request.args.get('phone_number')
    if not phone_number:
        return jsonify({"error": "Phone number is required"}), 400
    contact = contactDb.find_one({"phone_number": phone_number})
    if contact:
        contact['_id'] = str(contact['_id'])
        return jsonify(contact), 200
    else:
        return jsonify({"message": "Contact not found"}), 404


@app.route("/find_by_email", methods=['GET'])
def find_contact_by_email():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "Email is required"})
    contact = contactDb.find_one({"email": email})
    if contact:
        contact['_id'] = str(contact['_id'])
        return jsonify(contact)
    else:
        return jsonify({"message": "Contact not found"})


@app.route("/find_by_name", methods=['GET'])
def find_contact_by_name():
    firstname = request.args.get('first_name')
    lastname = request.args.get('last_name')
    if not firstname and not lastname:
        return jsonify({"error": "Name is required"})
    contact = contactDb.find_one({"First_name": firstname})
    contact = contactDb.find_one({"last_name": lastname})
    if contact:
        contact['_id'] = str(contact['_id'])
        return jsonify(contact)
    else:
        return jsonify({"message": "Contact not found"})


@app.route('/delete_contact', methods=['DELETE'])
def delete_contact_by_number():
    phone_number = request.args.get('phone_number')
    if not phone_number:
        return jsonify({"error": "Phone number is required"})
    result = contactDb.delete_one({"phone_number": phone_number})
    if result.deleted_count > 0:
        return jsonify({"message": "Contact deleted successfully"})
    else:
        return jsonify({"message": "Contact not found"})


@app.route('/delete_by_email', methods=['DELETE'])
def delete_contact_by_email():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "email is required"})
    result = contactDb.delete_one({"email": email})
    if result.deleted_count > 0:
        return jsonify({"message": "Contact deleted successfully"})
    else:
        return jsonify({"message": "Contact not found"})


@app.route('/delete_by_name', methods=['DELETE'])
def delete_contact_by_name():
    firstname = request.args.get('first_name')
    lastname = request.args.get('last_name')
    if not firstname and lastname:
        return jsonify({"error": "Name is required"})
    contact1 = contactDb.delete_one({"First_name": firstname})
    contact2 = contactDb.delete_one({"last_name": lastname})
    if contact1.deleted_count or contact2.deleted_count > 0:
        return jsonify({"message": "Contact deleted successfully"})
    else:
        return jsonify({"message": "Contact not found"})


def validate_first_name(first_name):
    if first_name is None or " " in first_name:
        raise Exception("Invalid Format check first name well")
    else:
        return first_name


def validate_last_name(last_name):
    if last_name is None or " " in last_name:
        raise Exception("Invalid format check last name")
    else:
        return last_name


def validate_email(email):
    if email is None or " " in email or "@" not in email or "." not in email:
        raise Exception("Invalid format check email")
    else:
        return email


def validate_phone_number(phone_number):
    convert_to_int = int(phone_number)

    if phone_number is None or " " in phone_number or len(phone_number) > 11:
        raise Exception("Invalid Format Check PhoneNumber")

    else:
        return str(convert_to_int)


def validate_password(password):
    if password is None or " " in password:
        raise Exception("Invalid Format Check password")
    else:
        return password


if __name__ == '__main__':
    app.run(debug=True)
