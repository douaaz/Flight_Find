import pymysql
import hashlib
import datetime
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from pymysql import IntegrityError
from pymysql.constants import ER

app = Flask(__name__)
app.secret_key = "YOUR SECRET KEY"

conn = pymysql.connect(host='localhost',
                               user='root',
                               password= None,
                               database='airlineSystem')

#----------------------------------------------  Maliciou Form Handling --------------------------------------------------------
def check_empty(*args):
    for e in args:
        try:
            if len(str(e)) == 0:
                return True
        except:
            return True
    return False


#---------------------------------------------- Public Use Case --------------------------------------------------------
# Welcome page & initial flight search
@app.route('/', methods = ["GET","POST"])
def indexPage():
    #check whether the user has already logged in:
    if session.get("email"):
        return redirect(url_for("customerHomePage"))
    elif session.get("baemail"):
        return redirect(url_for("baHomePage"))
    elif session.get("username"):
        return redirect(url_for("staffHomePage"))

    cursor = conn.cursor()
    query = "SELECT * FROM airport;"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    city_airport_list = ["Any"]
    for e in data:
       city_airport_list.append(f"{e[1]}|{e[0]}") 
    return render_template("index.html", city_airport_list=city_airport_list)


#AJAX public flight search result
@app.route("/publicSearchFlight", methods=["GET","POST"])
def publicSearchFlight():
    try:
        dept_airport = request.form["from"]
        arriv_airport = request.form["to"]
        date = request.form["date"]
        flight_num = request.form["flight_num"]
    except:
        return "Bad form"

    #filter input to prevent SQL injection
    forbidden = ["'", ";", "--", '"']
    for f in forbidden:
        if (f in dept_airport) or (f in arriv_airport) or (f in date):
            return jsonify({'error': "No result found!"})

    if flight_num != '':
        try:
            int(flight_num)
        except:
            return jsonify({'error': "No result found!"})

    cursor = conn.cursor()
    query = '''SELECT airline_name,flight_num,departure_airport,departure_time,
                arrival_airport,arrival_time,price,status FROM flight '''
    first = True
    if dept_airport != "" and dept_airport != 'Any':
        dept_airport = dept_airport.split('|')
        dept_airport = dept_airport[-1]
        if first:
            query += "WHERE departure_airport = '%s' " % dept_airport
            first = False

    if flight_num != "" and flight_num != 'Any':
        if first:
            query += "WHERE flight_num = %s " % flight_num
            first = False
        else:
            query += "AND flight_num = %s " % flight_num

    if arriv_airport != "" and arriv_airport != 'Any':
        arriv_airport = arriv_airport.split('|')
        arriv_airport = arriv_airport[-1]
        if first:
            query += "WHERE arrival_airport = '%s' " % arriv_airport
            first = False
        else:
            query += "AND arrival_airport = '%s' " % arriv_airport

    if date != "":
        if first:
            query += "WHERE DATE(departure_time) = '%s' " % date
        else:
            query += "AND DATE(departure_time) = '%s' " % date

    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    # error handling:
    if len(data) == 0:
        return jsonify({'error': "No results found!"})
    res = []
    for i in data:
        temp = [str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]), str(i[5]), str(i[6]), str(i[7])]
        res.append(temp)
    return jsonify({"data": res })

# register pages
@app.route("/customerRegisterPage")
def customerRegisterPage():
    return render_template("customerRegisterPage.html")

@app.route("/baRegisterPage")
def baRegisterPage():
    return render_template("baRegisterPage.html")

@app.route("/staffRegisterPage")
def staffRegisterPage():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM airline")
    data = cursor.fetchall()
    airline_list = []
    for e in data:
        airline_list.append(e[0])
    return render_template("staffRegisterPage.html", airlines=airline_list)


# posting register form
@app.route("/register", methods=["POST", "GET"])
def register():
    try:
        user_type = request.form["user_type"]
    except:
        return "Bad form"

    if user_type == "Customer":  # username duplication and other IO requirements waiting to be handled later

        # get info from form
        try:
            email = request.form["email"]
            username = request.form["username"]
            password = request.form["password"]
            building_number = request.form["building_number"]
            street = request.form["street"]
            city = request.form["city"]
            state = request.form["state"]
            phone_number = int(request.form["phone_number"])
            passport_number = request.form["passport_number"]
            passport_expiration = request.form["passport_expiration"]
            passport_country = request.form["passport_country"]
            date_of_birth = request.form["date_of_birth"]
        except:
            return "Bad form"

        if check_empty(email,username,building_number,street,city,state,passport_number,passport_country,passport_expiration,date_of_birth):
            return "Bad Form"
        m = hashlib.md5()
        m.update(password.encode(encoding="UTF-8"))
        hashed_pwd = m.hexdigest()

        cursor = conn.cursor()
        # check email duplicate
        cursor.execute("SELECT * FROM customer")
        data = cursor.fetchall()
        for e in data:
            if email == e[0]:
                return render_template("customerRegisterPage.html", error="email_duplicate")
                # insert user data into db
        query = "INSERT INTO customer VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (email, username, hashed_pwd, building_number, street, city,
                               state, phone_number, passport_number, passport_expiration,
                               passport_country, date_of_birth))
        conn.commit()
        cursor.close()
        return redirect(url_for("customerLoginPage"))

    elif user_type == "Booking Agent":
        try:
            email = request.form["email"]
            password = request.form["password"]
            ba_id = int(request.form["booking_agent_id"])
        except:
            return "Bad form"

        if check_empty(email,password,ba_id):
            return "Bad Form"

        m = hashlib.md5()
        m.update(password.encode(encoding="UTF-8"))
        hashed_pwd = m.hexdigest()
        

        cursor = conn.cursor()
        # check email duplicate
        cursor.execute("SELECT * FROM booking_agent")
        data = cursor.fetchall()
        for e in data:
            if email == e[0]:
                return render_template("baRegisterPage.html", error="email_duplicate")
            if ba_id == int(e[2]):
                return render_template("baRegisterPage.html", error="ID_duplicate")

        query = "INSERT INTO booking_agent VALUES(%s,%s,%s)"
        cursor.execute(query, (email, hashed_pwd, ba_id))
        conn.commit()
        cursor.close()
        return render_template("baLoginPage.html")

    elif user_type == "Airline Staff":
        try:
            username = request.form["username"]
            password = request.form["password"]
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            date_of_birth = request.form["date_of_birth"]
            airline_name = request.form["airline_name"]
        except:
            return "Bad form"

        if check_empty(username,password,first_name,last_name,date_of_birth,airline_name):
            return "Bad Form"

        m = hashlib.md5()
        m.update(password.encode(encoding="UTF-8"))
        hashed_pwd = m.hexdigest()

        cursor = conn.cursor()
        # check username duplicate
        cursor.execute("SELECT * FROM airline_staff")
        data = cursor.fetchall()

        #get airline options
        cursor.execute("SELECT * FROM airline")
        data2 = cursor.fetchall()
        airlines = [e[0] for e in data2]
        for e in data:
            if username == e[0]:
                return render_template("staffRegisterPage.html", error="username_duplicate", airlines=airlines)

        query = "INSERT INTO airline_staff VALUES(%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (username, hashed_pwd, first_name, last_name,
                               date_of_birth, airline_name))
        conn.commit()
        cursor.close()
        return render_template("staffLoginPage.html")
    else:
        return "Bad form"

# login pages
@app.route("/customerLoginPage")
def customerLoginPage():
    if session.get("email"):
        return redirect(url_for("customerHomePage"))
    return render_template("customerLoginPage.html")


