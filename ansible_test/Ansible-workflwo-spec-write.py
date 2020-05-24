import json
from ansibletest import AnsibleWorkflowSpec
from ansibleserializer import AnsibleSerializer

serializer = AnsibleSerializer()
spec = AnsibleWorkflowSpec()
data = spec.serialize(serializer)

# This next line is unnecessary in practice; it just makes the JSON pretty.
pretty = json.dumps(json.loads(data), indent=4, separators=(',', ': '))

open('ansible-workflow-spec.json', 'w').write(pretty)
