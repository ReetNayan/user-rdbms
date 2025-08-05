# User-RDBMS
A comprehensive system for managing user authentication, login records, and role-based access control. This project provides a backend API for user registration, sign-in, and activity tracking, along with a simple graphical user interface.

## Table of Contents

  - Project Overview
  - Features
  - System Architecture
  - Database Structure
  - Getting Started
      - Prerequisites
      - Installation
  - Usage
  - User Roles

## Project Overview

This User-RDBMS System is designed to offer a secure and organized way to handle user authentications. It keeps a detailed record of login attempts, distinguishes between successful and failed logins, and categorizes failed attempts based on the reason for failure. The system also implements a role-based access control mechanism, allowing for different levels of user permissions and capabilities.

## Features

  - **User Authentication:** Secure user registration and sign-in functionality.
  - **Password Hashing:** Passwords are an extra layer of security.
  - **Login Tracking:** Records all login attempts with timestamps and IP addresses.
  - **Failed Login-Attempt Logging:** Captures and stores details of failed login attempts, including the reason for failure.
  - **Role-Based Access Control (RBAC):** Assign different roles to users (Admin, Moderator, Standard) with specific permissions.
  - **Graphical User Interface (GUI):** A simple and intuitive desktop interface for interacting with the system.
  - **Database Management:** Automatically creates and initializes the necessary database and tables on the first run.
  - **Data Integrity:** Utilizes foreign key constraints to maintain consistency across database tables.

## System Architecture

The project is composed of the following key components:

  - **`frontEnd.py`**: A graphical user interface built with `tkinter` that allows users to register, log in, and access their respective dashboards.
  - **`backend.py`**: The core logic of the application. It handles user authentication, registration, and all interactions with the MySQL database.
  - **`dashboard.py`**: Defines the different dashboard views and functionalities available to each user role (Admin, Moderator, Standard).
  - **`hasher.py`**: A utility for hashing passwords using the SHA-256 algorithm, adding a layer of security by not storing plain-text passwords.
  - **`randWord.py`**: A helper module to generate random IP addresses for simulating login attempts from different locations.
  - **`Structure.md`**: A markdown file that outlines the database schema.
  - **`Working.md`**: A markdown file that explains the overall workflow and interaction between the different components of the system.
  - **`LICENSE`**: The GNU General Public License v3.0 under which this project is distributed.

## Database Structure

The system uses a MySQL database to store all its data. The database, named `LoginRecordSystemDB`, consists of five main tables:

1.  **`Users`**: Stores basic user information, including usernames, hashed passwords, and email addresses.
2.  **`LoginRecords`**: Logs every login attempt made by a user, along with the status (success or failure).
3.  **`FailedLoginAttempts`**: Contains detailed records of failed login attempts, including the reason for the failure.
4.  **`UserRoles`**: Defines the different roles available in the system (e.g., admin, standard, moderator).
5.  **`UserRoleMappings`**: Maps users to their assigned roles, establishing their permissions.

For a detailed schema of each table, please refer to the `Structure.md` file.

## Getting Started

To get the system up and running on your local machine, please follow the instructions below.

### Prerequisites

  - Python 3.x
  - MySQL Server
  - `mysql-connector-python` library

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/login-record-management-system.git
    cd login-record-management-system
    ```

2.  **Install the required Python library:**

    ```bash
    pip install mysql-connector-python
    ```

3.  **Set up your MySQL database:**

      - Make sure your MySQL server is running.
      - Open the `backend.py` file and update the database connection details (host, user, and password) to match your MySQL configuration:
        ```python
        database = mysql.connector.connect(host="localhost", user="root", passwd="root")
        ```

## Usage

To run the application, execute the `frontEnd.py` file:

```bash
python frontEnd.py
```

This will launch the main login window. From here, you can either sign in with existing credentials or register as a new user. Upon successful login, you will be directed to a dashboard that is tailored to your assigned role.

## User Roles

The system defines three distinct user roles, each with a specific set of permissions:

  - **Admin:**
      - Can view all data in the database.
      - Can update the roles of other users.
  - **Moderator:**
      - Can delete existing users.
      - Can view the `FailedLoginAttempts` table.
  - **Standard:**
      - Can view their own login records.

## License

This project is licensed under the GNU General Public License v3.0. For more details, please see the [LICENSE](https://www.google.com/search?q=LICENSE) file.
