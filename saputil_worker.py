from win32com import client

class Worker():
    def __init__(self, action=None, tcode=None, report=None, workload=None):
        self.pri_session = None
        self.session = None
        self.action = action
        self.tcode = tcode
        self.report = report
        self.workload = workload

    def do_work(self):
        self.pri_session = client.GetObject("SAPGUI").GetScriptingEngine.Children(0)
        self.create_sessions()
        if self.action == 'query':
            self.submit_query()
        elif self.action == 'download':
            self.download_spools()
        elif self.action == 'clear':
            self.clear_spools()
        self.close_session()
        return True

    def create_sessions(self):
        num_sess = len(self.pri_session.Children)
        self.pri_session.Children(0).createSession()
        sess = None
        while type(sess) != client.CDispatch:
            try:
                sess = self.pri_session.Children(num_sess)
            except:
                pass
        self.session = sess

    def close_session(self):
        self.session.findById("wnd[0]").close()

    def submit_query(self):
        self.goto_tcode()
        self.goto_report()
        self.submit_report()

    def goto_tcode(self):
        self.session.findById("wnd[0]/tbar[0]/okcd").text = self.tcode
        self.session.findById("wnd[0]").sendVKey(0)

    def goto_report(self):
        self.session.findById("wnd[0]/usr/ctxtRS38R-QNUM").text = self.report
        self.session.findById("wnd[0]/usr/btnP1").press()

    def submit_report(self):
        # for static fields
        for i in self.workload[0].values():
            for j in i.values():
                self.session.findById(j['field_id']).text = j['value']

        # for variables fields
        for w in self.workload[1]:
            for k, v in w.items():
                self.session.findById(k).text = v

            try:
                self.session.findById("wnd[1]/usr/txtRS38R-DBACC").text = "999999"
                self.session.findById("wnd[1]/tbar[0]/btn[0]").press()
            except:
                pass

            self.session.findById("wnd[0]").sendVKey(9)
            self.session.findById("wnd[1]/tbar[0]/btn[13]").press()
            self.session.findById("wnd[1]/usr/btnSOFORT_PUSH").press()
            self.session.findById("wnd[1]/tbar[0]/btn[11]").press()

    def download_spools(self):
        pass

    def clear_spools(self):
        pass
