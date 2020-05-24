#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2020/5/11 9:59 上午
# @file : workflow_engine.py
# @software : PyCharm

from SpiffWorkflow.workflow import Workflow
from SpiffWorkflow.task import Task
from ansible_util import AnsibleHepler

class workflowNew(Workflow):

    def __init__(self, workflow_spec, deserializing=False, **kwargs):
        super().__init__(workflow_spec)

    def execTask(self,task):
        try:
            keyList = locals()
            file_path = task.task_spec.file_path
            node_type = task.task_spec.node_type

            #todo ansible-playbook
            if node_type=='playbook':
                # parameters = task.task_spec.parameters
                # for key, value in parameters.items():
                #     keyList[key] = value
                autoAnsible = AnsibleHepler()
                results = autoAnsible.run_playbook(playbooks=['test.yml'])
                autoAnsible.get_result()
                return results
            else:
                pass
        except:
            return 100

    def complete_next(self, pick_up=True, halt_on_manual=True):
        blacklist = []
        if pick_up and self.last_task is not None:
            try:
                iter = Task.Iterator(self.last_task, Task.READY)
                task = next(iter)
            except:
                task = None
            self.last_task = None
            if task is not None:
                if not (halt_on_manual and task.task_spec.manual):
                    if hasattr(task.task_spec, "file_path"):
                        re_msg = self.execTask(task)
                        if re_msg==0:
                            if task.complete():
                                self.last_task = task
                                return True, task.task_spec.name
                        else:
                            return False
                    else:
                        if task.complete():
                            self.last_task = task
                            return True, task.task_spec.name
                blacklist.append(task)

        # Walk through all ready tasks.
        for task in Task.Iterator(self.task_tree, Task.READY):
            for blacklisted_task in blacklist:
                if task._is_descendant_of(blacklisted_task):
                    continue
            if not (halt_on_manual and task.task_spec.manual):
                if hasattr(task.task_spec, "file_path"):
                    re_msg = self.execTask(task)
                    if re_msg == 0:
                        if task.complete():
                            self.last_task = task
                            return True, task.task_spec.name
                    else:
                        return False
                else:
                    if task.complete():
                        self.last_task = task
                        return True,task.task_spec.name
            blacklist.append(task)

        # Walk through all waiting tasks.
        for task in Task.Iterator(self.task_tree, Task.WAITING):
            task.task_spec._update(task)
            if not task._has_state(Task.WAITING):
                self.last_task = task
                return True
        return False

    @classmethod
    def deserialize(cls, serializer, s_state, **kwargs):
        return serializer.deserialize_workflow(s_state, **kwargs)