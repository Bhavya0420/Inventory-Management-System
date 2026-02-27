from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from employees import connect_database
import time
import qrcode
from PIL import Image, ImageTk
import os
from datetime import datetime

def print_bill(billing_text):

    if billing_text.get(1.0, END).strip() == "":
        messagebox.showerror("Error", "No bill to print")
        return

    # Save temporary file
    file_path = os.path.abspath("temp_print_bill.txt")

    with open(file_path, "w") as file:
        file.write(billing_text.get(1.0, END))

    try:
        os.startfile(file_path, "print")   # Windows only
    except Exception as e:
        messagebox.showerror("Error", f"Printing failed: {e}")

def save_bill_file(billing_text):

    if not os.path.exists("bills"):
        os.makedirs("bills")

    bill_number = datetime.now().strftime("%Y%m%d%H%M%S")

    file_path = f"bills/bill_{bill_number}.txt"

    with open(file_path, "w") as file:
        file.write(billing_text.get(1.0, END))


def generate_bill(name_entry, contact_entry, cart_treeview, billing_text,cart_label,bill_amount_label,tax_label,netpay_label,product_name_entry,price_entry,quantity_entry,treeview):

    # 1️⃣ Validation
    if name_entry.get() == '':
        messagebox.showerror('Error', 'Customer name is required')
        return

    if contact_entry.get() == '':
        messagebox.showerror('Error', 'Customer contact is required')
        return

    if not cart_treeview.get_children():
        messagebox.showerror('Error', 'Cart is empty')
        return

    # 2️⃣ Clear old bill
    billing_text.delete(1.0, END)

    # 3️⃣ Header
    billing_text.insert(END, '\t   StockApp Inventory\n\n')
    billing_text.insert(END, 'Phone No: 9876543210, Bhimavaram, 226003\n')
    billing_text.insert(END, '-' * 41 + '\n')

    billing_text.insert(END, f'Customer Name: {name_entry.get()}\n')
    billing_text.insert(END, f'Phone no: {contact_entry.get()}\n')
    billing_text.insert(END, '-' * 41 + '\n')

    billing_text.insert(END, f'{"Name":15}{"Qty":5}{"Price":10}{"Total":10}\n')
    billing_text.insert(END, '-' * 41 + '\n')

    total_amount = 0

    # 4️⃣ Items
    for child in cart_treeview.get_children():
        item = cart_treeview.item(child)['values']

        name = item[1]
        price = float(item[2])
        quantity = int(item[3])
        total = price * quantity

        total_amount += total

        billing_text.insert(END, f'{name:15}{quantity:<5}{price:<10}{total:<10.2f}\n')

    billing_text.insert(END, '-' * 41 + '\n')

    # 5️⃣ Tax Calculation
    tax_percent = get_tax_percentage()
    tax_amount = (total_amount * tax_percent) / 100
    net_pay = total_amount + tax_amount

    billing_text.insert(END, f'Bill Amount : {total_amount:.2f}\n')
    billing_text.insert(END, f'Tax ({tax_percent}%) : {tax_amount:.2f}\n')
    billing_text.insert(END, f'Net Pay : {net_pay:.2f}\n')

    billing_text.insert(END, '-' * 41 + '\n')

    # 6️⃣ Generate QR Code
    qr_data = f"""
    Name: {name_entry.get()}
    Contact: {contact_entry.get()}
    Amount: {net_pay:.2f}
    """

    qr = qrcode.make(qr_data)
    qr = qr.resize((250, 250))

    qr_img = ImageTk.PhotoImage(qr)

    billing_text.image_create(END, image=qr_img)
    billing_text.qr_img = qr_img   # prevent garbage collection
    save_bill_file(billing_text)

    update_stock_after_billing(cart_treeview)
    treeview_data(treeview)   # refresh product list

    # 🔹 Clear Cart Treeview
    cart_treeview.delete(*cart_treeview.get_children())

    # 🔹 Reset Cart Label
    cart_label.config(text='My Cart \t Total Products: 0')

    name_entry.delete(0,END)
    contact_entry.delete(0,END)

    # 🔹 Reset Bill Summary Labels
    bill_amount_label.config(text='Bill Amount(₹)\n 0')
    tax_label.config(text=f'Tax ({get_tax_percentage()}%)\n 0')
    netpay_label.config(text='Net Pay(₹)\n 0')

    # 🔹 Clear Product Fields
    product_name_entry.config(state='normal')
    price_entry.config(state='normal')

    product_name_entry.delete(0, END)
    price_entry.delete(0, END)
    quantity_entry.delete(0, END)

    product_name_entry.config(state='readonly')
    price_entry.config(state='readonly')

    stock_label.config(text='In Stock: 0')

    treeview.selection_remove(treeview.selection())