@app.route("/baLoginPage")
def baLoginPage():
    if session.get("baemail"):
        return redirect(url_for("baHomePage"))
    return render_template("baLoginPage.html")


@app.route("/staffLoginPage")
def staffLoginPage():
    if session.get("username"):
        return redirect(url_for("staffHomePage"))
    return render_template("staffLoginPage.html")


# login authentification
@app.route('/loginAuth', methods=["POST", "GET"])
def loginAuth():

    try:
        user_type = request.form["user_type"]
    except:
        return "Bad form"

    if user_type == "Customer":

        try:
            email = request.form["email"]
            password = request.form["password"]
        except:
            return "Bad form"

        if check_empty(email,password):
            return "Bad Form"

        m = hashlib.md5()
        m.update(password.encode(encoding="UTF-8"))
        hashed_pwd = m.hexdigest()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customer WHERE email = %s", email)
        data = cursor.fetchone()
        cursor.close()

        email_not_found = False
        password_error = False
        if data:
            if str(data[2]) == str(hashed_pwd):
                session["email"] = email
                return redirect(url_for("customerHomePage"))
            else:
                password_error = True
                return render_template("customerLoginPage.html",
                                       email_not_found=email_not_found, password_error=password_error)
        else:
            email_not_found = True
            return render_template("customerLoginPage.html",
                                   email_not_found=email_not_found, password_error=password_error)

    elif user_type == "Booking Agent":
        try:
            email = request.form["baemail"]
            password = request.form["password"]
        except:
            return "Bad form"

        if check_empty(email, password):
            return "Bad Form"

        m = hashlib.md5()
        m.update(password.encode(encoding="UTF-8"))
        hashed_pwd = m.hexdigest()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM booking_agent WHERE email = %s", email)
        data = cursor.fetchone()
        cursor.close()

        email_not_found = False
        password_error = False
        if data:
            if str(data[1]) == str(hashed_pwd):
                session["baemail"] = email
                return redirect(url_for("baHomePage"))
            else:
                password_error = True
                return render_template("baLoginPage.html", email_not_found=email_not_found,
                                       password_error=password_error)
        else:
            email_not_found = True
            return render_template("baLoginPage.html", email_not_found=email_not_found, password_error=password_error)

    elif user_type == "Airline Staff":
        try:
            username = request.form["username"]
            password = request.form["password"]
        except:
            return "Bad form"

        if check_empty(username,password):
            return "Bad Form"

        m = hashlib.md5()
        m.update(password.encode(encoding="UTF-8"))
        hashed_pwd = m.hexdigest()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM airline_staff WHERE username = %s",username)
        data = cursor.fetchone()
        cursor.close()

        username_not_found = False
        password_error = False
        if data:
            if str(data[1]) == str(hashed_pwd):
                session["username"] = username
                return redirect(url_for("staffHomePage"))
            else:
                password_error = True
                return render_template("staffLoginPage.html", username_not_found=username_not_found,
                                       password_error=password_error)
        else:
            username_not_found = True
            return render_template("staffLoginPage.html", username_not_found=username_not_found,
                                   password_error=password_error)
    else:
        return "Bad form"

# Logout
@app.route('/logout', methods=["GET"])
def logout():
    if session.get("email"):
        session.pop("email")
    elif session.get("baemail"):
        session.pop("baemail")
    elif session.get("username"):
        session.pop("username")
    else:
        return "Bad form"
    return redirect(url_for("indexPage"))













#---------------------------------------------- Customer Use Case --------------------------------------------------------
# Customer Homepage
@app.route("/customerHomePage", methods=["GET"])
def customerHomePage():
    if session.get("email"):
        email = session["email"]
        cursor = conn.cursor()
        cursor.execute("SELECT email, name FROM customer WHERE email = %s", (email,))
        user_data = cursor.fetchone()
        # pre-send all airports to the page refresh
        query = "SELECT * FROM airport"
        cursor.execute(query)
        data2 = cursor.fetchall()
        cursor.close()
        city_airport_list = ["Any"]
        for e in data2:
            city_airport_list.append(e[1] + "|" + e[0])
        return render_template("customerHomePage.html", user_data= user_data, city_airport_list=city_airport_list)
    else:
        return redirect(url_for("indexPage"))
    
#Customer Search Flight
@app.route("/customerSearchFlight", methods=["GET", "POST"])
def customerSearchFlight():
    if session.get("email"):

        try:
            dept_airport = request.form["from"]
            arriv_airport = request.form["to"]
            date = request.form["date"]
        except:
            return "Bad form"

        cursor = conn.cursor()

        # Base query to get upcoming flights
        query = '''SELECT airline_name, flight_num, departure_airport, departure_time,
                          arrival_airport, arrival_time, price, status
                   FROM flight 
                   WHERE status = "Scheduled"
                   '''

        # Sanitize input to prevent SQL injection
        forbidden = ["'", ";", "--", '"']
        for f in forbidden:
            if (f in dept_airport) or (f in arriv_airport) or (f in date):
                return jsonify({'error': "No results found!"})

        conditions = []
        parameters = []

        # Add conditions based on user input
        if dept_airport and dept_airport != 'Any':
            dept_airport = dept_airport.split('|')[-1]
            conditions.append("departure_airport = %s")
            parameters.append(dept_airport)

        if arriv_airport and arriv_airport != 'Any':
            arriv_airport = arriv_airport.split('|')[-1]
            conditions.append("arrival_airport = %s")
            parameters.append(arriv_airport)

        if date:
            conditions.append("DATE(departure_time) = %s")
            parameters.append(date)

        # Append conditions to the base query
        if conditions:
            query += " AND " + " AND ".join(conditions)

        cursor.execute(query, tuple(parameters))
        data = cursor.fetchall()

        # Error handling if no data found
        if len(data) == 0:
            return jsonify({'error': "No results found!"})

        res = []
        for e in data:
            # Convert flight record to a list of its string representation
            record = [str(i) for i in e]

            # Query to count available tickets
            ticket_query = '''SELECT COUNT(ticket_id) ticket_num FROM ticket WHERE airline_name = %s
                        AND flight_num = %s
                        AND ticket_id NOT IN (SELECT ticket_id FROM purchases);'''
            cursor.execute(ticket_query, (record[0], record[1]))
            ticket_num = cursor.fetchone()[0]
            print(record[0], record[1])
            print(ticket_num)

            # If tickets are available, append 0, otherwise append 1
            if ticket_num and ticket_num > 0:
                record.append(0)
            else:
                record.append(1)

            res.append(record)

        cursor.close()
        return jsonify({"data": res})  # Return available flight data

    else:
        return redirect(url_for("indexPage"))


#customer purchase flight page
@app.route("/customerPurchaseDetail", methods=["GET", "POST"])
def customerPurchaseFlight():
    if session.get("email"):

        try:
            email = session["email"]
            airline_name = request.form["airline_name"]
            flight_num = int(request.form["flight_num"])
        except:
            return "Bad form"

        if check_empty(email,airline_name,flight_num):
            return "Bad Form"

        cursor = conn.cursor()
        query = '''SELECT COUNT(ticket_id) ticket_num FROM ticket WHERE airline_name = %s
                        AND flight_num = %s
                        AND ticket_id NOT IN (SELECT ticket_id FROM purchases);'''
        cursor.execute(query, (airline_name, flight_num))
        available_ticket_num = cursor.fetchone()
        available_ticket_num = available_ticket_num[0]

        if available_ticket_num == 0:
            return redirect(url_for("customerPurchaseResult",result = "Sold out!"))

        query = "SELECT airline_name,flight_num,departure_airport,departure_time,arrival_airport,arrival_time,price,status  FROM flight WHERE airline_name = %s AND flight_num = %s;"
        cursor.execute(query, (airline_name, flight_num))
        flight_info = cursor.fetchone()
        cursor.close()
        return render_template("customerPurchaseDetail.html", email=email, flight_info=flight_info,
                               available_ticket_num=available_ticket_num)
    else:
        return redirect(url_for("indexPage"))


