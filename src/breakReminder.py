import tkinter as tk
from tkinter import Toplevel
import time
import os
import json
import random
from datetime import datetime

class ReminderApp:
    def __init__(self, root, interval, reminder_messages):
        self.root = root
        self.interval = interval * 1000  # Convert to milliseconds for `after`
        self.reminder_messages = reminder_messages
        self.reminder_active = False
        self.schedule_next_reminder()

    def schedule_next_reminder(self):
        """Schedule the next reminder using tkinter's event loop."""
        self.root.after(self.interval, self.show_reminder)

    def show_reminder(self):
        """Display the reminder message."""
        if self.reminder_active:
            return  # Prevent overlapping reminders

        print("Reminder displayed at:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.reminder_active = True

        self.reminder_window = Toplevel(self.root)
        self.reminder_window.title("Break Reminder")
        self.reminder_window.attributes('-zoomed', True) # use topmost instad of zoomed in windows
        self.reminder_window.configure(background='black')

        # Random message selection
        message = random.choice(self.reminder_messages)
        label = tk.Label(self.reminder_window, text=message, fg="white", bg="black", font=("Helvetica", 32))
        label.pack(expand=True)

        self.reminder_window.attributes('-topmost', True)
        self.reminder_window.protocol("WM_DELETE_WINDOW", self.on_close_reminder)

    def on_close_reminder(self):
        """Close the reminder window and schedule the next one."""
        self.reminder_window.destroy()
        self.reminder_active = False
        print("Reminder closed at:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.schedule_next_reminder()  # Schedule the next reminder


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config.json')

    with open(config_path) as f:
        config = json.load(f)

    interval = int(config.get("reminderInMinutes", 35)) * 60
    reminder_messages = config.get("reminderMessages", ["Time for a break!"])

    root = tk.Tk()
    root.withdraw()

    ReminderApp(root, interval, reminder_messages)
    print("Reminder started at:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    root.mainloop()


if __name__ == "__main__":
    main()
