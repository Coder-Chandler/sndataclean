import jieba.analyse

# 字符串前面加u表示使用unicode编码
content = u'六一去哪里，当然来苏宁，即日起至6月3日，苏宁红孩子悠方店为您打造欢享童趣嘉年华，玩具满299减100，服纺全场61折；20180601当天前20名进店小朋友还有惊喜礼盒，别忘记您还可使用150-30元预存券，这个六一的欢乐，我们承包了。'

# 第一个参数：待提取关键词的文本
# 第二个参数：返回关键词的数量，重要性从高到低排序
# 第三个参数：是否同时返回每个关键词的权重
# 第四个参数：词性过滤，为空表示不过滤，若提供则仅返回符合词性要求的关键词
keywords = jieba.analyse.extract_tags(content, topK=20, withWeight=True, allowPOS=())
# 访问提取结果
for item in keywords:
    # 分别为关键词和相应的权重
    print(item[0], item[1])

# 同样是四个参数，但allowPOS默认为('ns', 'n', 'vn', 'v')
# 即仅提取地名、名词、动名词、动词
keywords = jieba.analyse.textrank(content, topK=20, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v', 'adj'))
# 访问提取结果
for item in keywords:
    # 分别为关键词和相应的权重
    print(item[0], item[1])


# # 加载jieba.posseg并取个别名，方便调用
# import jieba.posseg as pseg
# words = pseg.cut("我爱北京天安门")
# for word, flag in words:
#     # 格式化模版并传入参数
#     print('%s, %s' % (word, flag))
