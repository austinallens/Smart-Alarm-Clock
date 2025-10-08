import time
import datetime
import winsound  
import threading

#Looping beep that increases in length over time

def Beep(stop_event):
    length = 500
    while not stop_event.is_set:
        winsound.Beep(1000, length)
        length += 25
        time.sleep((length/1000)+0.2)

# Checks current time every 5 seconds and sets off Beep when 
# equal to alarm time then ends when the correct solution is input
def alarm_clock(alarm_time, on_alarm_trigger=None, check_solution=None):
    stop_event = threading.Event()

    while True:
        # Get current time
        now = datetime.datetime.now().strftime("%H:%M")
        
        if now == alarm_time:
            beeping_thread = threading.Thread(target=Beep, args=(stop_event,), daemon=True)
            beeping_thread.start()

            # Updates the GUI
            if on_alarm_trigger:
                on_alarm_trigger()

            # Waits for correct solution
            while True:
                time.sleep(0.5)
                if check_solution and check_solution():
                    stop_event.set()
                    beeping_thread.join()
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
