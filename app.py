# Setup dependencies
import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, json, jsonify
import datetime
from pprint import pprint

from crud import *

# Import Postgres database details from config file
pg_ipaddress = os.getenv("pg_ipaddress")
pg_port = os.getenv("pg_port")
pg_username = os.getenv("pg_username")
pg_password = os.getenv("pg_password")
pg_dbname = os.getenv("pg_dbname")

# Setup connection with Postgres
try:
       conn = psycopg2.connect(dbname=pg_dbname, host=pg_ipaddress, user=pg_username, password=pg_password)
       print('------------------------------------')
       print('PostgreSQL database now connected')
       print('------------------------------------')
except (Exception, psycopg2.DatabaseError) as error:
       print('----------------------------------------------------')
       print ("Error while fetching data from PostgreSQL", error)
       print('----------------------------------------------------')

if conn:
    conn.autocommit = True
    cur = conn.cursor()
    cur.close()

# Create Flask app instance
app = Flask(__name__)



# Route for Index page -- Homepage and Intro to the App
@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")



# Route for Project Dashboard -- fetches project data from database for display, writes an input field to database
@app.route("/dashboard", methods=['GET'])
def dashboard_data():
    if request.method == 'GET':
        cur = conn.cursor()
        # Fetch data from Project_Details table
        cur.execute('SELECT * FROM project_details' + ';')
        project_details_data = cur.fetchall()
        print('*****************************************')
        print('Data fetched from Project_Details table')
        print('*****************************************')
        # Create a dictionary of dictionaries with Project_Details table data
        project_list = {}
        for proj in project_details_data:
            project_dict = {}
            project_id = str(proj[0])
            project_dict['project_name'] = str(proj[1])
            street = str(proj[2])
            if street == 'None':
                street = None
            street2 = str(proj[3])
            if street2 == 'None':
                street2 = None
            city = str(proj[4])
            state = str(proj[5])
            zipcode = str(proj[6])
            zipcode = " " + zipcode
            if street:
                street = street + ", "
                if street2:
                    street2 = street2 + ", "            
                    project_dict['project_address'] = street + street2 + city + ", " + state + zipcode
                else:
                    project_dict['project_address'] = street + city + ", " + state + zipcode
            else:
                project_dict['project_address'] = city + ", " + state + zipcode
            revenue = str(proj[7])
            est_labor_rate = str(proj[8])
            est_labor_hours = str(proj[9])
            est_labor_expense = str(proj[10])
            act_start_date = str(proj[11])
            project_dict['act_start_date'] = act_start_date
            if str(proj[12]) != "":
                project_dict['act_end_date'] = str(proj[12])              
                            
            # Fetch Time_Sheets data for given project_id
            cur = conn.cursor()
            cur.execute('SELECT * FROM time_sheets WHERE project_id=' + str(project_id) + ';')
            timesheet_data = cur.fetchall()
            print('------------------------------------------')
            print('Data fetched from Time_Sheets table')
            print('------------------------------------------')
            # Create a list of dictionaries with Time_Sheets table data
            timesheet_all = []
            act_labor_hours = float(0)
            # Get individual timesheet_dict for display
            if not len(timesheet_data):
                print('No timesheets entered in database for this project, therefore skipping Project ID ' + str(project_id))
            for timesheet in timesheet_data:
                # Calling the pre-defined function
                (timesheet_dict, act_labor_hours) = get_timesheet_dict(timesheet, act_labor_hours, conn)
                timesheet_all.append(timesheet_dict)
            # Using the predefined function for actual labor hours, calculate actual labor rate
            act_labor_rate = get_actual_labor_rate(timesheet_all, act_labor_hours, conn)
            project_dict["timesheets"] = timesheet_all
            project_list["project_id: "+ str(project_id)] = project_dict
            project_dict['id'] = str(project_id)

            # Calculations for Project Financials - Budgeted/Estimated
            fin_est_revenue = revenue
            project_dict['fin_est_revenue '] = f'{float(revenue):,}'
            fin_est_labor_hours = est_labor_hours
            project_dict['fin_est_labor_hours'] = str(fin_est_labor_hours)
            fin_est_labor_rate = est_labor_rate
            project_dict['fin_est_labor_rate'] = f'{float(fin_est_labor_rate):,}'
            fin_est_labor_expense = float(fin_est_labor_hours) * float(fin_est_labor_rate)
            project_dict['fin_est_labor_expense'] = f'{float(fin_est_labor_expense):,}'
            fin_est_gross_profit = float(fin_est_revenue) - fin_est_labor_expense
            # project_dict['fin_est_gross_profit'] = "{:.2f}".format(fin_est_gross_profit)
            project_dict['fin_est_gross_profit'] = f'{float(fin_est_gross_profit):,}'
            fin_est_gross_margin = float(fin_est_gross_profit) / float(fin_est_revenue) * 100
            project_dict['fin_est_gross_margin'] = "{:.2f}".format(fin_est_gross_margin) + " %"

            # Calculations for Project Financials - Actual
            fin_act_revenue = revenue
            project_dict['fin_act_revenue'] = f'{float(fin_act_revenue):,}'
            fin_act_labor_hours = act_labor_hours
            project_dict['fin_act_labor_hours'] = str(fin_act_labor_hours)
            fin_act_labor_rate = act_labor_rate
            project_dict['fin_act_labor_rate'] = "{:.2f}".format(fin_act_labor_rate)
            fin_act_labor_expense = float(fin_act_labor_hours) * float(fin_act_labor_rate)
            project_dict['fin_act_labor_expense'] = f'{float(fin_act_labor_expense):,}'
            fin_act_gross_profit = float(fin_act_revenue) - float(fin_act_labor_expense)
            # project_dict['fin_act_gross_profit'] = "{:.2f}".format(fin_act_gross_profit)
            project_dict['fin_act_gross_profit'] = f'{float(fin_act_gross_profit):,}'
            fin_act_gross_margin = float(fin_act_gross_profit) / float(fin_act_revenue) * 100
            project_dict['fin_act_gross_margin'] = "{:.2f}".format(fin_act_gross_margin) + " %"
        # pprint(project_list)     
        
        # Create a dictionary of dictionaries with project_details table data chosen, and output as a JSON
        return render_template('dashboard.html', project_list=json.dumps(project_list))
           
    else:
        db_read_error = 'Oops - could not read from database!'
        return render_template('error.html', error_type=db_read_error) 

      

