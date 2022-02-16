def act_header_and_bottom(x):
    return f"""select 'ТОВ "Автосоюз"' as FIRM_NAME,
              '04655,  м. Київ, просп.Степана Бандери,28' as FIRM_ADR,
         ' 044-207-07-07'  as FIRM_TELEFON,
         'www.avtosojuz.ua' as FIRM_WWWORG,
         'sto@avtosojuz.ua' as FIRM_EMAILORG,
         dbo.Avtosojuz_active_bank() as FIRM_NMBANK,
         dbo.Avtosojuz_active_bank_iban() as FIRM_RS,
         '30223848' as FIRM_INN,
         isnull(c1.commune,'') as SIDE_CDINDTAXNUM_K,
         '30223848' as FIRM_EDRPOU,
         c1.lname as SIDE_PAYER,
         c2.lname as SIDE_OWNER,
         c3. lname as  SIDE_CD_K,
         s.custno as  KLIENT_CODE,
         c1.addr2e+', '+c1.addr2 as SIDE_CDADR_K,
         s.CONLNAME as SIDE_PAYER,
         s.UWTEL as SIDE_TEL_K,
         ad1.adindata as  WARRANT_NAME,
         ad2.adindata as   WARRANT_NUM,
         ad3.adindata as  WARRANT_DATE,
         v.make+' '+v.model as AUTO,
         convert(varchar(50),s.WRKORDNO)+'/'+convert(varchar(50),g.grecno) as NUM,
         'м. Київ' as MISZE_SKL,
         g.billd as DOCDATE,
         s.SERVD as  DATE_APPLICATION,
         'Приймальник' as VO_POS,
         s1.NAME as  VO_NAME,
         v.licno as FIELD1,
         v.model as FIELD2,
         v.MOTOTYPE as FIELD3,
         v.MOTORNO as FIELD4,
         v.SERIALNO as FIELD5,
         v.FREGD as FIELD6,
         v.LAST_SERVICE as FIELD7,
         s.DISTDRIV as FIELD8,
         s.CUSTRECOMMENDATION as FIELD15,
         'V' as Yes,
         '' as No,
         c1.lname as SIDE_OTV_FIO,
         '' as FIELD16,
         '' FIELD17,
         '' as VO_NAME,
         '' as FIELD18,
         s.WRKORDNO as  FIELD19,
         c1.VATID as  SIDE_EDRPOU_K
         

       



          from GBILS01 g
         join  GSALS01 s on g.GSALID=s.GSALID
          join cust c1 on c1.custno=s.custno
          join vehi v on v.vehiid=s.VEHIID
          join cust c3 on g.custno=c3.CUSTNO
          join cust c2 on c2.CUSTNO=v.OCUSTNO
          left join adin ad1 on ad1.adinid=c1.CUSTID and ad1.FIELDID='101'
          left join adin ad2 on ad2.adinid=c1.CUSTID and ad2.FIELDID='102'
          left join adin ad3 on ad3.adinid=c1.CUSTID and ad3.FIELDID='103'
          join sman_full s1 on s1.SMANID=g.HSMANID

          where g.grecno={x}
"""


def act_bonus(x):
    return f"""  select 'FIELD10' as field,round(sum((unitpr*num)-(round((unitpr-(unitpr*DISCPC)),2)*num)),2) as bonus from grows01 where grecno={x} and rtype in (1)
		  union all 
		  select 'FIELD11' as field,round(sum(((unitpr*num)-(round((unitpr-(unitpr*DISCPC)),2)*num))),2) as bonus  from grows01 where grecno={x} and rtype in (7)
		  union all
		 select 'FIELD12' as field,(
		 select round(sum(((unitpr*num)-(round((unitpr-(unitpr*DISCPC)),2)*num))),2) from grows01 where grecno={x} and rtype in (1))+
		 	 (select round(sum(((unitpr*num)-(round((unitpr-(unitpr*DISCPC)),2)*num))),2) from grows01 where grecno={x} and rtype in (7))  as bonus
"""


def act_sum(x):
    return f""" select 'FIELD14' as field,sum(rsum) as suma from GROWS01 where grecno={x} and rtype=1
union all 
 select 'FIELD13' as field,  sum(rsum) as suma from GROWS01 where grecno={x} and rtype in (7,4)
 union all
 select 'SUMWITHOUTPDV' as field,round(sum(rsum)/1.2,2) as suma from GROWS01 where grecno={x} and rtype in (7,1,4)
union all
select 'SUMPDV' as field,sum(rsum)-round((sum(rsum)/1.2),2) as suma from GROWS01 where grecno={x} and rtype in (7,1,4)
union all
select 'DOCSUM' as field,sum(rsum) as suma from GROWS01 where grecno={x} and rtype in (7,1,4)"""


