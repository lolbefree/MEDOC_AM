import datetime
import decimal
from datetime import date
import start_with_xml
import pyodbc
import sql_querys
import not_for_git
from int_to_char import num2text, decimal2text


class Docs:
    def __init__(self, grecno, type_doc):
        self.today = date.today().strftime("%d.%m.%Y")
        self.two_char_after_dot = lambda x: "%.2f" % x if x % 1 != 0 else int(x)
        self.grecno = grecno
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
        self.type_doc = type_doc

        self.str_to_save = start_with_xml.check_doc(self.type_doc, self.today)
        self.get_header_and_bottom()

    def add_row_to_xml(self, key, val):
        # print(f"""\t\t<ROW LINE="0" TAB="0" NAME="{key}">
        #   <VALUE>{val}</VALUE>\n
        #    </ROW>\n""")
        self.str_to_save += f"""\t\t<ROW LINE="0" TAB="0" NAME="{key}">
          <VALUE>{val}</VALUE>\n
           </ROW>\n"""

    def get_header_and_bottom(self):
        query = (eval(f"sql_querys.{self.type_doc}_header_and_bottom({self.grecno})"))
        print(query)
        lst = list(self.cursor.execute(query))
        # print(lst)
        desc = self.cursor.description

        column_names = [col[0] for col in desc]
        # print(len(column_names), len(lst[0]))
        for key, val in zip(column_names, lst[0]):
            # print(key, val)
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
        res = self.cursor.execute(sql_querys.act_bonus(self.grecno))
        for row in list(res):
            self.add_row_to_xml(row[0], self.two_char_after_dot(row[1]) if row[1] else "")
        self.get_central_table()

    def get_central_table(self):
        if self.type_doc == "act":
            filed9 = list(self.cursor.execute(f"""select 	row_number() over (order by rno) as TAB1_F1,
             note as FIELD9	from grows01 where grecno={self.grecno}"""))
            self.str_to_save += f"""\t\t<ROW LINE="0" TAB="0" NAME="FIELD9">
              <VALUE>{filed9[0][1] if filed9[0][1] else ""}</VALUE>
            </ROW>\n"""
        # print(eval(f"sql_querys.{self.type_doc}_rows({self.grecno})"))
        res = self.cursor.execute(eval(f"sql_querys.{self.type_doc}_rows({self.grecno})"))
        res = list(res) if not self.type_doc == "act" else list(res)[1:]
        desc = self.cursor.description
        column_names = [col[0] for col in desc]
        # print(column_names)
        range_res = 7 if self.type_doc == 'rahz' or self.type_doc == 'raht' else 8
        index_ = 0
        for num, item in enumerate(res[1 if self.type_doc == 'act' else 0:]):
            for i in range(range_res):
                # print(i)
                # print(column_names[i],f"{self.two_char_after_dot(res[index_][i]) if isinstance(res[index_][i], decimal.Decimal) else res[index_][i]}")
                self.str_to_save += f"""\t\t<ROW LINE="{num}" TAB="1" NAME="{column_names[i]}">
                  <VALUE>{self.two_char_after_dot(res[index_][i]) if isinstance(res[index_][i], decimal.Decimal) else res[index_][i]}</VALUE></ROW>\n"""

            index_ += 1

        # print(self.str_to_save)
        self.get_sum()

    def get_sum(self):
        res = list(self.cursor.execute(eval(f"sql_querys.{self.type_doc}_sum({self.grecno})")))
        doc_sum_text = ""
        for row in res:
            self.add_row_to_xml(row[0], self.two_char_after_dot(row[1]))
            if "DOCSUM" in row[0]:
                doc_sum_text = float(self.two_char_after_dot(row[1]))

        self.add_row_to_xml("DOCSUM_TEXT", doc_sum_text)
        self.str_to_save += """\t\t</DOCUMENT>
      <DOCKVT />
    </CARD>
  </ORG>
</ZVIT>
        """
        # print(self.str_to_save)
        with open(self.today + f"{self.type_doc}_{self.grecno}.xml", "w") as file:
            file.write(self.str_to_save)


if __name__ == '__main__':
    m = Docs(111021393, "vn")
    # m.get_header_and_bottom(m.grecno)

    # vn 111021393
    # act 121071808
    # raht  123047263
    # rahz 113005595
