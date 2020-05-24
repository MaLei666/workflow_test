from __future__ import print_function
from SpiffWorkflow.specs import WorkflowSpec,Simple,MultiInstance,Join,Gate,MultiChoice,StartTask
from SpiffWorkflow.operators import Equal,Attrib,Assign
from workflowexecute import taskSpec
class workflowSpec(WorkflowSpec):
    def __init__(self):
        WorkflowSpec.__init__(self)

        # The first step of our workflow is to let the general confirm
        # the nuclear strike.

        #workflow_run = taskSpec(self, 'Ping','hostname')
        #self.start.connect(workflow_run)
        #workflow_execute = taskSpec(self, 'Shell', ["ping", "-t", "1", "127.0.0.1"])
        #workflow_run.connect(workflow_execute)

        # data = {'post_assign':{'name':'Test','value':'TestValues'}}
        # MultiInstance对当前任务进行拆分，1：要创建的任务数
        multi_inst = MultiInstance(self,'workflow_task',1)

        self.start.connect(multi_inst)


        #taskSpec为任务规范，引用工作流规范，给定任务规范名称
        workflow_1 = taskSpec(self, 'SQL')
        workflow_2 = taskSpec(self, '脚本')
        workflow_3 = taskSpec(self, 'SQL3')


        # TaskSpec，将给定对任务作为输出任务添加
        multi_inst.connect(workflow_1)
        multi_inst.connect(workflow_2)
        multi_inst.connect(workflow_3)

        # 同步之前分割对任务，使用MultiInstance多实例模式时，join可以跨所有实例工作，在使用ThreadSplit时join将忽略来自另一个线程的实例。
        synch_1 = Join(self, 'synch_1')
        #self.start.connect(synch_1)

        workflow_1.connect(synch_1)
        workflow_2.connect(synch_1)
        workflow_3.connect(synch_1)

        #gate_test = Gate(self,'gate1','synch_1')
        #synch_1.connect(gate_test)

        # 实现具有一个或多个输入，和任意数量输出的任务。
        # 如果连接了多个输入，则任务执行隐式多重合并。
        # 如果连接了多个输出，则任务执行隐式并行分割。
        end = Simple(self, 'End')

        # 表示一个if条件，其中多个条件可能同时匹配，从而创建多个传出分支。此任务有一个或多个输入，以及一个或多个传入分支。
        # multichoice = MultiChoice(self, 'multi_choice_1')
        #
        synch_1.connect(end)

        #gate_test.connect(end)
        #synch_1.connect(end)
        #synch_1.connect(multi_inst)

        #end = Simple(self, 'End')
        #workflow_execute.connect(end)
        # As soon as all tasks are either "completed" or  "aborted", the
        # workflow implicitely ends.