def act_rows(x):
#     print(f"""
# select 	row_number() over (order by rno) as TAB1_F1,
# 		item as	TAB1_F2,
# 		name as TAB1_F3,
# 		case when rtype=1 then 'шт' when   rtype=7 then 'нг' else '' end as  TAB1_F4,
# 		num as TAB1_F5,
# 		unitpr as TAB1_F6,
# 		round((unitpr-(unitpr*DISCPC)),2) as TAB1_F7,
# 		round((unitpr-(unitpr*DISCPC)),2)*num as  TAB1_F8
# 		 from grows01 where grecno={x} and rtype in (1,7,4))""")
    return f"""
select 	row_number() over (order by rno) as TAB1_F1,
		item as	TAB1_F2,
		name as TAB1_F3,
		case when rtype=1 then 'шт' when   rtype=7 then 'нг' else '' end as  TAB1_F4,
		num as TAB1_F5,
		unitpr as TAB1_F6,
		round((unitpr-(unitpr*DISCPC)),2) as TAB1_F7,
		round((unitpr-(unitpr*DISCPC)),2)*num as  TAB1_F8
		 from grows01 where grecno={x} and rtype in (1,7,4)
"""


def vn_header_and_bottom(x):
    return f"""
select 'ТОВ "Автосоюз"' as FIRM_NAME,
              '04655,  м. Київ, просп.Степана Бандери,28' as FIRM_ADR,
         ' 044-207-07-07'  as FIRM_TELEFON,
         'www.avtosojuz.ua' as FIRM_WWWORG,
         'sto@avtosojuz.ua' as FIRM_EMAILORG,
         dbo.Avtosojuz_active_bank() as FIRM_NMBANK,
         dbo.Avtosojuz_active_bank_iban() as FIRM_RS,
         isnull(c1.commune,'') as FIRM_INN,
         '30223848' as FIRM_EDRPOU,

         isnull(c2.lname, ' ') as field1,
        c1. lname as  SIDE_CD_K,
         c1.custno as  KLIENT_CODE,
         c1.VATID as  SIDE_EDRPOU_K,
		 c1.COMMUNE as FIELD2,
          c1.addr2e+', '+c1.ADDR2 as SIDE_CDADR_K,
		  c1.wtel as SIDE_TEL_K,
		  '' as SIDE_TAXSYSTEM,
		  g.srecno as NUM,
		  g.BILLD as DOCDATE,
		  'м. Київ' as  MISZE_SKL,


	
         'Приймальник' as VO_POS,
         s1.NAME as  VO_NAME,
       
         convert(date,s.CREATED) as FIELD16,
         '' FIELD17,
         s1.name as VO_NAME,
         s.SORDNO as  FIELD18,
         c1.VATID as  SIDE_EDRPOU_K
        
          from sBILS01 g
         join  sSALS01 s on g.sSALID=s.sSALID
          join cust c1 on c1.custno=g.custno
         left  join vehi v on v.vehiid=s.VEHIID
         left  join cust c3 on g.custno=c3.CUSTNO
         left  join cust c2 on c2.CUSTNO=v.OCUSTNO
          left join adin ad1 on ad1.adinid=c1.CUSTID and ad1.FIELDID='101'
          left join adin ad2 on ad2.adinid=c1.CUSTID and ad2.FIELDID='102'
          left join adin ad3 on ad3.adinid=c1.CUSTID and ad3.FIELDID='103'
          join sman_full s1 on s1.SMANID=g.HSMANID

          where g.Ssalid={x}

    """


def vn_rows(x):
    return f"""

select row_number() over (order by rno) as TAB1_F1,
item as TAB1_F2,
              name as TAB1_F3,
              case when rtype=1 then 'шт' when   rtype=7 then 'нг' else '' end as  TAB1_F4,
              num as TAB1_F5,
              unitpr as TAB1_F6,
              round((unitpr-(unitpr*DISCPC)),2) as TAB1_F7,
              round((unitpr-(unitpr*DISCPC)),2)*num as  TAB1_F8

              from srows01 where ssalid={x} and rtype in (1,7)


"""


