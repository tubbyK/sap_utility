from saputil_bootstrap import *
from saputil_coord import *
from saputil_worker import *
from multiprocessing import Process
import yaml
import time


def unwrap_(action, tcode, report, workload):
    w = Worker(action, tcode, report, workload)
    w.do_work()

class SAP_Util():
    def __init__(self, max_session=None, query_file=None):
        self.max_sessions = 6 if max_session is None else max_session
        self.query_file = 'query.yml' if query_file is None else query_file
        self.sap = Bootstrap()
        self.query = None
        self.plan = None
        self.sessions = None
        self.workers = None

    def read_query(self):
        with open(self.query_file, 'r') as f:
            query = yaml.full_load(f)
        self.query = query

    def set_plan(self, report):
        self.plan = Coord(self.query[report], self.max_sessions-1)


if __name__ == '__main__':
    s = SAP_Util()
    s.read_query()
    s.set_plan('PO_MONITORING')
    procs = []
    action = 'query'
    tcode = s.plan.query['t_code']
    report = s.plan.query['query_name']
    for w in s.plan.workload:
        workload = [s.plan.query['static_fields'], w]
        p = Process(target=unwrap_, args=(action, tcode, report, workload))
        p.start()
        procs.append(p)
        time.sleep(5)
    [p.join() for p in procs]
    print('done')