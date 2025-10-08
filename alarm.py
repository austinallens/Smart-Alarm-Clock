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

# Get current time
now = datetime.datetime.now().strftime("%H:%M") 

# Checks current time every 5 seconds and sets off Beep when 
# equal to alarm time then ends when the correct solution is input
def alarm_clock(alarm_time):
    while True:
        if now == alarm_time:
            beeping = threading.Thread(target=Beep, daemon=True)
            beeping.start()
            while True:
                answer = input("Solution?: ") # Should be swapped out to a GUI display and input when made
                if answer == solution:
                    return
                

        time.sleep(5)  # check every 5 seconds

# Example usage
alarm_time = input("Enter alarm time (HH:MM, 24-hour format): ") #Should be swapped out for input from GUI
alarm_clock(alarm_time)