def vn_sum(x):
    return f"""
select 'SUMWITHOUTPDV' as field,round(isnull(sum(rsum)/1.2,0),2) as suma from srows01 where ssalid={x} and rtype in (7,1,4)
union all
select 'SUMPDV' as field,isnull(sum(rsum)-round(isnull(sum(rsum)/1.2,0),2),0) as suma from srows01 where ssalid={x} and rtype in (7,1,4)
union all
select 'DOCSUM' as field,isnull(sum(rsum),0) as suma from srows01 where ssalid={x} and rtype in (7,1,4)
union all
select 'DOCSUM_TEXT' as field,isnull(sum(rsum),0) as suma from srows01 where ssalid={x} and rtype in (7,1,4)


"""


def rahz_header_and_bottom(x):
    return f"""
select 'ТОВ "Автосоюз"' as FIRM_NAME,
              '04655,  м. Київ, просп.Степана Бандери,28' as FIRM_ADR,
         ' 044-207-07-07'  as FIRM_TELEFON,
         'www.avtosojuz.ua' as FIRM_WWWORG,
         'sto@avtosojuz.ua' as FIRM_EMAILORG,
         dbo.Avtosojuz_active_bank() as FIRM_NMBANK,
         dbo.Avtosojuz_active_bank_iban() as FIRM_RS,
         '302238426544' as FIRM_INN,
         '30223848' as FIRM_EDRPOU,

         c2.lname as field1,
        c1. lname as  SIDE_CD_K,
         c1.custno as  KLIENT_CODE,
         c1.VATID as  SIDE_EDRPOU_K,
		 c1.COMMUNE as FIELD2,
          c1.addr2e+', '+c1.ADDR2 as SIDE_CDADR_K,
		  c1.wtel as SIDE_TEL_K,
		  '' as SIDE_TAXSYSTEM,
		  g.prerecno as NUM,
		  g.PREBILLD as DOCDATE,
		  'м. Київ' as  MISZE_SKL,



         'Приймальник' as VO_POS,
         s1.NAME as  VO_NAME,

         convert(date,s.CREATED) as FIELD16,
         '' FIELD17,
         s1.name as VO_NAME,
          s.SORDNO as  FIELD18







          from sBILS01 g
         join  sSALS01 s on g.sSALID=s.sSALID
          left join cust c1 on c1.custno=g.custno
         left  join vehi v on v.vehiid=s.VEHIID
          left join cust c3 on g.custno=c3.CUSTNO
         left  join cust c2 on c2.CUSTNO=v.OCUSTNO
          left join adin ad1 on ad1.adinid=c1.CUSTID and ad1.FIELDID='101'
          left join adin ad2 on ad2.adinid=c1.CUSTID and ad2.FIELDID='102'
          left join adin ad3 on ad3.adinid=c1.CUSTID and ad3.FIELDID='103'
          left join sman_full s1 on s1.SMANID=s.SMANID

          where g.PRERECNO={x} and g.btype=99

    """


def rahz_rows(x):
    return f"""
select	row_number() over (order by rno) as TAB1_F1,

		name as TAB1_F3,
		case when rtype=1 then 'шт' when   rtype=7 then 'нг' else '' end as  TAB1_F4,
		num as TAB1_F5,
		unitpr as TAB1_F6,
		round((unitpr-(unitpr*DISCPC)),2) as TAB1_F7,
		round((unitpr-(unitpr*DISCPC)),2)*num as  TAB1_F8

		 from srows01 where prerecno={x} and rtype in (1,7,4)
"""


def rahz_sum(x):
    return f"""

 select 'FIELD3' as field,
		 round(isnull(sum(((unitpr*num)-(round((unitpr-(unitpr*DISCPC)),2)*num))),0),2) from srows01 where prerecno={x} and rtype in (1)
		 	 
 union all
 select 'SUMWITHOUTPDV' as field,round(isnull(sum(rsum)/1.2,0),2) as suma from srows01 where prerecno={x} and rtype in (7,1,4)
union all
select 'SUMPDV' as field,isnull(sum(rsum)-round(isnull(sum(rsum)/1.2,0),2),0) as suma from srows01 where prerecno={x} and rtype in (7,1,4)
union all
select 'DOCSUM' as field,isnull(sum(rsum),0) as suma from srows01 where prerecno={x} and rtype in (7,1,4)


"""


