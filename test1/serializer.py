#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2020/4/20 10:38 下午
# @file : serializer.py
# @software : PyCharm

from SpiffWorkflow.serializer.json import JSONSerializer
from strick import Nuclear

class NuclearSerializer(JSONSerializer):
    def serialize_nuclear_strike(self,task_spec):
        return self.serialize_task_spec(task_spec)

    def deserialize_nuclear_strike(self,wf_spec,s_state):
        spec=Nuclear(wf_spec,s_state['name'])
        self.deserialize_task_spec(wf_spec,s_state,spec)
        return spec
