from SpiffWorkflow.serializer.json import JSONSerializer
from ansibletest import AnsibleWorkflowSpec
from Ansibleexecute import AnsibleRun

class AnsibleSerializer(JSONSerializer):
    # 在使用JSON指定工作流之前，我们首先需要教SpiffWorkflow我们自定义的NuclearChoice在JSON中的外观
    def serialize_ansible_run(self, task_spec):
        s_state = self.serialize_task_spec(task_spec)
        s_state['args'] = task_spec.args
        return s_state

    def deserialize_ansible_run(self, wf_spec, s_state):
        spec = AnsibleRun(wf_spec, s_state['name'],s_state['args'])
        self.deserialize_task_spec(wf_spec, s_state, spec=spec)
        return spec
