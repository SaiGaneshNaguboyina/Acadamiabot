# Academiabot
Academia Bot is an intelligent chatbot designed to assist university students and faculty with their academic queries. Built with Flask, this chatbot provides instant answers to questions related to university data, course information, admissions, and more. It features user authentication, a clean interface, and a robust backend for efficient information retrieval.

✨ Features
User Authentication: Secure login and signup system for users.

Interactive Chat Interface: A user-friendly interface for seamless communication with the bot.

Intelligent Q&A: Leverages fuzzy string matching to provide accurate answers from a knowledge base.

Session Management: Maintains user sessions for a personalized experience.

MongoDB Integration: Stores user data securely in a MongoDB Atlas cluster.

Responsive Design: Optimized for various devices.

🚀 Technologies Used
Flask: Web framework for the backend.

Python: Programming language.

MongoDB Atlas: Cloud-based NoSQL database for user management.

FuzzyWuzzy: For fuzzy string matching to find relevant answers.

HTML, CSS, JavaScript: For the frontend user interface.

Tailwind CSS: For styling and responsive design.


🛠️ Installation and Setup
To get Academia Bot up and running on your local machine, follow these steps:

1. Clone the Repository
git clone <repository_url>
cd academia-bot

2. Create a Virtual Environment
It's recommended to use a virtual environment to manage dependencies.

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

Note: If requirements.txt is not provided, you'll need to create one. Based on the app.py file, the following packages are required:

Flask
pymongo
fuzzywuzzy
python-dotenv # For os.getenv (though a default is provided)
python-Levenshtein # dependency for fuzzywuzzy (for C implementation, install if not already present)

You can generate it using: pip freeze > requirements.txt after installing them manually.

4. MongoDB Atlas Configuration
Create a MongoDB Atlas Account: If you don't have one, sign up at MongoDB Atlas.

Create a Cluster: Set up a free-tier cluster.

Create a Database User: Go to "Database Access" and add a new database user with a strong password.

Allow Network Access: In "Network Access," add your current IP address or allow access from anywhere (for development purposes).

Get Connection String: Go to "Databases," click "Connect" on your cluster, choose "Connect your application," and copy the connection string.

Update app.py:
In app.py, modify the connection_string variable with your actual MongoDB Atlas connection string, ensuring you replace <username> and <password> with your database user's credentials. The provided code already uses urllib.parse.quote_plus for username and password, which is good practice.

username = urllib.parse.quote_plus('YOUR_MONGODB_USERNAME') # Replace with your username
password = urllib.parse.quote_plus('YOUR_MONGODB_PASSWORD') # Replace with your password
connection_string = f'mongodb+srv://{username}:{password}@cluster.zzisymh.mongodb.net/university_chatbot?retryWrites=true&w=majority&appName=Cluster'

5. Prepare University Data
The chatbot relies on university_data.csv for its knowledge base. Ensure this file is present in your project's root directory. The app.py script will read from this CSV to answer queries.

6. Set Flask Secret Key
For production, it's crucial to set a strong secret key. For development, a default is provided in app.py.

app.secret_key = os.getenv('FLASK_SECRET_KEY', 'a-default-secure-key-for-development')

You can set it as an environment variable:

export FLASK_SECRET_KEY='your_super_secret_key_here'
# On Windows: set FLASK_SECRET_KEY=your_super_secret_key_here

7. Run the Application
python app.py

The application will typically run on http://127.0.0.1:5000/.



📂 Project Structure
.
├── app.py
├── university_data.csv
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   └── welcome.html
└── static/
    └── img/
        └── logo.png


app.py: The main Flask application file containing all backend logic, routing, database interactions, and chatbot functionality.

university_data.csv: The dataset used by the chatbot to answer questions. Each row should ideally contain a question and its corresponding answer.

templates/: Contains HTML files rendered by Flask for various pages (e.g., login, signup, chatbot interface).

static/: Contains static assets like images, CSS, and JavaScript files.

static/img/logo.png: The logo image used in the application.

💡 Usage
Register: Navigate to the /signup page to create a new user account.

Login: After successful registration, log in using your credentials on the /login page.

Chat: Once logged in, you'll be redirected to the chatbot interface (/index). Start typing your questions related to the university, and the bot will provide answers based on the university_data.csv.

Logout: You can log out from the sidebar.

🤝 Contributing
Contributions are welcome! If you'd like to contribute, please follow these steps:

Fork the repository.

Create a new branch (git checkout -b feature/your-feature-name).

Make your changes.

Commit your changes (git commit -m 'Add some feature').

Push to the branch (git push origin feature/your-feature-name).

Open a Pull Request.

📄 License
This project is open-source and available under the MIT License.

📧 Contact
For any questions or inquiries, please contact koushikkumarpasupuleti@gmail.com.