# Route for Enter New Project page -- saves inputs to db, then redirects to Dashboard
@app.route('/new_project', methods=['GET', 'POST'])
def new_project_data():
    if request.method == 'GET':
        print('*****************')
        print('Getting form...')
        print('*****************')
        return render_template('new_project.html')    
    
    if request.method == 'POST':
        print('*****************')
        print('Posting form...')
        print('*****************')
        full_values_string = ''
        name = request.form['project_name']
        full_values_string += "(" + "'" + name + "'"
        street = request.form['street']
        full_values_string += ',' + "'" + street + "'"
        street2 = request.form['street2']
        full_values_string += ',' + "'" + street2 + "'"
        city = request.form['city']
        full_values_string += ',' + "'" + city + "'"
        state = request.form['state']
        full_values_string += ',' + "'" + state + "'"
        zipcode = request.form['zipcode']  
        full_values_string += ',' + "'" + zipcode + "'"
        revenue = str("{:.2f}".format(float(request.form['revenue'])))
        full_values_string += ',' + revenue
        est_labor_rate = str("{:.2f}".format(float(request.form['est_labor_rate'])))
        full_values_string += ',' + est_labor_rate
        est_labor_hours = request.form['est_labor_hours']
        full_values_string += ',' + est_labor_hours
        est_labor_expense = str("{:.2f}".format(float(est_labor_hours) * float(est_labor_rate)))
        full_values_string += ',' + est_labor_expense
        if 'act_start_date' in request.form and request.form['act_start_date'] != "":
            act_start_date = datetime.datetime.strptime(request.form['act_start_date'], '%m/%d/%Y').date()
        else:
            act_start_date = datetime.datetime.now()           
        full_values_string += ',' + "'" + str(act_start_date) + "'" + ')'
        # Print data list for database entry
        print('-------------------------------------------------------------------')
        print('Data list prepared for entry to Project_Details table in database')
        print('-------------------------------------------------------------------')
        print(full_values_string)
        print('-------------------------------------------------------------------')
        cur = conn.cursor()
        # Adding form input data to PostgreSQL database
        try:
            cur.execute('INSERT INTO project_details (name, street, street2, city, state, zip, revenue, est_labor_rate, est_labor_hours, est_labor_expense, act_start_date) VALUES ' + full_values_string + ';')
            print('-----------------------------------')
            print('Data added to database - woohoo!')
            print('-----------------------------------')
        except:
            print('---------------------------------------')
            db_write_error = 'Oops - could not write to database!'
            print('---------------------------------------')
            return render_template('error.html', error_type=db_write_error)
        return redirect(url_for('dashboard_data'))



