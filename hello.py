
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
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user, user_loaded_from_request 
# create a flask instance
app = Flask(__name__)
# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Secret key password enviromental variable
app.config['SECRET_KEY'] = os.environ.get("DB_PASS") 
# initialize database
db=SQLAlchemy(app)

# Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
####  All FORMS ###########################################################
# Create LoginForm
class LoginForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    submit = SubmitField("Submit")  
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
    name = StringField("Name:",validators=[DataRequired()])
    username = StringField("Username:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo("password_hash2", message = "Passwords Must Match")])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
# Create a Posts form for db
class PostForm(FlaskForm):
    title = StringField("Title:", validators=[DataRequired()])
    content = StringField("Content:", validators=[DataRequired()],widget=TextArea())
    author = StringField("Author:")
    slug = StringField("Slug:", validators=[DataRequired()])
    submit = SubmitField("Submit")
#########################################################################################################
##############################################################
###### CREATE THE DB MODELS #####################
################################
# Create Posts table
class Posts(db.Model):
   id = db.Column(db.Integer, primary_key = True) 
   title = db.Column(db.String(250),nullable=False)
   content = db.Column(db.Text,nullable=False)
   #author = db.Column(db.String(250),nullable=False)
   date_posted = db.Column(db.DateTime, default=datetime.utcnow)
   slug = db.Column(db.String(255))
## create a foreign key to relate to the primary key of the Users
   poster_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    
   def __repr__(self):
     return '<Name %r>' % self.name

# Create Users Model
class Users(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20),nullable=False,unique=True)
    name = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(120),nullable=False,unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # user can have many posts
    posts = db.relationship('Posts', backref='poster')
###Password to be added
    password_hash = db.Column(db.String(128))
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
     return '<Name %r>' % self.name
##################################################################
# Create Login Page
#########################
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
# Check the Hash
            if check_password_hash(user.password_hash, form.password.data): 
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
               flash("Wrong Password Matey") 
        else: 
            flash("That User Does not exist try again matey!!!!")   
    return render_template('login.html',form=form)
# Create Logout
@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("See ya matey you are logged out!!!!")  
    return redirect(url_for('login'))
##############################################################################
####    Create Dashboard Page
############################
@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
     form = UserForm()
     id = current_user.id
     name_to_update = Users.query.get_or_404(id)
     if request.method =="POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("User Updated Succesfully")
            return render_template("dashboard.html",form=form,name_to_update=name_to_update)
        except:
   
             flash("Issue with updating")
             return render_template("dashboard.html",form=form,name_to_update=name_to_update)
     else:
        return render_template("dashboard.html",form=form,name_to_update=name_to_update)
#########################################################################################
##### Index Main Page 
############################### 
@app.route('/')
def index():
    first_name = "Nige"
    stuff = "This is <strong>BOLD<strong> Text"
    favourite_pizza = ["Mexican","Cheese","Pepperoni"]
    return render_template("index.html",first_name=first_name,stuff=stuff,favourite_pizza=favourite_pizza)
###############################################################################################
###### Name Page 
#####################
@app.route('/name', methods=['GET','POST'])
def name():
    name = None
    form=NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully")
    return render_template("name.html",form=form,name=name) 
############################################################################
###### ADD A USER TO THE DATABASE 
###################################
@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name = None
    form=UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
# Password hash
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(name=form.name.data,username=form.username.data, email=form.email.data, password_hash= hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.password_hash.data = ''
        flash("User added to Database now click on login to create posts")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html",form=form,name=name,our_users=our_users)
#################################################################################
########### DELETE USERS IN DATABASE
#############################################
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
##########################################################################################
########### UPDATE DATABASE RECORD
###############################
@app.route('/update/<int:id>',methods=['GET','POST'])
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method =="POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("User Updated Succesfully")
            return render_template("update.html",form=form,name_to_update=name_to_update)
        except:
   
             flash("Issue with updating")
             return render_template("update.html",form=form,name_to_update=name_to_update)
    else:
        return render_template("update.html",form=form,name_to_update=name_to_update)
#########################################################################################
############ ADD A POST PAGE 
##########################################
@app.route('/add-post', methods=['GET','POST'])
@login_required
def add_post():
    form=PostForm()
    if form.validate_on_submit():
      poster = current_user.id
      post = Posts(title=form.title.data,content=form.content.data,poster_id=poster,slug=form.slug.data)
#Clear Form
      form.title.data = ''
      form.content.data = ''
      form.slug.data = ''
      #Add to DB
      db.session.add(post)
      db.session.commit()

      flash("Blog Post Submitted click on posts to view your post")

    return render_template("add_post.html",form=form)
######################################################################################
################# DELETE A POST 
##################################
@app.route('/posts/delete/int<id>')
@login_required
def delete_posts(id):
    form=PostForm()
    posts_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    if id == posts_to_delete.poster.id:
        try:
            db.session.delete(posts_to_delete)
            db.session.commit()
            flash("Post Deleted Succesfully")
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html", posts=posts,form=form)
        except:
            flash("There was problem deleting the post!! ")
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html", posts=posts)
    else:
         flash("You are not authorised to delete this post!! ")
         posts = Posts.query.order_by(Posts.date_posted)
         return render_template("posts.html", posts=posts)
##############################################################
########### EDIT THE POSTS 
########################################
@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
      post.title=form.title.data
      post.content=form.content.data
      post.slug=form.slug.data
     #Update the Post to the DB
      db.session.add(post)
      db.session.commit()
      flash("Post Updated Succesfully")
      return redirect(url_for('post',id=post.id))

    if current_user.id == post.poster_id:
        form.title.data = post.title
        form.content.data = post.content
        form.slug.data = post.slug
        return render_template("edit_post.html",form=form)
    else:
        flash("You are not authorised to Edit this post!! ")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)
####################################################################################
######### DISPLAY THE POSTS
##################################################
@app.route('/posts')
@login_required
def posts():
# Get the posts from the database
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)
#############################################################
######### ERROR PAGE IF NO POST AVAILABLE
#######################################
@app.route('/posts/<int:id>')
@login_required
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template("post.html",post=post)
################################################################################
######## Error Pages 
###########################
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
##########################################################################


if __name__ == "__main__":
    app.run(debug=True)