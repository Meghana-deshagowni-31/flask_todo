from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)


@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    new_task = Todo(task=task)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    todo = Todo.query.get_or_404(id)

    if request.method == 'POST':
        todo.task = request.form['task']
        db.session.commit()
        return redirect('/')

    return render_template('edit.html', todo=todo)


@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
