'''Notes: 
1. Use the following username and password to access the admin rights 
username: admin
password: password
2. Ensure you open the whole folder for this task in VS Code 
otherwise the # program will look in your root directory for the text files.'''

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")        
    task_data = [t for t in task_data if t != ""]   


task_list = []              
for t_str in task_data:     
    curr_t = {}             

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")  
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = (datetime.strptime(task_components[3], 
                                            DATETIME_STRING_FORMAT))
    curr_t['assigned_date'] = (datetime.strptime(task_components[4], 
                                                 DATETIME_STRING_FORMAT))
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)    

# defining custom functions for the program

def reg_user():
    '''Add a new user to the user.txt file'''
    while True:
        # - Request input of a new username
        new_username = input("New Username: ")
        # - Check if username already exists
        if new_username in username_password.keys():
            print("This user already exists - try another username")
            continue
        else:
        # - Request input of a new password
            new_password = input("New Password: ")

            # - Request input of password confirmation.
            confirm_password = input("Confirm Password: ")

            # - Check if the new password and confirmed password are the same.
            if new_password == confirm_password:
                # - If they are the same, add them to the user.txt file,
                print("New user added")
                username_password[new_username] = new_password
                
                with open("user.txt", "w") as out_file:
                    user_data = []
                    for k in username_password:
                        user_data.append(f"{k};{username_password[k]}")
                    out_file.write("\n".join(user_data))
                    break

            # - Otherwise you present a relevant message.
            else:
                print("Passwords do no match")

def add_task():
    '''Allow a user to add a new task to task.txt file.
    Prompt a user for the following: 
        - A username of the person whom the task is assigned to,
        - A title of a task,
        - A description of the task and 
        - the due date of the task.'''
    
    while True:
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = (datetime.strptime(task_due_date, 
                                                   DATETIME_STRING_FORMAT))
                break

            except ValueError:
                print("Invalid datetime format. Please use the format\
                       specified")


        # Then get the current date.
        curr_date = date.today()
        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
        
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")
        break