# customer purchase success page
@app.route("/customerPurchaseProcess", methods=["GET", "POST"])
def customerPurchaseProcess():
    if session['email']:
        try:
            email = session["email"]
            airline_name = request.form["airline_name"]
            flight_num = int(request.form["flight_num"])
        except:
            return "Bad Form"

        if check_empty(email,airline_name,flight_num):
            return "Bad Form"


        cursor = conn.cursor()

        #check if input flight_num is valid
        cursor.execute("SELECT * FROM flight WHERE airline_name = %s AND flight_num = %s AND status = 'Scheduled';",(airline_name,flight_num))
        d = cursor.fetchall()
        if len(d) == 0:
            return "Bad form"

        #try insertion if there is still tickets left at the moment of purchase
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        query = '''INSERT INTO purchases (ticket_id,customer_email,booking_agent_id,purchase_date) 
                        SELECT ticket_id, '%s', %s, '%s' FROM ticket
                        WHERE airline_name = '%s' AND flight_num = %d
                        AND ticket_id NOT IN (SELECT ticket_id FROM purchases)
                        LIMIT 1;'''%(email,"NULL",date,airline_name,flight_num)
        try:
            cursor.execute(query)
        except:
            cursor.close()
            return redirect(url_for("customerPurchaseResult", result="Sold out!"))

        conn.commit()
        cursor.close()
        return redirect(url_for("customerPurchaseResult",result = "success"))

    else:
        return redirect(url_for("indexPage"))

@app.route("/customerPurchaseResult?<string:result>",methods = ["GET"])
def customerPurchaseResult(result):
    return render_template("customerPurchaseResult.html",result = result)

# Customer trackspending Page
@app.route("/customer_track_spending", methods=["POST","GET"])
def customerTrackSpending(chartID = "Customer_Track_Spending"):
    if session.get("email"):
        email = session["email"]

        if check_empty(email):
            return "Bad Session"
        cursor = conn.cursor()
        #get username
        cursor.execute("SELECT email, name FROM customer WHERE email = %s", email)
        user_data = cursor.fetchone()
        #get annual_spending
        now = datetime.datetime.now()
        year = now.year - 1

        #get year option
        cursor.execute("SELECT distinct year(purchase_date) FROM purchases WHERE customer_email = %s", email)
        year_option = [i[0] for i in cursor.fetchall()]
        if len(year_option) == 0:
            year_option = []

        query = '''SELECT SUM(price) AS total FROM flight,purchases,ticket
                    WHERE purchases.customer_email = %s
                    AND year(purchases.purchase_date) = '2024'
                    AND purchases.ticket_id = ticket.ticket_id
                    AND (ticket.airline_name,ticket.flight_num) = (flight.airline_name,flight.flight_num)
                    '''
        cursor.execute(query, (email))
        annual_spending = cursor.fetchone()[0]
        if annual_spending == None:
            annual_spending = 0

        #get monthly-wise spending of last 6 months
        year += 1
        month = now.month - 1
        search_list = []
        month_list = []
        for i in range(6):
            m = month - i
            if m <= 0:
                m = 12+m
                search_list.append((email,year-1,m))
                month_list.append(str(year-1) + ".%d" % m)
            else:
                search_list.append((email,year,m))
                month_list.append(str(year)+".%d" % m)

        search_list.reverse()
        month_list.reverse()

        query = '''SELECT SUM(price) AS total FROM flight,purchases,ticket
                            WHERE purchases.customer_email = %s
                            AND year(purchases.purchase_date) = %s
                            AND month(purchases.purchase_date) = %s
                            AND purchases.ticket_id = ticket.ticket_id
                            AND (ticket.airline_name,ticket.flight_num) = (flight.airline_name,flight.flight_num)
                            '''
        monthly_spending = []
        for s in search_list:
            cursor.execute(query,s)
            spending =cursor.fetchone()[0]
            if spending == None:
                spending = 0
            monthly_spending.append(int(str(spending)))
        total_spending_in_range = sum(monthly_spending)
        cursor.close()

        return render_template("customerTrackSpending.html", user_data=user_data, year_option = year_option,
                               annual_spending = annual_spending, monthly_spending = monthly_spending,
                                xAxis_categories= month_list,total_spending_in_range = total_spending_in_range)
    else:
        return redirect(url_for("indexPage"))

# AJAX Refresh Chart
@app.route("/customerProcessSpending", methods = ["POST","GET"])
def customerProcessSpending():
    if session.get("email"):

        try:
            email = session["email"]
            start_month = int(request.form["start_month"])
            end_month = int(request.form["end_month"])
        except:
            return "Bad form"
        if (not start_month in range(1,13)) or (not end_month in range(1,13)):
            return "Bad form"

        year = request.form["year"]
        cursor = conn.cursor()
        cursor.execute("SELECT name from customer WHERE email = %s;", email)
        name = cursor.fetchone()[0]
        if not year:
            res = {}
            res["series1_data"] = [0]
            res["xAxis_categories"] = ["No data found"]
            res["total_spending_in_range"] = '0'
            res["title"] = name + "'s Monthly Spending"
            return jsonify({
                "data": res
            })
        else:
            try:
                year = int(year)
            except:
                return "Bad Form"

        # get monthly-wise spending of specified range
        search_list = []
        month_list = []
        for i in range(start_month,end_month+1):
            search_list.append((email,year,i))
            month_list.append("%d.%d" %(year,i))

        query = '''SELECT SUM(price) AS total FROM flight,purchases,ticket
                                    WHERE purchases.customer_email = %s
                                    AND year(purchases.purchase_date) = %s
                                    AND month(purchases.purchase_date) = %s
                                    AND purchases.ticket_id = ticket.ticket_id
                                    AND (ticket.airline_name,ticket.flight_num) = (flight.airline_name,flight.flight_num)
                                    '''
        monthly_spending = []
        for s in search_list:
            cursor.execute(query, s)
            spending = cursor.fetchone()[0]
            if spending == None:
                spending = 0
            monthly_spending.append(int(str(spending)))

        total_spending_in_range = sum(monthly_spending)
        cursor.close()
        res = {}
        res["series1_data"] = monthly_spending
        res["xAxis_categories"] = month_list
        res["total_spending_in_range"] = str(total_spending_in_range)
        res["title"] = name + "'s Monthly Spending"
        return jsonify({
            "data" : res
        })

    else:
        return redirect(url_for("indexPage"))


