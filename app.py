from flask import Flask, render_template, request, session, redirect, url_for, send_file, send_from_directory
import os

app = Flask(__name__, template_folder='/var/www/html/flask_app/templates')
app.secret_key = 'your_secret_key'  # Set a secret key for session

@app.route('/')
def index():
    return render_template('index.html')

def count_words(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
        return len(text.split())

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Process registration form data
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')

        # Extra Credit: Read and display word count from Limerick.txt
        # Handle file upload
        uploaded_file = request.files['uploadedFile']
        if uploaded_file:
            # Save the uploaded file
            file_path = os.path.join('/var/www/html/flask_app/uploads', uploaded_file.filename)
            uploaded_file.save(file_path)

            # Calculate word count
            word_count = count_words(file_path)
            # Store information in session
            session['username'] = username
            session['password'] = password
            session['first_name'] = first_name
            session['last_name'] = last_name
            session['email'] = email
            session['word_count'] = word_count
            session['file_path'] = file_path

            # Redirect to the success page
            return redirect(url_for('registration_success'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process login form data
        entered_username = request.form.get('username')
        entered_password = request.form.get('password')

        # Check if the entered credentials match the stored credentials
        if (entered_username == session.get('username') and
            entered_password == session.get('password')):
            return redirect(url_for('registration_success'))
        else:
            # Incorrect credentials, display an error or redirect to login page
            pass  # Handle incorrect credentials

    return render_template('login.html')

@app.route('/registration-success')
def registration_success():
    # Retrieve information from session
    username = session.get('username')
    password = session.get('password')
    first_name = session.get('first_name')
    last_name = session.get('last_name')
    email = session.get('email')
    religion = session.get('religion')
    word_count = session.get('word_count')
    limerick_text = session.get('limerick_text')

    return render_template('registration_success.html',
                           username=username,
                           password=password,
                           first_name=first_name,
                           last_name=last_name,
                           email=email,
                           religion=religion,
                           word_count=word_count,
                           limerick_text=limerick_text)
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('/var/www/html/flask_app/uploads', filename)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)
