from SpiffWorkflow.specs import WorkflowSpec
from SpiffWorkflow import Task,Workflow
#from SpiffWorkflow.serializer.json import JSONSerializer
from ansibleserializer import AnsibleSerializer
import time
with open('ansible-workflow-spec.json') as fp:
    workflow_json = fp.read()
serializer = AnsibleSerializer()

spec = WorkflowSpec.deserialize(serializer, workflow_json)

# Create the workflow.
workflow = Workflow(spec)
# Execute until all tasks are done or require manual intervention.
# For the sake of this tutorial, we ignore the "manual" flag on the
# tasks. In practice, you probably don't want to do that.

for i in range(20):
            print(i)
            workflow.complete_all(False)
            if workflow.is_completed():
                break
            time.sleep(0.5)


#workflow.complete_all(halt_on_manual=False)
#workflow.complete_next()
#tasks = workflow.get_tasks(Task.WAITING)
#for t in tasks:
#    print(t.get_name())
#    t.complete()
#time.sleep(10)
# 类似get_dump（返回当前内部任务树的完整转储以进行调试），但是将输出打印到终端，而不是返回输出
workflow.dump()
# get_tasks_from_spec_name：返回其规范具有给定名称的所有任务。
# get_data：返回具有给定名称的数据字段的值，如果数据字段不存在，则返回给定的默认值。
print(workflow.get_tasks_from_spec_name('synch_1')[0].get_data('Result'))
print(workflow.get_tasks_from_spec_name('synch_1')[1].get_data('Result'))
print(workflow.get_tasks_from_spec_name('multi_choice_1')[0].get_data('result'))
print(workflow.get_tasks_from_spec_name('End')[0].get_data('Result'))

print(workflow.get_tasks_from_spec_name('Ping')[0].get_data('result'))
# print(workflow.get_tasks_from_spec_name('Ping')[0].results)
