#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2020/5/6 9:12 上午
# @file : test.py
# @software : PyCharm


from SpiffWorkflow.specs import WorkflowSpec,Simple,MultiInstance,Join
from workflowexecute import taskSpec

class workflowSpec(WorkflowSpec):
    def __init__(self,nodeList,startTask,tasks,multis,joins,end,lineList):
        WorkflowSpec.__init__(self)
        self.lineList=lineList
        self.nodeList=nodeList

        # 所有节点id
        self.nodeIdList=[x['id'] for x in self.nodeList]

        task_list = locals()

        # 开始节点id
        startId=startTask['id']
        #开始节点之后的节点
        afterNodes=[x for x in self.lineList if x['from']==startId]
        beforeNode=None
        # 开始节点的下一个节点id
        beforeId = afterNodes[0]['from']
        afterId = afterNodes[0]['to']
        task,afterNodeName,beforeNodeName = self.buildFLows(beforeId,afterId)
        task_list[task.name] = task
        self.start.connect(task_list[afterNodeName])

        for i in range(len(self.nodeList)):
            afterNodes=self.buildWorks(afterNodes, task_list)

    def buildWorks(self,nowNodes,task_list):
        allAfterNodes = []
        for i in nowNodes:
            afterNodes = [x for x in self.lineList if x['from'] == i['to']]
            for each in afterNodes:
                beforeId = each['from']
                afterId = each['to']
                task, afterNodeName, beforeNodeName = self.buildFLows(beforeId, afterId)
                task_list[task.name] = task
                beforeNode = task_list[beforeNodeName]

                if task_list[afterNodeName] not in beforeNode.outputs:
                    beforeNode.connect(task_list[afterNodeName])
                allAfterNodes.append(each)
        return allAfterNodes

    def buildFLows(self,beforeId,afterId):
        task = None
        # 判断之后节点在nodeIdList列表中的index
        beforenode_index=self.nodeIdList.index(beforeId)
        afternode_index=self.nodeIdList.index(afterId)
        # 获取nodeList中对应节点的数据信息
        beforeNodeInfo=self.nodeList[beforenode_index]
        afterNodeInfo=self.nodeList[afternode_index]
        beforeNodeName=beforeNodeInfo['name']
        afterNodeName=afterNodeInfo['name']
        try:
            task=self.get_task_spec_from_name(afterNodeName)
        except:
            if afterNodeInfo['type']=='MultiInstance':
                task = MultiInstance(self, afterNodeName, 1)
            elif afterNodeInfo['type']=='task':
                task=taskSpec(self,afterNodeName)
            elif afterNodeInfo['type']=='join':
                task=Join(self,afterNodeName)
            elif afterNodeInfo['type'] == 'end':
                task = Simple(self, 'End')
            print(afterNodeName)
        return task,afterNodeName,beforeNodeName
