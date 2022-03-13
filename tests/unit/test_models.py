from hello import Users

def test_new_user():
    user = Users('nigelsquire72@gmail.com', 'FlaskisAwesome')
    assert user.email == 'nigelsquire72@gmail.com'
    assert user.password_hashed != 'FlaskisAwesome'