import psutil
import configparser
from win32com import client

class Bootstrap():
    def __init__(self):
        self.pid, self.sapgui, self.connection, self.pri_session = None, None, None, None
        self.proc_name, self.proc_path, self.connection_name = None, None, None
        self.load_config()
        self.close_proc()
        self.start_proc()
        self.start_client()
        self.start_connection()
        self.start_pri_session()

    def load_config(self):
        parser = configparser.ConfigParser()
        parser.read('config.ini')
        cfg = parser[parser.sections()[0]]
        self.proc_name = cfg['proc_name']
        self.proc_path = cfg['path']
        self.connection_name = cfg['connection_name']

    def close_proc(self):
        pid = [proc.pid for proc in psutil.process_iter() if proc.name() == self.proc_name]
        for p in pid: psutil.Process(p).terminate()

    # run SAP GUI program
    def start_proc(self):
        p = psutil.Popen(self.proc_path)
        self.pid = p.pid

    def start_client(self):
        while type(self.sapgui) != client.CDispatch:
            try:
                self.sapgui = client.GetObject('SAPGUI')
            except:
                pass

    def start_connection(self):
        while type(self.connection) != client.CDispatch:
            try:
                self.connection = self.sapgui.GetScriptingEngine.OpenConnection(self.connection_name, True)
                return
            except:
                pass

    def start_pri_session(self):
        self.pri_session = client.GetObject("SAPGUI").GetScriptingEngine.Children(0)

if __name__ == '__main__':
    B = Bootstrap()