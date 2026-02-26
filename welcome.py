from tkinter import *
from tkinter import messagebox
import login   # this will open your login page


def open_login(root):
    # Clear current widgets
    for widget in root.winfo_children():
        widget.destroy()

    login.login_page(root)


def show_welcome(root):
    root.title("Welcome - Inventory Management System")
    root.geometry("1270x675+0+0")
    root.resizable(0,0)
    root.config(bg="white")

    # LEFT SIDE (INFO SECTION)
    left_frame = Frame(root, bg="#096499")
    left_frame.place(x=0, y=0, width=800, height=675)

    Label(left_frame,
          text="Inventory\nManagement\nSystem",
          font=("times new roman", 40, "bold"),
          bg="#096499",
          fg="white",
          justify=LEFT).place(x=100, y=180)

    Label(left_frame,
          text="Manage stock, employees, and sales efficiently.\n"
               "Track inventory in real time and improve productivity.\n"
               "Secure login for Admin and Employees.",
          font=("times new roman", 18),
          bg="#096499",
          fg="white",
          justify=LEFT).place(x=100, y=380)

    # RIGHT SIDE (ACTION SECTION)
    right_frame = Frame(root, bg="white")
    right_frame.place(x=800, y=0, width=470, height=675)

    Label(right_frame,
          text="Welcome",
          font=("times new roman", 35, "bold"),
          bg="white",
          fg="#096499").place(x=130, y=200)

    Label(right_frame,
          text="Click below to continue to login",
          font=("times new roman", 16),
          bg="white",
          fg="gray").place(x=90, y=280)

    Button(right_frame,
           text="Go to Login",
           font=("times new roman", 18, "bold"),
           bg="#010c48",
           fg="white",
           cursor="hand2",
           command=lambda:open_login(root)).place(x=90, y=350, width=300, height=50)

def main():
    root = Tk()
    show_welcome(root)
    root.mainloop()


if __name__ == "__main__":
    main()