def raht_header_and_bottom(x):
    return f"""
select 'ТОВ "Автосоюз"' as FIRM_NAME,
              '04655,  м. Київ, просп.Степана Бандери,28' as FIRM_ADR,
         ' 044-207-07-07'  as FIRM_TELEFON,
         'www.avtosojuz.ua' as FIRM_WWWORG,
         'sto@avtosojuz.ua' as FIRM_EMAILORG,
         dbo.Avtosojuz_active_bank() as FIRM_NMBANK,
         dbo.Avtosojuz_active_bank_iban() as FIRM_RS,
         '302238426544' as FIRM_INN,
         '30223848' as FIRM_EDRPOU,
         c1.lname as SIDE_CD_K,
         c2.lname as SIDE_OWNER,
         c3. lname as  SIDE_PAYER,
         s.custno as  KLIENT_CODE,
         c1.addr2e+', '+c1.addr2 as SIDE_CDADR_K,
          s.UWTEL as SIDE_TEL_K,
		  v.make+' '+v.model as AUTO,
		 g.PRERECNO as NUM,
         g.PREBILLD as DOCDATE,
         'Приймальник' as VO_POS,
         s1.NAME as  VO_NAME,
         v.licno as FIELD1,
         v.model as FIELD2,
         v.MOTOTYPE as FIELD3,
         v.MOTORNO as FIELD4,
         v.SERIALNO as FIELD5,
         v.FREGD as FIELD6,
         s.DISTDRIV as FIELD8,
          '' as FIELD16,
         '' FIELD17,
         '' as VO_NAME,
         '' as FIELD18,
         s.WRKORDNO as  FIELD19,
         c1.VATID as  SIDE_EDRPOU_K


       



          from GBILS01 g
         join  GSALS01 s on g.GSALID=s.GSALID
          join cust c1 on c1.custno=s.custno
         left  join vehi v on v.vehiid=s.VEHIID
          join cust c3 on g.custno=c3.CUSTNO
          left join cust c2 on c2.CUSTNO=v.OCUSTNO
          left join adin ad1 on ad1.adinid=c1.CUSTID and ad1.FIELDID='101'
          left join adin ad2 on ad2.adinid=c1.CUSTID and ad2.FIELDID='102'
          left join adin ad3 on ad3.adinid=c1.CUSTID and ad3.FIELDID='103'
          join sman_full s1 on s1.SMANID=s.RECEIVER

          where g.prerecno={x}
    """


def raht_rows(x):
    return f"""
select	row_number() over (order by rno) as TAB1_F1,

		name as TAB1_F3,
		case when rtype=1 then 'шт' when   rtype=7 then 'нг' else '' end as  TAB1_F4,
		num as TAB1_F5,
		unitpr as TAB1_F6,
		round((unitpr-(unitpr*DISCPC)),2) as TAB1_F7,
		round((unitpr-(unitpr*DISCPC)),2)*num as  TAB1_F8

		 from grows01 where prerecno={x} and rtype in (1,7,4)
"""


def raht_sum(x):
    return f"""

 select 'FIELD14' as field,isnull(sum(rsum),0) as suma from GROWS01 where prerecno={x} and rtype=1
union all 
 select 'FIELD13' as field,  isnull(sum(rsum),0) as suma from GROWS01 where prerecno={x} and rtype=7
 union all
 select 'SUMWITHOUTPDV' as field,round(isnull(sum(rsum)/1.2,0),2) as suma from GROWS01 where prerecno={x} and rtype in (7,1,4)
union all
select 'SUMPDV' as field,isnull(sum(rsum)-round(isnull(sum(rsum)/1.2,0),2),0) as suma from GROWS01 where prerecno={x} and rtype in (7,1,4)
union all
select 'DOCSUM' as field,isnull(sum(rsum),0) as suma from GROWS01 where prerecno={x} and rtype in (7,1,4)



"""


def raht_bonus(x):
    return f"""select 'FIELD10' as field,round(isnull(sum((unitpr*num)-(round((unitpr-(unitpr*DISCPC)),2)*num)),0),2) as bonus from grows01 where prerecno={x} and rtype in (1)
		  union all 
		  select 'FIELD11' as field,round(isnull(sum(((unitpr*num)-(round((unitpr-(unitpr*DISCPC)),2)*num))),0),2) as bonus  from grows01 where prerecno={x} and rtype in (7)
		  union all
		 select 'FIELD12' as field,(
		 select round(isnull(sum(((unitpr*num)-(round((unitpr-(unitpr*DISCPC)),2)*num))),0),2) from grows01 where prerecno={x} and rtype in (1))+
		(select round(isnull(sum(((unitpr*num)-(round((unitpr-(unitpr*DISCPC)),2)*num))),0),2) from grows01 where prerecno={x} and rtype in (7))  as bonus


"""


def get_grecno(x):
    return f"select grecno from GBILS01 where GSALID = {x}"


def get_custname_from_GBILS(x):
    return f"select CUSTNAME from GBILS01 where grecnO={x}"
def get_custname_from_sBILS(x):
    return f"select CUSTNAME from sBILS01 where ssalid={x}"
