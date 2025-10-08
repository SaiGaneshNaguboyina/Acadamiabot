from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import os
import csv
from fuzzywuzzy import fuzz
from pymongo import MongoClient
import uuid
import urllib.parse
import smtplib
from email.mime.text import MIMEText
import random
import string

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'), static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'a-default-secure-key-for-development')

# MongoDB Atlas setup
username = urllib.parse.quote_plus('koushikkumarpasupuleti')
password = urllib.parse.quote_plus('kpp@2916')
connection_string = f'mongodb+srv://{username}:{password}@cluster.zzisymh.mongodb.net/university_chatbot?retryWrites=true&w=majority&appName=Cluster'
try:
    client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("Connected to MongoDB Atlas successfully!")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    exit(1)
db = client['university_chatbot']
users_collection = db['users']

def init_db():
    """Initializes the database by adding default users if the collection is empty."""
    try:
        if users_collection.count_documents({}) == 0:
            default_users = [
                {
                    'user_id': 'admin-id-1',
                    'username': 'admin',
                    'email': 'admin@example.com',
                    'password': 'password123'
                },
                {
                    'user_id': 'student-id-1',
                    'username': 'student',
                    'email': 'student@example.com',
                    'password': 'pass456'
                }
            ]
            users_collection.insert_many(default_users)
            print("Default users added to MongoDB Atlas.")
    except Exception as e:
        print(f"Error initializing database: {e}")

init_db()

def load_qa_from_csv(csv_path):
    qa_dict = {}
    try:
        if not os.path.exists(csv_path):
            print(f"Error: CSV file not found at {csv_path}")
            return qa_dict
        with open(csv_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category = row.get('category', '').strip().lower()
                question = row.get('question', '').strip().lower()
                answer = row.get('answer', '').strip()
                keywords = row.get('keywords', '').strip().split(',')
                keywords = [k.strip().lower() for k in keywords if k.strip()]
                if question and answer:
                    qa_dict[question] = {'answer': answer, 'keywords': keywords}
    except Exception as e:
        print(f"Error loading CSV file: {e}")
    return qa_dict

csv_file_path = os.path.join(os.path.dirname(__file__), 'university_data.csv')
module_qa = load_qa_from_csv(csv_file_path)

def find_answer(user_question):
    """Finds the most relevant answer to a given question using fuzzy matching."""
    if not module_qa:
        return "Error: Dataset is empty. Please check the CSV file and add question-answer pairs."
    user_question = user_question.strip().lower()
    best_match = None
    highest_score = 0
    threshold = 50
    if len(user_question) < 3:
        return "Please ask a more detailed question."
    for question, data in module_qa.items():
        question_score = fuzz.token_set_ratio(user_question, question)
        keyword_score = max([fuzz.token_set_ratio(user_question, kw) for kw in data['keywords']], default=0)
        score = max(question_score, keyword_score)
        if score > highest_score:
            highest_score = score
            best_match = question
    if best_match and highest_score >= threshold:
        answer = module_qa[best_match]['answer']
        if answer.startswith('"') and answer.endswith('"'):
            answer = answer[1:-1]
        return answer
    return "Sorry, I don't have an answer to that question. Please contact the project team leader for more information."

@app.before_request
def clear_session_on_welcome_access():
    if request.path == url_for('welcome'):
        session.clear()
        print("Session cleared on welcome page load")

@app.route('/')
def welcome():
    print("Displaying welcome page")
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            identifier = data.get('username')
            password = data.get('password')
        else:
            identifier = request.form.get('username')
            password = request.form.get('password')
        try:
            user = users_collection.find_one({
                "$or": [{"email": identifier}, {"username": identifier}]
            })
            if user and user['password'] == password:
                session['user_id'] = str(user['user_id'])
                session['username'] = user['username']
                flash('Login successful!', 'success')
                print(f"Login successful for {user['username']}. Redirecting to index.")
                if request.is_json:
                    return jsonify({'success': True, 'redirect': url_for('index')})
                return redirect(url_for('index'))
            else:
                error_msg = 'Invalid username/email or password. Please try again.'
                flash(error_msg, 'error')
                print("Login failed. Re-rendering login page with error.")
                if request.is_json:
                    return jsonify({'success': False, 'message': error_msg}), 401
                return render_template('login.html')
        except Exception as e:
            error_msg = f'An error occurred during login: {str(e)}'
            flash(error_msg, 'error')
            print(f"Login error: {e}")
            if request.is_json:
                return jsonify({'success': False, 'message': error_msg}), 500
            return render_template('login.html')
    print("Displaying login page (GET request).")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        user_id = str(uuid.uuid4())
        try:
            if users_collection.find_one({'username': username}):
                flash('Username already exists. Please choose a different one.', 'error')
                return render_template('signup.html', username=username, email=email)
            if users_collection.find_one({'email': email}):
                flash('Email already registered. Please use a different email or log in.', 'error')
                return render_template('signup.html', username=username, email=email)
            users_collection.insert_one({
                'user_id': user_id,
                'username': username,
                'email': email,
                'password': password
            })
            flash('Registration successful! Please log in.', 'success')
            print(f"Signup successful for {username}. Redirecting to login.")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'An error occurred during registration: {str(e)}', 'error')
            print(f"Signup error: {e}")
            return render_template('signup.html')
    print("Displaying signup page (GET request).")
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    print("User logged out. Redirecting to login page.")
    return redirect(url_for('login'))

# REMOVED /forgot_password route

@app.route('/index')
def index():
    print(f"Accessing /index route. Session: {session}")
    if 'user_id' in session:
        return render_template('index.html', username=session.get('username', 'User'))
    print("User not in session. Redirecting to login from /index.")
    flash('Please log in to access the chatbot.', 'error')
    return redirect(url_for('login'))

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        if not user_message:
            return jsonify({'response': 'Please provide a question.'}), 400
        answer = find_answer(user_message)
        print(f"Responding to '{user_message}' with: {answer}")
        return jsonify({'response': answer})
    except Exception as e:
        print(f"Chat API error: {e}")
        return jsonify({'response': 'An error occurred. Please try again.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)