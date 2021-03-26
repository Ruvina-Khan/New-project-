from flask import Flask,render_template,url_for,request,redirect,session
from werkzeug.utils import secure_filename
#from publisher.publishers import publishers
#from Student.students import students
import os
import Sql
#from flask_ngrok import run_with_ngrok
app = Flask(__name__,static_folder='static',template_folder='templates')

app.secret_key='hello'
#run_with_ngrok(app)

app.config['UPLOAD_IMAGE']= os.path.join('static','image')
app.config['IMAGE']= os.path.join('image')
@app.route('/signup', methods=['POST','GET'] )
def signup():
        if request.method=='POST':
            u_name=request.form['email']
            name= request.form['name']
            password=request.form['password']
            ADDRESS=request.form['ADDRESS']
            P_NO=request.form['P_NO']
            type_=request.form['optradio']
            print(type_)
            db_ = 'yt'
            if type_ == 'Publishers':
                db_ = 'Publishers'
            else:
                db_='Subscriber'
            f_path = os.path.join(app.config['UPLOAD_IMAGE'],u_name )
            os.mkdir(f_path)
            value=Sql.insert_(u_name,name,password,db_,ADDRESS)
            if type_ == 'Publishers':
                value1=Sql.insert_1(u_name,P_NO)
            else:
                value2=Sql.insert_2(u_name,P_NO)

            print('dscbshdcb')
            return redirect('/')
        else:
            return render_template("signup.html")
    #except:
       # return render_template("signup.html")

@app.route('/forget', methods=['POST','GET'] )
def forget():
    return render_template("forgetpass.html")

@app.route('/check_data', methods=['POST','GET'] )
def check_data():
    if request.method=='POST':
            U_NAME=request.form['U_NAME']
            PHONE_NO= request.form['PHONE_NO']
            type_=request.form['optradio']
            db_ = 'yt'
            if type_ == 'Publishers':
                db_ = 'P_NO'
            else:
                db_='S_NO'

            check=Sql.check_data(PHONE_NO,U_NAME,db_)
            a=''
            for i in check:
                a=i[0]
            if PHONE_NO == a:
                print(a)
                print(PHONE_NO)
            return render_template("enter_new.html")

    return render_template("signup.html")      

@app.route('/update_pass', methods=['POST','GET'] )
def update_pass():
    if request.method=='POST':
            PASSWORD=request.form['PASSWORD']
            U_NAME=request.form['U_NAME']
            type_=request.form['optradio']
            db_ = 'yt'
            if type_ == 'Publishers':
                db_ = 'Publishers'
            else:
                db_='Subscriber'

            check=Sql.update_pass(PASSWORD,U_NAME,db_)
            return redirect('/')
    return render_template("signup.html") 


@app.route('/', methods=['GET','POST'])
def Home():
    if request.method=='POST':
        u_name=request.form['email']
        password=request.form['password']
        type_=request.form['optradio']
        count= Sql.select(u_name,password,type_)
        if count==1:
            if type_=='Publishers':
                session['u_name']=u_name
                return redirect(url_for('home'))
            else:
                session['u_name']=u_name
                return redirect(url_for('student'))
        elif u_name== '' or password=='' or type_=='':
            return render_template('index.html',val='INVALID DETAILS')
        else:
            return render_template('index.html', val='INVALID  CREDENTIALS')

    else:
        return render_template("index.html")

#------------------------------- Publisher Section
@app.route("/pub_home", methods=['POST','GET'])
def publishers():
    if "u_name" in session:
        return render_template("pub_main.html", val = session['u_name'] )

@app.route("/pub_home1/<int:PHONE_NO>", methods=['POST','GET'])
def Publisher1(PHONE_NO):
    if "u_name" in session and request.method=='POST':
        PHONE_NO=request.form['PHONE_NO']
        var=0
        data=Sql.val(PHONE_NO,session['u_name'],var)
        return render_template("pub_main.html", val = session['u_name'] )

@app.route("/home", methods=['POST','GET'])
def home():
    if "u_name" in session:
        """data_ = Sql.fetch_data(session['u_name'],TYPE_)"""
        return render_template("publisher_home.html", val = session['u_name'] )

