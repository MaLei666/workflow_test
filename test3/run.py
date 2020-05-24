import json
from SpiffWorkflow import Task,Workflow
from SpiffWorkflow.specs import WorkflowSpec

from SpiffWorkflow.serializer.json import JSONSerializer
from test3.strike import NuclearStrike

class NuclearSerializer(JSONSerializer):
    def serialize_nuclear_strike(self, task_spec):
        return self.serialize_task_spec(task_spec)

    def deserialize_nuclear_strike(self, wf_spec, s_state):
        spec = NuclearStrike(wf_spec, s_state['name'])
        self.deserialize_task_spec(wf_spec, s_state, spec=spec)
        return spec

# Load from JSON
with open('nuclear.json') as fp:
    workflow_json = fp.read()
serializer = NuclearSerializer()
spec = WorkflowSpec.deserialize(serializer, workflow_json)

vartest = {'vartest':'hello vartest!'}

# Create the workflow.
workflow = Workflow(spec)
# Execute until all tasks are done or require manual intervention.
# For the sake of this tutorial, we ignore the "manual" flag on the
# tasks. In practice, you probably don't want to do that.

#workflow.complete_all(halt_on_manual=False)
workflow.dump()

#workflow.get_dump()
#workflow.complete_next(halt_on_manual=False)
#workflow.get_dump()
workflow.complete_next()

condition_keys = []
tasks = workflow.get_tasks(Task.READY)
for t in tasks:
    print(t.get_name())

user_selct = {'confirmation':'yes'}
task_data_dict = user_selct.copy()

for t in tasks:
    print("Ready:",t.task_spec.name)
    if hasattr(t.task_spec,"cond_task_specs"):
        for cond,name in t.task_spec.cond_task_specs:
            for cond_unit in cond.args:
                print("cond_unit",cond_unit)
                if hasattr(cond_unit,"name"):
                    condition_keys.append(cond_unit.name)

        
for t in tasks:
    t.set_data(**task_data_dict)
    t.complete()

print(condition_keys)
print(task_data_dict)
workflow.complete_next()
workflow.dump()


# 执行到一半保存
data = workflow.serialize(serializer)

pretty = json.dumps(json.loads(data), indent=4, separators=(',', ': '))

open('workflow-test.json', 'w').write(pretty)




tasks = workflow.get_tasks(Task.READY)
for t in tasks:
    print(t.get_name())

user_selct = {'confirmation':'yes'}
task_data_dict = user_selct.copy()

for t in tasks:
    print("Ready:",t.task_spec.name)
    if hasattr(t.task_spec,"cond_task_specs"):
        for cond,name in t.task_spec.cond_task_specs:
            for cond_unit in cond.args:
                print("cond_unit",cond_unit)
                if hasattr(cond_unit,"name"):
                    condition_keys.append(cond_unit.name)

        
for t in tasks:
    t.set_data(**task_data_dict)
    t.complete()
print(condition_keys)
print(task_data_dict)
workflow.get_tasks_from_spec_name('nuclear_strike')[0].set_data(**vartest)
workflow.complete_next()
print("NAME:",workflow.get_tasks_from_spec_name('nuclear_strike')[0].get_data('name'))
workflow.dump()

data = workflow.serialize(serializer)

pretty = json.dumps(json.loads(data), indent=4, separators=(',', ': '))

open('workflow-test-complete.json', 'w').write(pretty)


