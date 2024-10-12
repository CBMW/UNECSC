from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QMessageBox, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox, QDateEdit, QScrollArea, QListWidget, QListWidgetItem, QDesktopWidget
import sys
import bcrypt
from cryptography.fernet import Fernet
from datetime import date

# Separate Data Management class for users and members
class DataManager:
    def __init__(self):
        self.user_data = {
            "admin": {"password": bcrypt.hashpw(b"admin_pass", bcrypt.gensalt()), "role": "Admin"},
            "executive": {"password": bcrypt.hashpw(b"exec_pass", bcrypt.gensalt()), "role": "Executive"},
            "member": {"password": bcrypt.hashpw(b"member_pass", bcrypt.gensalt()), "role": "Member"},
        }
        
        self.members = [
            {"name": "Alice", "role": "Admin", "email": "alice@example.com", "phone": "123456789"},
            {"name": "Bob", "role": "Executive", "email": "bob@example.com", "phone": "987654321"},
            {"name": "Charlie", "role": "Member", "email": "charlie@example.com", "phone": "543216789"}
        ]

    def validate_user(self, username, password):
        if username in self.user_data:
            hashed_pw = self.user_data[username]["password"]
            return bcrypt.checkpw(password.encode('utf-8'), hashed_pw)
        return False

    def get_user_role(self, username):
        return self.user_data.get(username, {}).get("role", None)
    
    def add_member(self, name, role, email, phone):
        self.members.append({"name": name, "role": role, "email": email, "phone": phone})

data_manager = DataManager()

# Encryption setup
encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)

