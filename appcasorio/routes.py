import boto3
from flask import render_template, flash, redirect, url_for, request
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from appcasorio import appcasorio, db
from appcasorio.forms import LoginForm, RegistrationForm
from appcasorio.models import User, Image
from flask_login import current_user, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy



@appcasorio.route('/')  # essa e a rota debaixo modificam a função, associando-a à essas URL's
@appcasorio.route('/index')
def index():
    img = Image.query.filter_by(aprovado=1)
    return render_template('/index.html', img=img)


@appcasorio.route('/updatedphotos', methods=['POST'])
@login_required
def updatedphotos():
    data = request.form
    for d in data:
        print(d.split('['))
        arr = d.split('[')
        aprovado = 1 if arr[1] == "aproved]" else 0
        Image.query.filter_by(id=arr[0]).update(dict(aprovado=aprovado))
        db.session.commit()
    return redirect(url_for('uploadedphotos'))


@appcasorio.route('/uploadedphotos')
@login_required
def uploadedphotos():
    images = Image.query.all()
    return render_template('uploadedphotos.html', images=images)


@appcasorio.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # se o usuário já estiver logado, ele será redirecionado para index.html
    form = LoginForm()
    if form.validate_on_submit():
        # filtrando para incluir apenas o username que bate exatamente com o que está no form
        user = User.query.filter_by(username=form.username.data).first()  # first pra não ter que correr o banco inteiro
        if user is None or not user.check_password(form.password.data):  # checando a senha
            flash('Usuário ou senha inválidos. Por favor, tente novamente.')  # se nenhum dos dois baterem...
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)  # registrando o usuário como logado
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)


@appcasorio.route('/logout')  # fazendo o logout do usuário
def logout():
    logout_user()
    return redirect(url_for('index'))


@appcasorio.route('/upload', methods=['GET', 'POST'])
def upload():
    s3 = boto3.resource('s3')

    if request.method == "POST":  # se não for post, será GET e pulará as condições do if, usando apenas uma view
        for file in request.files.getlist("myfile"):  # criando uma lista de itens ao invés de receber apenas um
            filename = secure_filename(file.filename)
            if file.filename != '':  # se não for vazio
                s3.Bucket('desafio-surfmappers-estag').put_object(Key=filename, Body=file)
                s3.ObjectAcl('desafio-surfmappers-estag', filename).put(ACL='public-read')
                image = Image(url="https://desafio-surfmappers-estag.s3-us-west-2.amazonaws.com/" + filename)
                db.session.add(image)
                db.session.commit()
            print(file)
    return render_template('upload.html', title="Foto salva!")


@appcasorio.route('/newuser', methods=['GET', 'POST'])
def newuser():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, profile=form.profile.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Usuário registrado com sucesso!')
        return redirect(url_for('newuser'))
    return render_template('newuser.html', title='Novo Usuário', form=form)
