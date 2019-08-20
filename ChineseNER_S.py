# -*- coding: utf-8 -*-

"""
 Created by Overlord Yuan at 2019/8/9
"""

from flask import Flask
from flask import request
import re
import fool,datetime
from jpype import *
app = Flask(__name__)
import os
root = os.path.abspath(".")
lib = os.path.join(root,'lib')

startJVM(getDefaultJVMPath(),
         "-Djava.class.path="+lib+"/hanlp-portable-1.7.4.jar;"+lib,
         "-Xms1g",
         "-Xmx1g")
HanLP = JClass('com.hankcs.hanlp.HanLP')
segment =HanLP.newSegment().enablePlaceRecognize(True)\
    .enableNameRecognize(True)\
    .enableTranslatedNameRecognize(True)\
    .enableOrganizationRecognize(True)

import socket  # 导入 socket 模块




def analysis_B(ners,paraId,senId):
    res = []
    for obj in ners[0]:
        if obj[2]=='person' or obj[2]=='organization' or obj[2]=='location':
          entity = {}
          entity['entity'] =obj[3]
          entity['startPos'] = obj[0]
          entity['endPos'] = obj[1]
          if obj[2] == 'person':
              entity['typeName'] = '1-person'
          elif obj[2] == 'organization':
              entity['typeName'] = '2-organization'
          elif obj[2] == 'location':
              entity['typeName'] = '3-location'
          entity['paraID'] = paraId
          entity['senID'] = senId
          res.append(entity)
    return res
def analysis_C(nes,paraId,senId):
    res = []
    for term in nes:
        label = term.nature.toString()
        if label == "nr" or  label == "nrf" or label == "nt"or label == "ns":
            entity = {}
            entity['entity'] = term.word
            entity['startPos'] = term.offset
            entity['endPos'] = term.offset + term.length()
            if label == "nr" or label == "nrf":
                entity['typeName'] = "1-person"
            elif label == "nt":
                entity['typeName'] = "2-organization"
            else:
                entity['typeName'] = "3-location"
            entity['paraID'] = paraId
            entity['senID'] = senId
            res.append(entity)
    return res

def check(dict0,dict1):
    res = []
    for item in dict0:
        for obj in dict1:
            if item['entity']==obj['entity']:
               res.append(obj)
               break
    return res

@app.route('/bilstm-crf-cn_new', methods=['POST'])
def bilstm_crf_processing_new():
    ckpt1 = datetime.datetime.now()
    senId = 0
    paraId = 1
    content = request.form['content']
    sents = re.split("[。？!]", content)
    entities = []

    for sent in sents:
        if len(sent) == 0:
            continue
        senId += 1
        ners_B = fool.ner(sent)
        ners_C = segment.seg(sent)
        result0 = analysis_B(ners_B,paraId,senId)
        print(result0)
        result1 = analysis_C(ners_C, paraId, senId)
        print(result1)
        # print(result)
        result = check(result0,result1)
        entities.append(result)
    print(datetime.datetime.now()-ckpt1)
    entities =  sum(entities, [])
    print(entities)
    return str(entities)


if __name__ == '__main__':
    s = socket.socket()  # 创建 socket 对象
    host = socket.gethostname()  # 获取本地主机名
    port = 12345  # 设置端口
    s.bind((host, port))
    s.listen(5)                 # 等待客户端连接
    while True:
        c,addr = s.accept()     # 建立客户端连接
        print('连接地址：', addr)
        c.send('欢迎访问菜鸟教程')
        c.close()                # 关闭连接