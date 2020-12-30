import datetime

def search_by_id(project_id, conn):
    print('I am here: project_id=' + project_id)
    """Define query by project_id"""
    cur = conn.cursor()
    # Fetch data from Project_Details table based on project_id
    if project_id:
        cur.execute('SELECT * FROM project_details WHERE project_id=%s', [project_id]);
    # Fetch all data from Project_Details table if no project_id is specified
    else:
        cur.execute('SELECT * FROM project_details' + ';')
    project_details_data = cur.fetchall()
    print('*****************************************')
    print('Data fetched from Project_Details table')
    print('*****************************************')
    # Create a list of dictionaries with Project_Details table data
    for proj in project_details_data:
        project_list = {}
        project_id = str(proj[0])
        project_list['project_name'] = str(proj[1])
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
                project_list['project_address'] = street + street2 + city + ", " + state + zipcode
            else:
                project_list['project_address'] = street + city + ", " + state + zipcode
        else:
            project_list['project_address'] = city + ", " + state + zipcode
        revenue = str(proj[7])
        est_labor_rate = str(proj[8])
        est_labor_hours = str(proj[9])
        est_labor_expense = str(proj[10])
        act_start_date = str(proj[11])
        project_list['act_start_date'] = act_start_date
        if str(proj[12]):
            project_list['act_end_date'] = str(proj[12])              
                        
        # Fetch Time_Sheets data for given project_id
        cur = conn.cursor()
        print('Project ID = ' + str(project_id))
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

        # Calculations for Project Financials - Budgeted/Estimated
        fin_est_revenue = revenue
        project_list['fin_est_revenue '] = f'{float(revenue):,}'
        fin_est_labor_hours = est_labor_hours
        project_list['fin_est_labor_hours'] = str(fin_est_labor_hours)
        fin_est_labor_rate = est_labor_rate
        project_list['fin_est_labor_rate'] = f'{float(fin_est_labor_rate):,}'
        fin_est_labor_expense = float(fin_est_labor_hours) * float(fin_est_labor_rate)
        project_list['fin_est_labor_expense'] = f'{float(fin_est_labor_expense):,}'
        fin_est_gross_profit = float(fin_est_revenue) - fin_est_labor_expense
        # project_list['fin_est_gross_profit'] = "{:.2f}".format(fin_est_gross_profit)
        project_list['fin_est_gross_profit'] = f'{float(fin_est_gross_profit):,}'
        fin_est_gross_margin = float(fin_est_gross_profit) / float(fin_est_revenue) * 100
        project_list['fin_est_gross_margin'] = "{:.2f}".format(fin_est_gross_margin) + " %"

        # Calculations for Project Financials - Actual
        fin_act_revenue = revenue
        project_list['fin_act_revenue'] = f'{float(fin_act_revenue):,}'
        fin_act_labor_hours = act_labor_hours
        project_list['fin_act_labor_hours'] = str(fin_act_labor_hours)
        fin_act_labor_rate = act_labor_rate
        project_list['fin_act_labor_rate'] = "{:.2f}".format(fin_act_labor_rate)
        fin_act_labor_expense = float(fin_act_labor_hours) * float(fin_act_labor_rate)
        project_list['fin_act_labor_expense'] = f'{float(fin_act_labor_expense):,}'
        fin_act_gross_profit = float(fin_act_revenue) - float(fin_act_labor_expense)
        # project_list['fin_act_gross_profit'] = "{:.2f}".format(fin_act_gross_profit)
        project_list['fin_act_gross_profit'] = f'{float(fin_act_gross_profit):,}'
        fin_act_gross_margin = float(fin_act_gross_profit) / float(fin_act_revenue) * 100
        project_list['fin_act_gross_margin'] = "{:.2f}".format(fin_act_gross_margin) + " %"

    return project_list

def get_timesheet_dict(timesheet, act_labor_hours, conn):
    """Function for individual timesheet calculations - used later for Dashboard route"""
    timesheet_dict = {}
    timesheet_dict['project_id'] = str(timesheet[2])
    user_id = str(timesheet[1])
    timesheet_dict['user_id'] = user_id
    # Fetch user data from Users table
    cur = conn.cursor()
    cur.execute('SELECT user_id, name, pay_rate FROM users WHERE user_id=' + str(user_id));
    user_data = cur.fetchall()
    for user in user_data:
        employee_name = user[1]
        timesheet_dict['employee_name'] = employee_name
        hourly_pay_rate = user[2]
        timesheet_dict['hourly_pay_rate'] = hourly_pay_rate
                
    # Time Calculations
    timesheet_dict['start_time'] = str(timesheet[3])
    timesheet_dict['finish_time'] = str(timesheet[4])
    # Calculate difference of two Datetime objects to find hours worked
    start_time = str(timesheet[3])
    start_time = datetime.datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S')
    finish_time = str(timesheet[4])
    finish_time = datetime.datetime.strptime(finish_time,'%Y-%m-%d %H:%M:%S')     
    # Outputs a timedelta object   
    time_difference = finish_time - start_time
    # Convert time worked into hours worked
    hours_worked = float("{:.2f}".format(time_difference.total_seconds() / 3600))
    timesheet_dict['hours_worked'] = hours_worked    
    act_labor_hours += hours_worked
    return (timesheet_dict, act_labor_hours)

def get_actual_labor_rate(timesheet_all, act_labor_hours, conn):
    """ Function for actual labor rate calculations from timesheets - used later for Dashboard route"""
    sum_of_hours_t_rate = 0
    if not len(timesheet_all):
        print('Empty array - project has no timesheets')
        return 0
    for timesheet_dict in timesheet_all:
        sum_of_hours_t_rate += float(timesheet_dict['hours_worked']) * float(timesheet_dict['hourly_pay_rate'])
    return (float(sum_of_hours_t_rate)/act_labor_hours)