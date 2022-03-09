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