def update_stock_after_billing(cart_treeview):

    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('USE inventory_system')

        for child in cart_treeview.get_children():
            item = cart_treeview.item(child)['values']

            product_id = item[0]
            purchased_qty = int(item[3])

            cursor.execute(
                "UPDATE product_data SET quantity = quantity - %s WHERE id = %s",
                (purchased_qty, product_id)
            )

        connection.commit()

    except Exception as e:
        messagebox.showerror("Error", f"Stock update failed: {e}")

    finally:
        cursor.close()
        connection.close()

def logout():
    global current_frame
    response = messagebox.askyesno("Logout", "Do you really want to logout?")
    if response:
        for widget in window.winfo_children():
            widget.destroy()

        current_frame=None 
        
        from login import login_page
        login_page(window)

def update():
    date_time=time.strftime('%I:%M:%S %p on %A, %B %d, %Y')
    subtitleLabel.config(text=f'Welcome {current_emp_name}\t\t\t\t\t\t\t\t {date_time}')
    subtitleLabel.after(400,update)

def get_input(num):
        xnum = var_cal_input.get()+str(num)
        var_cal_input.set(xnum)

def clear_cal():
    var_cal_input.set('')

def perform_cal():
    result=var_cal_input.get()
    var_cal_input.set(eval(result))

