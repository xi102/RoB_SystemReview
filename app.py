import time
from flask import Flask, render_template, request, jsonify, redirect
import os
from werkzeug.utils import secure_filename
from dataProcess.pdfProcess import pdfTotxt, txtTo_Pre_Data
from dataProcess.predict import docPrediction, senPrediction,deleteFile

app = Flask(__name__)

UPLOAD_FOLDER = 'data/Upload_pdf'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # 设置文件上传的目标文件夹
basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径
# ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF','pdf'])  # 允许上传的文件后缀
ALLOWED_EXTENSIONS = set(['pdf']) # 允许上传的文件后缀

# 判断文件是否合法
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 具有上传功能的页面
@app.route('/index')
def upload_test():
    return render_template('upload.html')



@app.route('/upload', methods=['POST'], strict_slashes=False)
def api_upload02():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])  # 拼接成合法文件夹地址
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建
    upload_files = request.files.getlist('myfile')  # 从表单的file字段获取文件，myfile为该表单的name值
    # print(upload_files)
    for file in upload_files:
        filename = secure_filename(file.filename)
        if allowed_file(filename):  # 判断是否是允许上传的文件类型
            fxt = filename.split('.')[0][:10]  # 截取文件名的前5个字符作为新的文件名
            ext = filename.rsplit('.', 1)[1]  # 获取文件后缀
            # unix_time = int(time.time())
            # new_filename = str(unix_time) + '.' + ext  # 修改文件名
            new_filename = fxt + '.' + ext  # 修改文件名
            file.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
    return redirect('/pre_result')
    # return "hello world!!!"


@app.route('/pre_result')
def hello_world():
    #####（pdf转txt）
    pdf_Base_path = ".._V2.1/data/Upload_pdf"
    txt_Base_Path = ".._V2.1/data/Processed_txt"
    pdfTotxt(pdf_Base_path, txt_Base_Path)

    # ######（txt文本处理）
    inBasePath = '.._V2.1/data/Processed_txt'
    outBasePath = '.._V2.1/data/Txt_pre'
    txtTo_Pre_Data(inBasePath, outBasePath)

    #######（文档预测）
    txtFilePath = '.._V2.1/data/Txt_pre'
    modelBasePath = '.._V2.1/data/model'
    doc_pre_result = docPrediction(txtFilePath, modelBasePath)
    for key in doc_pre_result:
        print(key, ":", end=" ")
        for key02 in doc_pre_result[key]:
            print(doc_pre_result[key][key02], "  ", end=" ")
        print()

    # #######（句子预测）
    txtFilePath = '.._V2.1/data/Txt_pre'
    modelBasePath = '.._V2.1/data/model'
    sen_pre_result = senPrediction(txtFilePath, modelBasePath)
    for key in sen_pre_result:
        print(key, ":", end=" ")
        for key02 in sen_pre_result[key]:
            print(sen_pre_result[key][key02], "  ", end=" ")
        print()
    deleteFile(pdf_Base_path)
    deleteFile(txt_Base_Path)
    deleteFile(txtFilePath)
    return render_template('pre_result.html', doc_pre_result=doc_pre_result, sen_pre_result=sen_pre_result)


if __name__ == '__main__':
    app.run()
