import time
import datetime
import winsound  
import threading
from pathlib import Path

# Try to import pygame for custom sounds, fallback to winsound
try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("pygame not available, using winsound beeps only")

#Looping beep that increases in length over time

def Beep(stop_event, volume=50, sound_file=None):
    """
    Play alarm sound - either custom sound file or beep.
    volume: 0-100 percentage.
    sound_file: path to audio file (mp3, wav, ogg).
    """
    if sound_file and PYGAME_AVAILABLE and Path(sound_file).exists():
        # Play custom sound using pygame
        try:
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.set_volume(volume / 100.0)

            while not stop_event.is_set():
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play()
                time.sleep(0.1)
            
            pygame.mixer.music.stop()
            return
        except Exception as e:
            print(f"Error playing sound file: {e}")
            print("Falling back to beep")

    # Fallback to winsound beep
    length = 500
    # Map volume (0-100) to frequency (500-2000 Hz)
    base_freq = 500 + (volume * 15)

    while not stop_event.is_set():
        try:
            winsound.Beep(1000, length)
            length += 25
            time.sleep((length/1000)+0.2)
        except Exception as e:
            print(f"Beep error: {e}")
            time.sleep(1)

# Checks current time every 5 seconds and sets off Beep when 
# equal to alarm time then ends when the correct solution is input
def alarm_clock(alarm_time, stop_event, on_alarm_trigger=None, check_solution=None,
                volume=50, sound_file=None):
    """
    Checks current time every 5 seconds and triggers alarm
    volume: 0-100 percentage for alarm volume
    sound_file: optional path to custom sound file
    """
    while not stop_event.is_set():
        # Get current time
        now = datetime.datetime.now().strftime("%H:%M")
        
        if now == alarm_time:
            beeping_thread = threading.Thread(
                target=Beep, 
                args=(stop_event, volume, sound_file), 
                daemon=True
            )
            beeping_thread.start()


            # Updates the GUI
            if on_alarm_trigger:
                result = on_alarm_trigger()
                if result: # User answered correctly
                    stop_event.set()
                    beeping_thread.join()
                    return # Stops the Alarm                

        time.sleep(5)  # check every 5 seconds

def start_alarm(alarm_time, on_alarm_trigger=None, check_solution=None,
                volume=50, sound_file=None):
    """
    Starts an alarm in a background thread to allow usage with GUI
    volume: 0-100 percentage for alarm volume
    sound_file: optional path to custom sound file
    """
    # Starts an alarm in a background thread to allow usage with GUI
    stop_event = threading.Event()
    alarm_thread = threading.Thread(
        target=alarm_clock,
        args=(alarm_time, stop_event, on_alarm_trigger, check_solution, volume, sound_file),
        daemon=True
    )
    alarm_thread.start()
    return {'thread': alarm_thread, 'stop_event': stop_event}
