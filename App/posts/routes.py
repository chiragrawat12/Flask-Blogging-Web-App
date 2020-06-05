from flask import Blueprint,render_template,request,url_for,redirect,abort,flash
from flask_login import current_user,login_required
from App import db
from App.models import Post
from App.posts.forms import PostForm
from datetime import timedelta


posts =Blueprint('posts',__name__)



@login_required
@posts.route('/blog/new',methods=['GET','POST'])
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        post=Post(title=form.title.data , content=form.content.data , author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been Created!","flash-success")
        return redirect(url_for('main.blog'))
    
    return render_template("New_Post.html",title="Create New Post",form=form,legend="New Post")

@posts.route('/post/<int:post_id>',methods=['GET','POST'])
def post(post_id):
    post=Post.query.get_or_404(post_id)
    
    if request.method == "POST":
        if request.form['submit_btn'] == 'Edit':
            return redirect(url_for('posts.update_post',post_id=post_id))
        if request.form['submit_btn'] == 'Yes':
            if post.author != current_user:
                abort(403)
    
            db.session.delete(post)
            db.session.commit()
            flash("Post has been successfully deleted!","flash-success")
            return redirect(url_for("main.blog"))
          
        if request.form['submit_btn'] == 'No':
            return redirect(url_for('posts.post',post_id=post_id))
    return render_template("Post.html",title="Post-"+str(post_id),post=post,timedelta=timedelta)

@posts.route("/post/<int:post_id>/update",methods=['GET','POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash("Your Post has been updated!","flash-success")
        return redirect(url_for('posts.post',post_id=post_id))
    if request.method=='GET':
        form.title.data=post.title
        form.content.data=post.content
    return render_template('New_Post.html',title="Post-"+str(post_id)+"-Update", form=form,legend="Update Post")
    