def treeview_data(treeview):
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT id,name,price,quantity,status from product_data')
        records=cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('',END,values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

def search_product(search_entry,treeview):
    if search_entry.get()=='':
        messagebox.showwarning('Warning','Place enter product name to search')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_system')
            cursor.execute(f'SELECT id,name,price,quantity,status from product_data WHERE name LIKE %s',f'%{search_entry.get()}%')
            records=cursor.fetchall()
            if len(records)==0:
                messagebox.showerror('error','No records found')
                return
            treeview.delete(*treeview.get_children())
            for record in records:
                treeview.insert('',END, value=record)
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()

def show_all(search_entry,treeview):
    treeview_data(treeview)
    search_entry.delete(0,END)

def select_product(event,product_name_entry,price_entry,treeview):
    index=treeview.selection()
    if not index:
        return
    dict=treeview.item(index[0])
    content=dict['values']

    product_name_entry.config(state='normal')
    price_entry.config(state='normal')
    
    product_name_entry.delete(0,END)
    price_entry.delete(0,END)

    product_name_entry.insert(0,content[1])
    price_entry.insert(0,content[2])

    global instock_val
    instock_val=int(content[3])
    stock_label.config(text=f'In Stock: {instock_val}')

    quantity_val = 1
    quantity_entry.delete(0, END)
    quantity_entry.insert(0, quantity_val)
    

def clear_fields(product_name_entry, price_entry, quantity_entry, stock_label,treeview):
    
    # Enable readonly entries temporarily
    product_name_entry.config(state='normal')
    price_entry.config(state='normal')

    # Clear fields
    product_name_entry.delete(0, END)
    price_entry.delete(0, END)
    quantity_entry.delete(0, END)

    # Reset stock label
    stock_label.config(text='In Stock: 0')

    # Make entries readonly again
    product_name_entry.config(state='readonly')
    price_entry.config(state='readonly')

    treeview.selection_remove(treeview.selection())

def clear_all(billing_text,product_name_entry,quantity_entry,price_entry):
    # 2️⃣ Clear Bill Text Area
    billing_text.delete(1.0, END)

    # 3️⃣ Clear Entry Fields
    product_name_entry.delete(0, END)
    quantity_entry.delete(0, END)
    price_entry.delete(0, END)

def get_tax_percentage():
    cursor, connection = connect_database()
    if not cursor or not connection:
        return 0

    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT tax FROM tax_table WHERE id=1')
        result = cursor.fetchone()
        return float(result[0]) if result else 0
    except:
        return 0
    finally:
        cursor.close()
        connection.close()

def add_update_cart(product_name_entry, price_entry, quantity_entry,
                    cart_treeview, bill_amount_label, tax_label,
                    netpay_label, cart_label,treeview):

    if product_name_entry.get() == '':
        messagebox.showwarning('Warning', 'Please select a product')
        return
    try:
        price = float(price_entry.get())
        quantity = int(quantity_entry.get())
    except:
        messagebox.showerror('Error', 'Invalid quantity')
        return
    
    if quantity > instock_val:
        messagebox.showerror('Error', 'Quantity exceeds available stock')
        return
    if quantity <= 0:
        messagebox.showerror('Error', 'Quantity must be greater than 0')
        return

    product_name = product_name_entry.get()
    product_id = None

    # 🔹 Get selected product ID from main treeview
    selected = treeview.selection()
    if selected:
        product_id = treeview.item(selected[0])['values'][0]

    found = False

    # 🔹 Check if already in cart
    for child in cart_treeview.get_children():
        item = cart_treeview.item(child)['values']

        if item[1] == product_name:
            old_quantity = int(item[3])
            new_quantity = old_quantity + quantity

            if new_quantity > instock_val:
                messagebox.showerror('Error', 'Total quantity exceeds stock')
                return

            # ✅ Update SAME row (same ID)
            cart_treeview.item(child,
                               values=(product_id, product_name, price, new_quantity))
            found = True
            break

    if not found:
        # ✅ Insert using original product ID
        cart_treeview.insert('', END,
                             values=(product_id, product_name, price, quantity))

    # 🔹 Update cart count
    total_products = len(cart_treeview.get_children())
    cart_label.config(text=f'My Cart \t Total Products: {total_products}')

    calculate_bill(cart_treeview, bill_amount_label, tax_label, netpay_label)

def calculate_bill(cart_treeview, bill_amount_label, tax_label, netpay_label):

    total_amount = 0

    for child in cart_treeview.get_children():
        item = cart_treeview.item(child)['values']
        price = float(item[2])
        quantity = int(item[3])
        total_amount += price * quantity

    tax_percent = get_tax_percentage()
    tax_amount = (total_amount * tax_percent) / 100
    net_pay = total_amount + tax_amount

    bill_amount_label.config(text=f'Bill Amount(₹)\n {total_amount:.2f}')
    tax_label.config(text=f'Tax ({tax_percent}%)\n {tax_amount:.2f}')
    netpay_label.config(text=f'Net Pay(₹)\n {net_pay:.2f}')
        
def employee_dashboard(root,emp_name):
    global window, subtitleLabel
    global current_emp_name
    global var_cal_input
    global stock_label,instock_val
    global quantity_val,quantity_entry
    global tax_percent

    current_emp_name = emp_name

    for widget in root.winfo_children():
        widget.destroy()

    window=root
    window.title('Dashboard')
    window.geometry('1270x675+0+0')
    window.resizable(0,0)
    window.config(bg='white')

    bg_image=PhotoImage(file='images/inventory.png')
    titleLabel=Label(window, image=bg_image,compound=LEFT,text=' Inventory Management System', font= ('times new roman',40,'bold'),bg='#010c48',fg='white', anchor='w', padx=20)
    titleLabel.place(x=0,y=0, relwidth=1)
    window.bg_image = bg_image

    logoutButton = Button(window, text='Logout', font =('times new roman', 20,'bold'),fg='#010c48',command=logout)
    logoutButton.place(x=1100,y=10)

    subtitleLabel = Label(window, text=f'Welcome {emp_name} \t\t Date: 08-07-2024\t\t Time: 12:36:17 pm',font=('times new roman',15),bg='#4d636d',fg='white')
    subtitleLabel.place(x=0,y=70,relwidth=1)

    emp_dashboard_frame=Frame(window,width=1350,height=567,bg='white')
    emp_dashboard_frame.place(x=0,y=100)

    left_frame=Frame(emp_dashboard_frame,bg='white')
    left_frame.place(x=10,y=10,width=350,height=800)

    search_frame=Frame(left_frame,bg='white',bd=2,relief=RIDGE)
    search_frame.place(x=0,y=0,width=350,height=130)
    search_frame.grid_columnconfigure(0, weight=1)
    search_frame.grid_columnconfigure(1, weight=1)

    products_heading_label=Label(search_frame, text='All Products',font=('times new roman',16,'bold'),bg='#0f4d7d',fg='white')
    products_heading_label.grid(row=0,column=0,columnspan=2,sticky='we')

    prod_label= Label(search_frame,text='Product Name',font=('times new roman',14,'bold'), bg='white')
    prod_label.grid(row=1,column=0, padx=20,sticky='w')
    search_entry=Entry(search_frame, font=('times new roman',12), bg='lightyellow')
    search_entry.grid(row=1,column=1,pady=10,padx=(0,20)) 

    search_button=Button(search_frame,text='Search',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: search_product(search_entry,treeview))
    search_button.grid(row=2,column=0,padx=10)

    showall_button=Button(search_frame,text='Show All',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: show_all(search_entry,treeview))
    showall_button.grid(row=2,column=1,padx=10)


    treeview_frame=Frame(left_frame,bg='white',bd=2,relief=RIDGE)
    treeview_frame.place(x=0,y=140,width=350,height=380)

    scrolly=Scrollbar(treeview_frame,orient=VERTICAL)
    scrollx=Scrollbar(treeview_frame,orient=HORIZONTAL)
    treeview=ttk.Treeview(treeview_frame, columns=('id','name','price','quantity','status'),show='headings',yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.pack(side=BOTTOM, fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    treeview.pack(fill=BOTH, expand=1)

    treeview.heading('id',text='Id')
    treeview.heading('name',text='Product Name')
    treeview.heading('price',text='Price')
    treeview.heading('quantity',text='Quantity')
    treeview.heading('status',text='Status')

    treeview.column('id', width=50)
    treeview.column('name', width=120)
    treeview.column('price', width=80)
    treeview.column('quantity', width=80)
    treeview.column('status', width=80)

    treeview_data(treeview)

    middle_frame=Frame(emp_dashboard_frame,bg='white')
    middle_frame.place(x=370,y=10,width=480,height=800)

    top_frame=Frame(middle_frame,bg='white',bd=2,relief=RIDGE)
    top_frame.place(x=0,y=0,width=480,height=90)
    top_frame.grid_columnconfigure(0, weight=1)
    top_frame.grid_columnconfigure(1, weight=1)

    customers_heading_label=Label(top_frame, text='Customer Details',font=('times new roman',16,'bold'),bg='#0f4d7d',fg='white')
    customers_heading_label.grid(row=0,column=0,columnspan=4,sticky='we')

    name_label= Label(top_frame,text='Name',font=('times new roman',14,'bold'), bg='white')
    name_label.grid(row=1,column=0, padx=10,sticky='w')
    name_entry=Entry(top_frame, font=('times new roman',12), bg='lightyellow',width=15)
    name_entry.grid(row=1,column=1,pady=10,padx=(0,10)) 

    contact_label= Label(top_frame,text='Contact No.',font=('times new roman',14,'bold'), bg='white')
    contact_label.grid(row=1,column=2, padx=10,sticky='w')
    contact_entry=Entry(top_frame, font=('times new roman',12), bg='lightyellow',width=15)
    contact_entry.grid(row=1,column=3,pady=10,padx=(0,10)) 

    var_cal_input=StringVar()

    cal_frame=Frame(middle_frame,bg='white',bd=2,relief=RIDGE)
    cal_frame.place(x=0,y=100,width=220,height=300)
    for i in range(4):
        cal_frame.grid_columnconfigure(i, weight=1)
    txt_cal_input=Entry(cal_frame,textvariable=var_cal_input,font=('arial',15,'bold'),width=21,bd=10,relief=GROOVE,state='readonly',justify=RIGHT)
    txt_cal_input.grid(row=0,columnspan=4)

    btn_7=Button(cal_frame,text='7',font=('arial',15,'bold'),command=lambda: get_input(7),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=0)
    btn_8=Button(cal_frame,text='8',font=('arial',15,'bold'),command=lambda: get_input(8),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=1)
    btn_9=Button(cal_frame,text='9',font=('arial',15,'bold'),command=lambda: get_input(9),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=2)
    btn_sum=Button(cal_frame,text='+',font=('arial',15,'bold'),command=lambda: get_input('+'),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=3)

    btn_4=Button(cal_frame,text='4',font=('arial',15,'bold'),command=lambda: get_input(4),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=0)
    btn_5=Button(cal_frame,text='5',font=('arial',15,'bold'),command=lambda: get_input(5),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=1)
    btn_6=Button(cal_frame,text='6',font=('arial',15,'bold'),command=lambda: get_input(6),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=2)
    btn_sub=Button(cal_frame,text='-',font=('arial',15,'bold'),command=lambda: get_input('-'),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=3)

    btn_1=Button(cal_frame,text='1',font=('arial',15,'bold'),command=lambda: get_input(1),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=0)
    btn_2=Button(cal_frame,text='2',font=('arial',15,'bold'),command=lambda: get_input(2),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=1)
    btn_3=Button(cal_frame,text='3',font=('arial',15,'bold'),command=lambda: get_input(3),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=2)
    btn_mul=Button(cal_frame,text='*',font=('arial',15,'bold'),command=lambda: get_input('*'),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=3)

    btn_0=Button(cal_frame,text='0',font=('arial',15,'bold'),command=lambda: get_input(0),bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=0)
    btn_c=Button(cal_frame,text='c',font=('arial',15,'bold'),command= clear_cal,bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=1)
    btn_eq=Button(cal_frame,text='=',font=('arial',15,'bold'),command= perform_cal,bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=2)
    btn_div=Button(cal_frame,text='/',font=('arial',15,'bold'),command=lambda: get_input('/'),bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=3)

    cart_treeview_frame=Frame(middle_frame,bg='white',bd=2,relief=RIDGE)
    cart_treeview_frame.place(x=225,y=100,width=260,height=300)

    cart_label=Label(cart_treeview_frame, text='My Cart \t Total Products: 0', font=('times new roman',14,'bold'),bg='#f0f0f0',fg='black')
    cart_label.pack(fill=X)

    scrolly=Scrollbar(cart_treeview_frame,orient=VERTICAL)
    scrollx=Scrollbar(cart_treeview_frame,orient=HORIZONTAL)
    cart_treeview=ttk.Treeview(cart_treeview_frame, columns=('id','name','price','quantity'),show='headings',yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.pack(side=BOTTOM, fill=X)
    scrollx.config(command=cart_treeview.xview)
    scrolly.config(command=cart_treeview.yview)
    cart_treeview.pack(fill=BOTH, expand=1)

    cart_treeview.heading('id',text='Id')
    cart_treeview.heading('name',text='Name')
    cart_treeview.heading('price',text='Price')
    cart_treeview.heading('quantity',text='Quantity')

    cart_treeview.column('id', width=70)
    cart_treeview.column('name', width=100)
    cart_treeview.column('price', width=110)
    cart_treeview.column('quantity', width=90)

    bottom_frame=Frame(middle_frame,bg='white',bd=2,relief=RIDGE)
    bottom_frame.place(x=0,y=410,width=480,height=110)
    bottom_frame.grid_columnconfigure(0, weight=1)
    bottom_frame.grid_columnconfigure(1, weight=1)

    product_name_label= Label(bottom_frame,text='Product Name',font=('times new roman',14,'bold'), bg='white')
    product_name_label.grid(row=0,column=0, padx=(10,0),sticky='w')
    product_name_entry=Entry(bottom_frame, font=('times new roman',12), bg='#f0f0f0',width=15,state='readonly')
    product_name_entry.grid(row=1,column=0,padx=(10,0),pady=(0,15),sticky='w') 

    price_label= Label(bottom_frame,text='Price',font=('times new roman',14,'bold'), bg='white')
    price_label.grid(row=0,column=1,sticky='w')
    price_entry=Entry(bottom_frame, font=('times new roman',12), bg='#f0f0f0',width=15,state='readonly')
    price_entry.grid(row=1,column=1,pady=(0,15),sticky='w') 

    quantity_val=1
    quantity_label= Label(bottom_frame,text='Quantity',font=('times new roman',14,'bold'), bg='white')
    quantity_label.grid(row=0,column=2, padx=(0,10),sticky='w')
    quantity_entry=Entry(bottom_frame, font=('times new roman',12), bg='lightyellow',width=15)
    quantity_entry.grid(row=1,column=2,padx=(0,10),pady=(0,15),sticky='w')

    for i in range(3):
        bottom_frame.grid_columnconfigure(i, weight=1)

    instock_val=0

    stock_label= Label(bottom_frame,text=f'In Stock: {instock_val}',font=('times new roman',14,'bold'), bg='white')
    stock_label.grid(row=2,column=0, padx=(20,0),sticky='w')

    clear_button=Button(bottom_frame,text='Clear',font=('times new roman',12),width=10,cursor='hand2',fg='white',bg='#0f4d7d' ,command=lambda: clear_fields(product_name_entry, price_entry, quantity_entry, stock_label,treeview))
    clear_button.grid(row=2,column=1,padx=10,sticky='w')

    addUpdate_button=Button(bottom_frame,text='Add/Update Cart',font=('times new roman',12),width=15,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: add_update_cart(product_name_entry,price_entry, quantity_entry,cart_treeview,bill_amount_label,tax_label,netpay_label,cart_label,treeview))
    addUpdate_button.grid(row=2,column=2,sticky='w')

    right_frame=Frame(emp_dashboard_frame,bg='white')
    right_frame.place(x=860,y=10,width=450,height=800)

    billing_frame=Frame(right_frame,bg='lightyellow',bd=2,relief=RIDGE)
    billing_frame.place(x=0,y=0,width=400,height=400)
    
    billing_heading_label=Label(billing_frame, text='Customer Details',font=('times new roman',16,'bold'),bg='#0f4d7d',fg='white')
    billing_heading_label.pack(fill=X)

    scrolly = Scrollbar(billing_frame, orient=VERTICAL)
    scrolly.pack(side=RIGHT, fill=Y)

    billing_text = Text(billing_frame,bg='lightyellow',font=('consolas', 12),yscrollcommand=scrolly.set)
    billing_text.pack(fill=BOTH, expand=True)

    scrolly.config(command=billing_text.yview)

    billing_bottom_frame=Frame(right_frame,bg='white')
    billing_bottom_frame.place(x=0,y=410,width=400,height=110)
    billing_bottom_frame.grid_columnconfigure(0, weight=1)
    billing_bottom_frame.grid_columnconfigure(1, weight=1)

    bill_amount_label= Label(billing_bottom_frame,text='Bill Amount(₹)\n 0',font=('times new roman',12,'bold'),width=13, bg="#516676",fg='white',pady=5)
    bill_amount_label.grid(row=0,column=0,padx=2, pady=(0,10), sticky='w')

    tax_percent=get_tax_percentage()
    tax_label= Label(billing_bottom_frame,text=f'Tax\n {tax_percent}',font=('times new roman',12,'bold'),width=13, bg="#516676",fg='white',pady=5)
    tax_label.grid(row=0,column=1, pady=(0,10), sticky='w')

    netpay_label= Label(billing_bottom_frame,text='Net Pay(₹)\n 0',font=('times new roman',12,'bold'),width=13, bg="#516676",fg='white',pady=5)
    netpay_label.grid(row=0,column=2,padx=2, pady=(0,10), sticky='w')

    generate_bill_button=Button(billing_bottom_frame,text='Generate Bill',font=('times new roman',12,'bold'),width=13,cursor='hand2',fg='white',bg='#0f4d7d',pady=8,command=lambda: generate_bill(name_entry, contact_entry, cart_treeview, billing_text,cart_label,bill_amount_label,tax_label,netpay_label,product_name_entry,price_entry,quantity_entry,treeview))
    generate_bill_button.grid(row=1,column=0,padx=2,sticky='w')

    print_button=Button(billing_bottom_frame,text='Print',font=('times new roman',12,'bold'),width=13,cursor='hand2',fg='white',bg='#0f4d7d',pady=8,command=lambda: print_bill(billing_text))
    print_button.grid(row=1,column=1,sticky='w')

    clear_all_button=Button(billing_bottom_frame,text='Clear All',font=('times new roman',12,'bold'),width=13,cursor='hand2',fg='white',bg='#0f4d7d',pady=8, command=lambda: clear_all(billing_text,product_name_entry,quantity_entry,price_entry))
    clear_all_button.grid(row=1,column=2,padx=2,sticky='w')

    treeview.bind('<ButtonRelease-1>',lambda event: select_product(event,product_name_entry,price_entry,treeview))

    update()
