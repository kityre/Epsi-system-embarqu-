
import datetime
import time
import threading
import random
import operator



################################################################################
#   Watchdog to stop tasks
################################################################################
class Watchdog(threading.Thread):

	period = -1
	current_cpt = -1

    	############################################################################
	def __init__(self, period):

		self.period = period
		
		threading.Thread.__init__(self)


    	############################################################################
	def run(self):

		print(" : Starting watchdog")

		self.current_cpt = self.period

		while (1):

			if(self.current_cpt >= 0):

				self.current_cpt -= 1
				time.sleep(1)
				
			else :
				global watchdog
				watchdog = True
				self.current_cpt = self.period



################################################################################
#   Handle all connections and rights for the server
################################################################################
class my_task():


	name = None
	priority = -1
	period = -1
	execution_time = -1
	last_deadline = -1
	last_execution_time = None


    	############################################################################
	def __init__(self, name, priority, period, execution_time, last_execution):

		self.name = name
		self.priority = priority
		self.period = period
		self.execution_time = execution_time
		self.last_execution_time = last_execution


	############################################################################
	def run(self):

		# Update last_execution_time
		self.last_execution_time = datetime.datetime.now()

		global watchdog
		
		execution_time = random.randint(2, 30)

		print(self.name + " : Starting task (" + self.last_execution_time.strftime("%H:%M:%S") + ") : execution time = " + str(execution_time))

		while (watchdog == False):

			execution_time -= 1

			time.sleep(1)

			if (execution_time <= 0):
				print(self.name + " : Terminating normally (" + datetime.datetime.now().strftime("%H:%M:%S") + ")")
				return
		

		print(self.name + " : Pre-empting task (" + datetime.datetime.now().strftime("%H:%M:%S") + ")")

	

####################################################################################################
#
#
#
####################################################################################################
if __name__ == '__main__':

    

    nbWheel = 0
    nbMotor = 0
    oil = 0

	# Init and instanciation of watchdog
   


    last_execution = datetime.datetime.now()
	
	# Instanciation of task objects
    task_list = []
    task_list.append(my_task(name="pump_1", priority = 1, period = 5, execution_time = 2, last_execution = last_execution))
    task_list.append(my_task(name="pump_2", priority = 1, period = 15, execution_time = 3, last_execution = last_execution))
    task_list.append(my_task(name="motor_1", priority = 1, period = 5, execution_time = 5, last_execution = last_execution))
    task_list.append(my_task(name="motor_2", priority = 1, period = 5, execution_time = 3, last_execution = last_execution))

    print("wait 10 sec")
    time.sleep(10)
	# Global scheduling loop
    print("Start task at "+ str(datetime.datetime.now()) +" :" )
    while(1):
	
        for task_to_run in task_list :
		
            if task_to_run.name  == "pump_1":
                if oil == 0 :
                    task_to_run.priority = 1
                if oil > 0 and oil < 26:
                    task_to_run.priority = 2
                if oil > 25 and oil < 50:
                    task_to_run.priority = 3
                if oil == 50:
                    task_to_run.priority = 4
                    
                if operator.ge(datetime.datetime.now(), last_execution + datetime.timedelta(0, task_to_run.period)) and task_to_run.priority != 4:
                    if task_to_run.priority == 1:
                        oil += 10
                        time.sleep(task_to_run.execution_time)
                        task_to_run.last_execution_time = datetime.datetime.now()
                    if task_to_run.priority == 2:
                        oil += 10
                        time.sleep(task_to_run.execution_time)  
                        task_to_run.last_execution_time = datetime.datetime.now()    
                        
                    if oil > 50:
                        oil = oil - (oil - 50)
                    print( task_to_run.last_execution_time.strftime("%H:%M:%S") +" :" + task_to_run.name + ": add 10 oil in tank. Tank have now " + str(oil) + " oil")
                
            if task_to_run.name  ==  "pump_2":
                if oil == 0 :
                    task_to_run.priority = 1
                if oil > 0 and oil < 26:
                    task_to_run.priority = 2
                if oil > 25 and oil < 50:
                    task_to_run.priority = 3
                if oil == 50:
                    task_to_run.priority = 4
                    
                if operator.ge(datetime.datetime.now(), last_execution + datetime.timedelta(0, task_to_run.period)) and task_to_run.priority < 4:
                    if task_list.__getitem__(0).priority < 3:
                       if task_to_run.priority == 1:
                           oil += 20
                           time.sleep(task_to_run.execution_time)
                           task_to_run.last_execution_time = datetime.datetime.now()
                       if task_to_run.priority == 2:
                           oil += 20
                           time.sleep(task_to_run.execution_time)  
                           task_to_run.last_execution_time = datetime.datetime.now()                          
                       if oil > 50:
                           oil = oil - (oil - 50)
                       print(task_to_run.last_execution_time.strftime("%H:%M:%S") +" :" + task_to_run.name + ": add 20 oil in tank. Tank have now " + str(oil) + " oil")
            
                    
            if task_to_run.name  ==  "motor_2":
                if nbWheel / 4 < nbMotor :
                    task_to_run.priority = 1
                else:
                    task_to_run.priority = 2
                    
                if operator.ge(datetime.datetime.now(), last_execution + datetime.timedelta(0, task_to_run.period)):
                    if task_to_run.priority == 1 and operator.ge(oil, 5):
                        nbWheel += 1
                        oil -= 5
                        time.sleep(task_to_run.execution_time)
                        task_to_run.last_execution_time = datetime.datetime.now()
                        
                        print(task_to_run.last_execution_time.strftime("%H:%M:%S") +" :" + task_to_run.name + ": add 1 wheel. Now we have " + str(nbWheel)+  " Wheel and " + str(oil) + " oil")   
                    if task_to_run.priority == 2 and operator.ge(oil, 5):
                        nbWheel += 1
                        oil -= 5
                        time.sleep(task_to_run.execution_time)
                        task_to_run.last_execution_time = datetime.datetime.now()  

                        print(task_to_run.last_execution_time.strftime("%H:%M:%S") +" :" + task_to_run.name + ": add 1 wheel. Now we have " + str(nbWheel)+  " Wheel and " + str(oil) + " oil")                            
            
            if task_to_run.name  ==  "motor_1":
                if nbWheel / 4 > nbMotor :
                    task_to_run.priority = 1
                else:
                    task_to_run.priority = 2
                    
                if operator.ge(datetime.datetime.now(), last_execution + datetime.timedelta(0, task_to_run.period)):
                    if task_to_run.priority == 1 and operator.ge(oil, 25):
                        nbMotor += 1
                        oil -= 25
                        time.sleep(task_to_run.execution_time)
                        task_to_run.last_execution_time = datetime.datetime.now()
                        print(task_to_run.last_execution_time.strftime("%H:%M:%S") +" :" + task_to_run.name + ": add 1 motor. Now we have " + str(nbMotor)+  " motor and " + str(oil) + " oil")  
                    if task_to_run.priority == 2 and task_list.__getitem__(3).priority != 1  and operator.ge(oil, 25):
                        nbMotor += 1
                        oil -= 25
                        time.sleep(task_to_run.execution_time)
                        task_to_run.last_execution_time = datetime.datetime.now()  

                        print(task_to_run.last_execution_time.strftime("%H:%M:%S") +" :" + task_to_run.name + ": add 1 motor. Now we have " + str(nbMotor)+  " motor and " + str(oil) + " oil")  
            
            
			
			
			
		
		
		

