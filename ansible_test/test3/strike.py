#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2020/5/10 10:44 下午
# @file : strike.py
# @software : PyCharm

from SpiffWorkflow.specs import Simple


class NuclearStrike(Simple):
    def _on_complete_hook(self, my_task):
        print("Rocket sent!")
