
# import json
# from datetime import datetime

# class employee:
#     main_task_list = []

#     def __init__(self, emp_name, emp_id):
#         self.emp_name = emp_name
#         self.emp_id = emp_id
#         self.login_time = datetime.now().strftime("%Y-%m-%d %H:%M")
#         self.logout_time = datetime.now().strftime("%Y-%m-%d %H:%M")
#         self.tasks = []

#     def log_in(self):
      
#         print(f"{self.emp_name} logged in at {self.login_time}")

#     def log_out(self):
               
#         print(f"{self.emp_name} logged out at {self.logout_time}")
#         self.save_to_json()

#     def add_task(self, task_title, task_description, task_success):
#         task = {
#             "task_title": task_title,
#             "task_description": task_description,
#             "start_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
#             "end_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
#             "task_success": task_success
#         }
#         self.tasks.append(task)
    
        

#     def save_to_json(self):
#         daily_task_data = {
#             "emp_name": self.emp_name,
#             "emp_id": self.emp_id,
#             "login_time": self.login_time,
#             "logout_time": self.logout_time,
#             "tasks": self.tasks
#         }
#         filename = f"{datetime.now().strftime('%Y-%m-%d')}_{self.emp_name}.json"
#         with open(filename, "w") as json_file:
#             json.dump(daily_task_data, json_file, indent=4)
        
#         self.main_task_list.append(daily_task_data)


# employee1 = employee("surya", 1)
# employee1.log_in()
# employee1.add_task("python task","create a employee working hour and task tracking system",True)
# employee1.add_task("second task","create a employee working hour and task tracking system",True)
# employee1.log_out()



# print( employee.main_task_list)











 
