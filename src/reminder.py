import tkinter as tk
from tkinter import Toplevel
import threading
import time
import os
import pygame

class ReminderApp:
    def __init__(self, root, interval, play_music):
        self.root = root
        pygame.mixer.init()
        self.interval = interval  # Interval in seconds
        self.play_music = play_music
        self.music_file = "music.mp3"
        self.reminder_active = False
        self.next_reminder_time = time.time() + self.interval  # Initialize the next reminder time
        self.start_timer()

    def start_timer(self):
        self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
        self.timer_thread.start()

    def run_timer(self):
        while True:
            current_time = time.time()
            # Check if it's time for the next reminder and if the reminder window is not currently active
            if current_time >= self.next_reminder_time and not self.reminder_active:
                self.show_reminder()
                # Wait for the reminder window to close before calculating the next reminder time
                while self.reminder_active:
                    time.sleep(1)  # Short sleep to prevent high CPU usage
                # Set the next reminder time
                self.next_reminder_time = time.time() + self.interval

    def show_reminder(self):
        self.reminder_active = True
        self.reminder_window = Toplevel(self.root)
        self.reminder_window.title("Reminder")
        self.reminder_window.state('zoomed')
        self.reminder_window.configure(background='black')
        label = tk.Label(self.reminder_window, text="Time for a break!", fg="white", bg="black", font=("Helvetica", 32))
        label.pack(expand=True)
        self.reminder_window.attributes('-topmost', True)  # Make window topmost
        self.reminder_window.protocol("WM_DELETE_WINDOW", self.on_close_reminder)

        if self.play_music and os.path.exists(self.music_file):
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.play()


    def on_close_reminder(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
        self.reminder_window.destroy()
        self.reminder_active = False  # Allow the timer to continue

def main():
    interval = int(input("Enter the time in minutes for the reminder (default 35): ") or 35) * 60
    play_music = input("Do you want to play music (y/n)? ").lower().startswith('y')

    root = tk.Tk()
    root.withdraw()

    app = ReminderApp(root, interval, play_music)
    print("Github repo: https://github.com/k-msalehi/breakReminder")
    print("OK, Reminder started!")
    root.mainloop()

    pygame.mixer.quit()

if __name__ == "__main__":
    main()
