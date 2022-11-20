from flask import Flask,request,jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os




app = Flask(__name__)

#confinguration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "custom key"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()

db.init_app(app)


      
#TODO_LIST

class Todo_list(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(200),nullable = False)
    description = db.Column(db.String(400), nullable = False)
    completed = db.Column(db.Boolean,nullable = False , default = False)
    date_created = db.Column(db.DateTime,nullable = False , default = datetime.utcnow)
    
    def __repr__(self):
        return self.id
 

#create schema

ma = Marshmallow(app)

class TodoListSchema(ma.Schema):
    class Meta:
        fields = ('name','description','completed', 'date_created')

todolist_schema = TodoListSchema(many=False)

todolists_schema = TodoListSchema(many=True)

# #instantiate db object
# with app.app_context():
#     db.create_all()

@app.route('/todolist', methods=['POST'])
def add_todo():
    try:
        name = request.json['name']  
        description = request.json['description']

        new_todo = Todo_list(name=name, description=description)
        
        db.session.add(new_todo)
        db.session.commit()
        
        return todolist_schema.jsonify(new_todo)
    
    except Exception as e:
        
        return jsonify({'Error':"Invalids request"})
         
@app.route('/todolist', methods=['GET'])
def get_todos():
    todos = Todo_list.query.all()
    result_set = todolists_schema.dump(todos)
    return jsonify(result_set)

@app.route('/todolist/<int:id>', methods=['GET'])
def get_todo(id):
    todo = Todo_list.query.get_or_404(int(id))
    return todolist_schema.jsonify(todo)
    
@app.route('/')
def index():
    return '<h1>Hello World</h1>'

if __name__=='__main__':
    app.run(debug=True)