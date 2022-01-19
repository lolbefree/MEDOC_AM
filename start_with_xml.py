
def check_doc(x, create_date):
    act = f"""<?xml version="1.0" encoding="windows-1251"?>
<ZVIT>
  <TRANSPORT>
    <VERSION>4.1</VERSION>
    <CREATEDATE>{create_date}</CREATEDATE>
  </TRANSPORT>
  <ORG>
    <FIELDS>
      <EDRPOU>30223848</EDRPOU>
    </FIELDS>
    <CARD RTFDOC="1">
      <FIELDS>
        <DOCNAME>Акт виконаних робіт</DOCNAME>
        <CHARCODE>AVS_ACT</CHARCODE>
        <PARTCODE>7</PARTCODE>
        <SDOCTYPE>10104</SDOCTYPE>
        <PCTTYPE>-1</PCTTYPE>
      </FIELDS>
      <DOCUMENT>\n"""

    vn = f"""<?xml version="1.0" encoding="windows-1251"?>
<ZVIT>
  <TRANSPORT>
    <VERSION>4.1</VERSION>
    <CREATEDATE>{create_date}</CREATEDATE>
  </TRANSPORT>
  <ORG>
    <FIELDS>
      <EDRPOU>30223848</EDRPOU>
    </FIELDS>
    <CARD RTFDOC="1">
      <FIELDS>
        <DOCNAME>Видаткова накладна</DOCNAME>
        <CHARCODE>AVS_VN</CHARCODE>
        <PARTCODE>7</PARTCODE>
        <SDOCTYPE>10105</SDOCTYPE>
        <PCTTYPE>-1</PCTTYPE>
      </FIELDS>
      <DOCUMENT>\n"""

    raht = f"""<?xml version="1.0" encoding="windows-1251"?>
<ZVIT>
  <TRANSPORT>
    <VERSION>4.1</VERSION>
    <CREATEDATE>{create_date}</CREATEDATE>
  </TRANSPORT>
  <ORG>
    <FIELDS>
      <EDRPOU>30223848</EDRPOU>
    </FIELDS>
    <CARD RTFDOC="1">
      <FIELDS>
        <DOCNAME>Рахунок ТО</DOCNAME>
        <CHARCODE>AVS_RAHT</CHARCODE>
        <PARTCODE>7</PARTCODE>
        <SDOCTYPE>10103</SDOCTYPE>
        <PCTTYPE>-1</PCTTYPE>
      </FIELDS>
      <DOCUMENT>\n"""
    rahz = f"""<?xml version="1.0" encoding="windows-1251"?>
<ZVIT>
  <TRANSPORT>
    <VERSION>4.1</VERSION>
    <CREATEDATE>{create_date}</CREATEDATE>
  </TRANSPORT>
  <ORG>
    <FIELDS>
      <EDRPOU>30223848</EDRPOU>
    </FIELDS>
    <CARD RTFDOC="1">
      <FIELDS>
        <DOCNAME>Рахунок запчастини</DOCNAME>
        <CHARCODE>AVS_RAHZ</CHARCODE>
        <PARTCODE>7</PARTCODE>
        <SDOCTYPE>10103</SDOCTYPE>
        <PCTTYPE>-1</PCTTYPE>
      </FIELDS>
      <DOCUMENT>\n"""
    return locals().get(x)