from datetime import date

import pyodbc
import not_for_git


class Docs:
    def __init__(self):
        self.today = date.today().strftime("%d.%m.%Y")
        self.two_char_after_dot = lambda x: "%.2f" % x if x % 1 != 0 else int(x)
        self.server = not_for_git.db_server
        self.database = not_for_git.db_name
        self.username = not_for_git.db_user
        self.password = not_for_git.db_pw
        self.driver = '{SQL Server}'  # Driver you need to connect to the database
        self.numpad_mod = ""
        self.cnn = pyodbc.connect(
            'DRIVER=' + self.driver + ';PORT=port;SERVER=' + self.server + ';PORT=1443;DATABASE=' + self.database +
            ';UID=' + self.username +
            ';PWD=' + self.password)
        self.cursor = self.cnn.cursor()

    def get_data(self):
        res = list(self.cursor.execute("dbo.vehicleready"))
        for i in res:
            print(i)


m = Docs()
m.get_data()
