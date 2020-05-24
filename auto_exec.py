#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2020/5/6 11:12 上午
# @file : auto_exec.py
# @software : PyCharm

from workflowserializer import workflowSerializer
from SpiffWorkflow.specs import WorkflowSpec
from SpiffWorkflow.task import Task
from workflow_engine import workflowNew
from SpiffWorkflow.workflow import Workflow
import json
from wfspec import workflowSpec
# # todo 接收传递的参数，修改json
# param={
#         "host_list": [
#             "localhost",
#         ],
#         "playbooks": ["test.yml"],
#         "password": "vagrant",
#         "username": "vagrant"
#     }
# with open('workflow-spec.json') as fp:
#     workflow_json = json.load(fp)
# workflow_json['task_specs']['task1']['parameters'] =param
#
# # print(workflow_json['task_specs']['task1']['parameters'])
#
# with open('workflow-spec.json','w') as fp:
#     json.dump(workflow_json,fp,indent=4, separators=(',', ': '))


# # todo 读取并执行
with open('workflow-spec.json') as fp:
    workflow_json=fp.read()

serializer=workflowSerializer()
spec=WorkflowSpec.deserialize(serializer,workflow_json)
workflowtest=workflowNew(spec)

completed=workflowtest.is_completed()
while not completed:
    # workflowtest.dump()
    tasks = workflowtest.get_tasks(Task.READY)
    # for t in tasks:
    #     print("Ready:", t.task_spec.name)
    print("Ready:", tasks)
    re_status,task_name=workflowtest.complete_next()
    print('stage:',task_name,re_status)
    if re_status==False:
        data = workflowtest.serialize(serializer)
        pretty = json.dumps(json.loads(data), indent=4, separators=(',', ': '))
        open('workflow-interrupt.json', 'w').write(pretty)
        completed=True
        break
    else:
        completed=workflowtest.is_completed()

if not workflowtest.is_completed():
    print('error')

# # # # todo 断点读取并执行
# with open('workflow-interrupt.json') as fp:
#     workflow_json=fp.read()
#
# serializer=workflowSerializer()
# workflow_restore=workflowNew.deserialize(serializer,workflow_json)
# workflowtest=workflowNew(workflow_restore.spec)
# # workflowtest=Workflow(workflow_restore.spec)
#
# workflowtest.spec=workflow_restore.spec
# workflowtest.task_tree=workflow_restore.task_tree
# # workflowtest.dump()
#
# completed=workflowtest.is_completed()
# while not completed:
#     # workflowtest.dump()
#     tasks = workflowtest.get_tasks(Task.READY)
#     for t in tasks:
#         print("Ready:", t.task_spec.name)
#         re_status=workflowtest.complete_next()
#         # re_status=t.complete()
#         print(re_status)
#         if re_status==False:
#             data = workflowtest.serialize(serializer)
#             pretty = json.dumps(json.loads(data), indent=4, separators=(',', ': '))
#             open('workflow-interrupt.json', 'w').write(pretty)
#             completed=True
#             break
#         else:
#             completed=workflowtest.is_completed()
#
#     # workflowtest.dump()
#     # a=workflowtest.get_tasks(state=Task.ANY_MASK)
#     # print(a)
#
# # if not workflowtest.is_completed():
# #     print('error')