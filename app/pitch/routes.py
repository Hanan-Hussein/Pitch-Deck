from flask import Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app.pitch.forms import PitchForm,CommentsForm
from app.models import Pitch
from app import db
from flask import render_template, url_for, flash, redirect, request


posts= Blueprint('posts',__name__)


@posts.route('/comments/<id>',methods=['POST', 'GET'])
@login_required
def comments(id):
    form = CommentsForm()
    pitch = Pitch.query.filter_by(id=id).first()
    if form.validate_on_submit():
        pitch.comments+=form.content.data + '~'
        db.session.commit()
        flash('Your comment was added successfully')
        
        return redirect(url_for('main.home'))
    form.content.data = "Your comment here"
    return render_template('comments.html', form=form , pitch=pitch)





@posts.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    form = PitchForm()
    if form.validate_on_submit():
        pitch = Pitch(title=form.title.data,
                      content=form.content.data, user_id=current_user.id,category=form.category.data)
        db.session.add(pitch)
        db.session.commit()
        flash('Your pitch was successfully added')
        return redirect(url_for('main.home'))
    return render_template('create.html', form=form, title='New Pitch')


@posts.route('/post/like/<int:pitchid>', methods=['GET'])
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
    # pitch.dislikes -= 1
    db.session.commit()
    # return str(pitch.likes)
    return redirect(url_for('main.home'))


@posts.route('/post/dislikes/<int:pitchid>', methods=['POST', 'GET'])
@login_required
def dislikes(pitchid):
    """
    Adds a dislikes when click of a button

    Returns:
        _type_: _description_
    """

    pitch = Pitch.query.filter_by(id=pitchid).first()

    pitch.dislikes += 1
    # pitch.likes -= 1
    db.session.commit()
    return redirect(url_for('main.home'))

@posts.route('/categories/<category>')
def categories(category):
    pitches = Pitch.query.filter_by(category=category)
    return render_template('categories.html', pitches=pitches)

@login_required
@posts.route('/post/edit/<postid>',methods=['POST', 'GET'])
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
        return redirect(url_for("main.home"))
    else:
        form.title.data=edites.title
        form.content.data=edites.content
        form.category.data=edites.category
        
    return render_template('post_edit.html',form=form)

@posts.route('/post/delete/<pitchid>')
def post_delete(pitchid):
    pitch = Pitch.query.filter_by(id=pitchid).first()
    db.session.delete(pitch)
    db.session.commit()
    return redirect(url_for('main.home'))

