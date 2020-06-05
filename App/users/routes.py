from flask import Blueprint,render_template,url_for,flash,redirect,request
from flask_login import login_user, current_user, logout_user, login_required
from App import bcrypt, db
from sqlalchemy import desc
from datetime import timedelta
from App.models import User, Post
from App.users.forms import RegistrationForm,ResetPasswordForm,LoginForm,UpadteAccountForm,RequestResetForm
from App.users.utils import save_picture,send_reset_email



users = Blueprint('users',__name__)


@users.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.blog'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.blog'))
        else:
            flash("Loging Failed! Please check email and password","flash-unsuccess")    
    return render_template("LoginPage.html",title="Login Page",form=form)



@users.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.blog'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(first_name=form.first_name.data.capitalize(),last_name=form.last_name.data.capitalize(),email=form.email.data.lower(),password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash("Your Account has been created! You are now able to login","flash-success")
        return redirect(url_for('users.login'))
    return render_template("Register.html",title="Registering Page",form=form)

@login_required
@users.route('/logout',methods=['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpadteAccountForm()
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    posts=Post.query.filter_by(author = user).order_by(desc(Post.date_posted)).paginate(page = page , per_page=3)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file 
        elif request.form['profile-choose']=='remove-profile':
            if current_user.image_file!="default.jpg":
                os.remove(app.root_path+"/static/profile_pic/"+current_user.image_file)
                current_user.image_file="default.jpg"
            db.session.commit()
        current_user.first_name =form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()

        flash('Your Account information has been Updated!','flash-success')
        return redirect(url_for('users.account'))
   
    elif request.method=='GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    
    image_file=url_for('static',filename='profile_pic/' + current_user.image_file)
    return render_template('Account.html',title="Account",image_file=image_file,form=form,timedelta=timedelta,posts=posts,user=user)

@users.route("/user/<string:email>")
@login_required
def user_posts(email):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(email=email).first_or_404()
    posts=Post.query.filter_by(author = user).order_by(Post.date_posted.desc()).paginate(page = page , per_page=3)
    return render_template('User_Post.html', posts=posts , user=user,timedelta=timedelta)


@users.route('/reset_password',methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.blog'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email has been sent with instructions to reset your password.','flash-success')
        return redirect(url_for('users.login'))
    return render_template('Reset_Request.html',title='Reset Password',form=form)

@users.route('/reset_password/<token>',methods=['GET','POST'])
def  reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.blog'))
    user=User.verify_reset_token(token)
    if user is None:
        flash('That is an Invalid or expired token','flash-unsuccess')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('your password has been updated! You are now able to login.','flash-success')
        return redirect(url_for('users.login'))
    return render_template('Reset_Token.html',title='Reset Password',form=form)
