import joblib
import os
import heapq

######定义文档评估预测函数
def docPrediction(txtFilePath, modelBasePath):
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
    tfv = joblib.load(".._V2.1/data/model/TF-IDF_vectors_model.m")
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
# result=[]
# f=open('..__V2.1/data/Txt_pre/Chiu S, 2016.txt', 'r', encoding='UTF-8')
# for line in f.readlines():
#     data.append(line)
# print(len(data))
# tfv = joblib.load(".._V2.1/data/model/TF-IDF_vectors_model.m")
# X = tfv.transform(data)
# model=joblib.load('.._V2.1/dataProcess/sentence_model_RSG.m')
# pre_label=model.predict_proba(X)
# for i in range(len(pre_label)):
#     result.append(pre_label[i][1])
# print(len(result))
# re1=list(map(result.index,heapq.nlargest(3,result)))
# print(re1)
# for j in re1:
#     print(result[j])
#     print(data[j])





#########测试代码，将写入到后台代码部分
# txtFilePath='.._V2.1/data/Txt_pre'
# modelBasePath='.._V2.1/data/model'
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
# txtFilePath='.._V2.1/data/Txt_pre'
# modelBasePath='.._V2.1/data/model'
# sen_pre_result=senPrediction(txtFilePath,modelBasePath)
# print(len(sen_pre_result))
# # print(sen_pre_result)
# # for i in range(len(sen_pre_result)):
# #     print(sen_pre_result[i])
# for key in sen_pre_result:
#     # print(key,":",sen_pre_result[key])
#     print(key,":",end=" ")
#     for key02 in sen_pre_result[key]:
#         print(sen_pre_result[key][key02],"  ",end=" ")
#     print()