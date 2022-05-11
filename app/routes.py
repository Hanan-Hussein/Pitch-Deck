from flask import render_template, url_for, flash, redirect, request
from . import app, db, bcrypt,mail
from flask_mail import Mail, Message
import secrets
import os
from PIL import Image
from app.models import User, Pitch
from flask_login import login_user, current_user, logout_user, login_required
from app.forms import Register, Login, PitchForm, CommentsForm,UpdateAccountForm
db.create_all()


def comments_cutter(string_comments):
    """Takes in a string cuts it and returns a list of comments
    """
    return string_comments.split(';')


@app.route('/')
def home():
    # All pitches here
    pitches = Pitch.query.all()

    # comments_list = comments_cutter(pitches.comments)
    return render_template('index.html', pitches=pitches)


@app.route('/comments/<id>',methods=['POST', 'GET'])
@login_required
def comments(id):
    form = CommentsForm()
    pitch = Pitch.query.filter_by(id=id).first()
    if form.validate_on_submit():
        pitch.comments+=form.content.data + '~'
        db.session.commit()
        flash('Your comment was added successfully')
        
        return redirect(url_for('home'))
    form.content.data = "Your comment here"
    return render_template('comments.html', form=form , pitch=pitch)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Register()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your Account Has been Created! You are now able to login  in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/authentification/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Welcome {user.username.title()} !! ', 'success')
            # args is a dict
            # get returns none if the next key does not exist
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    """
    
    """

    #base of file name
    random_hex= secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex +f_ext

    picture_path=os.path.join(app.root_path,'static/profiles',picture_fn)

    output_size=(125,125)
    i=Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn

@app.route('/account',methods=['POST', 'GET'])
@login_required
def account():
    """
    """
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture=save_picture(form.picture.data)
            current_user.profile=picture
             
        current_user.username=form.username.data
        current_user.email=form.email.data

        db.session.commit()
        flash('Your Account Has been updated!','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':

        form.username.data=current_user.username
        form.email.data=current_user.email
    
    msg=Message("Hello",sender="apollolibrary99@gmail.com",recipients=['abduba13@gmail.com'])
    msg.body = "Rich JAFFARRRRRRRR"
    mail.send(msg)
    image_file= url_for('static',filename='profiles/'+current_user.profile)
    return render_template('account.html', title='Account',image_file=image_file,form=form )


@app.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    form = PitchForm()
    if form.validate_on_submit():
        pitch = Pitch(title=form.title.data,
                      content=form.content.data, user_id=current_user.id,category=form.category.data)
        db.session.add(pitch)
        db.session.commit()
        flash('Your pitch was successfully added')
        return redirect(url_for('home'))
    return render_template('create.html', form=form, title='New Pitch')


@app.route('/post/like/<int:pitchid>', methods=['GET'])
@login_required
def likes(pitchid):
    """
    Adds a like when click of a button

    Returns:
        _type_: _description_
    """

    pitch = Pitch.query.filter_by(id=pitchid).first()

    # update = pitch.likes + 1
    pitch.likes += 1
    pitch.dislikes -= 1
    db.session.commit()
    # return str(pitch.likes)
    return redirect(url_for('home'))


@app.route('/post/dislikes/<int:pitchid>', methods=['POST', 'GET'])
@login_required
def dislikes(pitchid):
    """
    Adds a dislikes when click of a button

    Returns:
        _type_: _description_
    """

    pitch = Pitch.query.filter_by(id=pitchid).first()

    pitch.dislikes += 1
    pitch.likes -= 1
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/categories/<category>')
def categories(category):
    pitches = Pitch.query.filter_by(category=category)
    return render_template('categories.html', pitches=pitches)

@app.route('/post/edit/<postid>',methods=['POST', 'GET'])
def post_edit(postid):
    form = PitchForm()

    edites= Pitch.query.filter_by(id=postid).first()
    
    if form.validate_on_submit():
        edites.title = form.title.data
        edites.content=form.content.data
        edites.category=form.category.data
        
        db.session.add(edites)
        db.session.commit()
        flash('Your Pitch Has been updated!','success')
        return redirect(url_for("home"))
    else:
        form.title.data=edites.title
        form.content.data=edites.content
        form.category.data=edites.category
        
    return render_template('post_edit.html',form=form)

@app.route('/post/delete/<pitchid>')
def post_delete(pitchid):
    pitch = Pitch.query.filter_by(id=pitchid).first()
    db.session.delete(pitch)
    db.session.commit()
    return redirect(url_for('home'))

