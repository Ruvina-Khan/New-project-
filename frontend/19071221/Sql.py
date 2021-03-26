import cx_Oracle as cx
from werkzeug.utils import secure_filename

conn = cx.connect("C##RDBMS","rdbms1998","localhost/XE")
def insert_(u_name,name,password,db_,ADDRESS):
    crsr=conn.cursor()
    crsr.execute(f"insert into {db_}(u_name,name,password,ADDRESS) values('{u_name}','{name}','{password}','{ADDRESS}')")
    conn.commit()
    crsr.close()
    return "True"

def insert_1(u_name,P_NO):
    crsr=conn.cursor()
    crsr.execute(f"insert into P_NO (PHONE_NO ,U_NAME  ) values('{P_NO}','{u_name}')")
    conn.commit()
    crsr.close()
    return "True"

def insert_2(u_name,P_NO):
    crsr=conn.cursor()
    crsr.execute(f"insert into S_NO (PHONE_NO,U_NAME) values('{P_NO}','{u_name}')")
    conn.commit()
    crsr.close()
    return "True"

def check_data(PHONE_NO,U_NAME,db_):
    crsr=conn.cursor()
    data=crsr.execute(f"select PHONE_NO from {db_} where U_NAME='{U_NAME}'")
    
    return data

def update_pass(PASSWORD,U_NAME,db_):
    crsr=conn.cursor()
    data=crsr.execute(f"update {db_} set password='{PASSWORD}'where U_NAME='{U_NAME}'")
    conn.commit()
    crsr.close()
    
    return "True"

"""def insert_data(values,Db_,u_name):
    crsr=conn.cursor()
    query = f"Select U_NAME from Publishers where u_name='{u_name}'"
    crsr=conn.cursor()
    u_name=crsr.execute(query)
#    values['u_name'] = u_name
    for i in u_name:
        values['u_name'] = i[0]

    
    Q= ''
    for i in values.keys():
        if(type(values[i])==int):
            Q=Q+str(values[i])+","
        else:
            Q=Q+"'"+values[i]+"'"+","
            
    Q1 = Q[:-1]
    print(Q1)
    query= f"insert into {Db_} values(" +Q1+ ")"
    crsr=conn.cursor()
    crsr.execute(query)
    conn.commit()
    crsr.close()
    return "True"
"""
def insert_data(ISSN,Title,UNITS,PRICE,IMAGE_name,u_name):
    """crsr=conn.cursor()
    query = f"Select U_NAME from Publishers where u_name='{u_name}'"
    crsr=conn.cursor()
    u_name=crsr.execute(query)"""
#    values['u_name'] = u_name
    query= f"insert into publications(ISSN,Title,UNITS,PRICE,IMAGE_name,email) values('{ISSN}','{Title}','{UNITS}','{PRICE}','{IMAGE_name}','{u_name}')"
    crsr=conn.cursor()
    crsr.execute(query)
    conn.commit()
    crsr.close()
    return "True"

def insert_data1(TYPE_,ISSN,u_name):
    crsr=conn.cursor()
    query = f"Select U_NAME from Publishers where u_name='{u_name}'"
    crsr=conn.cursor()
    u_name=crsr.execute(query)
#    values['u_name'] = u_name
    query= f"insert into PUBLICATION_TYPE values('{TYPE_}','{ISSN}')"
    crsr=conn.cursor()
    crsr.execute(query)
    conn.commit()
    crsr.close()
    return "True"

"""
def fetch_data(u_name,TYPE_):
    crsr=conn.cursor()
    data=crsr.execute(f"select * from {TYPE_} where email='{u_name}'")

    return data"""

def fetch_data(u_name,TYPE_):
    crsr=conn.cursor()
    data=crsr.execute(f" select * from publications where email= '{u_name}' and ISSN IN (SELECT ISSN FROM PUBLICATION_TYPE WHERE TYPE_='{TYPE_}')")

    return data    

def edit_data(ISSN,Title,UNITS,PRICE,IMAGE_name,u_name):   
    query= f"update publications Set Title='{Title}', UNITS= {UNITS}, PRICE={PRICE}, IMAGE_name= '{IMAGE_name}' where ISSN = '{ISSN}'"
    crsr=conn.cursor()
    crsr.execute(query)
    conn.commit()
    crsr.close()
    return "True"
