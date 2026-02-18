from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db = SQLAlchemy()

db.init_app(app)


class Task(db.Model):    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')
    priority = db.Column(db.String(10), default='medium')

    def __repr__(self):
        return f'<{self.title}: {self.description}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority
        }


with app.app_context():
    db.create_all()




@app.route('/')
def home():
    return"""
<h1> Task Master </h1>
    <nav>
        <a href="/tasks">View All Tasks</a> |
        <a href="/tasks/pending">Pending</a> |
        <a href="/tasks/completed">Completed</a>
    </nav>
"""



@app.route("/tasks")
def fetch_tasks():
    tasks = Task.query.all()
    data = []
    for task in tasks:
        data.append(task.to_dict())
    
    return data

@app.route("/tasks/<string:status>")
def pending_tasks(status):
    tasks = Task.query.filter_by(status=status).all()
    data = []
    for task in tasks:
        data.append(task.to_dict())
    
    return data

@app.route("/task/<int:id>")
def fetch_task(id):
    task = Task.query.get(id)
    data = task.to_dict()
    return data


if __name__ == "__main__":
    app.run(debug=True)