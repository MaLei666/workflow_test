#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2020/4/28 11:01 下午
# @file : auto_build.py
# @software : PyCharm
import json
from wfspec import workflowSpec
from workflowserializer import workflowSerializer

with open('test.json') as fp:
    workflow_json=fp.read()

workflow_json=json.loads(workflow_json)
name=workflow_json['name']
nodeList=workflow_json['nodeList']
lineList=workflow_json['lineList']


spec = workflowSpec(nodeList=nodeList,lineList=lineList,name=name)
step1=spec.buildNodelist()
step2=spec.buildConnect()
serializer = workflowSerializer()


data = spec.serialize(serializer)
# print(data)
pretty = json.dumps(json.loads(data), indent=4, separators=(',', ': '))

open('workflow-spec.json', 'w').write(pretty)








