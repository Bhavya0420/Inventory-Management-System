# 📦 Inventory Management System

A desktop-based Inventory Management System built using **Python (Tkinter)** and **MySQL**.
This application helps manage products, employees, stock levels, sales billing, and inventory updates efficiently.

---

## 🚀 Features

### 🔐 Authentication

* Welcome page
* Secure Login system (Admin & Employee roles)
* Password show/hide feature
* Logout functionality

### 📦 Product Management

* Add new products
* Update product details
* Delete products
* Search products
* View stock availability
* Auto update stock after billing

### 🛒 Billing System

* Add/Update items to cart
* Auto bill calculation (Total + Tax + Net Pay)
* Generate formatted bill
* Save bill in `bills/` folder
* Generate QR code for bill file
* Print bill
* Clear cart / Clear all functionality
* Stock reduction after billing

### 📊 Real-Time Updates

* Treeview refresh after stock changes
* Automatic stock reduction
* Cart reset after bill generation

---

## 🛠️ Technologies Used

* Python
* Tkinter (GUI)
* MySQL
* PIL (Pillow)
* qrcode
* OS module

---

## 🧾 Billing Flow

1. Select product
2. Add to cart
3. Click **Generate Bill**
4. Bill is:

   * Displayed in billing area
   * Saved inside `bills/` folder
   * QR code generated
   * Stock reduced automatically
5. Cart resets for next customer

---

## 🖥️ Screenshots

* Welcome Page
* <img width="1907" height="1055" alt="image" src="https://github.com/user-attachments/assets/d7a8e656-fa89-46c2-940c-6f8a474062eb" />

* Login Page
 <img width="1911" height="1060" alt="image" src="https://github.com/user-attachments/assets/a084ac01-db46-4183-8a88-569eec5b739e" />

* Admin Dashboard
  <img width="1902" height="1051" alt="image" src="https://github.com/user-attachments/assets/d8b80fd5-16ea-4194-a988-98e1d1b35c80" />

  
* Billing Section
<img width="1909" height="1057" alt="image" src="https://github.com/user-attachments/assets/73cb2d72-d5ea-42a4-992b-b583d39a1890" />
<img width="1903" height="1052" alt="image" src="https://github.com/user-attachments/assets/d27a6f8d-d41f-42c7-8247-db7d1be9c16c" />

---

## 🎯 Future Improvements

* PDF bill generation
* Sales reports dashboard
* Low stock alerts
* Export to Excel
* Cloud-based hosting
* User activity logs



