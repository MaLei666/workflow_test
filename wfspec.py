#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2020/4/29 10:58 上午
# @file : wfspec.py
# @software : PyCharm

from SpiffWorkflow.specs import WorkflowSpec,Simple,MultiInstance,Join
from workflowexecute import taskSpec

class workflowSpec(WorkflowSpec):
    def __init__(self,nodeList,lineList,name):
        WorkflowSpec.__init__(self,name)
        self.lineList=lineList
        self.nodeList=nodeList
        self.task_list = locals()


    def buildNodelist(self):
        task=None
        for node in self.nodeList:
            nodeId=str(node['id'])
            nodeName=node['name']
            nodeType=node['type']
            try:
                task=self.get_task_spec_from_name(nodeName)
            except:
                if nodeType=='StartTask':
                    self.start.description=nodeId
                    task = self.start
                elif nodeType=='MultiInstance':
                    task = MultiInstance(self, nodeName, 1,description=nodeId)
                elif nodeType=='playbook':
                    file_path = node['file_path']
                    task=taskSpec(self,nodeName,description=nodeId,node_type=nodeType,file_path=file_path)
                elif nodeType=='join':
                    task=Join(self,nodeName,description=nodeId)
                elif nodeType == 'end':
                    task = Simple(self, nodeName,description=nodeId)
                else:
                    task = Simple(self, nodeName,description=nodeId)
            finally:
                print(nodeId,nodeName)
                self.task_list[nodeId]=task
        return task

    def buildConnect(self):
        for line in self.lineList:
            beginId=line['from']
            afterId=line['to']
            try:
                self.task_list[beginId].connect(self.task_list[afterId])
            except Exception as e:
                print(e)

