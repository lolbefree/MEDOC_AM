import datetime
import decimal
from datetime import date
import start_with_xml
import pyodbc
import sql_querys
import not_for_git
from int_to_char import num2text, decimal2text
import sys
import os


class Docs:
    def __init__(self, entry_id, type_doc):
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
        self.entry_id = list(self.cursor.execute(sql_querys.get_grecno(entry_id)))[0][0] \
            if type_doc == 'act' else entry_id if type_doc == "vn" else ""
        self.type_doc = type_doc

        self.str_to_save = start_with_xml.check_doc(self.type_doc, self.today)
        self.get_header_and_bottom()

    def add_row_to_xml(self, key, val):
        self.str_to_save += f"""\t\t<ROW LINE="0" TAB="0" NAME="{key}">
          <VALUE>{val}</VALUE>\n
           </ROW>\n"""

    def get_header_and_bottom(self):
        query = (eval(f"sql_querys.{self.type_doc}_header_and_bottom({self.entry_id})"))
        lst = list(self.cursor.execute(query))
        desc = self.cursor.description

        column_names = [col[0] for col in desc]
        for key, val in zip(column_names, lst[0]):
            if isinstance(val, datetime.datetime):
                val = val.strftime("%d.%m.%Y")
            self.add_row_to_xml(key, val if val else "")

        if self.type_doc == "act":
            self.get_act_bonus()
        elif self.type_doc == "vn":
            self.get_central_table()
        elif self.type_doc == "rahz":
            self.get_central_table()
        elif self.type_doc == "raht":
            self.get_act_bonus()

    def get_act_bonus(self):
        res = self.cursor.execute(sql_querys.act_bonus(self.entry_id))
        for row in list(res):
            self.add_row_to_xml(row[0], self.two_char_after_dot(row[1]) if row[1] else "")
        self.get_central_table()

    def get_central_table(self):
        if self.type_doc == "act":
            filed9 = [note for note in list(self.cursor.execute(f"""select 	row_number() over (order by rno) as TAB1_F1,
             note as FIELD9	from grows01 where grecno={self.entry_id}""")) if note[1]]
            self.str_to_save += f"""\t\t<ROW LINE="0" TAB="0" NAME="FIELD9">
              <VALUE>{filed9[0][1] if len(filed9) > 0 else ""}</VALUE>
            </ROW>\n"""
        res = list(self.cursor.execute(eval(f"sql_querys.{self.type_doc}_rows({self.entry_id})")))

        desc = self.cursor.description
        column_names = [col[0] for col in desc]
        range_res = len(column_names)
        index_ = 0
        for num, item in enumerate(res):
            for i in range(range_res):
                self.str_to_save += f"""\t\t<ROW LINE="{num}" TAB="1" NAME="{column_names[i]}">
                   <VALUE>{self.two_char_after_dot(res[index_][i]) if isinstance(res[index_][i], decimal.Decimal) 
                else "" if res[index_][i] is None else res[index_][i]}</VALUE></ROW>\n"""

            index_ += 1

        self.get_sum()

    def get_sum(self):
        res = list(self.cursor.execute(eval(f"sql_querys.{self.type_doc}_sum({self.entry_id})")))

        doc_sum_text = ""
        for row in res:
            self.add_row_to_xml(row[0], '' if row[1] is None else self.two_char_after_dot(row[1]))
            if "DOCSUM" in row[0]:
                doc_sum_text = float(self.two_char_after_dot(row[1]))

        self.add_row_to_xml("DOCSUM_TEXT", doc_sum_text)
        self.str_to_save += """\t\t</DOCUMENT>
      <DOCKVT />
    </CARD>
  </ORG>
</ZVIT>
        """
        if self.type_doc == "act":
            client = list(self.cursor.execute(sql_querys.get_custname_from_GBILS(self.entry_id)))[0][0]
        elif self.type_doc == "vn":
            client = list(self.cursor.execute(sql_querys.get_custname_from_sBILS(self.entry_id)))[0][0]

        client = ''.join(e for e in client if e.isalnum() or e == ' ')
        path_to_save = f'//Fileserver//бухгалтерія/edoc/{client}/'
        if not os.path.isdir(path_to_save):
            os.mkdir(path_to_save)

        with open(f"{path_to_save}{self.type_doc}_{self.entry_id}.xml", "w") as file:
            file.write(self.str_to_save)


if __name__ == '__main__':
    # m = Docs(3, "act")
    m = Docs(sys.argv[1], sys.argv[2])

    # vn 111021393
    # act 121071808
    # raht  123047263
    # rahz 113005595
