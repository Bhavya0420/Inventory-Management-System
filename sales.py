from tkinter import *
from tkinter import ttk


def sales_form(window):
    global back_image,right_image

    sales_frame=Frame(window,width=1070,height=567,bg='white')
    sales_frame.place(x=200,y=100)

    heading_label=Label(sales_frame, text='View Customer Bills',font=('times new roman',16,'bold'),bg='#0f4d7d',fg='white')
    heading_label.place(x=0,y=0,relwidth=1)

    back_image=PhotoImage(file='images/back_button.png')
    back_button=Button(sales_frame,image=back_image,bd=0, cursor='hand2',bg='white',command=lambda: sales_frame.place_forget())
    back_button.place(x=10,y=30)

    # ================= SEARCH SECTION =================
    invoice_label = Label(sales_frame,text='Invoice No.',font=('times new roman', 12),bg='white')
    invoice_label.place(x=250, y=60)

    invoice_entry = Entry(sales_frame,font=('times new roman', 12),bg='lightyellow')
    invoice_entry.place(x=340, y=60, width=150)

    search_button = Button(sales_frame,text='Search',font=('times new roman', 12, 'bold'),bg='#0f4d7d',fg='white',cursor='hand2')
    search_button.place(x=510, y=58, width=70)

    clear_button = Button(sales_frame,text='Clear',font=('times new roman', 12, 'bold'),bg='#0f4d7d',fg='white',cursor='hand2')
    clear_button.place(x=590, y=58, width=70)

    # ================= LEFT LISTBOX =================
    list_frame = Frame(sales_frame, bd=2, relief=RIDGE)
    list_frame.place(x=160, y=110, width=200, height=350)

    scroll_y = Scrollbar(list_frame, orient=VERTICAL)
    bill_list = Listbox(
        list_frame,
        font=('times new roman', 11),
        yscrollcommand=scroll_y.set
    )

    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_y.config(command=bill_list.yview)
    bill_list.pack(fill=BOTH, expand=1)


    # ================= BILL TEXT AREA =================
    bill_frame = Frame(sales_frame, bd=2, relief=RIDGE)
    bill_frame.place(x=400, y=110, width=350, height=350)

    bill_heading = Label(
        bill_frame,
        text='Customer Bill Area',
        font=('times new roman', 12, 'bold'),
        bg='#0f4d7d',
        fg='white'
    )
    bill_heading.pack(fill=X)

    scroll_bill = Scrollbar(bill_frame, orient=VERTICAL)
    bill_text = Text(
        bill_frame,
        yscrollcommand=scroll_bill.set,
        font=('courier', 10)
    )

    scroll_bill.pack(side=RIGHT, fill=Y)
    scroll_bill.config(command=bill_text.yview)
    bill_text.pack(fill=BOTH, expand=1)

    # ================= RIGHT IMAGE =================
    right_image = PhotoImage(file='images/salespage.png')  # put your image here
    image_label = Label(sales_frame, image=right_image, bg='white')
    image_label.place(x=800, y=200)

    return sales_frame
