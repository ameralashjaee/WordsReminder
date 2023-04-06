from cgitb import text
import threading
import tkinter as tk
from tkinter import ACTIVE, BOTH, END, LEFT, RIGHT, Button, Entry, Label, Toplevel, messagebox
import sqlite3
import time

import sqlite3
import time

from tkinter import filedialog

from tkinter import Y
from tkinter import *
import pyttsx3
import winsound
from PIL import ImageTk, Image



engine = pyttsx3.init()
is_started = False
stop_event = threading.Event()

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('mywords.db')


# Create a table
# conn.execute('''CREATE TABLE WORDS
#              (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
#              eng           TEXT    NOT NULL,
#              ara    TEXT     NOT NULL,
#              explain           TEXT NOT NULL
#              image_path         TEXT NULL);''')

# Commit the changes
# conn.commit()

c = conn.cursor()
c.execute("select * from WORDS")


row=c.fetchall()
for wors in row:
 print(wors)
# Close the connection


def save_word():
    eng1 = eng.get()
    ara1 = ara.get()
    exp1 = exp.get()
    img_path = path
    print(path)
    if len(eng1)==0 or len(ara1)==0 or len(exp1)==0:
        messagebox.showinfo("Success", "error entry!")
    else:
        c = conn.cursor()
        a=c.execute("SELECT ID FROM WORDS WHERE eng=(?)",(eng1,)).fetchone()
        if a:
            messagebox.showinfo("Success", "this word is saved before")
        else:
            c = conn.cursor()
            c.execute("INSERT INTO WORDS (eng, ara,explain,image_path) VALUES (?, ?, ?,?)", (eng1, ara1,exp1,img_path))
            conn.commit()
            messagebox.showinfo("Success", "Word saved successfully!")


