import time
import datetime
import winsound  
import threading

#Current stand in math problem, should be replaced by inputs from section C
mathProblem = "2+2"
solution = "4"

#Looping beep that increases in length over time
def Beep():
    length = 500
    while True:
        winsound.Beep(1000, length)
        length += 25
        time.sleep((length/1000)+0.2)

# Checks current time every 5 seconds and sets off Beep when 
# equal to alarm time then ends when the correct solution is input
def alarm_clock(alarm_time, on_alarm_trigger=None, check_solution=None):
    
    global beep_active

    while True:
        # Get current time
        now = datetime.datetime.now().strftime("%H:%M")
        
        if now == alarm_time:
            beep_active = True
            beeping_thread = threading.Thread(target=Beep, daemon=True)
            beeping_thread.start()

            # Updates the GUI
            if on_alarm_trigger:
                on_alarm_trigger()

            # Waits for correct solution
            while True:
                time.sleep(0.5)
                if check_solution and check_solution():
                    beep_active = False
                    return # Stops the Alarm
                

        time.sleep(5)  # check every 5 seconds

def start_alarm(alarm_time, on_alarm_trigger=None, check_solution=None):
    # Starts an alarm in a background thread to allow usage with GUI
    alarm_thread = threading.Thread(
        target=alarm_clock,
        args=(alarm_time, on_alarm_trigger, check_solution),
        daemon=True
    )
    alarm_thread.start()
    return alarm_thread

# Only run this if the file is executed directly (not imported)
if __name__ == "__main__":
    alarm_time = input("Enter alarm time (HH:MM, 24-hour format): ")
    
    def simple_check():
        answer = input("Solution?: ")
        return answer == solution
    
    alarm_clock(alarm_time, check_solution=simple_check)
