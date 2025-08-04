# Bank-of-collective-
functioning bank application with intermediate / advance features like fd and fund transfer # 💰 Flask Banking App

This is a simple banking-style web application built using **Flask** and **SQLite**. Users can sign up, log in, transfer funds, make fixed deposits, and more. An admin (master) account is also included for management purposes.

---

## 🚀 Features

### 🔐 User Authentication
- **Signup** and **login** functionality for users.
- A special **master account** with ID `99` is automatically created on first run:
  - **Username:** `yuvraaj_main`
  - **Password:** `yuvraaj_password`

### 👤 User Account
- After logging in, users are redirected to a dashboard showing their:
  - Username
  - Wallet Balance (`amt`)
  - Fixed Deposit Amount (`fdamt`)

### 💸 Send Funds
- Users can send money to another user by entering their ID and the amount.
- Validation checks for sufficient balance and receiver existence.

### 🏦 Fixed Deposit
- Users can invest funds in a fixed deposit for a specified duration (5/10/15 years).
- The amount is transferred from the user's main balance (`amt`) to their FD account (`fdamt`).
- All FD funds are also added to the master bank's wallet (`User ID = 99`).

### 🔍 Find User
- Search for another user by entering their ID.

### 🧹 Admin: Clear Users
- Clears all users **except the master**.

### 🔐 Admin Code Panel
- Enter a predefined code (``) to view a list of all users in the system.

---

## 🗂️ Project Structure
project/
├── app.py # Main Flask application
├── users.db # SQLite database (auto-created)
├── templates/
│ ├── home.html
│ ├── signup.html
│ ├── login.html
│ ├── acc.html
│ ├── send.html
│ ├── finduser.html
│ ├── fixed_deposit.html
│ └── setcode.html
└── admin/
└── second.py # Blueprint for future admin functionality


