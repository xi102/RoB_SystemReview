# from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.converter import PDFPageAggregator
# from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
import os, re
from nltk.tokenize import sent_tokenize
import nltk

'''
    pdf转txt处理函数，两个参数：待输入PDF文件的路径：InputPath，待输出txt文件的路径：OutputPath
'''


def parse(InputPath, OutputPath):
    # rb以二进制读模式打开本地pdf文件
    fn = open(InputPath, 'rb')
    # 创建一个pdf文档分析器
    parser = PDFParser(fn)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)
    # 提供初始密码doc.initialize("lianxipython")
    # 如果没有密码，就创建一个空的字符串
    doc.initialize(" ")
    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDF资源管理器
        resource = PDFResourceManager()
        # 创建一个PDF参数分析器
        laparams = LAParams()
        # 创建聚合器，用于读取文档对象
        device = PDFPageAggregator(resource, laparams=laparams)
        # 创建解释器，对文档编码，解释成python能够识别的格式
        interpreter = PDFPageInterpreter(resource, device)
        # 循环遍历列表，每次处理一页内容
        # doc.get_pages()获取page列表
        pdfStr = ''
        for page in doc.get_pages():
            # 利用解释器的process_page()方法解析读取单独页数
            interpreter.process_page(page)
            # 使用聚合器get_result()方法获取内容
            layout = device.get_result()
            # 这里layout是一个LTPage对象，里面存放着这个page解析出来的各种对象
            for out in layout:
                # 判断是否含有get_text()方法，获取我们想要的文字
                if (isinstance(out, LTTextBoxHorizontal)):
                    pdfStr = pdfStr + out.get_text() + '\n'
            f = open(OutputPath, 'wb')
            f.write(pdfStr.encode())


def pdfTotxt(PdfBasePath, TxtBasePath):
    pdf_Name_List = os.listdir(PdfBasePath)  # list类型，每个元素为对应的PDF文件名
    for name in pdf_Name_List:
        inPutPath = PdfBasePath + '/' + name
        outPutPath = TxtBasePath + '/' + name.split(".")[0] + '.txt'
        parse(inPutPath, outPutPath)
        # print("完成转换:",name)


#####测试代码，将写入到后台代码部分
# pdf_Base_path = "../data/Upload_pdf"
# txt_Base_Path="../data/Processed_txt"
# pdfTotxt(pdf_Base_path,txt_Base_Path)

pattern = r"""(?x)                   # set flag to allow verbose regexps 
    	              (?:[A-Z]\.)+           # abbreviations, e.g. U.S.A. 
    	              |\d+(?:\.\d+)?%?       # numbers, incl. currency and percentages 
    	              |\w+(?:[-']\w+)*       # words w/ optional internal hyphens/apostrophe 
    	              |\.\.\.                # ellipsis 
    	              |(?:[.,;"'?():-_`])    # special characters with meanings 
    	            """
# 正则表达式过滤特殊符号用空格符占位，双引号、单引号、句点、逗号
pat_letter = re.compile(r'[^a-zA-Z \']+')

######定义文档处理函数，将pdf转换后的txt文档清洗为预测模型所需的格式形式
def txtTo_Pre_Data(inBasePath, outBasePath):
    txt_Name_List = os.listdir(inBasePath)  # list类型，每个元素为对应的txt文件名
    for name in txt_Name_List:
        inPutPath = inBasePath + '/' + name
        outPutPath = outBasePath + '/' + name.split(".")[0] + '.txt'
        f = open(inPutPath, 'r', encoding='UTF-8').read()
        f1 = open(outPutPath, 'w', encoding='utf-8')
        content = f.replace("\n", " ").replace("  ", " ")
        for line in sent_tokenize(content):
            new_line = pat_letter.sub(' ', line).strip().lower()
            word_list = nltk.regexp_tokenize(new_line, pattern)
            filtered_words = [w for w in word_list if (w not in nltk.corpus.stopwords.words('english'))]
            if len(filtered_words) > 5:
                # print(len(filtered_words))
                # print(filtered_words)
                for word in filtered_words:
                    f1.write(str(word) + ' ')
                f1.write('\n')
        f1.close()

# ######测试代码，将写入后台程序
# inBasePath='../data/Processed_txt'
# outBasePath='../data/Txt_pre'
# txtTo_Pre_Data(inBasePath,outBasePath)