def edit_data1(TYPE_,ISSN,u_name):   
    query= f"update publication_type Set TYPE_='{TYPE_}' where ISSN = '{ISSN}'"
    crsr=conn.cursor()
    crsr.execute(query)
    conn.commit()
    crsr.close()
    return "True"

def select(u_name,password,type_):
    count=0
    crsr=conn.cursor()
    data=crsr.execute(f"Select * from {type_} where u_name='{u_name}' and password='{password}' ")
    for i in data:
        count=count+1
    
    if count==1:
        return count

def delete_data(ISSN):   
    query= f"delete from publications  where ISSN = '{ISSN}'"
    crsr=conn.cursor()
    crsr.execute(query)
    conn.commit()
    crsr.close()
    return "True"


"""def val(PHONE_NO,u_name):
    crsr=conn.cursor()
    crsr.execute(f"insert into P_NO values ('{PHONE_NO}','{u_name}')")
    conn.commit()
    crsr.close()
    return "True" """

def val(PHONE_NO,u_name,var):
    if var==0:
        crsr=conn.cursor()
        crsr.execute(f"insert into P_NO values ('{PHONE_NO}','{u_name}')")
        conn.commit()
        crsr.close()
    else:
        crsr=conn.cursor()
        crsr.execute(f"insert into S_NO values ('{PHONE_NO}','{u_name}')")
        conn.commit()
        crsr.close()
    
    return "True"

#student content


def show_(cnt,u_name):
    crsr=conn.cursor()
    data=crsr.execute(f" select * from publications where ISSN IN (SELECT ISSN FROM PUBLICATION_TYPE WHERE TYPE_='{cnt}')")
    return data
"""def fetch_data(u_name,TYPE_):
    crsr=conn.cursor()
    data=crsr.execute(f"select * from {TYPE_} where email='{u_name}'")

    return data
"""

def show_cart_data(u_name):
    crsr=conn.cursor()
    data=crsr.execute(f"select Title from publications where ISSN IN (select ISSN FROM SUBSCRIBED WHERE EMAIL='{u_name}')")
    return data

"""def up_p(var,u_name):
    crsr=conn.cursor()
    variable=crsr.execute(f" select count from subscribed where sub_id=(select max(SUB_ID) as lastid from subscribed)")
    for i in variable:
        a=i[0]

    print(a)
    
    data=crsr.execute(f"select price from publications where Title ='{var}'")
    b=''
    for j in data:
        b=j[0]

    print(b)

    data1=a*b

    print(data1)
    
    
    return data1"""

def show_cart_data1(u_name):
    crsr=conn.cursor()
    data1=crsr.execute(f"select sum(COUNT) from SUBSCRIBED where user_email='{u_name}'")
    for i in data1:
        a=i[0]

    return a

def add_count(u_name):
    crsr=conn.cursor()
    data1=crsr.execute(f" select (subscribed.count*publications.price) as updated_price,Title,COUNT from subscribed left join publications on (subscribed.ISSN=publications.ISSN) where subscribed.user_email='{u_name}'")
    """data_total= 0
    for i in data1:
        data_total += i[0]
    final_ = {'data':data1, 'total': data_total}
    
    print(final_)"""
    return data1

def sum_total(u_name):
    crsr=conn.cursor()
    data1=crsr.execute(f" select sum(subscribed.count*publications.price)as sum_update from subscribed left join publications on (subscribed.ISSN=publications.ISSN) where subscribed.user_email='{u_name}'")
    """data_total= 0
    for i in data1:
        data_total += i[0]
    final_ = {'data':data1, 'total': data_total}
    
    print(final_)"""
    return data1

def sum_total1(u_name):
    crsr=conn.cursor()
    data1=crsr.execute(f" select sum(subscribed.count*publications.price)as sum_update from subscribed left join publications on (subscribed.ISSN=publications.ISSN) where subscribed.user_email='{u_name}'")
    for i in data1:
        a=i[0]
    print(a)
    return a


"""def show_up_p(up_p,u_name):
    crsr=conn.cursor()
    var1=crsr.execute(f" insert into subscribed (UPDATE_PRCE) values('{up_p}') where sub_id=(select max(SUB_ID) as lastid from subscribed)")
    conn.commit()
    crsr.close()

    return "True"    """

    
