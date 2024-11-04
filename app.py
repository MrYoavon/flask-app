from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from todo import Todo, db

# create flask object with file name
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'  # define connection string

db.init_app(app)


# with app.app_context():
#     db.create_all()


# route index page to root of website
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # ADD TASK button clicked
        content_task = request.form['content']
        new_task = Todo(content=content_task)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('index'))  # Redirect after adding
        except:
            return 'There was an issue adding your new task to db!!'
    else:
        # retrieve all data from Todo table
        tasks = Todo.query.order_by(Todo.date_created).all()
        # Send all tasks that retrieved from DB to index page
        return render_template('index.html', tasks=tasks)


@app.route('/delete_task/<string:tid>', methods=['GET', 'POST'])
def delete_task(tid):
    # retrieve task by task id from db
    task = Todo.query.filter_by(id=tid).first()
    if task:  # Check if task exists
        db.session.delete(task)  # Delete task from db
        db.session.commit()
        print(f"task {tid} deleted")
    else:
        # Optional: Add flash message or logging to indicate task not found
        return 'Task not found', 404

    tasks = Todo.query.order_by(Todo.date_created).all()
    # return render_template('index.html', tasks=tasks)
    return redirect(url_for('index'))  # Redirect after deleting


@app.route('/update_task/<string:tid>', methods=['GET', 'POST'])
def update_task(tid):
    # add code
    if request.method == 'POST':
        task = Todo.query.filter_by(id=tid).first()
        task.content = request.form['content']
        task.date_created = func.now()
        db.session.commit()
        task = Todo.query.order_by(Todo.date_created).all()
        # return render_template('index.html', tasks=task)
        return redirect(url_for('index'))  # Redirect after updating
    else:
        task = Todo.query.filter_by(id=tid).first()
        return render_template('update_task.html', task=task)


# This code run when this file is call but not when it imported by other file
if __name__ == "__main__":
    # start running the web page
    app.run(debug=True)