# Customer Viewflight Page
@app.route("/customerViewFlight")
def customerViewFlight():
    if session.get("email"):
        email = session["email"]

        if check_empty(email):
            return "Bad Session"
        cursor = conn.cursor()
        #get customer booked flight records
        query = '''SELECT f.airline_name,f.flight_num,f.departure_airport,f.departure_time,
                    f.arrival_airport,f.arrival_time,f.price,f.status
                    FROM flight AS f, ticket AS t, purchases AS p
                    WHERE p.customer_email = %s
                    AND p.ticket_id = t.ticket_id
                    AND (t.airline_name,t.flight_num) = (f.airline_name,f.flight_num);'''

        cursor.execute(query,email)
        booked_flight_data = cursor.fetchall()
        result = []
        departure_airport_option = []
        arrival_airport_option = []
        airline_name_option = []
        flight_num_option = []
        for e in booked_flight_data:
            temp = {
            "airline_name": e[0],
            "flight_num": int(str(e[1])),  # Convert to integer
            "departure_airport": e[2],
            "departure_time": str(e[3]),  # Convert to string
            "arrival_airport": e[4],
            "arrival_time": str(e[5]),  # Convert to string
            "price": int(str(e[6])),  # Convert to integer
            "status": e[7]
        }
            result.append(temp)

            if not(e[2] in departure_airport_option):
                departure_airport_option.append(e[2])

            if not(e[4] in arrival_airport_option):
                arrival_airport_option.append(e[4])

            if not(e[0] in airline_name_option):
                airline_name_option.append(e[0])

            if not(e[1] in flight_num_option):
                flight_num_option.append(e[1])

        return render_template("customerViewFlight.html",
                               departure_airport_option = departure_airport_option,
                               arrival_airport_option = arrival_airport_option,
                               flight_num_option = flight_num_option,
                               airline_name_option = airline_name_option,
                               booked_flight_data = result,
                               email = email)
    else:
        return redirect(url_for("indexPage"))












#---------------------------------------------- Booking Agent Use Case --------------------------------------------------------
#Booking Agent Hompage
@app.route("/baHomePage", methods=["GET", "POST"])
def baHomePage():
    if session.get("baemail"):
        email = session["baemail"]
        if check_empty(email):
            return "Bad Session"
        # send all airports to the page refresh
        cursor = conn.cursor()
        query = "SELECT * FROM airport"
        cursor.execute(query)
        data2 = cursor.fetchall()
        cursor.close()
        city_airport_list = ["Any"]
        for e in data2:
            city_airport_list.append(e[1] + "|" + e[0])
        return render_template("baHomePage.html", city_airport_list=city_airport_list,
                               email=email)
    else:
        return redirect(url_for("indexPage"))



@app.route("/baSearchFlight", methods=["POST","GET"])
def baSearchFlight():
    if session.get("baemail"):
        try:
            dept_airport = request.form["from"]
            arriv_airport = request.form["to"]
            date = request.form["date"]
        except:
            return  "Bad form"


        cursor = conn.cursor()
        query = '''SELECT airline_name,flight_num,departure_airport, departure_time,
                    arrival_airport, arrival_time, price, status
                    FROM flight 
                    WHERE status = "Scheduled"
                    '''

        forbidden = ["'", ";", "--", '"']
        for f in forbidden:
            if (f in dept_airport) or (f in arriv_airport) or (f in date):
                return jsonify({'error': "No results found!"})

        if dept_airport != "" and dept_airport != 'Any':
            dept_airport = dept_airport.split('|')
            dept_airport = dept_airport[-1]
            query += "AND departure_airport = '%s' " % dept_airport

        if arriv_airport != "" and arriv_airport != 'Any':
            arriv_airport = arriv_airport.split('|')
            arriv_airport = arriv_airport[-1]
            query += "AND arrival_airport = '%s' " % arriv_airport

        if date != "":
            query += "AND DATE(departure_time) = '%s' " % date

        cursor.execute(query)
        data = cursor.fetchall()

        # error handling:
        if len(data) == 0:
            return jsonify({
                'error': "No results found!"
            })

        res = []
        for e in data:
            record = [str(item) for item in e]
            query = '''SELECT COUNT(ticket_id) ticket_num FROM ticket WHERE airline_name = %s
                        AND flight_num = %s
                        AND ticket_id NOT IN (SELECT ticket_id FROM purchases);'''
            cursor.execute(query, (record[0], record[1]))
            ticket_num = cursor.fetchone()[0]
            if ticket_num > 0:
                record.append(0)
            else:
                record.append(1)

            res.append(record)
        cursor.close()
        return jsonify({
            "data": res  # shoud be the data for all available flights
        })
    else:
        return redirect(url_for("indexPage"))


@app.route("/baPurchaseDetail", methods=["GET", "POST"])
def baPurchaseDetail():
    if session.get("baemail"):
        try:
            email = session["baemail"]
            airline_name = request.form["airline_name"]
            flight_num = int(request.form["flight_num"])
        except:
            return "Bad form"

        if check_empty(email,airline_name):
            return "Bad Form"

        cursor = conn.cursor()
        query = '''SELECT ticket_id FROM ticket WHERE airline_name = %s
                            AND flight_num = %s
                            AND ticket_id not in (SELECT ticket_id FROM purchases);'''
        cursor.execute(query, (airline_name, flight_num))
        available_ticket_num = len(cursor.fetchall())
        if available_ticket_num == 0:
            return redirect(url_for("baPurchaseResult", result = "Sold out!"))

        query = "SELECT airline_name,flight_num,departure_airport,departure_time,arrival_airport,arrival_time,price,status  FROM flight WHERE airline_name = %s AND flight_num = %s;"
        cursor.execute(query, (airline_name, flight_num))
        flight_info = cursor.fetchone()
        cursor.close()
        return render_template("baPurchaseDetail.html", email=email, flight_info=flight_info,
                               available_ticket_num=available_ticket_num)
    else:
        return redirect(url_for("indexPage"))

@app.route("/baPurchaseProcess",methods = ["POST","GET"])
def baPurchaseProcess():
    if session['baemail']:
        try:
            email = session["baemail"]
            cust_email = request.form["cust_email"]
            airline_name = request.form["airline_name"]
            flight_num = int(request.form["flight_num"])
        except:
            return "Bad form"

        if check_empty(email,cust_email,airline_name):
            return "Bad Form"

        cursor = conn.cursor()

        #get booking agent id
        query = '''SELECT booking_agent_id FROM booking_agent WHERE email = %s;'''
        cursor.execute(query,email)
        ba_id = cursor.fetchone()[0]

        #check if input customer_email is valid
        query = "SELECT * FROM customer WHERE email = %s"
        cursor.execute(query,(cust_email))
        cust_num = len(cursor.fetchall())
        if cust_num == 0:
            cursor.close()
            return redirect(url_for("baPurchaseResult",result = "Customer email not found!"))


        #check if input flight_num is valid
        cursor.execute("SELECT * FROM flight WHERE airline_name = %s AND flight_num = %s AND status = 'Scheduled';",(airline_name,flight_num))
        d = cursor.fetchall()
        if len(d) == 0:
            return "Bad form"

        #try insertion if there is still ticket left at the moment of purchase
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        query = '''INSERT INTO purchases (ticket_id,customer_email,booking_agent_id,purchase_date) 
                                    SELECT ticket_id, '%s', %s, '%s' FROM ticket
                                    WHERE airline_name = '%s' AND flight_num = %s
                                    AND ticket_id NOT IN (SELECT ticket_id FROM purchases)
                                    LIMIT 1;''' % (cust_email, ba_id, date, airline_name, flight_num)
        try:
            cursor.execute(query)

        except:
            cursor.close()
            return redirect(url_for("baPurchaseResult", result="Sold out!"))

        conn.commit()
        cursor.close()
        return redirect(url_for("baPurchaseResult",result = "success"))
    else:
        return redirect(url_for("indexPage"))


@app.route("/baPurchaseResult?<string:result>",methods = ["GET"])
def baPurchaseResult(result):
    try:
        result = str(result)
    except:
        return "Bad form"
    return render_template("baPurchaseResult.html", result=result)