def view_all():
    '''Reads the task from task.txt file and prints to the console
    in the format of Output 2 presented in the task pdf (i.e. includes
    spacing and labelling)'''

    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t \
            {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t \
            {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)


def view_mine():
    '''Reads the task from task.txt file and prints to the console
    in the format of Output 2 presented in the task pdf (i.e. includes
    spacing and labelling). Allows user to mark their tasks as complete
    or edit them.'''
    
    t_index_list = []
    for t in task_list:
        if t['username'] == curr_user:
            # Hold the task's number to be displayed later:
            t_index = int(task_list.index(t)) + 1 
            # Add the index of the user task to a list:
            t_index_list.append(str(t_index)) 
            disp_str = f"Task: \t\t {t_index}. {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t \
                {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t \
                {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)

    while True:    
        vm_menu_1 = input("""\n
Select one of your tasks by entering a number
OR press -1 t return to main menu: """)
        
        if vm_menu_1 in t_index_list:
            vm_menu_2 = input('''\n
Please select one of the options below:
    m - mark the task as complete
    e - edit the task
    : ''').lower()
            # index of chosen task in task_list:
            this_t_index = int(vm_menu_1) - 1   
            # calling the dictionary of chosen task:
            this_t = task_list[this_t_index]    

            if vm_menu_2 == 'm':
                this_t['completed'] = True          
                print('Task marked as complete.')

                with open("tasks.txt", "w") as task_file:
                    task_list_to_write = []
                    for t in task_list:
                        str_attrs = [
                            t['username'],
                            t['title'],
                            t['description'],
                            t['due_date'].strftime(DATETIME_STRING_FORMAT),
                            t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                            "Yes" if t['completed'] else "No"
                        ]
                        task_list_to_write.append(";".join(str_attrs))
                    task_file.write("\n".join(task_list_to_write))

            elif vm_menu_2 == 'e':
                if this_t['completed'] == False:
                    while True:
                        new_username = input('Assign new user to task: ')
                        if new_username in username_password.keys():
                            this_t['username'] = new_username
                            break
                        else:
                            print("User does not exist. Enter existing user.")
                            continue
                    
                    while True:
                        try:
                            new_due_date = input('New due date of task \
                                                 (YYYY-MM-DD): ')
                            this_t['due_date'] = (datetime.strptime
                                    (new_due_date, DATETIME_STRING_FORMAT))
                            break

                        except ValueError:
                            print("Invalid datetime format. \
                                  Please use the format specified")
                            continue

                    with open("tasks.txt", "w") as task_file:
                        task_list_to_write = []
                        for t in task_list:
                            str_attrs = [
                                t['username'],
                                t['title'],
                                t['description'],
                                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                "Yes" if t['completed'] else "No"
                            ]
                            task_list_to_write.append(";".join(str_attrs))
                        task_file.write("\n".join(task_list_to_write))
                        print('Task successfully updated.\n')

                else:
                    print("Task marked as complete - cannot be edited.")
                    continue

            else: 
                print('Error: option does not exist. Please try again.')
                continue

        elif vm_menu_1 == "-1": 
            main()

        else:
            print("Wrong input - please try again!\n")
        continue 

def generate_reports():
    '''Generates output files with basic stats of 
    all task and user info held by this programme.'''

    # Create task_overview.txt if it doesn't exist
    if not os.path.exists("task_overview.txt"):
        with open("task_overview.txt", "w") as tasks_file:
            pass

    total_t = len(task_list)

    comp_list = []
    uncomp_list = []
    overdue_list = []

    for t in task_list:
        if t["completed"] == True:
            comp_list.append(t)
        else:
            uncomp_list.append(t)

    total_comp = len(comp_list)
    total_uncomp = len(uncomp_list)   
        
    for t in task_list:
        # casting due date value to date type to compare the dates:
        curr_due_date = datetime.date(t["due_date"]) 
        if curr_due_date > date.today() and t["completed"] == False:
            overdue_list.append(t)
    
    total_overdue = len(overdue_list)            

    percent_uncomp = round(total_uncomp / total_t * 100, 2)
    percent_overdue = round(total_overdue / total_t * 100, 2)

    # Format the output in a readable clear way:
    task_overview = f'''
    ---------------------TASK OVERVIEW REPORT----------------------:
                     
    \tThe total number of tasks:                   \t{total_t}
    \t-----------------------------------------------------------
    \tThe total number of completed tasks:         \t{total_comp}
    \t-----------------------------------------------------------
    \tThe total number of uncompleted tasks:       \t{total_uncomp}
    \t-----------------------------------------------------------
    \tThe total number of tasks that haven’t 
    \tbeen completed and that are overdue:         \t{total_overdue}
    \t-----------------------------------------------------------
    \tThe percentage of tasks that are incomplete: \t{percent_uncomp}
    \t-----------------------------------------------------------
    \tThe percentage of tasks that are overdue:    \t{percent_overdue}
    \t-----------------------------------------------------------\n'''
    
    # Write the string to file:
    with open("task_overview.txt", 'w') as tasks_file:
         print(task_overview, file=tasks_file)


    # Create user_overview.txt if it doesn't exist
    if not os.path.exists("user_overview.txt"):
        with open("user_overview.txt", "w") as users_file:
            pass

    user_list = username_password.keys() 
    total_users = len(user_list)

    # Format the output in a readable clear way:
    user_overview = f'''\n
    =====================USER OVERVIEW REPORT=====================

    The total number of users registered with task_manager.py: \t{total_users}
    --------------------------------------------------------------
    The total number of tasks that have been 
    generated and tracked using task_manager.py:               \t{total_t}
    --------------------------------------------------------------\n'''
    
    # Write the string to file:
    with open("user_overview.txt", 'w') as users_file:
        print(user_overview, file=users_file)

    for user in username_password.keys():
        user_tasks = []
        user_comp_list = []
        user_uncomp_list = []
        user_overdue_list = []

        for t in task_list:
            if user == t['username']:
                user_tasks.append(t)
                total_user_tasks = len(user_tasks)

                if t["completed"] == True:
                    user_comp_list.append(t)
                else:
                    user_uncomp_list.append(t)

                curr_due_date = datetime.date(t["due_date"])
                if curr_due_date > date.today() and t["completed"] == False:
                    user_overdue_list.append(t)
    
        total_user_tasks = len(user_tasks)
        percentage_user_tasks = round(total_user_tasks / total_t * 100, 2)
        # Try-except block to handle division by zero error:
        try:
            percentage_user_comp = round(len(user_comp_list) / 
                                         total_user_tasks * 100, 2)
            percentage_user_uncomp = round(len(user_uncomp_list) / 
                                           total_user_tasks * 100, 2)
            percentage_user_overdue = round(len(user_overdue_list) / 
                                            total_user_tasks * 100, 2)
        except:
            percentage_user_comp = "This user has no tasks assigned"
            percentage_user_uncomp = "This user has no tasks assigned"
            percentage_user_overdue = "This user has no tasks assigned"

        # Format the output in a readable clear way:
        user_detail = f'''\n 
----------------DETAILED REPORT FOR USER {user}-----------------

\tThe total number of tasks assigned to {user}:    \t{total_user_tasks}
\t-----------------------------------------------------------
\tThe percentage of the total number of tasks 
\tthat have been assigned to {user}:               \t{percentage_user_tasks}
\t-----------------------------------------------------------
\tThe percentage of the tasks assigned to {user}
\tthat have been completed:                        \t{percentage_user_comp}
\t-----------------------------------------------------------
\tThe percentage of the tasks assigned to {user} 
\tthat must still be completed:                    \t{percentage_user_uncomp}
\t-----------------------------------------------------------
\tThe percentage of the tasks assigned to {user} 
\tthat has not yet been completed and are overdue: \t{percentage_user_overdue}
\t-----------------------------------------------------------'''
        
        # Write the string to file:
        with open("user_overview.txt", 'a') as users_file:
            print(user_detail, file=users_file)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.'''

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

#-----MAIN MENU SECTION-----
def main():
    while True:
        # presenting the menu to the user and 
        # making sure that the user input is converted to lower case.
        print()
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    gr - Generate reports                 
    ds - Display statistics
    e - Exit
    : ''').lower()

        if menu == 'r':
            reg_user()
            
        elif menu == 'a':
            add_task()

        elif menu == 'va':
            view_all()     

        elif menu == 'vm':
            view_mine()
                    
        elif menu == 'gr':
            generate_reports()

        elif menu == 'ds' and curr_user == 'admin':  
            if (not os.path.exists("task_overview.txt") or not 
                os.path.exists("user_overview.txt")):
                generate_reports()

            with open('task_overview.txt') as f:
                task_overview_stats = f.read()
                print(task_overview_stats)

            with open('user_overview.txt') as f:
                user_overview_stats = f.read()
                print(user_overview_stats)


        elif menu == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("You have made a wrong choice, Please Try again")

main()