"""@app.route("/pub/<string:TYPE_>", methods=['POST','GET'])
def showingpublications(TYPE_):
    if "u_name" in session:
        data_ = Sql.fetch_data(session['u_name'],TYPE_)
        return render_template("pub_home.html", val = session['u_name'], data1 = data_, img_path=os.path.join(app.config['UPLOAD_IMAGE'],session['u_name']).replace("\\","/") ) """ 

@app.route("/pub/<string:TYPE_>", methods=['POST','GET'])
def showingpublications(TYPE_):
    if "u_name" in session:
        data_ = Sql.fetch_data(session['u_name'],TYPE_)
        return render_template("pub_home.html", val = session['u_name'], data1 = data_, img_path=os.path.join(app.config['UPLOAD_IMAGE'],session['u_name']).replace("\\","/") ) 

"""@app.route("/pub/<string:TYPE_>",methods=['POST','GET'])
def showingpublications(TYPE_):
        if "u_name" in session:
            if TYPE_ == 'periodicals':
                var= Sql.fetch_data(session['u_name'],TYPE_)
    
            elif TYPE_=='journals':
                var= Sql.fetch_data(session['u_name'],TYPE_)
    
            elif TYPE_ == 'magazines':
                var= Sql.fetch_data(session['u_name'],TYPE_)
    
            else:
                return "error"
            return render_template("pub_home.html", val = session['u_name'], data1 = data_, img_path=os.path.join(app.config['UPLOAD_IMAGE'],session['u_name']).replace("\\","/") )"""
          


"""@app.route("/pub_form", methods=['POST','GET'])
def pub_form():
    status = ''
    if "u_name" in session:
        if request.method == 'POST':
            image = request.files['pic'] 
            values = {'ISSN':request.form['ISSN'],
                    'Title':request.form['Title'],
                    'UNITS':int(request.form['unit']),
                    'TYPE_':request.form['type'],
                    #'DATE_':request.form['date'],
                    'PRICE':int(request.form['Price']),
                    'IMAGE_name':secure_filename(image.filename)}
            Db_ = values['TYPE_']
            status = Sql.insert_data(values,Db_,session['u_name'])
            image.save(os.path.join(app.config['UPLOAD_IMAGE'],session['u_name'],secure_filename(image.filename)))
            return render_template("pub_form.html",val = session['u_name'], return_ = status)
        return render_template("pub_form.html",val = session['u_name'], return_ = status)"""



@app.route("/pub_form", methods=['POST','GET'])
def pub_form():
    status = ''
    if "u_name" in session:
        if request.method == 'POST':
            image = request.files['pic'] 
            ISSN=request.form['ISSN']
            Title=request.form['Title']
            UNITS=request.form['unit']
            #'TYPE_':request.form['type'],
            #DATE_=request.form['date']
            PRICE=request.form['Price']
            TYPE_=request.form['type']
            IMAGE_name=secure_filename(image.filename)
            status = Sql.insert_data(ISSN,Title,UNITS,PRICE,IMAGE_name,session['u_name'])
            image.save(os.path.join(app.config['UPLOAD_IMAGE'],session['u_name'],secure_filename(image.filename)))
            status1 = Sql.insert_data1(TYPE_,ISSN,session['u_name'])
            return render_template("pub_form.html",val = session['u_name'], return_ = status)
        return render_template("pub_form.html",val = session['u_name'], return_ = status)
"""
@app.route("/upload", methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        if "u_name" in session:
            if request.files:
                image = request.files['pic']
                image.save(os.path.join(app.config['UPLOAD_IMAGE'],session['u_name'],secure_filename(image.filename)))
                return render_template("pub_home.html", val = session['type'],values = values )"""

@app.route("/test", methods=['POST','GET'])
def test():
    return render_template("test.html",img_path=os.path.join(app.config['UPLOAD_IMAGE'],session['u_name'],'candies.jpg'))

@app.route("/pub_form_Edit", methods=['POST','GET'])
def pub_edit():

    if "u_name" in session:
        data_ = Sql.fetch_data()
        return render_template("pub_form.html", val = session['u_name'], data1 = data_, img_path=os.path.join(app.config['UPLOAD_IMAGE'],session['u_name']).replace("\\","/") )