# Booking Agent view commission
@app.route("/baViewCommission", methods = ["GET", "POST"])
def baViewCommission():
    if session.get("baemail"):
        cursor = conn.cursor()
        email = session["baemail"]

        if check_empty(email):
            return "Bad Session"

        #get year option
        query = '''SELECT year(purchase_date) AS year FROM purchases 
                    WHERE booking_agent_id = (SELECT booking_agent_id FROM booking_agent WHERE email = %s);'''
        cursor.execute(query,email)
        year_data = cursor.fetchall()
        year_option = []
        for e in year_data:
            year_option.append(e[0])

        #get  date
        date_mark = (datetime.datetime.now()-datetime.timedelta(days=30)).strftime("%Y-%m-%d")

        #get total_commission
        query = '''SELECT SUM(price*0.1) AS total_commission FROM ticket, purchases, flight
                    WHERE ticket.ticket_id = purchases.ticket_id
                    AND (ticket.airline_name, ticket.flight_num) = (flight.airline_name, flight.flight_num)
                    AND purchases.booking_agent_id = (SELECT booking_agent_id FROM booking_agent WHERE email = %s)
                    AND purchases.purchase_date > %s'''

        cursor.execute(query,(email,date_mark))
        total_commission = cursor.fetchone()[0]
        if not total_commission:
            total_commission = 0
        else:
            total_commission = float(total_commission)

        #get sold ticket num
        query = '''SELECT COUNT(ticket_id) sold_ticket_num FROM purchases 
                    WHERE booking_agent_id = (SELECT booking_agent_id FROM booking_agent WHERE email = %s)
                    AND  purchase_date > %s;'''
        cursor.execute(query,(email,date_mark))
        sold_ticket_num = cursor.fetchone()[0]
        cursor.close()
        if sold_ticket_num != 0:
            commission_average = total_commission/sold_ticket_num
        else:
            commission_average = 0
        return render_template("baViewCommission.html", email = email, year_option = year_option,
                                total_commission = total_commission, sold_ticket_num = sold_ticket_num,
                                commission_average = commission_average)
    else:
        return redirect(url_for("indexPage"))


#AJAX refresh commission
@app.route("/baProcessCommission",methods = ["POST","GET"])
def baProcessCommission():
    if session.get("baemail"):
        try:
            email = session["baemail"]
            start_date = request.form["start_date"]
            end_date = request.form["end_date"]
        except:
            return "Bad form"

        if check_empty(email,start_date,end_date):
            return "Bad Form"

        cursor = conn.cursor()
        query = '''SELECT SUM(price*0.1) AS total_commission FROM ticket, purchases, flight
                    WHERE ticket.ticket_id = purchases.ticket_id
                    AND (ticket.airline_name, ticket.flight_num) = (flight.airline_name, flight.flight_num)
                    AND purchases.booking_agent_id = (SELECT booking_agent_id FROM booking_agent WHERE email = '%s')
                    AND  purchases.purchase_date >= "%s"
                    AND purchases.purchase_date <= "%s" ;''' %(email,start_date,end_date)
        cursor.execute(query)
        total_commission = cursor.fetchone()[0]
        if not total_commission:
            total_commission = 0
        else:
            total_commission = float(total_commission)
        query = '''SELECT COUNT(ticket_id) sold_ticket_num FROM purchases 
                    WHERE booking_agent_id = (SELECT booking_agent_id FROM booking_agent WHERE email = '%s')
                    AND  purchase_date >= "%s"
                    AND purchase_date <= "%s";''' %(email,start_date,end_date)
        cursor.execute(query)
        sold_ticket_num = cursor.fetchone()[0]
        cursor.close()
        if sold_ticket_num != 0:
            commission_average = total_commission/sold_ticket_num
        else:
            commission_average = 0
        return jsonify({"data" : {"total_commission":total_commission, "sold_ticket_num":sold_ticket_num,
                               "average_commission_in_range":commission_average}})
    else:
        return redirect(url_for("indexPage"))

#booking agent view top 5 customers and draw 2 charts
@app.route("/baTopCustomers",methods = ["GET"])
def baTopCustomers():
    if session.get("baemail"):
        email = session["baemail"]

        if check_empty(email):
            return "Bad Session"

        date_mark = (datetime.datetime.now()-datetime.timedelta(days=180)).strftime("%Y-%m-%d")
        #get top 5 customer by ticket_num
        query = '''SELECT customer_email, name, COUNT(ticket_id) AS ticket_num
                    FROM purchases, customer
                    WHERE customer.email = purchases.customer_email
                    AND booking_agent_id = (SELECT booking_agent_id FROM booking_agent WHERE email = %s)
                    AND purchases.purchase_date > %s
                    GROUP BY customer_email
                    ORDER BY ticket_num DESC
                    LIMIT 5;'''
        cursor = conn.cursor()
        cursor.execute(query,(email,date_mark))
        cust_info = cursor.fetchall()
        top5_tickets = []
        c1xAxis_categories_email = []
        c1xAxis_categories_name = []
        for e in cust_info:
            top5_tickets.append(e[2])
            c1xAxis_categories_email.append(e[0])
            c1xAxis_categories_name.append(e[1])

        # get top 5 customer by total commission
        query = '''SELECT customer_email, name, SUM(price*0.1) total_commission
                    FROM purchases, customer, flight, ticket
                    WHERE purchases.booking_agent_id = (SELECT booking_agent_id FROM booking_agent 
                                                            WHERE email = %s)
                    AND customer.email = purchases.customer_email
                    AND purchases.ticket_id = ticket.ticket_id
                    AND (ticket.airline_name, ticket.flight_num) = (flight.airline_name, flight.flight_num)
                    GROUP BY customer_email
                    ORDER BY total_commission DESC
                    LIMIT 5;'''

        cursor.execute(query,email)
        top5_commission = []
        c2xAxis_categories_email = []
        c2xAxis_categories_name = []
        cust_info = cursor.fetchall()
        cursor.close()
        for e in cust_info:
            top5_commission.append(float(e[2]))
            c2xAxis_categories_email.append(e[0])
            c2xAxis_categories_name.append(e[1])


        return render_template("baTopCustomers.html", email=email, top5_tickets = top5_tickets,
                               c1xAxis_categories_name = c1xAxis_categories_name,
                                c1xAxis_categories_email = c1xAxis_categories_email,
                                top5_commission = top5_commission,
                                c2xAxis_categories_name = c2xAxis_categories_name,
                                c2xAxis_categories_email = c2xAxis_categories_email )

    else:
        return redirect(url_for("indexPage"))

#Booking Agent View Booked Flights
@app.route("/baViewFlight", methods=["GET"])
def baViewFlight():
    if session.get("baemail"):
        email = session["baemail"]
        if check_empty(email):
            return "Bad Session"

        cursor = conn.cursor()
        query = '''SELECT flight.airline_name,flight.flight_num,departure_airport,
                    departure_time,arrival_airport,arrival_time,price,status, customer_email
                    FROM flight, ticket, purchases
                    WHERE purchases.booking_agent_id = (SELECT booking_agent_id FROM
                                                       booking_agent WHERE email = %s)

                    AND purchases.ticket_id = ticket.ticket_id
                    AND (ticket.airline_name,ticket.flight_num) = (flight.airline_name,
                                                                  flight.flight_num);'''

        cursor.execute(query, (email,))
        booked_flight_data = cursor.fetchall()
        cursor.close()
        result = []
        departure_airport_option = []
        arrival_airport_option = []
        airline_name_option = []
        flight_num_option = []
        for e in booked_flight_data:
            temp = list(e)
            temp[1] = int(e[1])
            temp[6] = int(e[6])
            temp[3] = str(e[3])
            temp[5] = str(e[5])
            result.append(temp)

            if not (e[2] in departure_airport_option):
                departure_airport_option.append(e[2])

            if not (e[4] in arrival_airport_option):
                arrival_airport_option.append(e[4])

            if not (e[0] in airline_name_option):
                airline_name_option.append(e[0])

            if not (e[1] in flight_num_option):
                flight_num_option.append(e[1])

        return render_template("baViewFlight.html",
                               departure_airport_option=departure_airport_option,
                               arrival_airport_option=arrival_airport_option,
                               flight_num_option=flight_num_option,
                               airline_name_option=airline_name_option,
                               booked_flight_data=result,
                               email=email)
    else:
        return redirect(url_for("indexPage"))


