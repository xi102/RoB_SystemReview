# 自动化偏倚风险评估系统

## 项目说明

这是一个自动化偏倚风险评估（Automated Risk of Bias Assessment）的演示

用Flask和Jinja2随便糊了个前端和后端

训练数据集是自己爬的Cochrane的文章，搜刮了一些随机对照试验（Randomized Controlled Trial, RCT）的文章构建了一点数据集，用BERT炼的丹

## 运行和调试

### 准备训练好的模型

如果自己训练了一份就把`data/model`里面的文件替换掉就好了

训练好的模型我放到`data/model`里面一份，由于TF-IDF那个模型的文件太大了，我放到release里面了

```bash
curl --create-dirs -O --output-dir ./data/model https://github.com/xi102/RoB_SystemReview/releases/download/v0.1.0/TF-IDF_vectors_model.m
```

### 安装依赖

```bash
pip install -r requerements.txt
```

### 运行调试

```bash
python Start.py
```

请勿将此命令用于生产环境，默认设置开启Debug模式、端口5000，生产环境请自行关闭Debug并设置防火墙策略

## 各目录功能



## 关于

本项目相关论文

[夏渊.系统评价中自动化偏倚风险评估的相关算法研究[D].四川:电子科技大学,2020.](http://d.wanfangdata.com.cn/thesis/ChJUaGVzaXNOZXdTMjAyMDEwMjgSCUQwMTk2MzI3OBoIdmluMXhwcXo%3D)  
[基于 BERT 的自动化偏倚风险评价方法的研究](http://www.cjebm.com/article/10.7507/1672-2531.202006177)  
