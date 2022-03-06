from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from wtforms.widgets import TextArea


# create a flask instance
app = Flask(__name__)
# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Secret key password enviromental variable
app.config['SECRET_KEY'] = os.environ.get("DB_PASS") 
# initialize database
db=SQLAlchemy(app)

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(120),nullable=False,unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self):
     return '<Name %r>' % self.name


# Create another table
class Posts(db.Model):
   id = db.Column(db.Integer, primary_key = True) 
   title = db.Column(db.String(250),nullable=False)
   content = db.Column(db.Text,nullable=False)
   author = db.Column(db.String(250),nullable=False)
   date_posted = db.Column(db.DateTime, default=datetime.utcnow)
   slug = db.Column(db.String(255))

   def __repr__(self):
     return '<Name %r>' % self.name

# Create a Posts form for db
class PostForm(FlaskForm):
    title = StringField("Title:", validators=[DataRequired()])
    content = StringField("Content:", validators=[DataRequired()],widget=TextArea())
    author = StringField("Author:", validators=[DataRequired()])
    slug = StringField("Slug:", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/posts')
def posts():
    # Get the posts from the database
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)

@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template("post.html",post=post)

# Add Post Page
@app.route('/add-post', methods=['GET','POST'])
def add_post():
    form=PostForm()
    if form.validate_on_submit():
      post = Posts(title=form.title.data,content=form.content.data,author=form.author.data,slug=form.slug.data)
     #Clear Form
      form.title.data = ''
      form.content.data = ''
      form.author.data = ''
      form.slug.data = ''
      #Add to DB
      db.session.add(post)
      db.session.commit()

      flash("Blog Post Submitted")

    return render_template("add_post.html",form=form)
   

# Delete Users in Database
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form=UserForm()
    try: 
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User deleted")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html",form=form,name=name,our_users=our_users)
    except:
        flash("There was a problem")
        return render_template("add_user.html",form=form,name=name,our_users=our_users)


       

# Create a new form for db
class UserForm(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Update Database Record
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method =="POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        
        try:
            db.session.commit()
            flash("User Updated Succesfully")
            return render_template("update.html",form=form,name_to_update=name_to_update)
        except:
   
             flash("Issue with updating")
             return render_template("update.html",form=form,name_to_update=name_to_update)
    else:
        return render_template("update.html",form=form,name_to_update=name_to_update)


# Add db Userform route
@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name = None
    form=UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User added to Database")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html",form=form,name=name,our_users=our_users)

# Index(main) 
@app.route('/')
def index():
    first_name = "Nige"
    stuff = "This is <strong>BOLD<strong> Text"
    favourite_pizza = ["Mexican","Cheese","Pepperoni"]
    return render_template("index.html",first_name=first_name,stuff=stuff,favourite_pizza=favourite_pizza)

# localhost:5000/user/Nige/ User.html
@app.route('/user/<name>')
def user(name):
    return render_template("user.html",user_name=name)
    
# Create Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Create Internal server error
@app.errorhandler(500)      
def page_not_found(e):
    return render_template("500.html"), 500

#create name page
@app.route('/name', methods=['GET','POST'])
def name():
    name = None
    form=UserForm()

#validate the Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully")
    return render_template("name.html",form=form,name=name) 

if __name__ == "__main__":
    app.run(debug=True)