"""@app.route("/edit/<string:ISSN>", methods=['POST','GET'])
def edit(ISSN):
    
   
        if "u_name" in session:
            if request.method == 'POST':
                image = request.files['pic']
                values = {
                        'Title':request.form['Title'],
                        'UNITS':int(request.form['unit']),
                        'TYPE_':request.form['type'],
                        'DATE_':request.form['date'],
                        'PRICE':int(request.form['Price']),
                        'IMAGE_name':secure_filename(image.filename)}
                print("NOW SQL")
                Sql.edit_data(ISSN,values,values['TYPE_'])
                print("SUCCss SQL")
                image.save(os.path.join(app.config['UPLOAD_IMAGE'],session['u_name'],secure_filename(image.filename)))
                return redirect('/pub_home')
            return render_template("edit.html",val = session['u_name'], isn = ISSN)"""
    
@app.route("/edit/<string:ISSN>", methods=['POST','GET'])
def edit(ISSN):
    
   
        if "u_name" in session:
            if request.method == 'POST':
                image = request.files['pic']
                Title=request.form['Title']
                UNITS=int(request.form['unit'])
                TYPE_=request.form['type']
                DATE_=request.form['date']
                PRICE=int(request.form['Price'])
                IMAGE_name=secure_filename(image.filename)
                print("NOW SQL")
                Sql.edit_data(ISSN,Title,UNITS,PRICE,IMAGE_name,session['u_name'])
                print("SUCCss SQL")
                image.save(os.path.join(app.config['UPLOAD_IMAGE'],session['u_name'],secure_filename(image.filename)))
                status1 = Sql.edit_data1(TYPE_,ISSN,session['u_name'])
                return redirect('/pub_home')
            return render_template("edit.html",val = session['u_name'], isn = ISSN)

@app.route("/delete/<string:ISSN>", methods=['POST','GET'])
def delete(ISSN):
    
    
        if "u_name" in session:
            print("wwww")
            Sql.delete_data(ISSN)
            return redirect('/pub_home')
    

@app.route("/logout", methods = ['POST','GET'])     
def logout():
    if "u_name" in session:
        session.pop('u_name',None)
        return redirect('/')


        
            


#-------------------------------Student Section

@app.route("/sub_home1", methods=['POST','GET'])
def Subscriber1():
    if "u_name" in session and request.method=='GET':
        PHONE_NO=request.form['PHONE_NO']
        data=Sql.val(PHONE_NO,session['u_name'],var)
        return render_template("publisher_home.html", val = session['u_name'] )



@app.route("/std_home", methods=['POST','GET'])
def student():
    if "u_name" in session:
        return render_template("student_home.html",u_name=session['u_name'])

@app.route("/content/<string:cnt>", methods=['POST','GET'])
def content(cnt):
    if "u_name" in session:
        var = Sql.show_(cnt,session['u_name'])
        return render_template("show.html",val=var,u_name=session['u_name'], img_path=os.path.join(app.config['UPLOAD_IMAGE']).replace("\\","/"))        

"""@app.route("/content/<string:cnt>",methods=['POST','GET'])
def content(cnt):
        if "u_name" in session:
            if cnt == 'periodicals':
                var= Sql.show_(cnt)
    
            elif cnt=='journals':
                var= Sql.show_(cnt)
    
            elif cnt == 'magazines':
                var= Sql.show_(cnt)
    
            else:
                return "error"
            return render_template("show.html",val=var,u_name=session['u_name'], img_path=os.path.join(app.config['UPLOAD_IMAGE'],session['u_name']).replace("\\","/"))"""


@app.route("/buy/<string:ISSN>", methods=['POST','GET'])
def buy(ISSN):
        if "u_name" in session:
            return render_template("payment.html",isn=ISSN,u_name=session['u_name'])



"""@app.route("/add_cart/<string:ISSN>", methods=['POST','GET'])
def add_cart(ISSN):
        if "u_name" in session:
            cart=Sql.add_cart(ISSN,u_name=session['u_name'])
            cart1=Sql.add_cart1(ISSN).replace("\('","").replace("\,')","")
            print(cart1)
            return redirect(url_for('content', cnt = cart1))
        return render_template("show.html")"""

