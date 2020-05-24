from SpiffWorkflow.serializer.json import JSONSerializer
from workflowexecute import taskSpec

class workflowSerializer(JSONSerializer):
    # 在使用JSON指定工作流之前，我们首先需要教SpiffWorkflow我们自定义的NuclearChoice在JSON中的外观

    # def playbookTask(self):
    #     # Todo 执行playbook需要的参数
    #     json_info={
    #         "host_list": [
    #             "localhost"
    #         ],
    #         "playbooks": ["test"],
    #         "password": "test",
    #         "username": "test"
    #     }
    #     return json_info


    def serialize_workflow_run(self, task_spec,node_type,file_path):
        task_spec.node_type = node_type
        # Todo 调用数据库查询对应节点的文件地址,目前给定默认值
        task_spec.file_path = file_path
        # if node_type == 'playbook':
        #     task_spec.parameters = self.playbookTask()
        s_state = self.serialize_task_spec(task_spec)
        s_state['args'] = task_spec.args
        s_state['file_path'] = task_spec.file_path
        s_state['node_type']=task_spec.node_type
        # s_state['parameters']=task_spec.parameters
        return s_state

    def deserialize_workflow_run(self, wf_spec, s_state):
        spec = taskSpec(wf_spec=wf_spec,
                        name=s_state['name'],
                        args=s_state['args'],
                        file_path=s_state['file_path'],
                        # parameters=s_state['parameters'],
                        node_type=s_state['node_type'])
        self.deserialize_task_spec(wf_spec, s_state, spec=spec)
        return spec