# Route for Enter New User page, saves inputs to db, then redirects to Dashboard
@app.route('/new_user', methods=['GET', 'POST'])
def userdata_html_to_db():
    if request.method == 'GET':
        print('*****************')
        print('Getting form...')
        print('*****************')
        return render_template('new_user.html')    
    
    if request.method == 'POST':
        print('*****************')
        print('Posting form...')
        print('*****************')
        full_values_string = ''
        name = request.form['user_name']
        full_values_string += "(" + "'" + name + "'"
        job_title = request.form['job_title']
        full_values_string += ',' + "'" + job_title + "'"
        pay_rate = request.form['pay_rate']
        full_values_string += ',' + "'" + pay_rate + "'"
        email = request.form['email']
        full_values_string += ',' + "'" + email + "'"
        phone = request.form['phone']
        full_values_string += ',' + "'" + phone + "'" + ")"
        # Print data list for database entry
        print('-------------------------------------------------------------------')
        print('Data list prepared for entry to Users table in database')
        print('-------------------------------------------------------------------')
        print(full_values_string)
        print('-------------------------------------------------------------------')
        cur = conn.cursor()
        # Adding form input data to PostgreSQL database
        try:
            cur.execute('INSERT INTO users (name, job_title, pay_rate, email, phone) VALUES ' + full_values_string + ';')
            print('-----------------------------------')
            print('Data added to database - woohoo!')
            print('-----------------------------------')
        except:
            print('---------------------------------------')
            db_write_error = 'Oops - could not write to database!'
            print('---------------------------------------')
            return render_template('error.html', error_type=db_write_error)
        return redirect(url_for('dashboard_data'))



