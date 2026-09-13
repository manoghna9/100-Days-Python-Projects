from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


# --------------------------------------------------
# CREATE THE FLASK APP
# --------------------------------------------------

app = Flask(__name__)


# --------------------------------------------------
# DATABASE SETUP
# --------------------------------------------------

# Our database will be a SQLite file called todo.db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"

# Create the database object
db = SQLAlchemy(app)


# --------------------------------------------------
# TASK MODEL
# --------------------------------------------------

# This class represents the Task table in our database
class Task(db.Model):

    # Unique ID for every task
    id = db.Column(db.Integer, primary_key=True)

    # The actual task text
    title = db.Column(db.String(200), nullable=False)

    # Whether the task is completed or not
    completed = db.Column(db.Boolean, default=False)


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.route("/")
def home():

    # Get every task from the database
    tasks = Task.query.all()

    # Send those tasks to our HTML page
    return render_template("index.html", tasks=tasks)


# --------------------------------------------------
# ADD A NEW TASK
# --------------------------------------------------

@app.route("/add", methods=["POST"])
def add_task():

    # Get the text entered in the form
    task_title = request.form.get("task")

    # Make sure the user didn't submit an empty task
    if task_title and task_title.strip():

        # Create a new Task object
        new_task = Task(title=task_title.strip())

        # Add it to the database
        db.session.add(new_task)

        # Save the change
        db.session.commit()

    # Go back to the home page
    return redirect(url_for("home"))


# --------------------------------------------------
# MARK TASK AS COMPLETE / INCOMPLETE
# --------------------------------------------------

@app.route("/complete/<int:task_id>")
def complete_task(task_id):

    # Find the task using its ID
    task = Task.query.get_or_404(task_id)

    # Change True → False or False → True
    task.completed = not task.completed

    # Save the change
    db.session.commit()

    # Go back to the home page
    return redirect(url_for("home"))


# --------------------------------------------------
# DELETE A TASK
# --------------------------------------------------

@app.route("/delete/<int:task_id>")
def delete_task(task_id):

    # Find the task using its ID
    task = Task.query.get_or_404(task_id)

    # Remove it from the database
    db.session.delete(task)

    # Save the change
    db.session.commit()

    # Go back to the home page
    return redirect(url_for("home"))


# --------------------------------------------------
# CREATE THE DATABASE
# --------------------------------------------------

with app.app_context():
    db.create_all()


# --------------------------------------------------
# RUN THE APPLICATION
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)