@app.route("/add_cart/<string:ISSN>", methods=['POST','GET'])
def count(ISSN):
    if "u_name" in session:
        if request.method == 'POST':
            COUNT=request.form['COUNT']
            print(COUNT)
            """status = Sql.count(ISSN,COUNT)"""
            cart=Sql.add_cart(ISSN,COUNT,u_name=session['u_name'])
            """cart3=Sql.add_count(ISSN,u_name=session['u_name'])"""
            cart1=Sql.add_cart1(ISSN).replace("\('","").replace("\,')","")
            print(cart1)
            return redirect(url_for('content', cnt = cart1))
        return render_template("pub_form.html",val = session['u_name'], return_ = status)



@app.route("/plan", methods=['POST','GET'])
def plan():
    if "u_name" in session:
        return render_template("plan.html",u_name=session['u_name'])

      
@app.route("/pay", methods=['POST','GET'])
def pay():
    if "u_name" in session:
        """up_p=Sql.up_p(var,session['u_name'])"""
        cart3=Sql.add_count(u_name=session['u_name'])
        cart4=Sql.sum_total(u_name=session['u_name'])
        

        var1=Sql.show_cart_data1(session['u_name'])
        """show=Sql.show_up_p(up_p,session['u_name'])"""
        var2=Sql.show_cart_data2(session['u_name'])
        return render_template("payment.html",u_name=session['u_name'],VAL1=var1,VAL2=var2,cart=cart3,total=cart4)
       

"""@app.route("/content/<string:cnt>", methods=['POST','GET'])
def content(cnt):
    if "u_name" in session:
        var = Sql.show_(cnt)
        return render_template("show.html",val=var,u_name=session['u_name'], img_path=os.path.join(app.config['UPLOAD_IMAGE'],session['u_name']).replace("\\","/"))         
"""
@app.route("/apply_coupon", methods=['POST','GET'])
def payment():
    if "u_name" in session:
        if request.method=='POST':
            Coupon_code= request.form['Coupon_code']
            var=Sql.payment(Coupon_code)
            if(Coupon_code==var):
                var1=Sql.payment1(Coupon_code)
                var2=Sql.show_cart_data1(session['u_name'])
                total=Sql.sum_total(session['u_name'])
                if(var2>=var1):
                    var3=Sql.payment2(Coupon_code)
                    """var4=Sql.show_cart_data2(session['u_name'])"""
                    var4=Sql.sum_total1(session['u_name'])
                    print(var3)
                    print(var4)
                    discount=((var3/100)*var4)
                    amount=var4-discount
                    print(discount)
                    print(amount)
                else:
                    return 'nothing'
                return render_template("payment1.html",u_name=session['u_name'],dis=round(discount,2),cou=Coupon_code,total_=var4,amount_=amount)           

            return render_template("plan.html",u_name=session['u_name'])

        return render_template("payment.html",u_name=session['u_name'])        
#-------------------------------
@app.route("/final_pay/<string:cou>", methods=['POST','GET'])
def final_pay(cou):
    if "u_name" in session:
        if request.method=='POST':
            CARD_NO= request.form['CARD_NO']
            status=Sql.subscription(cou,CARD_NO,u_name=session['u_name'])
            end=Sql.end_page(u_name=session['u_name'])
        return render_template("end_page.html",u_name=session['u_name'],end1=end)
    
    return render_template("plan.html",u_name=session['u_name'])      

@app.route("/f_pay", methods=['POST','GET'])
def f_pay():
    if "u_name" in session:
        if request.method=='POST':
            CARD_NO= request.form['CARD_NO']
            print(CARD_NO)
            status=Sql.subscription1(CARD_NO,u_name=session['u_name'])
            end=Sql.end_page(u_name=session['u_name'])
            
        return render_template("end_page.html",u_name=session['u_name'],end1=end)
    
    return render_template("plan.html",u_name=session['u_name'])    


@app.route("/delete_sub", methods=['POST','GET'])
def delete_sub():
    if "u_name" in session:
        if request.method=='POST':
            delete =Sql.delete_sub(u_name=session['u_name'])
            
            
        return render_template("payment.html",u_name=session['u_name'])
    
    return render_template("plan.html",u_name=session['u_name'])    


#-------------------------------
if __name__=="__main__":
    app.run(debug=True)



