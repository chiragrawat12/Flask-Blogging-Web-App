from flask import render_template,request,Blueprint,redirect,url_for
from flask_login import login_required,current_user
from App.models import Post
from datetime import timedelta

main =Blueprint('main',__name__)

@main.route('/home',methods=['GET','POST'])
@main.route('/',methods=['GET','POST'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.blog'))
    if request.method=='POST':
        if request.form["submit_btn"] == "Login":
            return redirect(url_for('main.login'))
        elif request.form["submit_btn"] == "Register":
            return redirect(url_for('main.register'))
        else:
            pass
    else:
        return render_template('Home.html',title="Home")






@main.route('/blog')
@login_required
def blog():
    page = request.args.get('page', 1 , type=int)
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(page = page , per_page=3)
    return render_template('Blog.html',title="Blog",posts=posts,timedelta=timedelta)


