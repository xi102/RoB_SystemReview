import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer as TFIV
from sklearn import svm
# from sklearn.externals import joblib
import joblib


############定义TF-IDF词向量训练函数
def trainTFIDF_Vec(file_path):
    # 使用pandas读入训练和测试csv文件
    data = pd.read_csv(file_path)
    # 将训练数据转成词list
    train_data = []
    for i in range(0, len(data['Context'])):
        train_data.append(data['Context'][i])
    # 初始化TFIV对象，去停用词，加1-2元语言模型
    tfv = TFIV(min_df=3, max_features=None, strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}',
               ngram_range=(1, 2), use_idf=1, smooth_idf=1, sublinear_tf=1, stop_words='english')
    # 合并训练和测试集以便进行TFIDF向量化操作
    X_all = train_data
    # 对所有的数据进行向量化操作，耗时比较长
    tfv.fit(X_all)
    return tfv

# train_data='D:/Projects/PythonProjects/NLP_Projects/RiskOfBias/data/document_classification/RoB_and_txt03.csv'
# tfv = trainTFIDF_Vec(train_data)
# ##保存TF-IDF训练好的词向量模型
# joblib.dump(tfv, "TF-IDF_vectors_model.m")

############定义分类模型训练函数
def train_classifier_model(train_file,context,category):
    train=pd.read_csv(train_file)
    train_data = []
    y_train=[]
    for i in range(0, len(train[context])):
        if pd.notnull(train[category][i]):
            train_data.append(train[context][i])
            y_train.append(train[category][i])
    print(len(train_data))
    print(len(y_train))
    # # 初始化TFIV对象，去停用词，加1-2元语言模型
    # tfv = TFIV(min_df=3, max_features=None, strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}',
    #            ngram_range=(1, 2), use_idf=1, smooth_idf=1, sublinear_tf=1, stop_words='english')
    # tfv.fit(train_data)
    ###加载已经训练好的tfidf词向量模型对训练数据进行向量化操作
    tfv=joblib.load('D:/Projects/PythonProjects/NLP_Projects/RoB_SystemReview/data/model/TF-IDF_vectors_model.m')
    X_all=tfv.transform(train_data)
    # 训练svm分类模型
    svclf = svm.LinearSVC(loss='hinge', C=1.0,max_iter=10000)
    svclf.fit(X_all, y_train)
    # #模型保存
    modelpath = "sentence_model_" +"SR"+ ".m"
    joblib.dump(svclf, modelpath)

# train_file='D:/Projects/PythonProjects/NLP_Projects/RiskOfBias/data/document_classification/RoB_and_txt03.csv'
# context='Context'
# category='IOD_level'
# train_classifier_model(train_file,context,category)

# train_file='D:\Projects\PythonProjects\\NLP_Projects\RiskOfBias\data\sentence_classification\SR_quote_sentence.csv'
# context='sentence'
# category='label'
# train_classifier_model(train_file,context,category)