# Global variable to store logged in user
current_user = None

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cyber Security Club - Login")
        self.setGeometry(400, 150, 500, 400)

        # Username field
        self.username_label = QLabel(self)
        self.username_label.setText("Username")
        self.username_label.setGeometry(100, 100, 100, 40)
        
        self.username_input = QLineEdit(self)
        self.username_input.setGeometry(200, 100, 200, 40)

        # Password field
        self.password_label = QLabel(self)
        self.password_label.setText("Password")
        self.password_label.setGeometry(100, 150, 100, 40)
        
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setGeometry(200, 150, 200, 40)

        # Login button
        self.login_button = QPushButton(self)
        self.login_button.setText("Login")
        self.login_button.setGeometry(200, 220, 100, 40)
        self.login_button.clicked.connect(self.login)

        self.failed_attempts = 0  # Track login attempts
        
        # Center the window
        self.center_window()

    def center_window(self):
        """Centers the window on the screen."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def login(self):
        global current_user
        username = self.username_input.text()
        password = self.password_input.text()

        if data_manager.validate_user(username, password):
            current_user = {"username": username, "role": data_manager.get_user_role(username)}
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        else:
            self.failed_attempts += 1
            QMessageBox.warning(self, "Login Failed", f"Invalid username or password. Attempts: {self.failed_attempts}/3")
            if self.failed_attempts >= 3:
                QMessageBox.critical(self, "Login Blocked", "Too many failed attempts. Please try again later.")
                self.login_button.setEnabled(False)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cyber Security Club - Dashboard")
        self.setFixedSize(800, 600)  # Make the window non-resizable

        # Default to light mode
        self.setStyleSheet(self.light_mode_stylesheet())

        # Tabs for Dashboard, Settings, Accounts
        self.tabs = QTabWidget(self)
        self.tabs.setGeometry(20, 20, 760, 550)

        self.dashboard_tab = QWidget()
        self.settings_tab = QWidget()
        self.accounts_tab = QWidget()

        # Adding tabs to the Tab Widget
        self.tabs.addTab(self.dashboard_tab, "Dashboard")
        self.tabs.addTab(self.settings_tab, "Settings")
        self.tabs.addTab(self.accounts_tab, "Accounts")

        # Adjust tab text color for dark mode
        self.tabs.setStyleSheet("QTabBar::tab { color: black; }")

        # Build out each tab
        self.build_dashboard()
        self.build_settings()
        self.build_accounts()
        
        # Center the window
        self.center_window()

    def center_window(self):
        """Centers the window on the screen."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def light_mode_stylesheet(self):
        return "background-color: #ffffff; color: #000000;"

    def dark_mode_stylesheet(self):
        return "background-color: #1f1f1f; color: #ffffff;"

    def build_dashboard(self):
        layout = QVBoxLayout()

        # Create Post Section
        create_post_label = QLabel("Create Post for Newsletter:")
        self.create_post_input = QLineEdit()
        self.create_post_input.setPlaceholderText("Enter post title...")
        
        self.create_post_content = QLineEdit()
        self.create_post_content.setPlaceholderText("Enter post content...")

        layout.addWidget(create_post_label)
        layout.addWidget(self.create_post_input)
        layout.addWidget(self.create_post_content)

        # Meeting Section
        meeting_label = QLabel("Enter Meeting Details:")
        self.meeting_input_time = QLineEdit()
        self.meeting_input_time.setPlaceholderText("Meeting time (e.g. 10:00 AM, 15 Oct 2024)")
        
        self.meeting_input_via = QLineEdit()
        self.meeting_input_via.setPlaceholderText("Meeting via (e.g., Zoom, Discord, etc.)")

        send_sms_button = QPushButton("Send SMS")
        send_sms_button.clicked.connect(self.send_sms)

        layout.addWidget(meeting_label)
        layout.addWidget(self.meeting_input_time)
        layout.addWidget(self.meeting_input_via)
        layout.addWidget(send_sms_button)

        # Website Statistics Section
        stats_label = QLabel("Website Statistics:")
        layout.addWidget(stats_label)

        self.stats_daily_hits = QLabel("Daily Website Hits: 0")
        self.stats_weekly_hits = QLabel("Weekly Website Hits: 0")
        self.stats_ddos_attempts = QLabel("DDoS Attempts: 0")
        self.stats_sqli_attempts = QLabel("SQL Injection Attempts: 0")

        layout.addWidget(self.stats_daily_hits)
        layout.addWidget(self.stats_weekly_hits)
        layout.addWidget(self.stats_ddos_attempts)
        layout.addWidget(self.stats_sqli_attempts)

        self.dashboard_tab.setLayout(layout)

    def send_sms(self):
        if current_user["role"] in ["Admin", "Executive"]:
            meeting_details_time = self.meeting_input_time.text()
            meeting_details_via = self.meeting_input_via.text()
            # This is where you'd integrate the Twilio API or another SMS service.
            QMessageBox.information(self, "SMS Sent", f"Meeting details sent: {meeting_details_time} via {meeting_details_via}")
        else:
            QMessageBox.warning(self, "Access Denied", "You do not have permission to send SMS.")

    def build_settings(self):
        layout = QVBoxLayout()

        # Light/Dark Mode Switch
        self.dark_mode_checkbox = QCheckBox("Dark Mode", self)
        self.dark_mode_checkbox.setChecked(False)  # Default to unchecked for light mode
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_theme)

        layout.addWidget(self.dark_mode_checkbox)

        # User Settings (Change username, password, etc.)
        layout.addWidget(QLabel("User Settings:"))

        self.change_username_input = QLineEdit()
        self.change_username_input.setPlaceholderText("Change Username")
        self.change_password_input = QLineEdit()
        self.change_password_input.setPlaceholderText("Change Password")
        self.change_password_input.setEchoMode(QLineEdit.Password)

        layout.addWidget(self.change_username_input)
        layout.addWidget(self.change_password_input)

        save_button = QPushButton("Save Changes")
        save_button.clicked.connect(self.update_user_settings)

        layout.addWidget(save_button)

        self.settings_tab.setLayout(layout)

    def toggle_theme(self):
        if self.dark_mode_checkbox.isChecked():
            # Dark mode
            self.setStyleSheet(self.dark_mode_stylesheet())
            self.tabs.setStyleSheet("QTabBar::tab { color: white; }")  # Set tab text to white for visibility
        else:
            # Light mode
            self.setStyleSheet(self.light_mode_stylesheet())
            self.tabs.setStyleSheet("QTabBar::tab { color: black; }")  # Set tab text to black

    def update_user_settings(self):
        new_username = self.change_username_input.text()
        new_password = self.change_password_input.text()

        if new_username:
            current_user['username'] = new_username
            QMessageBox.information(self, "Username Changed", "Username updated successfully!")
            self.change_username_input.clear()  # Clear the input after saving

        if new_password:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            current_user['password'] = hashed_password
            QMessageBox.information(self, "Password Changed", "Password updated successfully!")
            self.change_password_input.clear()  # Clear the input after saving

    def build_accounts(self):
        layout = QVBoxLayout()

        # Tabs for sorting members by role
        self.role_tabs = QTabWidget(self)
        self.admin_tab = QWidget()
        self.executive_tab = QWidget()
        self.member_tab = QWidget()

        self.role_tabs.addTab(self.admin_tab, "Admins")
        self.role_tabs.addTab(self.executive_tab, "Executives")
        self.role_tabs.addTab(self.member_tab, "Members")

        # Build member list for each role
        self.build_member_list(self.admin_tab, "Admin")
        self.build_member_list(self.executive_tab, "Executive")
        self.build_member_list(self.member_tab, "Member")

        layout.addWidget(self.role_tabs)

        # Add New Member Section
        layout.addWidget(QLabel("Add New Club Member"))

        self.member_name_input = QLineEdit()
        self.member_name_input.setPlaceholderText("Member Name")
        self.member_access_input = QComboBox()
        self.member_access_input.addItems(["Admin", "Executive", "Member"])
        self.member_email_input = QLineEdit()
        self.member_email_input.setPlaceholderText("Email")
        self.member_phone_input = QLineEdit()
        self.member_phone_input.setPlaceholderText("Phone Number")
        self.member_join_date_input = QDateEdit()
        self.member_join_date_input.setDate(date.today())

        layout.addWidget(self.member_name_input)
        layout.addWidget(self.member_access_input)
        layout.addWidget(self.member_email_input)
        layout.addWidget(self.member_phone_input)
        layout.addWidget(self.member_join_date_input)

        add_member_button = QPushButton("Add Member")
        add_member_button.clicked.connect(self.add_member)
        layout.addWidget(add_member_button)

        self.accounts_tab.setLayout(layout)

    def build_member_list(self, tab, role):
        '''Function to build the member list panel,
        features scroll wheel once users exceed the visible
        list box.'''
        member_layout = QVBoxLayout()

        # Scrollable list of members
        member_list = QListWidget()

        for member in data_manager.members:
            if member['role'] == role:
                item = QListWidgetItem(f"{member['name']} ({member['email']})")
                member_list.addItem(item)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(member_list)

        member_layout.addWidget(scroll_area)
        tab.setLayout(member_layout)

    def add_member(self):
        '''Function to add a member to DB.
        Note; DB does not exist yet'''
        member_name = self.member_name_input.text()
        member_access = self.member_access_input.currentText()
        member_email = self.member_email_input.text()
        member_phone = self.member_phone_input.text()
        member_join_date = self.member_join_date_input.text()

        # Add the member details to the database
        data_manager.add_member(member_name, member_access, member_email, member_phone)
        QMessageBox.information(self, "Member Added", f"Member {member_name} with access {member_access} added!")

        # Refresh the member lists
        self.build_member_list(self.admin_tab, "Admin")
        self.build_member_list(self.executive_tab, "Executive")
        self.build_member_list(self.member_tab, "Member")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())
