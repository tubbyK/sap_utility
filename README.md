Automate SAP GUI submission of reports.

[Overview]
I frequently need to run reports in SAP SQVI that result in large datasets (relative to SAP that is). However, downloading a large data is exponentially slow and prone to interrupts. The solution is to breakdown a single report into multiple small ones.

This tool takes a parameters of a report, automatically generates a list of smaller report parameterse and run them in parallel. For exapmle, it takes a report that needs to start/end over 10 years will be broken down to monthly interval resulting in 240 mini reports instead of 1 big report. See my other tool SAP_Spool2CSV to automatically merge spool files to csv.

Side note, don't think running in parallel does anything for SAP as it is either single threaded or slows down when multiple sessions are opened. This is purely an exercise of doing instantiation in multiprocessing.

[Example of Use]
from sap_utility import *
s = SAP_Util()
s.read_query()
s.set_plan('Example')
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
