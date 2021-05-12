from tkinter import messagebox

import win32com.client

SAP_GUI_APPLICATION = "SAPGUI"
SAP_LOGON = "SAP Logon"

GUI_MAIN_WINDOW = "wnd[0]"
GUI_CHILD_WINDOW1 = "wnd[1]"
GUI_CHILD_WINDOW2 = "wnd[2]"

GUI_MAIN_USER_AREA = "wnd[0]/usr"
GUI_CHILD_USER_AREA1 = "wnd[1]/usr"
GUI_CHILD_USER_AREA2 = "wnd[2]/usr"


class SAPGuiApplication:

    @staticmethod
    def get_connection():
        try:
            session = SAPGuiApplication.connect()
            return session
        except RuntimeError:
            messagebox.showerror("Erro", "O sistema não conseguir conectar ao SAP!\nVerifique se está logado!")
            return None

    @staticmethod
    def connect():
        appl = SAPGuiApplication.__get_object()
        if appl:
            engine = SAPGuiApplication.__get_script_engine(appl)
            if engine:
                conn = SAPGuiApplication.__get_connection(engine)
                if conn:

                    return SAPGuiApplication.__get_session(conn)

    @staticmethod
    def __get_connection(sap_gui):
        try:
            conn = sap_gui.Children(0)
            if isinstance(conn, win32com.client.CDispatch):
                return conn
        except Exception as error:
            hr, msg, exc, arg = error.args
            msg = "Application {0} not running.".format(SAP_LOGON)
            msg += "COM: {0} ({1})".format(msg, hr)
            raise RuntimeError(msg)

    @staticmethod
    def __get_session(conn):
        try:
            session = conn.Children(0)
            if isinstance(session, win32com.client.CDispatch):
                return session
        except Exception as error:
            hr, msg, exc, arg = error.args
            msg = "Application {0} not running.".format(SAP_LOGON)
            msg += "COM: {0} ({1})".format(msg, hr)
            raise RuntimeError(msg)

    @staticmethod
    def __get_script_engine(sap_gui):
        try:
            sap_application = sap_gui.GetScriptingEngine
            if isinstance(sap_application, win32com.client.CDispatch):
                return sap_application
        except Exception as error:
            hr, msg, exc, arg = error.args
            msg = "Application {0} not running.".format(SAP_LOGON)
            msg += "COM: {0} ({1})".format(msg, hr)
            raise RuntimeError(msg)

    @staticmethod
    def __get_object():
        try:
            sap_gui = win32com.client.GetObject(SAP_GUI_APPLICATION)
            if isinstance(sap_gui, win32com.client.CDispatch):
                return sap_gui
        except Exception as error:
            hr, msg, exc, arg = error.args
            msg = "Application {0} not running.".format(SAP_LOGON)
            msg += "COM: {0} ({1})".format(msg, hr)
            raise RuntimeError(msg)



