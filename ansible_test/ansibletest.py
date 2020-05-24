from __future__ import print_function
from SpiffWorkflow.specs import WorkflowSpec,Simple,MultiInstance,Join,Gate,MultiChoice,StartTask 
from SpiffWorkflow.operators import Equal,Attrib,Assign
from Ansibleexecute import AnsibleRun
class AnsibleWorkflowSpec(WorkflowSpec):
    def __init__(self):
        WorkflowSpec.__init__(self)

        # The first step of our workflow is to let the general confirm
        # the nuclear strike.

        #ansible_run = AnsibleRun(self, 'Ping','hostname')
        #self.start.connect(ansible_run)
        #ansible_execute = AnsibleRun(self, 'Shell', ["ping", "-t", "1", "127.0.0.1"])
        #ansible_run.connect(ansible_execute)
        
        data = {'post_assign':{'name':'Test','value':'TestValues'}}
        # MultiInstance对当前任务进行拆分，1：要创建的任务数
        multi_inst = MultiInstance(self,'ansible_exec',1)

        self.start.connect(multi_inst)

        #AnsibleRun为任务规范，引用工作流规范，给定任务规范名称
        ansible_run = AnsibleRun(self, 'Ping','yes')
        ansible_execute = AnsibleRun(self, 'Shell', "no")

        # TaskSpec，将给定对任务作为输出任务添加
        multi_inst.connect(ansible_run)
        multi_inst.connect(ansible_execute)

        # 同步之前分割对任务，使用MultiInstance多实例模式时，join可以跨所有实例工作，在使用ThreadSplit时join将忽略来自另一个线程的实例。
        synch_1 = Join(self, 'synch_1')
        #self.start.connect(synch_1)

        
        ansible_run.connect(synch_1)
        ansible_execute.connect(synch_1)
        
        #gate_test = Gate(self,'gate1','synch_1')
        #synch_1.connect(gate_test)

        # 实现具有一个或多个输入，和任意数量输出的任务。
        # 如果连接了多个输入，则任务执行隐式多重合并。
        # 如果连接了多个输出，则任务执行隐式并行分割。
        end = Simple(self, 'End')
        end2 = Simple(self,'End2')

        # 表示一个if条件，其中多个条件可能同时匹配，从而创建多个传出分支。此任务有一个或多个输入，以及一个或多个传入分支。
        multichoice = MultiChoice(self, 'multi_choice_1')
        
        synch_1.connect(multichoice)
        cond = Equal(Attrib('Result'), 'yes')
        multichoice.connect_if(cond,end)
        cond = Equal(Attrib('Result'), 'no')
        multichoice.connect_if(cond,end2)
        #gate_test.connect(end)
        #synch_1.connect(end)
        #synch_1.connect(multi_inst)
    
        #end = Simple(self, 'End')
        #ansible_execute.connect(end)
        # As soon as all tasks are either "completed" or  "aborted", the
        # workflow implicitely ends.
