# -*- coding: utf-8 -*-
from __future__ import division
from SpiffWorkflow.specs.base import TaskSpec
from SpiffWorkflow.task import Task

class taskSpec(TaskSpec):
    # 序列化和反序列化

    """
    This class executes an external process, goes into WAITING until the
    process is complete, and returns the results of the execution.
    """
    def __init__(self, wf_spec, name,node_type,file_path,args=None,**kwargs):
        """
        Constructor.

        :type  wf_spec: WorkflowSpec
        :param wf_spec: A reference to the workflow specification.
        :type  name: str
        :param name: The name of the task spec.
        :type  args: list
        :param args: args to pass to process (first arg is the file_path).
        :type  kwargs: dict
        :param kwargs: kwargs to pass-through to TaskSpec initializer.
        """

        assert wf_spec is not None
        assert name is not None

        TaskSpec.__init__(self, wf_spec, name, **kwargs)
        self.node_type=node_type
        self.file_path = file_path
        # self.parameters = kwargs.get('parameters',  [])
        self.args = args

        # print(name)
        # print(kwargs.get('pre_assign',  []))
        # print(self.file_path)

    def _start(self, my_task, force=False):
        """Returns False when successfully fired, True otherwise"""
        result = "workflow run well!!!"
        # my_task=my_task.parent
        data = {'result': result,'Result': self.args}
        my_task.set_data(**data)
        my_task.results = data
        # if hasattr(my_task.task_spec, "file_path"):
        #     re_msg = self.execTask(my_task)
        #     print(re_msg)
        return True


    def _update_hook(self, my_task):
        if not self._start(my_task):
            my_task.state = Task.WAITING
            return
        super(taskSpec, self)._update_hook(my_task)

    def serialize(self, serializer):
        return serializer.serialize_workflow_run(self,self.node_type,self.file_path)

    @classmethod
    def deserialize(self, serializer, wf_spec, s_state):
        spec = serializer.deserialize_workflow_run(wf_spec, s_state)
        return spec
