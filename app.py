# Setup dependencies
from flask import Flask, render_template, request, redirect, jsonify, json
import psycopg2
import datetime
from datetime import date, timedelta
from pprint import pprint

# Import Postgres database details from config file
from postgres_config import pg_ipaddress, pg_port, pg_username, pg_password, pg_dbname

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


# Route for Index page / Dashboard -- fetches data from db and displays on dashboard
@app.route("/", methods=['GET'])
def index():
    if request.method == 'GET':
        cur = conn.cursor()
        # Fetch data from project_details table
        cur.execute('SELECT * FROM project_details');
        project_details_data = cur.fetchall()
        print('------------------------------------------')
        print('Data fetched from Project_Details table')
        print('------------------------------------------')
        print(project_details_data)
        print('------------------------------------------')

        #  Create a list of dictionaries with selected project_details table data, and output as a JSON
        project_list = []
        for db_row in project_details_data:
            project_dict = {}
            project_dict['name'] = db_row[1]
            project_dict['revenue'] = str(db_row[7])
            project_dict['est_labor_hours'] = str(db_row[9])
            project_dict['est_labor_expense'] = str(db_row[10])
            project_dict['act_start_date'] = str(db_row[11])
            project_list.append(project_dict)
        return render_template('index.html', project_list=json.dumps(project_list))
    else:
        print('---------------------------------------')
        db_read_error = 'Oops - could not read from database!'
        print('---------------------------------------')
        return render_template('error.html', error_type=db_read_error)

      
# Route for Enter New Project page -- saves inputs to db, then redirects to Project Details page
@app.route('/new_project', methods=['GET', 'POST'])
def projdata_html_to_db():
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
        return render_template('project_details.html')
    if request.method == 'GET':
        print('*****************')
        print('Getting form...')
        print('*****************')
        return render_template('new_project.html')


# Route for Enter New User page, saves inputs to db, then redirects to Project Details page
@app.route('/new_user', methods=['GET', 'POST'])
def userdata_html_to_db():
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
        return render_template('project_details.html')
    if request.method == 'GET':
        print('*****************')
        print('Getting form...')
        print('*****************')
        return render_template('new_user.html')


# Close database connection
    if(conn):
        cur.close()
        conn.close()
        print('PostgreSQL connection is closed')

if __name__ == "__main__":
    app.run(debug=True)