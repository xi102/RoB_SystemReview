# from dataProcess.pdfProcess import *
# from dataProcess.predict import *

#####测试代码，将写入到后台代码部分（pdf转txt）
# pdf_Base_path = "D:/Projects/PythonProjects/NLP_Projects/RoB_SystemReview/data/Upload_pdf"
# txt_Base_Path="D:/Projects/PythonProjects/NLP_Projects/RoB_SystemReview/data/Processed_txt"
# pdfTotxt(pdf_Base_path,txt_Base_Path)
#
# # ######测试代码，将写入后台程序（txt文本处理）
# inBasePath='D:/Projects/PythonProjects/NLP_Projects/RoB_SystemReview/data/Processed_txt'
# outBasePath='D:/Projects/PythonProjects/NLP_Projects/RoB_SystemReview/data/Txt_pre'
# txtTo_Pre_Data(inBasePath,outBasePath)
#
# #######测试代码，将写入到后台代码部分（文档预测）
# txtFilePath='D:/Projects/PythonProjects/NLP_Projects/RoB_SystemReview/data/Txt_pre'
# modelBasePath='D:/Projects/PythonProjects/NLP_Projects/RoB_SystemReview/data/model'
# doc_pre_result=docPrediction(txtFilePath,modelBasePath)
# print(len(doc_pre_result))
# for i in range(len(doc_pre_result)):
#     print(doc_pre_result[i])
#
# # #######测试代码，将写入到后台代码部分（句子预测）
# txtFilePath='D:/Projects/PythonProjects/NLP_Projects/RoB_SystemReview/data/Txt_pre'
# modelBasePath='D:/Projects/PythonProjects/NLP_Projects/RoB_SystemReview/data/model'
# sen_pre_result=senPrediction(txtFilePath,modelBasePath)
# print(len(sen_pre_result))
# for i in range(len(sen_pre_result)):
#     print(sen_pre_result[i])

import joblib
import os


######定义文档评估预测函数
def docPrediction(txtFilePath, modelBasePath):
    model_name_list = ['RSG', 'AC', 'BOP', 'BOA', 'IOD', 'SR']
    ##加载词向量模型
    tfv = joblib.load("D:/Projects/PythonProjects/NLP_Projects/RoB_SystemReview/data/model/TF-IDF_vectors_model.m")
    txt_Name_List = os.listdir(txtFilePath)  # list类型，每个元素为对应的txt文件名
    data = []
    for name in txt_Name_List:
        inPutPath = txtFilePath + '/' + name
        f = open(inPutPath, 'r', encoding='UTF-8').read().replace("\n", " ").replace("  ", " ")
        data.append(f)
    X = tfv.transform(data)
    pre_result = {}
    for modelName in model_name_list:
        dic = {}
        model = joblib.load(modelBasePath + '/' + 'doc_model_' + modelName + '_level.m')
        pre_label = model.predict(X)
        for i in range(len(pre_label)):
            dic[txt_Name_List[i]] = pre_label[i]
        pre_result[modelName] = dic
    return pre_result


######定义句子预测函数
def senPrediction(txtFilePath, modelBasePath):
    model_name_list = ['RSG', 'AC', 'BOP', 'BOA', 'IOD', 'SR']
    ##加载词向量模型
    tfv = joblib.load("D:/Projects/PythonProjects/NLP_Projects/RoB_SystemReview/data/model/TF-IDF_vectors_model.m")
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
            model = joblib.load(modelBasePath + '/' + 'sentence_model_' + modelName + '.m')
            pre_label = model.predict(X)
            for i in range(len(pre_label)):
                if pre_label[i] == 1:
                    category_pre_result.append(data[i])
            dic01[modelName] = category_pre_result
        dic[name] = dic01
    return dic


#########测试代码，将写入到后台代码部分
# txtFilePath='D:/Projects/PythonProjects/NLP_Projects/RoB_SystemReview/data/Txt_pre'
# modelBasePath='D:/Projects/PythonProjects/NLP_Projects/RoB_SystemReview/data/model'
# doc_pre_result=docPrediction(txtFilePath,modelBasePath)
# # print(len(doc_pre_result))
# print(doc_pre_result)
# for key in doc_pre_result:
#     # print(key," : ",doc_pre_result[key])
#     print(key,":",end=" ")
#     for key02 in doc_pre_result[key]:
#         # print(doc_pre_result[key][key02],"  ",end=" ")
#         if doc_pre_result[key][key02] ==1.0:
#             print('Low risk','  ',end=" ")
#         elif doc_pre_result[key][key02]==0.0:
#             print('High/Unclear','  ',end=" ")
#     print()

#######测试代码，将写入到后台代码部分
# txtFilePath='D:/Projects/PythonProjects/NLP_Projects/RoB_SystemReview/data/Txt_pre'
# modelBasePath='D:/Projects/PythonProjects/NLP_Projects/RoB_SystemReview/data/model'
# sen_pre_result=senPrediction(txtFilePath,modelBasePath)
# print(len(sen_pre_result))
# print(sen_pre_result)
# # for i in range(len(sen_pre_result)):
# #     print(sen_pre_result[i])
# for key in sen_pre_result:
#     # print(key,":",sen_pre_result[key])
#     print(key,":",end=" ")
#     for key02 in sen_pre_result[key]:
#         print(sen_pre_result[key][key02],"  ",end=" ")
#     print()
