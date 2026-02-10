import tkinter as tk
import requests
import webbrowser
import json

# ---------- CONFIG ----------
VIEWER_USER = "viewer"
VIEWER_PWD = "100225"

ADMIN_USER = "jay"
ADMIN_PWD = "p0s1t1ve"

DATA_URL = "https://drive.google.com/uc?id=106HX8DXqMs3cm07r6ECtIpbHk8OtisFS"
EDIT_URL = "https://drive.google.com/file/d/106HX8DXqMs3cm07r6ECtIpbHk8OtisFS/view"

login_count = 0


# ---------- DATA ----------
def load_data():
    try:
        return requests.get(DATA_URL).json()
    except:
        return {"jar": [], "greetings": []}


data = load_data()
jar = data.get("jar", [])
greetings = data.get("greetings", [])


# ---------- WINDOW ----------
root = tk.Tk()
root.title("The Love Jar")
root.geometry("600x450")
root.configure(bg="#111")


# ---------- HELPERS ----------
def clear():
    for f in (login_frame, home_frame, admin_frame, list_frame):
        f.pack_forget()


def exit_app():
    root.destroy()


# ---------- LOGIN ----------
def login():
    global login_count
    user = user_entry.get().strip()
    pwd = pass_entry.get().strip()

    if user == VIEWER_USER and pwd == VIEWER_PWD:
        login_count += 1
        clear()
        home_frame.pack(expand=True)

    elif user == ADMIN_USER and pwd == ADMIN_PWD:
        clear()
        admin_frame.pack(expand=True)

    else:
        error_label.config(text="invalid login")


login_frame = tk.Frame(root, bg="#111")
login_frame.pack(expand=True)

tk.Label(login_frame, text="the love jar", fg="white", bg="#111",
         font=("Georgia", 20)).pack(pady=20)

user_entry = tk.Entry(login_frame)
user_entry.pack(pady=5)

pass_entry = tk.Entry(login_frame, show="*")
pass_entry.pack(pady=5)

tk.Button(login_frame, text="login", command=login).pack(pady=10)

error_label = tk.Label(login_frame, fg="red", bg="#111")
error_label.pack()


# ---------- HOME (VIEWER) ----------
home_frame = tk.Frame(root, bg="#111")

tk.Label(home_frame, text="🫙", font=("Georgia", 40),
         bg="#111", fg="white").pack(pady=10)

tk.Button(home_frame, text="exit", command=exit_app).pack(pady=6)


# ---------- ADMIN ----------
admin_frame = tk.Frame(root, bg="#111")

tk.Label(admin_frame, text="admin panel",
         fg="white", bg="#111", font=("Georgia", 18)).pack(pady=15)

input_box = tk.Text(admin_frame, height=3, width=45)
input_box.pack(pady=8)

def add_greeting():
    text = input_box.get("1.0", "end").strip()
    if text:
        greetings.append(text)
        input_box.delete("1.0", "end")
        status.config(text="greeting added")

def add_jar():
    text = input_box.get("1.0", "end").strip()
    if text:
        jar.append(text)
        input_box.delete("1.0", "end")
        status.config(text="jar item added")

def view_list(title, items):
    clear()
    list_frame.pack(expand=True)
    list_label.config(text=title)
    text_area.delete("1.0", "end")
    for i, item in enumerate(items, 1):
        text_area.insert("end", f"{i}. {item}\n\n")

tk.Button(admin_frame, text="a. add greeting", command=add_greeting).pack()
tk.Button(admin_frame, text="b. add jar item", command=add_jar).pack()
tk.Button(admin_frame, text="c. view jar",
          command=lambda: view_list("jar items", jar)).pack()
tk.Button(admin_frame, text="d. view greetings",
          command=lambda: view_list("greetings", greetings)).pack()

def show_login_count():
    status.config(text=f"login count: {login_count}")

def reset_login_count():
    global login_count
    login_count = 0
    status.config(text="login count reset")

tk.Button(admin_frame, text="e. view login count",
          command=show_login_count).pack()
tk.Button(admin_frame, text="f. reset login count",
          command=reset_login_count).pack()

tk.Button(admin_frame, text="g. exit", command=exit_app).pack(pady=6)

tk.Button(admin_frame, text="open json (drive)",
          command=lambda: webbrowser.open(EDIT_URL)).pack(pady=4)

status = tk.Label(admin_frame, fg="#aaa", bg="#111")
status.pack(pady=8)


# ---------- LIST VIEW ----------
list_frame = tk.Frame(root, bg="#111")

list_label = tk.Label(list_frame, fg="white",
                      bg="#111", font=("Georgia", 16))
list_label.pack(pady=10)

text_area = tk.Text(list_frame, width=60, height=15)
text_area.pack()

tk.Button(list_frame, text="back",
          command=lambda: (clear(), admin_frame.pack(expand=True))).pack(pady=8)


# ---------- START ----------
root.mainloop()
