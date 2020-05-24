# -*- coding: utf-8 -*-
from __future__ import division
from SpiffWorkflow.specs.base import TaskSpec
from SpiffWorkflow.task import Task
class AnsibleRun(TaskSpec):
    # 序列化和反序列化

    """
    This class executes an external process, goes into WAITING until the
    process is complete, and returns the results of the execution.
    """
    def __init__(self, wf_spec, name, args=None, **kwargs):
        """
        Constructor.

        :type  wf_spec: WorkflowSpec
        :param wf_spec: A reference to the workflow specification.
        :type  name: str
        :param name: The name of the task spec.
        :type  args: list
        :param args: args to pass to process (first arg is the command).
        :type  kwargs: dict
        :param kwargs: kwargs to pass-through to TaskSpec initializer.
        """

        assert wf_spec is not None
        assert name is not None
        TaskSpec.__init__(self, wf_spec, name, **kwargs)
        print(name)
        self.args = args
        print(kwargs.get('pre_assign',  []))


    def _start(self, my_task, force=False):
        """Returns False when successfully fired, True otherwise"""
        result = "Ansible run well!!!"
        data = {'result': result,'Result': self.args}
        my_task.set_data(**data)
        my_task.results = data
        return True

    def _update_hook(self, my_task):
        if not self._start(my_task):
            my_task.state = Task.WAITING
            return
        super(AnsibleRun, self)._update_hook(my_task)

    def serialize(self, serializer):
        return serializer.serialize_ansible_run(self)


    @classmethod
    def deserialize(self, serializer, wf_spec, s_state):
        spec = serializer.deserialize_ansible_run(wf_spec, s_state)
        return spec