def show_cart_data2(u_name):
    crsr=conn.cursor()
    data1=crsr.execute(f"select SUM(price) from publications where ISSN IN (select ISSN FROM SUBSCRIBED WHERE EMAIL='{u_name}')")
    for i in data1:
        a=i[0]

    return a


def add_cart(ISSN,COUNT,u_name):
    crsr=conn.cursor()
    
    var1= (f" select price from publications where ISSN='{ISSN}'")
    for i in var1:
        b=i[0]
    print(b)
    """data1= COUNT*b    
    print(data1)"""
    crsr.execute(f"insert into SUBSCRIBED (ISSN,USER_EMAIL,COUNT) values('{ISSN}','{u_name}','{COUNT}')")
    """var=crsr.execute(f" select count from subscribed where sub_id=(select max(SUB_ID) as lastid from subscribed)")
    for i in var:
        a=i[0]
    data=(f" select price from publications where ISSN='DM06'")
    for i in data:
        b=i[0]
    data1=a*b
    var=crsr.execute(f" insert into (UPDATE_PRCE) values('{data1}') where sub_id=(select max(SUB_ID) as lastid from subscribed)")"""
    conn.commit()
    crsr.close()
    return "True"

def add_cart1(ISSN):
    crsr=conn.cursor()
    data=crsr.execute(f" select TYPE_ from publication_type where ISSN ='{ISSN}'")

    for i in data:
        d_ = i
    
    return d_[0]

"""def show_cart_data1(title,type_):
    crsr=conn.cursor()
    data=crsr.execute(f"select {title} from subscription where TYPE_='{type_}'")
   

    return data"""

def payment(Coupon_code):
    crsr=conn.cursor()
    data=crsr.execute(f" select COUPON_CODE from plan where Coupon_code ='{Coupon_code}'")
    for i in data:
        a=i[0]

    return a
    
    
    


def payment1(Coupon_code):
    crsr=conn.cursor()
    data1=crsr.execute(f" select PRODUCT_LIMIT from plan where Coupon_code ='{Coupon_code}'")
    for i in data1:
        a=i[0]

    return a
    
def delete_sub(u_name):
    crsr=conn.cursor()
    data1=crsr.execute(f"delete from subscribed where USER_EMAIL='{u_name}' ")
    conn.commit()
    crsr.close()

    return "True"
    
   
def payment2(Coupon_code):
    crsr=conn.cursor()
    data1=crsr.execute(f" select OFFER from plan where Coupon_code ='{Coupon_code}'")
    for i in data1:
        a=i[0]

    return a
    
def subscription(cou,CARD_NO,u_name):
    crsr=conn.cursor()
    data1=crsr.execute(f"insert into subscription (COUPON_CODE,EMAIL) values('{cou}','{u_name}')")
    d= crsr.execute(f"select max(scheme_id) as lastid from subscription")
    for i in d:
        a=i[0]
        print(a)
    data2=crsr.execute(f"insert into payment(CARD_NO,EMAIL,ORDERID) values('{CARD_NO}','{u_name}','{a}')")
    conn.commit()
    crsr.close()

    return "TRUE"    
      
def subscription1(CARD_NO,u_name):
    crsr=conn.cursor()
    data1=crsr.execute(f"insert into subscription (EMAIL) values('{u_name}')")
    d= crsr.execute(f"select max(scheme_id) as lastid from subscription")
    for i in d:
        a=i[0]
        print(a)
    data2=crsr.execute(f"insert into payment(CARD_NO,EMAIL,ORDERID) values('{CARD_NO}','{u_name}','{a}')")
    conn.commit()
    crsr.close()

    return "TRUE"  

def end_page(u_name):
    crsr=conn.cursor()
    
    data=crsr.execute(f"select ORDERID,P_ID,P_DATE,CARD_NO from payment where P_ID=(select max(P_ID) as lastid from PAYMENT)")

    return data
    
"""def final_pay(CARD_NO):
    crsr=conn.cursor()
    data1=crsr.execute(f"insert into PAYMENT (CARD_NO) values('{CARD_NO}') WHERE ")
    conn.commit()
    crsr.close()

    return "TRUE" 
"""
"""def count(ISSN,count):
    crsr=conn.cursor()
    data=crsr.execute(f" insert into SUBSCRIBED (count) values('{count}') where ISSN ='{ISSN}' ")

    for i in data:
        d_ = i
    
    return d_[0]  """