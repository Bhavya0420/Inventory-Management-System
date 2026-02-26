from tkinter import *
from tkinter import ttk, messagebox
from employees import connect_database
from admin_dashboard import admin_dashboard
from employee_dashboard import employee_dashboard
import welcome

def go_back(root):
    for widget in root.winfo_children():
        widget.destroy()
    welcome.show_welcome(root)

def login(root):
    empid = empid_entry.get()
    password = password_entry.get()
    role = role_combobox.get()

    if empid == "" or password == "":
        messagebox.showerror("Error", "All fields are required")
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    cursor.execute("USE inventory_system")
    cursor.execute(
        "SELECT * FROM employee_data WHERE empid=%s AND password=%s AND usertype=%s",
        (empid, password, role)
    )

    row = cursor.fetchone()
    connection.close()

    if row:
        messagebox.showinfo("Success", "Login Successful")
        for widget in root.winfo_children():
            widget.destroy()

        if role == "Admin":
            admin_name = row[1]
            admin_dashboard(root,admin_name)
        else:
            employee_dashboard(root)
    else:
        messagebox.showerror("Error", "Invalid Credentials")


# ---------------- MAIN WINDOW ---------------- #
def login_page(main_root):
    global root,back_image,empid_entry, password_entry,role_combobox
    root=main_root
    root.title("Login - Inventory System")
    root.geometry('1270x675+0+0')
    root.resizable(False, False)
    root.config(bg="white")

    # ---------------- LEFT FRAME (IMAGE) ---------------- #

    left_frame = Frame(root, bg="white")
    left_frame.place(x=0, y=0, width=800, height=675)

    back_image=PhotoImage(file='images/back_button.png')
    back_button=Button(left_frame,image=back_image,bd=0, cursor='hand2',bg='white',command=lambda: go_back(root))
    back_button.place(x=30,y=30)

    bg_image = PhotoImage(file="images/login.png")  # Add your image here
    image_label = Label(left_frame, image=bg_image,bg='white')
    image_label.place(x=0, y=0, relwidth=1, relheight=1)

    back_button.lift()

    # Prevent image garbage collection
    left_frame.bg_image = bg_image


    # ---------------- RIGHT FRAME (FORM) ---------------- #

    right_frame = Frame(root, bg="white")
    right_frame.place(x=800, y=0, width=470, height=675)

    title = Label(right_frame, text="Login",
                font=("times new roman", 28, "bold"),
                bg="white", fg="#096499")
    title.place(x=180, y=150)

    # Employee ID
    Label(right_frame, text="Employee ID",
        font=("times new roman", 16),
        bg="white").place(x=70, y=230)

    empid_entry = Entry(right_frame,
                        font=("times new roman", 15),
                        bg="#f0f0f0")
    empid_entry.place(x=70, y=260, width=320, height=35)

    # Password
    Label(right_frame, text="Password",
        font=("times new roman", 16),
        bg="white").place(x=70, y=310)

    password_entry = Entry(right_frame,
                        show="*",
                        font=("times new roman", 15),
                        bg="#f0f0f0")
    password_entry.place(x=70, y=340, width=320, height=35)

   # Eye Images
    eye_open = PhotoImage(file="images/eye_open.png")
    eye_close = PhotoImage(file="images/eye_close.png")

    # Toggle Function
    def toggle_password():
        if password_entry.cget("show") == "":
            password_entry.config(show="*")
            eye_button.config(image=eye_close)
        else:
            password_entry.config(show="")
            eye_button.config(image=eye_open)

    # Eye Button
    eye_button = Button(right_frame,
                        image=eye_close,
                        bd=0,
                        bg="#f0f0f0",
                        activebackground="white",
                        cursor="hand2",
                        command=toggle_password)
    eye_button.place(x=360, y=345)

    # Role Selection
    Label(right_frame, text="Select Role",
        font=("times new roman", 16),
        bg="white").place(x=70, y=390)

    role_combobox = ttk.Combobox(right_frame,
                                values=("Admin", "Employee"),
                                state="readonly",
                                font=("times new roman", 14))
    role_combobox.place(x=70, y=420, width=320, height=35)
    role_combobox.current(0)

    # Login Button
    Button(right_frame, text="Login",
        font=("times new roman", 18, "bold"),
        bg="#010c48",
        fg="white",
        cursor="hand2",
        command=lambda: login(root)).place(x=70, y=490, width=320, height=45)
    root.bind("<Return>", lambda event: login(root))

