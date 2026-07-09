from flask import Flask

# Create the Flask application
app = Flask(__name__)

# Home page
@app.route("/")
def home():
    return "<h1>Hello, World!</h1>"

# About page
@app.route("/about")
def about():
    return "<h2>About Me</h2><p>I am learning Flask!</p>"

# Contact page
@app.route("/contact")
def contact():
    return "<h2>Contact</h2><p>Email: example@email.com</p>"

# Run the application
if __name__ == "__main__":
    app.run(debug=True) #starts web server