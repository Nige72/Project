from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from sqlalchemy import ForeignKey
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from wtforms.widgets import TextArea
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 

# create a flask instance
app = Flask(__name__)
# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Secret key password enviromental variable
app.config['SECRET_KEY'] = os.environ.get("DB_PASS") 
# initialize database
db=SQLAlchemy(app)
# Create Posts table
class Posts(db.Model):
   id = db.Column(db.Integer, primary_key = True) 
   title = db.Column(db.String(250),nullable=False)
   content = db.Column(db.Text,nullable=False)
   author = db.Column(db.String(250),nullable=False)
   date_posted = db.Column(db.DateTime, default=datetime.utcnow)
   slug = db.Column(db.String(255))


   def __repr__(self):
     return '<Name %r>' % self.name

# Create Users Model
class Users(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20),nullable=False,unique=True)
    name = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(120),nullable=False,unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
###Password to be added
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
#####
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
     return '<Name %r>' % self.name

###

# Create a Posts form for db
class PostForm(FlaskForm):
    title = StringField("Title:", validators=[DataRequired()])
    content = StringField("Content:", validators=[DataRequired()],widget=TextArea())
    author = StringField("Author:", validators=[DataRequired()])
    slug = StringField("Slug:", validators=[DataRequired()])
    submit = SubmitField("Submit")
# Delete Posts
@app.route('/posts/delete/int<id>')
def delete_posts(id):
    posts_to_delete = Posts.query.get_or_404(id)
    try:
        db.session.delete(posts_to_delete)
        db.session.commit()
        flash("Post Deleted Succesfully")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)
    except:
        flash("There was problem deleting the post!! ")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)
# Display the posts
@app.route('/posts')
def posts():
# Get the posts from the database
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)
# Error page if no post
@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template("post.html",post=post)
# Edit Posts
@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
     post.title=form.title.data
     post.content=form.content.data
     post.author=form.author.data
     post.slug=form.slug.data
#Update the Post to the DB
     db.session.add(post)
     db.session.commit()
     flash("Post Updated Succesfully")
     return redirect(url_for('post',id=post.id))
    form.title.data = post.title
    form.content.data = post.content
    form.author.data = post.author
    form.slug.data = post.slug
    return render_template("edit_post.html",form=form)

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
# Create Password Form
class PassForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired()])
    password_hash = PasswordField("Password:", validators=[DataRequired()])
    submit = SubmitField("Submit")  
# Create Name Form
class NamerForm(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    submit = SubmitField("Submit")       
# Create a new User form for db
class UserForm(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo("password_hash2", message = "Passwords Must Match")])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
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
# Password hash
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(name=form.name.data, email=form.email.data, password_hash= hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.password_hash.data = ''
        flash("User added to Database")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html",form=form,name=name,our_users=our_users)

#create Password testing page
@app.route('/test_pw', methods=['GET','POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form=PassForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        form.email.data = ''
        form.password_hash.data = ''
# Lookup Users by email
        pw_to_check = Users.query.filter_by(email=email).first()
# Check Hashed Password
        passed = check_password_hash(pw_to_check.password_hash,password)
    return render_template("test_pw.html",email=email,name=name,password=password,form=form,pw_to_check=pw_to_check,passed=passed) 
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
    form=NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully")
    return render_template("name.html",form=form,name=name) 

if __name__ == "__main__":
    app.run(debug=True)