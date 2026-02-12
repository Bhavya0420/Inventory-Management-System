from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from employees import connect_database

def select_data(event,category_combobox,supplier_combobox,name_entry,price_entry,discount_spinbox,quantity_entry,status_combobox,treeview):
    index=treeview.selection()
    if not index:
        return
    dict=treeview.item(index[0])
    content=dict['values']
    
    name_entry.delete(0,END)
    price_entry.delete(0,END)
    quantity_entry.delete(0,END)
    discount_spinbox.delete(0,END)

    category_combobox.set(content[1])
    supplier_combobox.set(content[2])
    name_entry.insert(0,content[3])
    price_entry.insert(0,content[4])
    discount_spinbox.insert(0,content[5])
    quantity_entry.insert(0,content[7])
    status_combobox.set(content[8])

def treeview_data(treeview):
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT * from product_data')
        records=cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('',END,values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

def fetch_supplier_category(category_combobox,supplier_combobox):
    category_options=[]
    supplier_options=[]
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventory_system')
    cursor.execute('SELECT name from category_data')
    names=cursor.fetchall()
    if len(names)>0:
        category_combobox.set('Select')
        for name in names:
            category_options.append(name[0])
        category_combobox.config(values=category_options)

    cursor.execute('SELECT name from supplier_data')
    names=cursor.fetchall()
    if len(names)>0:
        supplier_combobox.set('Select')
        for name in names:
            supplier_options.append(name[0])
        supplier_combobox.config(values=supplier_options)


def add_product(category,supplier,name,price,discount,quantity,status,treeview):
    if category=='Empty':
        messagebox.showerror('Error','Please add categories')
    elif supplier=='Empty':
        messagebox.showerror('Error','Please add suppliers')
    elif category=='Select' or supplier=='Select' or name=='' or price=='' or quantity=='' or status=='Select Status':
        messagebox.showerror('Error','All fields are required')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_system')  
            cursor.execute('CREATE TABLE IF NOT EXISTS product_data (id INT AUTO_INCREMENT PRIMARY KEY,category VARCHAR(100),supplier VARCHAR(100), name VARCHAR(100), price DECIMAL(10,2),quantity INT, status VARCHAR(50))') 

            cursor.execute('SELECT * from product_data WHERE category=%s AND supplier=%s AND name=%s',(category,supplier,name))
            existing_product=cursor.fetchone()
            if existing_product:
                messagebox.showerror('Error','Product already exists')
                return
            discounted_price=round(float(price)*(1-float(discount)/100),2)
            cursor.execute('INSERT INTO product_data (category,supplier,name,price,discount,discounted_price,quantity,status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',(category,supplier,name,price,discount,discounted_price,quantity,status))
            connection.commit()
            messagebox.showinfo('Success','Data is inserted successfully')
            treeview_data(treeview)
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()

def update_product(category,supplier,name,price,discount,quantity,status,treeview):
    index=treeview.selection()
    if not index:
        messagebox.showerror('Error','No row is selected')
        return 
    dict=treeview.item(index)
    content=dict['values']
    id=content[0]

    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT * FROM product_data WHERE id=%s',(id,))
            
        current_data=cursor.fetchone()
        current_data=list(current_data[1:])
        current_data=list(current_data)
        current_data[3]=str(current_data[3])
        current_data[4]=str(current_data[4])
        del current_data[5]
        current_data=tuple(current_data)
        
        quantity=int(quantity)
        new_data=(category,supplier,name,price,discount,quantity,status)
        if current_data==new_data:
            messagebox.showinfo('Info','No changes detected')
            return

        discounted_price=round(float(price)*(1-float(discount)/100),2)  
        cursor.execute('UPDATE product_data SET category=%s, supplier=%s,name=%s, price=%s, discount=%s, discounted_price=%s, quantity=%s,status=%s WHERE id=%s',(category,supplier,name,price,discount,discounted_price,quantity,status,id))
        connection.commit()
        messagebox.showinfo('Success','Data is updated successfully')
        treeview_data(treeview)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

def delete_product(treeview,category_combobox,supplier_combobox,name_entry,price_entry,discount_spinbox,quantity_entry,status_combobox):
    index=treeview.selection()
    if not index:
        messagebox.showerror('Error','No row is selected')
    else:
        result=messagebox.askyesno('Confirm','Do you really want to delete this record')
        if result:
            cursor,connection=connect_database()
            if not cursor or not connection:
                return
            content=treeview.item(index)
            row=content['values']
            id=row[0]
            try:
                cursor.execute('USE inventory_system')
                cursor.execute('DELETE FROM product_data WHERE id=%s', (id,))
                connection.commit()
                treeview_data(treeview)
                messagebox.showinfo('Success','Record is deleted')
                clear_fields(category_combobox,supplier_combobox,name_entry,price_entry,discount_spinbox,quantity_entry,status_combobox,treeview)
            except Exception as e:
                messagebox.showerror('Error', f'Error due to {e}')
            finally:
                cursor.close()
                connection.close()

def clear_fields(category_combobox,supplier_combobox,name_entry,price_entry,discount_spinbox,quantity_entry,status_combobox,treeview):
    treeview.selection_remove(treeview.selection())
    category_combobox.set('Select')
    supplier_combobox.set('Select')
    name_entry.delete(0,END)
    price_entry.delete(0,END)
    discount_spinbox.delete(0,END)
    discount_spinbox.insert(0,0)
    quantity_entry.delete(0,END)
    status_combobox.set('Select Status')

def search_product(search_combobox,search_entry,treeview):
    if search_combobox.get()=='Search By':
        messagebox.showwarning('Warning','Please select an search option')
    elif search_entry.get()=='':
        messagebox.showwarning('Warning','Place enter value to search')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_system')
            cursor.execute(f'SELECT * from product_data WHERE {search_combobox.get()} LIKE %s',f'%{search_entry.get()}%')
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

def show_all(search_combobox,search_entry,treeview):
    treeview_data(treeview)
    search_combobox.set('Search By')
    search_entry.delete(0,END)

def product_form(window):
    global back_image,logo

    product_frame=Frame(window,width=1070,height=567,bg='white')
    product_frame.place(x=200,y=100)

    back_image=PhotoImage(file='images/back_button.png')
    back_button=Button(product_frame,image=back_image,bd=0, cursor='hand2',bg='white',command=lambda: product_frame.place_forget())
    back_button.place(x=10,y=0)

    left_frame=Frame(product_frame,bg='white',bd=2, relief=RIDGE)
    left_frame.place(x=20,y=40)

    heading_label=Label(left_frame, text='Manage Product Details',font=('times new roman',16,'bold'),bg='#0f4d7d',fg='white')
    heading_label.grid(row=0,columnspan=2,sticky='we')

    category_label= Label(left_frame,text='Category',font=('times new roman',12), bg='white')
    category_label.grid(row=1,column=0, padx=20, sticky='w')
    category_combobox=ttk.Combobox(left_frame,font=('times new roman',12),width=18, state='readonly')
    category_combobox.set('Empty')
    category_combobox.grid(row=1,column=1,pady=30) 

    supplier_label= Label(left_frame,text='Supplier',font=('times new roman',12), bg='white')
    supplier_label.grid(row=2,column=0, padx=20, sticky='w')
    supplier_combobox=ttk.Combobox(left_frame,font=('times new roman',12),width=18, state='readonly')
    supplier_combobox.set('Empty')
    supplier_combobox.grid(row=2,column=1)

    name_label= Label(left_frame,text='Name',font=('times new roman',12), bg='white')
    name_label.grid(row=3,column=0, padx=20,sticky='w')
    name_entry=Entry(left_frame, font=('times new roman',12), bg='lightyellow')
    name_entry.grid(row=3,column=1,pady=30) 

    price_label= Label(left_frame,text='Price',font=('times new roman',12), bg='white')
    price_label.grid(row=4,column=0, padx=20,sticky='w')
    price_entry=Entry(left_frame, font=('times new roman',12), bg='lightyellow')
    price_entry.grid(row=4,column=1) 

    discount_label= Label(left_frame,text='Discount(%)',font=('times new roman',12), bg='white')
    discount_label.grid(row=5,column=0, padx=20,sticky='w',pady=(30,0))
    discount_spinbox=Spinbox(left_frame,from_=0, to=100,font=('times new roman',12),width=19)
    discount_spinbox.grid(row=5,column=1,pady=(30,0))

    quantity_label= Label(left_frame,text='Quantity',font=('times new roman',12), bg='white')
    quantity_label.grid(row=6,column=0, padx=20,sticky='w')
    quantity_entry=Entry(left_frame, font=('times new roman',12), bg='lightyellow')
    quantity_entry.grid(row=6,column=1,pady=30) 

    status_label= Label(left_frame,text='Status',font=('times new roman',12), bg='white')
    status_label.grid(row=7,column=0, padx=20, sticky='w')
    status_combobox=ttk.Combobox(left_frame,values=('Active','Inactive'),font=('times new roman',12),width=18, state='readonly')
    status_combobox.set('Select Status')
    status_combobox.grid(row=7,column=1)

    button_frame=Frame(left_frame,bg='white')
    button_frame.grid(row=8,columnspan=2,pady=(30,20))

    add_button=Button(button_frame,text='Add',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: add_product(category_combobox.get(),supplier_combobox.get(),name_entry.get(),price_entry.get(),discount_spinbox.get(),quantity_entry.get(),status_combobox.get(),treeview))
    add_button.grid(row=0,column=0,padx=10)

    update_button=Button(button_frame,text='Update',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: update_product(category_combobox.get(),supplier_combobox.get(),name_entry.get(),price_entry.get(),discount_spinbox.get(),quantity_entry.get(),status_combobox.get(),treeview))
    update_button.grid(row=0,column=1,padx=10)

    delete_button=Button(button_frame,text='Delete',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: delete_product(treeview,category_combobox,supplier_combobox,name_entry,price_entry,discount_spinbox,quantity_entry,status_combobox))
    delete_button.grid(row=0,column=2,padx=10)

    clear_button=Button(button_frame,text='Clear',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d', command=lambda: clear_fields(category_combobox,supplier_combobox,name_entry,price_entry,discount_spinbox,quantity_entry,status_combobox,treeview))
    clear_button.grid(row=0,column=3,padx=10) 

    search_frame=LabelFrame(product_frame,text='Search Product',font=('times new roman',14,'bold'),bg='white')
    search_frame.place(x=480,y=30)

    search_combobox=ttk.Combobox(search_frame,values=('Category','Supplier','Name','Status'),state='readonly',width=16,font=('times new roman',14))
    search_combobox.grid(row=0,column=0,padx=10)
    search_combobox.set('Search By')

    search_entry=Entry(search_frame, font=('times new roman',12), bg='lightyellow',width=16)
    search_entry.grid(row=0,column=1) 

    search_button=Button(search_frame,text='Search',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: search_product(search_combobox,search_entry,treeview))
    search_button.grid(row=0,column=2,padx=(10,0),pady=10) 

    show_button=Button(search_frame,text='Show All',font=('times new roman',12),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: show_all(search_combobox,search_entry,treeview))
    show_button.grid(row=0,column=3,padx=10) 

    treeview_frame=Frame(product_frame,bg='white')
    treeview_frame.place(x=480,y=125,width=570,height=430)

    scrolly=Scrollbar(treeview_frame,orient=VERTICAL)
    scrollx=Scrollbar(treeview_frame,orient=HORIZONTAL)
    treeview=ttk.Treeview(treeview_frame, columns=('id','category','supplier','name','price','discount','discounted_price','quantity','status'),show='headings',yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.pack(side=BOTTOM, fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    treeview.pack(fill=BOTH, expand=1)

    treeview.heading('id',text='Id')
    treeview.heading('category',text='Category')
    treeview.heading('supplier',text='Supplier')
    treeview.heading('name',text='Product Name')
    treeview.heading('price',text='Price')
    treeview.heading('discount',text='Discount')
    treeview.heading('discounted_price',text='Discounted Price')
    treeview.heading('quantity',text='Quantity')
    treeview.heading('status',text='Status')

    fetch_supplier_category(category_combobox,supplier_combobox)
    treeview_data(treeview)

    treeview.bind('<ButtonRelease-1>',lambda event: select_data(event,category_combobox,supplier_combobox,name_entry,price_entry,discount_spinbox,quantity_entry,status_combobox,treeview))

    return product_frame