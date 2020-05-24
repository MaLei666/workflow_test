import json
import shutil
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from ansible import context
import ansible.constants as C
# import logging
# logging.basicConfig(filename='ansible.log',               #通过logging.basicConfig函数对日志的输出格式及方式做相关配置
#                     format='%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s',datefmt='%Y-%m-%d %H:%M:%S %p',
#                     level=10)

class ResultCallback(CallbackBase):
    """
    重写callbackBase类的部分方法
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}
        self.task_ok = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, **kwargs):
        self.host_failed[result._host.get_name()] = result


class AnsibleHepler(object):
    def __init__(self,
                 connection='smart',  # 连接方式 local 本地方式，smart ssh方式
                 remote_user=None,  # 远程用户
                 ack_pass=None,  # 提示输入密码
                 sudo=None, sudo_user=None, ask_sudo_pass=None,
                 module_path=None,  # 模块路径，可以指定一个自定义模块的路径
                 become=None,  # 是否提权
                 become_method=None,  # 提权方式 默认 sudo 可以是 su
                 become_user=None,  # 提权后，要成为的用户，并非登录用户
                 check=False, diff=False,
                 listhosts=None, listtasks=None, listtags=None,
                 verbosity=3,
                 syntax=None,
                 start_at_task=None,
                 inventory=None):

        # 函数文档注释
        """
        初始化函数，定义的默认的选项值，
        在初始化的时候可以传参，以便覆盖默认选项的值
        """
        context.CLIARGS = ImmutableDict(
            connection=connection,
            remote_user=remote_user,
            ack_pass=ack_pass,
            sudo=sudo,
            sudo_user=sudo_user,
            ask_sudo_pass=ask_sudo_pass,
            module_path=module_path,
            become=become,
            become_method=become_method,
            become_user=become_user,
            verbosity=verbosity,
            listhosts=listhosts,
            listtasks=listtasks,
            listtags=listtags,
            syntax=syntax,
            start_at_task=start_at_task,
        )

        # 三元表达式，假如没有传递 inventory, 就使用 "localhost,"
        # 确定 inventory 文件
        self.inventory = inventory if inventory else "localhost,"

        # 实例化数据解析器
        self.loader = DataLoader()

        # 实例化 资产配置对象
        self.inv_obj = InventoryManager(loader=self.loader, sources=self.inventory)

        # 设置密码，可以为空字典，但必须有此参数
        self.passwords = {}

        # 实例化回调插件对象
        self.results_callback = ResultCallback()

        # 变量管理器
        self.variable_manager = VariableManager(self.loader, self.inv_obj)

        #结果集
        self.results_raw = {}

    def run(self, host_list=['localhost'], gether_facts="no", module="ping", args='',username='prouser',password='S3userPW0'):
        for host in host_list:
            self.inv_obj.add_host(host)
        self.variable_manager.extra_vars['ansible_ssh_user'] = username
        self.variable_manager.extra_vars['ansible_ssh_pass'] = password
        # self.variable_manager.set_inventory()
        #{'ansible_ssh_user': username, 'ansible_ssh_pass': password}
        # print(self.variable_manager.extra_vars)
        play_source = dict(
            name="Ad-hoc",
            hosts=host_list,
            gather_facts=gether_facts,
            tasks=[
                # 这里每个 task 就是这个列表中的一个元素，格式是嵌套的字典
                # 也可以作为参数传递过来，这里就简单化了。
                {"action": {"module": module, "args": args}},
            ])
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inv_obj,
                variable_manager=self.variable_manager,
                loader=self.loader,
                passwords=self.passwords,
                stdout_callback=self.results_callback)
            C.HOST_KEY_CHECKING = False  # 关闭第一次使用ansible连接客户端是输入命令
            result = tqm.run(play)

        finally:
            if tqm is not None:
                tqm.cleanup()
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    def run_playbook(self, playbooks, host_list=['localhost'],subset='all',extra_vars={},username='vagrant',password='vagrant'):
        self.inv_obj._inventory.remove_group(subset)
        self.inv_obj.add_group(subset)
        for host in host_list:
            self.inv_obj.add_host(host,group=subset)
        print(self.inv_obj.get_groups_dict())
        # print(self.variable_manager.get_vars())
        print(self.inv_obj.hosts)
        # host_list_str = ','.join([item for item in hosts])
        # self.variable_manager.extra_vars['host_list'] = host_list_str
        # self.variable_manager.extra_vars['host'] = hosts
        self.variable_manager.extra_vars['ansible_ssh_user'] = username
        self.variable_manager.extra_vars['ansible_ssh_pass'] = password
        for k, v in extra_vars.items():
            self.variable_manager.extra_vars[k] = v

        playbook = PlaybookExecutor(playbooks=playbooks,  # 注意这里是一个列表
                                    inventory=self.inv_obj,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader,
                                    passwords=self.passwords)

        # 使用回调函数
        playbook._tqm._stdout_callback = self.results_callback
        C.HOST_KEY_CHECKING = False  # 关闭第一次使用ansible连接客户端是输入命令
        result = playbook.run()
        return result

    def get_result(self):
        result_raw = {'success': {}, 'failed': {}, 'unreachable': {}}

        # print(self.results_callback.host_ok)
        for host, result in self.results_callback.host_ok.items():
            result_raw['success'][host] = result._result
        for host, result in self.results_callback.host_failed.items():
            result_raw['failed'][host] = result._result
        for host, result in self.results_callback.host_unreachable.items():
            result_raw['unreachable'][host] = result._result

        # 最终打印结果，并且使用 JSON 继续格式化
        print("Ansible执行结果集:%s" % json.dumps(result_raw, indent=4))
        return self.results_raw

# ansible2 = AnsibleHepler()
# ansible2.run(['172.16.120.109'],module='shell',args='df -h')
# ansible2.run(['172.16.120.110'],module='shell',args='df -h')
# ansible2.get_result()
# ansible2 = AnsibleHepler()
# test = { 'ansible_ssh_user': 'root', 'ansible_ssh_pass': 'test'}
# ansible2.run_playbook(['/vagrant/test.yml'],host_list=['172.16.120.109','172.16.120.108'])
# ansible2.get_result()

#
# a=AnsibleHepler(inventory='/home/workflow_test/hosts')
# a.run_playbook(["test.yml"],username='root',password='Malei666')
# # a.run(['localhost'],module='shell',args='df -h',username='root',password='Malei666')
# a.get_result()