#---------------------------------------------- Airline Staff Use Case --------------------------------------------------------

#Airline Staff Home Page
@app.route("/staffHomePage",methods = ["GET"])
def staffHomePage():
    if session.get("username"):
        username = session["username"]
        if check_empty(username):
            return "Bad Session"

        query = "SELECT airline_name FROM airline_staff WHERE username = %s;"
        cursor = conn.cursor()
        cursor.execute(query,username)
        try:
            airline_name = cursor.fetchone()[0]
        except:
            return "Your information has been removed from the database. Please contact your admin for further info."

        #get city_airport_list
        query = "SELECT * FROM airport;"
        cursor.execute(query)
        d = cursor.fetchall()
        city_airport_list = []
        for e in d:
            s = e[1]+'|'+e[0]
            city_airport_list.append(s)

        #get flight_data
        query = '''SELECT airline_name,flight_num,departure_airport,departure_time,
                    arrival_airport,arrival_time,price,status 
                    FROM flight 
                    WHERE airline_name = %s;'''
        cursor.execute(query,(airline_name,))
        flight_data = cursor.fetchall()
        result = []
        for e in flight_data:
            temp = list(e)
            temp[1] = int(e[1])
            temp[6] = int(e[6])
            temp[3] = str(e[3])
            temp[5] = str(e[5])
            result.append(temp)
        flight_data = result

        #get airplane
        query = '''SELECT * FROM airplane WHERE airline_name = %s;'''
        cursor.execute(query,airline_name)
        airplane = cursor.fetchall()
        cursor.close()
        return render_template("staffHomePage.html",username=username, airline_name=airline_name,
                               city_airport_list=city_airport_list,
                               flight_data=flight_data, airplane=airplane)
    else:
            return redirect(url_for("indexPage"))

@app.route("/staffChangeFlight",methods = ["POST","GET"])
def staffChangeFlight():
    if session.get("username"):
        try:
            username = session["username"]
            flight_num = int(request.form["flight_num"])
            status = request.form["status"]
        except:
            return "Bad form"

        if status not in ["Scheduled","Delayed","In-progress","Cancelled","Canceled"]:
            return "Bad status form"

        cursor = conn.cursor()
        query = "SELECT airline_name FROM airline_staff WHERE username = %s;"
        cursor.execute(query, username)
        try:
            airline_name = cursor.fetchone()[0]
        except:
            return "Your information has been removed from the database. Please contact your admin for further info."
        query = '''UPDATE flight SET status = %s
                    WHERE airline_name = %s
                    AND flight_num = %s ;'''
        cursor = conn.cursor()
        cursor.execute(query,(status,airline_name,flight_num))
        conn.commit()
        query = '''SELECT airline_name,flight_num,departure_airport,departure_time,
                    arrival_airport,arrival_time,price,status 
                    FROM flight 
                    WHERE airline_name = %s;'''
        cursor.execute(query,airline_name)
        data = cursor.fetchall()
        result = []
        for e in data:
            temp = list(e)
            temp[1] = int(str(e[1]))
            temp[6] = int(str(e[6]))
            temp[3] = str(e[3])
            temp[5] = str(e[5])
            result.append(temp)
        data = result
        cursor.close()
        return jsonify({"data":data})
    else:
        return redirect(url_for("indexPage"))

@app.route("/staffAddAirport", methods=["POST", "GET"])
def staffAddAirport():
    if session.get("username"):
        username = session.get("username")

        # Query to fetch the permission of the current user
        query = "SELECT permission_type FROM permission WHERE username = %s;"
        cursor = conn.cursor()
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        
        # Check if the user exists and has the required permission
        if not result or result[0] != "Admin":
            cursor.close()
            return jsonify({'data': "Error: You do not have the required permissions to perform this action!"})
        try:
            airport_name = request.form["airport_name"]
            airport_city = request.form["airport_city"]
        except:
            cursor.close()
            return "Bad form"

        if check_empty(airport_name, airport_city):
            cursor.close()
            return "Bad Form"

        # Check if the airport name already exists
        query = "SELECT airport_name FROM airport WHERE airport_name = %s;"
        cursor.execute(query, (airport_name,))
        if cursor.fetchone():
            cursor.close()
            return jsonify({"data": "Error: Airport name already exists!"})

        # Insert the new airport into the database
        query = "INSERT INTO airport (airport_name, airport_city) VALUES (%s, %s);"
        cursor.execute(query, (airport_name, airport_city))
        conn.commit()
        cursor.close()
        return jsonify({'data': "Success"})
    else:
        return redirect(url_for("indexPage"))


@app.route("/staffAddAirplane",methods = ["POST","GET"])
def staffAddAirplane():
    if session.get("username"):
        try:
            username = session["username"]
            airplane_id = int(request.form["airplane_id"])
            seats = int(request.form["seats"])
        except:
            return "Bad form"
        if airplane_id < 0 or seats < 0:
            return  "Bad form"

        cursor = conn.cursor()
        query = "SELECT airline_name FROM airline_staff WHERE username = %s;"
        cursor.execute(query, username)
        try:
            airline_name = cursor.fetchone()[0]
        except:
            return "Your information has been removed from the database. Please contact your admin for further info."

        query = "SELECT airline_name,airplane_id FROM airplane;"
        cursor.execute(query)
        d = cursor.fetchall()
        for e in d:
            if e[0] == airline_name and int(e[1]) == int(airplane_id):
                return jsonify({"data":"Error: airplane_id duplicate"})

        query = "INSERT INTO airplane VALUES(%s,%s,%s);"
        cursor.execute(query,(airline_name,airplane_id,seats))
        conn.commit()
        cursor.close()
        return jsonify({"data":"Success"})

    else:
        return redirect(url_for("indexPage"))

@app.route("/staffCreateFlight",methods = ["GET"])
def staffCreateFlight():
    if session.get("username"):
        username = session["username"]
        if check_empty(username):
            return "Bad Session"
        query = "SELECT airline_name FROM airline_staff WHERE username = %s;"
        cursor = conn.cursor()
        cursor.execute(query,username)
        airline_name = cursor.fetchone()[0]
        cursor.close()
        return render_template("staffCreateFlight.html",username = username, airline_name = airline_name)
    else:
        return redirect(url_for("indexPage"))

