#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2020/4/20 10:31 下午
# @file : test2.py
# @software : PyCharm

import xml
import json
from SpiffWorkflow.serializer.json import JSONSerializer
from test1.test import NuclearStrikeWorkflowSpec
#
# serializer = JSONSerializer()
# spec = NuclearStrikeWorkflowSpec()
# data = spec.serialize(serializer)
#
# # This next line is unnecessary in practice; it just makes the JSON pretty.
# pretty = json.dumps(json.loads(data), indent=4, separators=(',', ': '))
#
# open('workflow-spec.json', 'w').write(pretty)


from SpiffWorkflow.serializer.xml import XmlSerializer
serializer=XmlSerializer()
spec = NuclearStrikeWorkflowSpec()
data = spec.serialize(serializer)

# This next line is unnecessary in practice; it just makes the JSON pretty.
# pretty = json.dumps(json.loads(data), indent=4, separators=(',', ': '))

open('workflow-spec.xml', 'w').write(data)