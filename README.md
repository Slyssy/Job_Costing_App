##### Data Analysis & Visualization Bootcamp, UT-Austin, 12 December 2020
##### Team Members: Alicia Pelkey, Amy Banerji, Julie Gandre, Karen Kitchens, Michael Donatucci, Stephen Lyssy

<a href="https://project-2-jobcosting.herokuapp.com/">Deployed Link</a>

# Job Costing App

## Table of contents:
* [General info](#general-info)
* [App Workflow](#app-workflow)
* [Screenshots](#screenshots)
* [App Routes](#app-routes)
* [Technologies](#technologies)
* [Limitations](#limitations)
* [Future Improvements](#future-improvements)

## General info:
Smaller Construction management teams have less resources and time to keep up with their busy days. Other than managing the team and projects, they need to focus on the financial timelines and discussing projects with Stakeholders. The Job Costing App will make user experience with project management tools friendlier, and allows them to give live updates to their customers, clients, and bosses.

This app will allow for the leads to see progress in the financial and day to day workload by tracking and visualizing budgeted labor values, and comparing them to the actual labor values. This limits the back and forth of chasing employees around for timesheets and daily progress. Knowing when a project is exceeding budgeted time is often the first step to preventing a project from becoming a major loss.

## App Workflow:
<img src=images/app_workflow.jpg width="600" />

## Screenshots:
![dashboard](images/dashboard.png)
![details](images/project_details.png)
![project](images/new_project.png) 
![time](images/enter_time.png) 
![user](images/new_user.png)
![visualization](images/visualization.png)

## App Routes: 
* Homepage
    @app.route("/", methods=['GET'])
* Project dashboard
    @app.route("/dashboard", methods=['GET'])
* Individual project details
    @app.route("/search", methods=['GET', 'POST'])
* Enter a new project
    @app.route("/new_project", methods=['GET', 'POST'])
* Enter a new user
    @app.route("/new_user", methods=['GET', 'POST'])
* Enter a new time sheet
    @app.route("/new_time", methods=['GET', 'POST'])    

## Technologies:
* Python 
* Flask
* Psycopg2
* PostgresSQL
* JavaScript & D3
* HTML & CSS
* Jinja
* Bootstrap
* Plotly
* Heroku

## Limitations:
* App performance
* App navigation
* No options yet to update or delete data from the database
* Currently only tracks labor expense

## Future Improvements:
* Routes for updating and deleting data.
* Status updates and percentage complete for each project.
* Database expansion to include a full range of expenses for projects such as: materials, subcontractors, sales tax, overhead, labor burden, and overtime.
* Features that would make this a full project management app: pdf document storage, time sheet tracking, change order tracking, and the ability for customers, subcontractors, and venders to access the app.
* Authentication for users.