@app.route("/staffCreateProcess",methods = ["POST","GET"])
def staffCreateProcess():
    if session.get("username"):
        try:
            username = session["username"]
            flight_num = int(request.form["flight_num"])
            departure_airport = request.form["departure_airport"]
            departure_date = request.form["departure_date"]
            departure_time = request.form["departure_time"]
            arrival_airport = request.form["arrival_airport"]
            arrival_date = request.form["arrival_date"]
            arrival_time = request.form["arrival_time"]
            price = int(request.form["price"])
            status = request.form["status"]
            airplane_id = int(request.form["airplane_id"])
        except:
            return "Bad form"

        if check_empty(username,departure_date,departure_time,arrival_airport,arrival_date,arrival_time,status):
            return "Bad Form"

        if price < 0 or flight_num < 0 or status not in ["Upcoming","Delayed","In-progress","Cancelled","Canceled"]:
            return "Bad form"

        cursor = conn.cursor()
        query = "SELECT airline_name FROM airline_staff WHERE username = %s;"
        cursor.execute(query, username)
        try:
            airline_name = cursor.fetchone()[0]
        except:
            return "Your information has been removed from the database. Please contact your admin for further info."
        #check flight_num duplicate
        query = '''SELECT * FROM flight WHERE airline_name = %s AND flight_num = %s;'''
        cursor.execute(query,(airline_name,flight_num))
        d = cursor.fetchall()
        if len(d) > 0:
            return redirect(url_for("staffCreateResult",result = "This flight number already exists!"))

        #check if airport inputs are valid
        query = '''SELECT airport_name FROM airport'''
        cursor.execute(query)
        d = cursor.fetchall()
        l = []
        for e in d:
            l.append(e[0])

        if not(arrival_airport  in l):
            return redirect(url_for("staffCreateResult",result = "Please enter a valid arrival airport"))
        if not(departure_airport  in l):
            return redirect(url_for("staffCreateResult", result="Please enter a valid departure airport"))

        #check if plane_id is valid
        query = '''SELECT * FROM airplane WHERE airline_name = %s AND airplane_id = %s;'''
        cursor.execute(query,(airline_name,airplane_id))
        d = cursor.fetchall()
        if len(d) == 0:
            return redirect(url_for("staffCreateResult", result="Invalid airplane id!"))

        departure_time = departure_date+' '+ departure_time+":00"
        arrival_time = arrival_date + ' ' +  arrival_time+":00"
        query = '''INSERT INTO flight VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
        cursor.execute(query,(airline_name,
                                flight_num,
                                departure_airport,
                                departure_time,
                                arrival_airport,
                                arrival_time,
                                price,
                                status,
                                airplane_id))
        conn.commit()
        cursor.close()
        return redirect(url_for("staffCreateResult",result = "Success"))
    else:
        return  redirect(url_for("indexPage"))


@app.route("/staffCreateResult?<string:result>",methods = ["GET"])
def staffCreateResult(result):
    if session.get("username"):
        return render_template("staffCreateResult.html",result = result)
    else:
        return redirect(url_for("indexPage"))

@app.route("/staffViewBA",methods = ["GET"])
def staffViewBA():
    if session.get("username"):
        username = session["username"]
        if check_empty(username):
            return "Bad Session"

        #get airline
        query = '''SELECT airline_name FROM airline_staff WHERE username = %s;'''
        cursor = conn.cursor()
        cursor.execute(query,username)
        airline_name = cursor.fetchone()[0]

        #get top5 ba by tickets sold last month
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month - 1
        if month == 0:
            month = 12
            year -= 1

        query = '''SELECT b.email, COUNT(b.email) num_of_ticket
                    FROM booking_agent b, ticket t, purchases p
                    WHERE p.booking_agent_id = b.booking_agent_id
                    AND p.ticket_id = t.ticket_id
                    AND t.airline_name = %s
                    AND MONTH(p.purchase_date) = %s
                    AND YEAR(p.purchase_date) = %s
                    GROUP BY b.email
                    ORDER BY num_of_ticket DESC
                    LIMIT 5;'''
        cursor.execute(query,(airline_name,month,year))
        top5_ba_tickets_m = []
        c1xAxis_categories_email_m = []
        d = cursor.fetchall()
        for e in d:
            top5_ba_tickets_m.append(int(e[1]))
            c1xAxis_categories_email_m.append(e[0])

        # get top5 ba by tickets sold last year
        year = datetime.datetime.now().year - 1
        query = '''SELECT b.email, COUNT(b.email) num_of_ticket
                            FROM booking_agent b, ticket t, purchases p
                            WHERE p.booking_agent_id = b.booking_agent_id
                            AND p.ticket_id = t.ticket_id
                            AND t.airline_name = %s
                            AND YEAR(p.purchase_date) = %s
                            GROUP BY b.email
                            ORDER BY num_of_ticket DESC
                            LIMIT 5;'''
        cursor.execute(query, (airline_name,year))
        top5_ba_tickets_y = []
        c1xAxis_categories_email_y = []
        d = cursor.fetchall()
        for e in d:
            top5_ba_tickets_y.append(int(e[1]))
            c1xAxis_categories_email_y.append(e[0])

        #get top5 ba by commission earned last year
        query = '''SELECT b.email, SUM(f.price*0.1) commission
                        FROM flight f, purchases p, booking_agent b, ticket t
                        WHERE b.booking_agent_id = p.booking_agent_id
                        AND p.ticket_id = t.ticket_id
                        AND (t.airline_name,t.flight_num) = (f.airline_name,f.flight_num)
                        AND YEAR(p.purchase_date) = %s
                        AND t.airline_name = %s
                        GROUP BY b.email
                        ORDER BY commission DESC
                        LIMIT 5;'''
        cursor.execute(query,(year,airline_name))
        d = cursor.fetchall()
        top5_ba_commission = []
        c2xAxis_categories_email = []
        for e in d:
            top5_ba_commission.append(float(e[1]))
            c2xAxis_categories_email.append(e[0])
        cursor.close()
        return render_template("staffViewBA.html",username= username,
                               top5_ba_tickets_m = top5_ba_tickets_m,
                               c1xAxis_categories_email_m = c1xAxis_categories_email_m,
                               top5_ba_tickets_y = top5_ba_tickets_y,
                               c1xAxis_categories_email_y = c1xAxis_categories_email_y,
                               top5_ba_commission = top5_ba_commission,
                               c2xAxis_categories_email	 = c2xAxis_categories_email,
                               )
    else:
        return redirect(url_for("indexPage"))

@app.route("/staffViewCustomers",methods = ["GET"])
def staffViewCustomers():
    if session.get("username"):
        username = session["username"]
        if check_empty(username):
            return "Bad Session"

        year = datetime.datetime.now().year - 1
        query = '''SELECT c.name,p.customer_email,COUNT(*) ticket_num
                    FROM purchases p , ticket t,customer c
                    WHERE p.ticket_id = t.ticket_id
                    AND c.email = p.customer_email
                    AND t.airline_name = (SELECT airline_name FROM airline_staff WHERE username = %s)
                    AND YEAR(p.purchase_date) = %s
                    GROUP BY p.customer_email
                    ORDER BY ticket_num DESC
                    LIMIT 1;'''
        cursor = conn.cursor()
        cursor.execute(query,(username,year))
        most_frequent_cust = {}
        d = cursor.fetchone()
        cursor.close()
        if d:
            most_frequent_cust[1] = d[1]
            most_frequent_cust[0] = d[0]
        else:
            most_frequent_cust[1] = None
            most_frequent_cust[0] = None

        return render_template("staffViewCustomers.html", username = username,
                               most_frequent_cust = most_frequent_cust)
    else:
        return redirect(url_for("indexPage"))

@app.route("/staffProcessCustomers",methods = ["POST","GET"])
def staffProcessCustomers():
    if session.get("username"):
        try:
            username = session["username"]
            customer_email = request.form["customer_email"]
        except:
            return "Bad form"

        if check_empty(username,customer_email):
            return "Bad Form"

        query = '''SELECT distinct f.airline_name,f.flight_num,departure_airport,departure_time,
                    arrival_airport,arrival_time,price,status 
                    FROM flight f, ticket t, purchases p
                    WHERE (t.airline_name,t.flight_num) = (f.airline_name,f.flight_num)
                    AND p.ticket_id = t.ticket_id
                    AND p.customer_email = %s
                    AND f.airline_name = (SELECT airline_name FROM airline_staff 
                                          WHERE username = %s); '''
        cursor = conn.cursor()
        try:
            cursor.execute(query,(customer_email,username))
        except:
            return "Customer email does not exist!"

        d = cursor.fetchall()
        cursor.close()
        res = []
        for e in d:
            temp = e
            temp[5] = str(e[5])
            temp[3] = str(e[3])
            temp[6] = float(e[6])
            res.append(temp)

        return jsonify({"data":res})
    else:
        return redirect(url_for("indexPage"))

@app.route("/staffViewReport",methods = ["GET"])
def staffViewReport():
    if session.get("username"):
        username = session["username"]
        if check_empty(username):
            return "Bad Session"

        query = "SELECT airline_name FROM airline_staff WHERE username = %s;"
        cursor = conn.cursor()
        try:
            cursor.execute(query, username)
            airline_name = cursor.fetchone()[0]
        except:
            return "Your information has been removed from the database. Please contact your admin for further info."

        # get top3 destination last year
        last_year = datetime.datetime.now().year - 1
        query = '''SELECT airport_city, COUNT(*) traffic_num
                            FROM airport a, flight f,ticket t
                            WHERE a.airport_name = f.arrival_airport
                            AND (f.airline_name, f.flight_num) = (t.airline_name,t.flight_num)
                            AND f.status != "Cancelled"
                            AND f.airline_name = %s
                            AND year(f.arrival_time) = %s
                            AND t.ticket_id in (SELECT ticket_id FROM purchases)
                            GROUP BY airport_city
                            ORDER BY traffic_num DESC
                            LIMIT 3;'''
        cursor.execute(query, (airline_name, last_year))
        top3_destinations_y = cursor.fetchall()

        # get top3 destination during last three months
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        endmark = datetime.date(year, month, 1)
        endmark = str(endmark) + " 00:00:00"
        month -= 3
        if month <= 0:
            month += 12
            year -= 1
        startmark = datetime.date(year, month, 1)
        startmark = str(startmark) + " 00:00:00"
        query = '''SELECT airport_city, COUNT(*) traffic_num
                                    FROM airport a, flight f, ticket t
                                    WHERE a.airport_name = f.arrival_airport
                                    AND (f.airline_name, f.flight_num) = (t.airline_name, t.flight_num)
                                    AND f.status != "Cancelled"
                                    AND f.airline_name = %s
                                    AND f.arrival_time < %s
                                    AND f.arrival_time >= %s
                                    AND t.ticket_id in (SELECT ticket_id FROM purchases)
                                    GROUP BY airport_city
                                    ORDER BY traffic_num DESC
                                    LIMIT 3;'''
        cursor.execute(query, (airline_name, endmark, startmark))
        top3_destinations_m = cursor.fetchall()

        # get annually_indirect
        year = datetime.datetime.now().year - 1
        query = '''SELECT SUM(f.price) annually_indirect
                            FROM purchases p , ticket t, flight f
                            WHERE p.ticket_id = t.ticket_id
                            AND (t.airline_name,t.flight_num) = (f.airline_name,f.flight_num)
                            AND f.airline_name = %s
                            AND p.booking_agent_id IS NOT NULL
                            AND YEAR(p.purchase_date) = %s'''
        cursor.execute(query, (airline_name, year))
        annually_indirect = cursor.fetchone()[0]
        if not annually_indirect:
            annually_indirect = 0

        # get annually_direct
        query = '''SELECT SUM(f.price) annually_direct
                                FROM purchases p , ticket t, flight f
                                WHERE p.ticket_id = t.ticket_id
                                AND (t.airline_name,t.flight_num) = (f.airline_name,f.flight_num)
                                AND f.airline_name = %s
                                AND p.booking_agent_id IS NULL
                                AND YEAR(p.purchase_date) = %s'''
        cursor.execute(query, (airline_name, year))
        annually_direct = cursor.fetchone()[0]
        if not annually_direct:
            annually_direct = 0

        # get monthly indirect
        year += 1
        month = datetime.datetime.now().month - 1
        if month == 0:
            year -= 1
            month = 12
        query = '''SELECT SUM(f.price) monthly_indirect
                                    FROM purchases p , ticket t, flight f
                                    WHERE p.ticket_id = t.ticket_id
                                    AND (t.airline_name,t.flight_num) = (f.airline_name,f.flight_num)
                                    AND f.airline_name = %s
                                    AND p.booking_agent_id IS NOT NULL
                                    AND YEAR(p.purchase_date) = %s
                                    AND MONTH(p.purchase_date) = %s;'''
        cursor.execute(query, (airline_name, year, month))
        monthly_indirect = cursor.fetchone()[0]
        if not monthly_indirect:
            monthly_indirect = 0

        # get monthly direct
        query = '''SELECT SUM(f.price) monthly_direct
                                            FROM purchases p , ticket t, flight f
                                            WHERE p.ticket_id = t.ticket_id
                                            AND (t.airline_name,t.flight_num) = (f.airline_name,f.flight_num)
                                            AND f.airline_name = %s
                                            AND p.booking_agent_id IS NULL
                                            AND YEAR(p.purchase_date) = %s
                                            AND MONTH(p.purchase_date) = %s;'''
        cursor.execute(query, (airline_name, year, month))
        monthly_direct = cursor.fetchone()[0]
        if not monthly_direct:
            monthly_direct = 0

        #get total_num_of_tickets sold last year
        year = datetime.datetime.now().year - 1
        query = '''SELECT COUNT(t.ticket_id) total_ticket_num
                    FROM ticket t, purchases p
                    WHERE airline_name = (SELECT airline_name FROM airline_staff WHERE username = %s)
                    AND t.ticket_id = p.ticket_id
                    AND YEAR(p.purchase_date) = %s;'''
        cursor.execute(query,(username,year))
        total_ticket_num = cursor.fetchone()[0]
        if not total_ticket_num:
            total_ticket_num = 0

        #get month-wise tickets sold num
        query = '''SELECT COUNT(t.ticket_id) total_ticket_num
                    FROM ticket t, purchases p
                    WHERE airline_name = (SELECT airline_name FROM airline_staff WHERE username = %s)
                    AND t.ticket_id = p.ticket_id
                    AND YEAR(p.purchase_date) = %s
                    AND MONTH(p.purchase_date) = %s;'''
        xAxis_categories = []
        monthly_ticket_breakdown = []
        for i in range(1,13):
            cursor.execute(query,(username,year,i))
            ticket_num = cursor.fetchone()[0]
            if not ticket_num:
                ticket_num = 0
            xAxis_categories.append("%s.%s"%(year,i))
            monthly_ticket_breakdown.append(ticket_num)

        cursor.close()
        return render_template("staffViewReport.html",username = username,
                               total_ticket_num = total_ticket_num,
                               monthly_ticket_breakdown = monthly_ticket_breakdown,
                               xAxis_categories = xAxis_categories,
                               airline_name=airline_name,
                               top3_destinations_y=top3_destinations_y,
                               top3_destinations_m=top3_destinations_m,
                               annually_indirect=annually_indirect,
                               monthly_indirect=monthly_indirect,
                               annually_direct=annually_direct,
                               monthly_direct=monthly_direct
                               )

    else:
        return redirect(url_for("indexPage"))


if __name__ == "__main__":
    app.run()