# Route for new Time Entry -- saves inputs to Time_Sheets table in db, then redirects to Dashboard
@app.route('/new_time', methods=['GET', 'POST'])
def time_html_to_db():     
    if request.method == 'GET':
        # Fetch all employee names from database for dropdown menu
        cur = conn.cursor()
        cur.execute('SELECT name FROM users')
        employee_names_fetch = cur.fetchall()
        print('------------------------------------------------------------')   
        print('All employee names fetched from database for dropdown list')   
        print('------------------------------------------------------------')   
        print(employee_names_fetch)
        print('------------------------------------------------------------')   
        # Convert employee names to a JSON
        employee_list = []
        for db_row in employee_names_fetch:
            employee_dict = {}
            employee_dict['name'] = db_row[0]
            employee_list.append(employee_dict)
        
        # Fetch all project names from database for dropdown menu
        cur.execute('SELECT name FROM project_details')    
        project_names_fetch = cur.fetchall()
        print('-----------------------------------------------------------')   
        print('All project names fetched from database for dropdown list')   
        print('-----------------------------------------------------------')   
        print(project_names_fetch)
        print('-----------------------------------------------------------') 
        # Convert project names to a list
        project_list = []
        for db_row in project_names_fetch:
            project_dict = {}
            project_dict['name'] = db_row[0]
            project_list.append(project_dict)
        
        # Create a dictionary for employee and project names, and convert to a JSON for the dropdown menus
        dropdown_dict = {}
        dropdown_dict['employee_list'] = employee_list
        dropdown_dict['project_list'] = project_list
        pprint(dropdown_dict)
        return render_template('enterTime.html', dropdown_dict=json.dumps(dropdown_dict))
        
    if request.method == 'POST':
        # Required fields, and missing fields check
        required_fields_list = ['employee_name', 'project_name', 'start_time', 'finish_time']
        missing_fields = []
        for req_field in required_fields_list:
            if req_field not in request.form:
                missing_fields.append(req_field)
        if len(missing_fields):
            missing_fields_error = 'Oops - could not find these fields ' + ' '.join(missing_fields)
            return render_template('error.html', error_type=missing_fields_error)
        
        # Fetching employee and project names from form input    
        employee_name = request.form['employee_name']
        project_name = request.form['project_name']
        # Fetching user_id and project_id from Users and Project Details tables in database  
        cur = conn.cursor() 
        cur.execute('SELECT user_id FROM users WHERE name=%s;', [employee_name])
        user_id_fetch = cur.fetchall()
        for user in user_id_fetch:
            user_id = user[0]  
        cur.execute('SELECT project_id FROM project_details WHERE name=%s;', [project_name])
        project_id_data = cur.fetchall()        
        for project in project_id_data:
            project_id = project[0]

        # Fetching time data from form input, and formatting it for database entry
        start_time = request.form['start_time']
        start_time = " ".join(reversed(start_time.split(" ")))
        start_time = datetime.datetime.strptime(start_time, "%m/%d/%Y %H:%M").strftime('%Y-%m-%d %H:%M:%S')
        print('Start timestamp = ' + start_time)
        start_time = str(start_time)
        finish_time = request.form['finish_time']
        finish_time = " ".join(reversed(finish_time.split(" ")))
        finish_time = datetime.datetime.strptime(finish_time, "%m/%d/%Y %H:%M").strftime('%Y-%m-%d %H:%M:%S')
        print('Finish timestamp = ' + finish_time)
        finish_time=str(finish_time)

        # Adding data to Time_Sheets table in database:
        try:
            cur = conn.cursor() 
            cur.execute("INSERT INTO time_sheets (user_id, project_id, start_time, finish_time) VALUES (%s, %s, %s, %s)", (user_id, project_id, start_time, finish_time))
            print('-----------------------------------')
            print('Data added to database - woohoo!')
            print('-----------------------------------')
        except:
            db_write_error = 'Oops - could not write to database!'
            return render_template('error.html', error_type=db_write_error)
        return redirect(url_for('dashboard_data'))



# Route for queried Project_Details pages -- fetches project data from database for display, writes an input field to database
@app.route("/search", methods=['GET', 'POST'])
def project_search():    
    if request.method == 'GET':
        project_id = request.args.get("project_id")
        project_dict = search_by_id(project_id, conn)
        pprint(project_dict)

        # Create a dictionary with project_details table data chosen, and output as a JSON      
        if project_id:
            return render_template('search.html', project_dict=project_dict)
        else:
            return redirect(url_for('dashboard_data'))

        if not project_dict:
            db_read_error = 'Oops - could not read from database!'
            return render_template('error.html', error_type=db_read_error)  

    if request.method == 'POST':
        act_end_date = request.form['end_date']
        cur = conn.cursor()
        # Adding project end date to Project_Details table in database
        project_id = request.form['project_id']
        pprint(project_id)
       
        try:
            sql_insert_string = "UPDATE project_details SET act_comp_date = TO_DATE('" + act_end_date + "', 'MM/DD/YYYY') WHERE project_id=" + project_id + ";"
            print(sql_insert_string)
            cur.execute(sql_insert_string)                  
            print('-----------------------------------')
            print('Data added to database - woohoo!')
            print('-----------------------------------')
            project_dict = search_by_id(project_id, conn)
            pprint(project_dict)
            return render_template('search.html', project_dict=project_dict)
        except:
            db_write_error = 'Oops - could not write to database!'
            return render_template('error.html', error_type=db_write_error)
        return render_template('search.html')
        



# Close database connection
    if(conn):
        cur.close()
        conn.close()
        print('PostgreSQL connection is closed')

if __name__ == "__main__":
    app.run(debug=True)