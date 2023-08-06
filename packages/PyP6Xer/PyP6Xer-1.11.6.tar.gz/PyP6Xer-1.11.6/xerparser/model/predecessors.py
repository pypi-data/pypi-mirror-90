from xerparser.model.classes.taskpred import TaskPred

class Predecessors:
    task_pred = []
    def __init__(self):
        self.index=0

    def find_by_id(self, code_id):
        obj = list(filter(lambda x: x.task_pred_id == code_id, self.task_pred))
        if len(obj) > 0:
            obj[0]
        else:
            obj = None
        return obj

    def add(self, params):
        pred = TaskPred(params)
        self.task_pred.append(pred)

    @property
    def relations(self):
        return self.task_pred

    @property
    def leads(self):
        return list(filter(lambda x: x.lag_hr_cnt < 0 if x.lag_hr_cnt else None, self.task_pred))

    @property
    def finish_to_start(self):
        return list(filter(lambda x: x.pred_type == 'PR_FS', self.task_pred))
    @staticmethod
    def get_successors(act_id):
        succ = list(filter(lambda x: x.pred_task_id == act_id, Predecessors.task_pred))
        return succ

    @staticmethod
    def get_predecessors(act_id):
        succ = list(filter(lambda x: x.task_id == act_id, Predecessors.task_pred))
        return succ

    @staticmethod
    def count():
        return len(Predecessors.task_pred)

    def __len__(self):
        return len(self.task_pred)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.task_pred):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self.task_pred[idx]

