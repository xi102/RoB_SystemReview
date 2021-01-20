import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer as TFIV
# from sklearn.externals import joblib
import joblib
import os,shutil
import heapq
'''
    预测过程中对输入数据进行向量化操作时必须保证调用的向量化模型与训练分类模型时所采用的向量化模型一致，否则将会报错
    ValueError: X has 585818 features per sample; expecting 585480
    即训练的分类模型中向量模型的特征维度必须与对测试数据进行向量化操作的向量模型的特征维度一致。
'''
######定义文档评估预测函数
def docPrediction(txtFilePath,modelBasePath):
    model_name_list = ['RSG', 'AC', 'BOP', 'BOA', 'IOD', 'SR']
    ##加载词向量模型
    tfv = joblib.load("./data/model/TF-IDF_vectors_model.m")
    txt_Name_List = os.listdir(txtFilePath)  # list类型，每个元素为对应的txt文件名
    data = []
    for name in txt_Name_List:
        inPutPath = txtFilePath + '/' + name
        f = open(inPutPath, 'r', encoding='UTF-8').read().replace("\n", " ").replace("  ", " ")
        data.append(f)
    X = tfv.transform(data)
    pre_result={}
    for modelName in model_name_list:
        dic = {}
        model=joblib.load(modelBasePath+'/'+'doc_model_'+modelName+'_level.m')
        pre_label=model.predict(X)
        for i in range(len(pre_label)):
            dic[txt_Name_List[i]]=pre_label[i]
        pre_result[modelName]=dic
    return pre_result

# #########测试代码，将写入到后台代码部分
# txtFilePath='./data/Txt_pre'
# modelBasePath='./data/model'
# doc_pre_result=docPrediction(txtFilePath,modelBasePath)
# print(len(doc_pre_result))
# print(doc_pre_result)
# for key in doc_pre_result:
#     print(key,":",end=" ")
#     for key02 in doc_pre_result[key]:
#         print(doc_pre_result[key][key02],"  ",end=" ")
#     print()

######定义句子预测函数
def senPrediction(txtFilePath, modelBasePath):
    model_name_list = ['RSG', 'AC', 'BOP', 'BOA', 'IOD', 'SR']
    ##加载词向量模型
    tfv = joblib.load("./data/model/TF-IDF_vectors_model.m")
    txt_Name_List = os.listdir(txtFilePath)  # list类型，每个元素为对应的txt文件名
    dic = {}
    for name in txt_Name_List:
        data = []
        inPutPath = txtFilePath + '/' + name
        f = open(inPutPath, 'r', encoding='UTF-8')
        for line in f.readlines():
            data.append(line)
        X = tfv.transform(data)
        dic01 = {}
        for modelName in model_name_list:
            category_pre_result = []
            result = []
            model = joblib.load(modelBasePath + '/' + 'sentence_model_' + modelName + '.m')
            pre_label = model.predict_proba(X)
            for i in range(len(pre_label)):
                result.append(pre_label[i][1])
            re1 = list(map(result.index, heapq.nlargest(3, result)))
            # print(re1)
            for j in re1:
                category_pre_result.append(data[j])
            dic01[modelName] = category_pre_result
        dic[name] = dic01
    return dic


# data=[]
# f=open('./data/Txt_pre/Li P, 2010.txt', 'r', encoding='UTF-8')
# for line in f.readlines():
#     data.append(line)
# print(len(data))
# tfv = joblib.load("./data/model/TF-IDF_vectors_model.m")
# X = tfv.transform(data)
# model=joblib.load('./data/model/sentence_model_BOA.m')
# pre_label=model.predict(X)
# print(pre_label)
# pre_data=list(map(lambda x:[x],pre_label))
# print(len(pre_data))
# for i in range(len(pre_label)):
#     if pre_label[i]==1:
#         print(data[i])

# #######测试代码，将写入到后台代码部分
# txtFilePath='./data/Txt_pre'
# modelBasePath='./data/model'
# sen_pre_result=senPrediction(txtFilePath,modelBasePath)
# print(len(sen_pre_result))
# print(sen_pre_result)
# for key in sen_pre_result:
#     print(key,":",end=" ")
#     for key02 in sen_pre_result[key]:
#         print(sen_pre_result[key][key02],"  ",end=" ")
#     print()

########预测完成后需要删除上传文件路径以及文件处理过程中间产生的路径下的文件
def deleteFile(filePath):
    rootdir = filePath
    filelist = os.listdir(rootdir)
    for f in filelist:
        filepath = os.path.join(rootdir, f)
        if os.path.isfile(filepath):
            os.remove(filepath)
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath, True)
    # shutil.rmtree(rootdir,True)