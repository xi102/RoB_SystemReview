"""
应用启动类
"""

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask import render_template, redirect, url_for, flash, request
from Form import Login_Form, Register_Form
from Model import Users, db
from flask_login import LoginManager, login_user, logout_user, login_required
import os
from werkzeug.utils import secure_filename
from dataProcess.pdfProcess import pdfTotxt, txtTo_Pre_Data
from dataProcess.predict import docPrediction, senPrediction, deleteFile

app = Flask(__name__)

# 各项插件的配置
app.config['SECRET_KEY'] = 'kkk'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Asdfghjkl123@211.83.111.224:3306/DataBase_XiaYuan'  # 配置教研室服务器数据库
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/database_java'  # 配置本机数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
bootstrap = Bootstrap(app)
moment = Moment(app)
db.init_app(app)
login_manger = LoginManager()
login_manger.session_protection = 'strong'
login_manger.login_view = 'systemReviewer.login'
login_manger.init_app(app)


@login_manger.user_loader
def load_user(user_id):
    from Model import Users
    return Users.query.get(int(user_id))


@app.route('/')
def login():
    form = Login_Form()
    return render_template('login.html', form=form)


@app.route('/index')
@login_required
def index():
    return render_template('upload.html')


@app.route('/login', methods=['GET', 'POST'])
def do_login():
    form = Login_Form()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is not None and user.password == form.password.data:
            login_user(user)
            flash('登录成功')
            return render_template('upload.html', username=form.username.data)
        else:
            flash('用户或密码错误')
            return render_template('login.html', form=form)


# 用户登出
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已退出登录')
    form = Login_Form()
    return render_template('login.html', form=form)
    # return redirect(url_for(''))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Register_Form()
    if form.validate_on_submit():
        user = Users(username=form.username.data, password=form.password.data, phone=form.phone.data,email=form.email.data,
                     name=form.name.data, organization=form.organization.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径
# ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF','pdf'])  # 允许上传的文件后缀
ALLOWED_EXTENSIONS = set(['pdf'])  # 允许上传的文件后缀


# 判断文件是否合法
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


####上传文件目标路径（pdf文件）
UPLOAD_FOLDER = 'data/Upload_pdf'


@app.route('/upload', methods=['POST'], strict_slashes=False)
@login_required
def api_upload02():
    file_dir = os.path.join(basedir, UPLOAD_FOLDER)  # 拼接成合法文件夹地址
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建
    upload_files = request.files.getlist('myfile')  # 从表单的file字段获取文件，myfile为该表单的name值
    for file in upload_files:
        filename = secure_filename(file.filename)
        if allowed_file(filename):  # 判断是否是允许上传的文件类型
            fxt = filename.split('.')[0][:10]  # 截取文件名的前5个字符作为新的文件名
            ext = filename.rsplit('.', 1)[1]  # 获取文件后缀
            new_filename = fxt + '.' + ext  # 修改文件名
            file.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
    return redirect('/pre_result')


@app.route('/pre_result')
@login_required
def pre_result():
    #####（pdf转txt）
    pdf_Base_path = "./data/Upload_pdf"
    txt_Base_Path = "./data/Processed_txt"
    pdfTotxt(pdf_Base_path, txt_Base_Path)
    ###删除上传pdf文件夹中文件
    deleteFile(pdf_Base_path)

    # ######（txt文本处理）
    inBasePath = './data/Processed_txt'
    outBasePath = './data/Txt_pre'
    txtTo_Pre_Data(inBasePath, outBasePath)
    ####删除中间结果文件夹
    deleteFile(txt_Base_Path)

    #######（文档预测）
    txtFilePath = './data/Txt_pre'
    modelBasePath = './data/model'
    doc_pre_result = docPrediction(txtFilePath, modelBasePath)

    # #######（句子预测）
    sen_pre_result = senPrediction(txtFilePath, modelBasePath)
    ###删除最终作为预测的文档
    deleteFile(txtFilePath)
    return render_template('pre_result.html', doc_pre_result=doc_pre_result, sen_pre_result=sen_pre_result)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