# ids = []
# for i in ids2:
#     afterNodeIds = [x for x in lineList if x['from'] == i['to']]
#     for each in afterNodeIds:
#         beforeId = each['from']
#         afterId = each['to']
#         task, afterNodeName, beforenode_index = self.buildFLows(beforeId, afterId, nodeIdList, nodeList)
#         task_list[task.name] = task
#         beforeNodeName = nodeList[beforenode_index]['name']
#         beforeNode = task_list[beforeNodeName]
#
#         if task_list[afterNodeName] not in beforeNode.outputs:
#             beforeNode.connect(task_list[afterNodeName])
#         ids.append(each)
#
# ids2 = []
# task = None
# for i in ids:
#     afterNodeIds = [x for x in lineList if x['from'] == i['to']]
#     toNode = [x['to'] for x in afterNodeIds]
#     # num=len(set(toNode))
#     for each in afterNodeIds:
#         beforeId = each['from']
#         afterId = each['to']
#         task, afterNodeName, beforenode_index = self.buildFLows(beforeId, afterId, nodeIdList, nodeList)
#         # num-=1
#         task_list[task.name] = task
#         beforeNodeName = nodeList[beforenode_index]['name']
#         beforeNode = task_list[beforeNodeName]
#
#         if task_list[afterNodeName] not in beforeNode.outputs:
#             beforeNode.connect(task_list[afterNodeName])
#         ids2.append(each)
#
# ids = []
# for i in ids2:
#     afterNodeIds = [x for x in lineList if x['from'] == i['to']]
#     for each in afterNodeIds:
#         beforeId = each['from']
#         afterId = each['to']
#         task, afterNodeName, beforenode_index = self.buildFLows(beforeId, afterId, nodeIdList, nodeList)
#         task_list[task.name] = task
#         beforeNodeName = nodeList[beforenode_index]['name']
#         beforeNode = task_list[beforeNodeName]
#
#         if task_list[afterNodeName] not in beforeNode.outputs:
#             beforeNode.connect(task_list[afterNodeName])
#         ids.append(each)
#
# ids2 = []
# task = None
# for i in ids:
#     afterNodeIds = [x for x in lineList if x['from'] == i['to']]
#     toNode = [x['to'] for x in afterNodeIds]
#     # num=len(set(toNode))
#     for each in afterNodeIds:
#         beforeId = each['from']
#         afterId = each['to']
#         task, afterNodeName, beforenode_index = self.buildFLows(beforeId, afterId, nodeIdList, nodeList)
#         # num-=1
#         task_list[task.name] = task
#         beforeNodeName = nodeList[beforenode_index]['name']
#         beforeNode = task_list[beforeNodeName]
#
#         if task_list[afterNodeName] not in beforeNode.outputs:
#             beforeNode.connect(task_list[afterNodeName])
#         ids2.append(each)
#
# ids = []
# for i in ids2:
#     afterNodeIds = [x for x in lineList if x['from'] == i['to']]
#     for each in afterNodeIds:
#         beforeId = each['from']
#         afterId = each['to']
#         task, afterNodeName, beforenode_index = self.buildFLows(beforeId, afterId, nodeIdList, nodeList)
#         task_list[task.name] = task
#         beforeNodeName = nodeList[beforenode_index]['name']
#         beforeNode = task_list[beforeNodeName]
#
#         if task_list[afterNodeName] not in beforeNode.outputs:
#             beforeNode.connect(task_list[afterNodeName])
#         ids.append(each)
#
# ids2 = []
# task = None
# for i in ids:
#     afterNodeIds = [x for x in lineList if x['from'] == i['to']]
#     toNode = [x['to'] for x in afterNodeIds]
#     # num=len(set(toNode))
#     for each in afterNodeIds:
#         beforeId = each['from']
#         afterId = each['to']
#         task, afterNodeName, beforenode_index = self.buildFLows(beforeId, afterId, nodeIdList, nodeList)
#         # num-=1
#         task_list[task.name] = task
#         beforeNodeName = nodeList[beforenode_index]['name']
#         beforeNode = task_list[beforeNodeName]
#
#         if task_list[afterNodeName] not in beforeNode.outputs:
#             beforeNode.connect(task_list[afterNodeName])
#         ids2.append(each)
#
# ids = []
# for i in ids2:
#     afterNodeIds = [x for x in lineList if x['from'] == i['to']]
#     for each in afterNodeIds:
#         beforeId = each['from']
#         afterId = each['to']
#         task, afterNodeName, beforenode_index = self.buildFLows(beforeId, afterId, nodeIdList, nodeList)
#         task_list[task.name] = task
#         beforeNodeName = nodeList[beforenode_index]['name']
#         beforeNode = task_list[beforeNodeName]
#
#         if task_list[afterNodeName] not in beforeNode.outputs:
#             beforeNode.connect(task_list[afterNodeName])
#         ids.append(each)
#
# ids2 = []
# task = None
# for i in ids:
#     afterNodeIds = [x for x in lineList if x['from'] == i['to']]
#     toNode = [x['to'] for x in afterNodeIds]
#     # num=len(set(toNode))
#     for each in afterNodeIds:
#         beforeId = each['from']
#         afterId = each['to']
#         task, afterNodeName, beforenode_index = self.buildFLows(beforeId, afterId, nodeIdList, nodeList)
#         # num-=1
#         task_list[task.name] = task
#         beforeNodeName = nodeList[beforenode_index]['name']
#         beforeNode = task_list[beforeNodeName]
#
#         if task_list[afterNodeName] not in beforeNode.outputs:
#             beforeNode.connect(task_list[afterNodeName])
#         ids2.append(each)
#
# ids = []
# for i in ids2:
#     afterNodeIds = [x for x in lineList if x['from'] == i['to']]
#     for each in afterNodeIds:
#         beforeId = each['from']
#         afterId = each['to']
#         task, afterNodeName, beforenode_index = self.buildFLows(beforeId, afterId, nodeIdList, nodeList)
#         task_list[task.name] = task
#         beforeNodeName = nodeList[beforenode_index]['name']
#         beforeNode = task_list[beforeNodeName]
#
#         if task_list[afterNodeName] not in beforeNode.outputs:
#             beforeNode.connect(task_list[afterNodeName])
#         ids.append(each)