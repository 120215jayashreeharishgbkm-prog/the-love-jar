from tkinter import messagebox
import tkinter as tk
import json, random

#--conf--

VIEWER_USER = "krishnag"
VIEWER_PWD = "100225"
ADMIN_USER = "jay"

# load json
with open("data1.json","r") as f:
    d = json.load(f)

ap = d["ap"]
quotes = d.get("jar", [])
greets = d.get("greetings", [])
lc = d.get("lc", 0)
idx = 0

#--funcs--

def save_json():
    """save current data back to json"""
    with open("data1.json","w") as f:
        json.dump(d, f, indent=4)

def login():
    global lc
    u = username_entry.get().strip()
    p = password_entry.get().strip()
    if u == VIEWER_USER and p == VIEWER_PWD:
        # increment login count
        lc += 1
        d["lc"] = lc
        save_json()  # save updated count
        login_frame.pack_forget()
        home_frame.pack(expand=True)
        if not quotes:
            tk.messagebox.showinfo("Jar empty","your jar is empty 😢")
    elif u == ADMIN_USER and p == ap:
        login_frame.pack_forget()
        admin_frame.pack(expand=True)
    else:
        error_label.config(text="invalid login")

def show_q():
    if quotes:
        quote_label.config(text=quotes[idx])
    else:
        quote_label.config(text="(jar empty)")

def nxt():
    global idx
    if idx < len(quotes)-1:
        idx += 1
        show_q()

def prev():
    global idx
    if idx > 0:
        idx -= 1
        show_q()

def open_j():
    home_frame.pack_forget()
    jar_frame.pack(expand=True)
    if greets:
        greeting_label.config(text=random.choice(greets))
    show_q()

def exa():
    root.destroy()

#--admin funcs--

def add_greet():
    s = admin_entry.get().strip()
    if s:
        greets.append(s)
        d["greetings"] = greets
        save_json()
        admin_entry.delete(0, tk.END)
        status_label.config(text="added greet ✔")

def add_jar():
    s = admin_entry.get().strip()
    if s:
        quotes.append(s)
        d["jar"] = quotes
        save_json()
        admin_entry.delete(0, tk.END)
        status_label.config(text="added jar item ✔")

def view_jar():
    tk.messagebox.showinfo("Jar Items","\n".join(quotes))

def view_greet():
    tk.messagebox.showinfo("Greetings","\n".join(greets))

def view_lc():
    tk.messagebox.showinfo("Login Count",f"Viewer logins: {lc}")

def reset_lc():
    global lc
    lc = 0
    d["lc"] = lc
    save_json()
    status_label.config(text="login count reset ✔")

#--ui--

root = tk.Tk()
root.title("The Love Jar")
root.geometry("560x400")
root.configure(bg="#111")

login_frame = tk.Frame(root, bg="#111")
login_frame.pack(expand=True)

tk.Label(login_frame,text="the love jar",fg="white",bg="#111",font=("Georgia",20)).pack(pady=20)
username_entry = tk.Entry(login_frame); username_entry.pack(pady=5)
password_entry = tk.Entry(login_frame,show="*"); password_entry.pack(pady=5)
tk.Button(login_frame,text="login",command=login).pack(pady=10)
error_label = tk.Label(login_frame,text="",fg="red",bg="#111"); error_label.pack()

# viewer home
home_frame = tk.Frame(root,bg="#111")
tk.Label(home_frame,text="🫙",font=("Georgia",40),bg="#111",fg="white").pack(pady=10)
tk.Button(home_frame,text="open jar",command=open_j).pack(pady=6)
tk.Button(home_frame,text="exit",command=exa).pack(pady=6)

# jar frame
jar_frame = tk.Frame(root,bg="#111")
greeting_label = tk.Label(jar_frame,fg="#aaa",bg="#111",wraplength=480,font=("Georgia",11),justify="center")
greeting_label.pack(pady=10)
quote_label = tk.Label(jar_frame,fg="white",bg="#111",wraplength=480,font=("Georgia",14),justify="center")
quote_label.pack(pady=30)
btn_frame = tk.Frame(jar_frame,bg="#111"); btn_frame.pack()
tk.Button(btn_frame,text="prev",command=prev).grid(row=0,column=0,padx=15)
tk.Button(btn_frame,text="next",command=nxt).grid(row=0,column=1,padx=15)

# admin frame
admin_frame = tk.Frame(root,bg="#111")
tk.Label(admin_frame,text="admin · the love jar",fg="white",bg="#111",font=("Georgia",18)).pack(pady=20)
admin_entry = tk.Entry(admin_frame); admin_entry.pack(pady=6)
tk.Button(admin_frame,text="add greet",command=add_greet).pack(pady=3)
tk.Button(admin_frame,text="add jar",command=add_jar).pack(pady=3)
tk.Button(admin_frame,text="view jar",command=view_jar).pack(pady=3)
tk.Button(admin_frame,text="view greets",command=view_greet).pack(pady=3)
tk.Button(admin_frame,text="view login count",command=view_lc).pack(pady=3)
tk.Button(admin_frame,text="reset login count",command=reset_lc).pack(pady=3)
tk.Button(admin_frame,text="exit",command=exa).pack(pady=6)
status_label = tk.Label(admin_frame,text="",fg="#aaa",bg="#111"); status_label.pack(pady=10)

root.mainloop()
