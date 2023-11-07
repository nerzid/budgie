from functools import partial
from typing import List


class ActionObj:
    def __init__(self, op_seq: List[partial]):
        self.op_seq = op_seq

    def execute(self):
        for op in self.op_seq:
            op()
