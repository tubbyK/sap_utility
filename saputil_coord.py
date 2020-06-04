import yaml
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import itertools

class Coord():
    def __init__(self, query, num_sessions):
        self.query = query
        self.num_sessions = num_sessions
        self.var_ids = self.get_var_ids()
        self.var_values = self.get_var_values()
        self.work_list = self.flatten()
        self.var_payload = self.generate_var_payload()
        self.workload = self.allocate_workload()

    def allocate_workload(self):
        # divide work by num_sessions
        splits = int((len(self.var_payload) / self.num_sessions) + 1)
        workload = [self.var_payload[x:x + splits] for x in range(0, len(self.var_payload), splits)]
        return workload

    def generate_var_payload(self):
        var_payload = []
        for wl in self.work_list:
            w = dict(zip(self.var_ids, wl))
            var_payload.append(w)
        return var_payload

    def flatten(self):
        result = []
        interim = [i for i in itertools.product(*self.var_values)]
        for li in interim:
            result.append([i for i in itertools.chain(*li)])
        return result

    def get_var_ids(self):
        result = []
        for v in self.query['variable_fields'].values():
            result.append(v['id_lower'])
            result.append(v['id_higher'])
        return result

    def get_var_values(self):
        result = []
        for v in self.query['variable_fields'].values():
            li, li_low, li_high = [], [], []
            start, end = v['start'], v['end']
            partition_on = v['partition_on']
            if v['type'] == 'date':
                end = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
                li = self.generate_date_list(start, end)
            elif v['type'] == 'int':
                li_low = [i for i in range(start,end,partition_on)]
                li_high = [i for i in range(start+partition_on, end+partition_on, partition_on)]
                li = [[i,j] for i, j in zip(li_low, li_high)]
            elif v['type'] == 'list':
                li_low = v['type']
                li_high = ['']*len(li_low)
                li = [[i, j] for i, j in zip(li_low, li_high)]
            result.append(li)
        return result

    def generate_date_list(self, start, end):
        result_low, result_high = [], []
        start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in [start,end]]
        tot = lambda dt: dt.month+12 * dt.year
        for t in range(tot(start)-1, tot(end)):
            y, m = divmod(t, 12)
            d_low = datetime(y, m+1, 1)
            result_low.append(d_low.strftime("%Y-%m-%d"))
            d_high = d_low + relativedelta(months=1) - timedelta(days=1)
            result_high.append(d_high.strftime("%Y-%m-%d"))
            result = [[i,j] for i, j in zip(result_low, result_high)]
        return result

if __name__ == '__main__':
    S = Coord()