def send_notification():
#  time.sleep(300)
 global is_started
 while not stop_event.is_set():

    winsound.MessageBeep(1000)
    conn = sqlite3.connect('mywords.db')
    c = conn.cursor()
    c.execute("SELECT eng, ara, explain, image_path FROM WORDS ORDER BY RANDOM() LIMIT 1")
    row = c.fetchone()
    if row:

        eng, ara, explain, image_path = row
        if image_path:
            top = Toplevel()
            top.attributes("-topmost", True)

            screen_width = top.winfo_screenwidth()
            screen_height = top.winfo_screenheight()
            window_width = 400
            window_height = 500
            x_coordinate = (screen_width/2) - (window_width/2)
            y_coordinate = (screen_height/2) - (window_height/2)

            top.geometry("{}x{}+{}+{}".format(window_width, window_height, int(x_coordinate), int(y_coordinate)))
            try:
                image = Image.open(image_path)
                image = image.resize((300, 300), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(image)
                image_label = Label(top, image=photo)
                image_label.image = photo
                image_label.pack()
            except OSError:
                default_image = Image.new('RGB', (300, 300), color='white')
                photo = ImageTk.PhotoImage(default_image)
                image_label = Label(top, image=photo)
                image_label.image = photo
                image_label.pack()
        else:
            top = Toplevel()
            top.attributes("-topmost", True)

            screen_width = top.winfo_screenwidth()
            screen_height = top.winfo_screenheight()
            window_width = 200
            window_height = 200
            x_coordinate = (screen_width/2) - (window_width/2)
            y_coordinate = (screen_height/2) - (window_height/2)

            image_label = Label(top, text="")
            image_label.pack()


        text_label = Label(top, text=f"{eng}\n{ara}\n{explain}")
        text_label.pack()

        entry = Entry(top)
        entry.pack()

        def check():
            if entry.get() == eng:
                top.destroy()
            else:
                entry.config(bg='red')

        def speak():
            engine = pyttsx3.init()
            engine.say(f"{eng}")
            engine.runAndWait()

        check_button = Button(top, text="Check", command=check)
        check_button.pack()

        s_button = Button(top, text="speak", command=speak)
        s_button.pack()

        top.wait_window()
        time.sleep(300)
 is_started = False



def start():
    global is_started
    if is_started:
        print("App is already in start mode")
    else:
        winsound.Beep(500,150)
        global t
        t = threading.Thread(target=send_notification)
        t.start()
        is_started = True
        print("App started")

def stop():
    global is_started
    stop_event.set()
    is_started = False
    print("App stopped")






def show_all_words():
    # Connect to the database

    c = conn.cursor()

    # Get all the words from the database
    c.execute("SELECT * FROM WORDS")
    rows = c.fetchall()

    # Create a new window to display the words
    word_window = tk.Toplevel()
    word_window.title("All Words")

    # Create a listbox to display the words
    word_listbox = tk.Listbox(word_window)
    word_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add each word to the listbox
    for row in rows:
        word_listbox.insert(tk.END, row[1])

    # Create a frame to hold the editing controls
    edit_frame = tk.Frame(word_window)
    edit_frame.pack(side=tk.RIGHT, fill=tk.Y)

    # Create text boxes for the attributes
    eng_box = tk.Entry(edit_frame)
    ara_box = tk.Entry(edit_frame)
    expl_box = tk.Entry(edit_frame)
    image_box = tk.Entry(edit_frame)

    # Create labels for the text boxes
    eng_label = tk.Label(edit_frame, text="English:")
    ara_label = tk.Label(edit_frame, text="Arabic:")
    expl_label = tk.Label(edit_frame, text="Explanation:")
    image_label = tk.Label(edit_frame, text="Image Path:")

    # Pack the labels and text boxes
    eng_label.pack()
    eng_box.pack()
    ara_label.pack()
    ara_box.pack()
    expl_label.pack()
    expl_box.pack()
    image_label.pack()
    image_box.pack()

    # Create a function to save the changes
    def save_changes():
    # Get the selected word
        if not word_listbox.curselection():
         return
        selected_word = word_listbox.get(word_listbox.curselection())

        # Get the new attribute values from the text boxes
        new_eng = eng_box.get()
        new_ara = ara_box.get()
        new_expl = expl_box.get()
        new_image = image_box.get()

        # Update the word in the database
        if new_eng != "" and new_ara != "" and new_expl != "" and new_image != "":
            c.execute("UPDATE WORDS SET eng=?, ara=?, explain=?, image_path=? WHERE eng=?", (new_eng, new_ara, new_expl, new_image, selected_word))
        else:
            c.execute("DELETE FROM WORDS WHERE eng=?", (new_eng,))
        conn.commit()

        # Clear the text boxes
        eng_box.delete(0, tk.END)
        ara_box.delete(0, tk.END)
        expl_box.delete(0, tk.END)
        image_box.delete(0, tk.END)
        word_listbox.delete(0, tk.END)

        # Get all the words from the database
        c.execute("SELECT * FROM words")
        rows = c.fetchall()

        # Add each word to the listbox
        for row in rows:
            word_listbox.insert(tk.END, row[1])

        # Disable the delete button
        delete_button.config(state=tk.DISABLED)

    # Create a button to delete the selected word
    delete_button = tk.Button(edit_frame, text="Delete Word", command=lambda: c.execute("DELETE FROM WORDS WHERE eng=?", (word_listbox.get(word_listbox.curselection()),)) if len(word_listbox.curselection()) > 0 else None, state=tk.DISABLED)
    delete_button.pack()

    # Bind the listbox selection to enable/disable the delete button
    word_listbox.bind("<<ListboxSelect>>", lambda e: delete_button.config(state=tk.NORMAL) if len(word_listbox.curselection()) > 0 else delete_button.config(state=tk.DISABLED))


    # Create a button to save the changes
    save_button = tk.Button(edit_frame, text="Save Changes", command=save_changes)
    save_button.pack()



def select_img_path():
    file_path = filedialog.askopenfilename()
    global path
    path=file_path

    img_path_label.config(text=file_path)
    
    print(str(file_path))
    return str(file_path)
app = tk.Tk()
app.title("Word Reminder")

word_label = tk.Label(text="Word:")
word_label.grid(row=0, column=0)

eng = tk.Entry()
eng.grid(row=0, column=1)

translation_label = tk.Label(text="Translation:")
translation_label.grid(row=1, column=0)
exp_l = tk.Label(text="explain:")
exp_l.grid(row=2, column=0)
ara = tk.Entry()
ara.grid(row=1, column=1)
exp = tk.Entry()
exp.grid(row=2, column=1)

save_button = tk.Button(text="Save Word", command=save_word)
save_button.grid(row=4, column=0, columnspan=2, pady=10)

start1 = tk.Button(text="start", command=start)
start1.grid(row=5, column=0, columnspan=2, pady=10)

stop_button = tk.Button(text="Stop", command=stop)
stop_button.grid(row=6, column=0, columnspan=2, pady=10)
c = conn.cursor()
c.execute("select * from WORDS")


row=c.fetchall()

word_button = tk.Button(app, text="Show All Words", command=show_all_words)
word_button.grid(row=7, column=0, columnspan=2, pady=10)

img_path_button = tk.Button(text="Image", command=select_img_path)

img_path_button.grid(row=3, column=0, columnspan=2, pady=10)

img_path_label = tk.Label(text="")
img_path_label.grid(row=3, column=2, columnspan=2, pady=10)
app.mainloop()
start()
