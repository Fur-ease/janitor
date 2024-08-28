from PyQt5.QtWidgets import QApplication, QDialog, QStackedWidget, QTableWidgetItem
import sys
import sqlite3
from PyQt5.uic import loadUi

con = sqlite3.Connection('sqlite.db')
cur = con.cursor()


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('firstpage.ui', self)
        self.btnAdmin.clicked.connect(self.adminLogin)
        self.btnSupervisor.clicked.connect(self.supervisorLogin)
        self.btnJanitor.clicked.connect(self.janitorLogin)

    def adminLogin(self):
        widget.setCurrentIndex(3)

    def supervisorLogin(self):
        widget.setCurrentIndex(4)

    def janitorLogin(self):
        widget.setCurrentIndex(5)


class Administrator(QDialog):
    def __init__(self):
        super(Administrator, self).__init__()
        loadUi('adminpage.ui', self)
        self.btnSupervisors.clicked.connect(self.supervisors_page)
        self.btnDashboard.clicked.connect(self.home_page)
        self.btnJanitors.clicked.connect(self.janitors_page)
        self.btnLogout.clicked.connect(self.logout)
        self.adminPages.setCurrentIndex(0)

        # load data
        self.dashboardFunctionalities()
        self.supervisorsFunctionalities()


    def supervisors_page(self):
        self.adminPages.setCurrentIndex(1)

    def home_page(self):
        self.adminPages.setCurrentIndex(0)

    def janitors_page(self):
        self.adminPages.setCurrentIndex(2)

    def logout(self):
        widget.setCurrentIndex(1)

    def dashboardFunctionalities(self):
        cur.execute('SELECT COUNT(*) FROM supervisors')
        supevisorscount = cur.fetchone()[0]
        self.supervisorsCount.setText(str(supevisorscount))

        cur.execute('SELECT COUNT(*) from janitors')
        janitorscount = cur.fetchone()[0]
        self.janitorsCount.setText(str(janitorscount))

        cur.execute('select count(*) from tasks')
        taskscount = cur.fetchone()[0]
        self.tasksCount.setText(str(taskscount))

        tableRow = 0
        cur.execute('SELECT COUNT(*) FROM tasks WHERE TaskStatus="Pending"')
        self.tasksTable.setRowCount(cur.fetchone()[0])

        query = 'SELECT TaskDescription, JanitorName, SupervisorName, TaskStatus, DateAssigned, TimeAssigned FROM tasks WHERE TaskStatus = "Pending"'
        for row in cur.execute(query):
            self.tasksTable.setItem(tableRow, 0, QTableWidgetItem(row[0]))
            self.tasksTable.setItem(tableRow, 1, QTableWidgetItem(row[1]))
            self.tasksTable.setItem(tableRow, 2, QTableWidgetItem(row[2]))
            self.tasksTable.setItem(tableRow, 3, QTableWidgetItem(row[3]))
            self.tasksTable.setItem(tableRow, 4, QTableWidgetItem(row[4]))
            self.tasksTable.setItem(tableRow, 5, QTableWidgetItem(row[5]))
            tableRow += 1

    def supervisorsFunctionalities(self):
        table_row = 0
        cur.execute('SELECT COUNT(*) FROM supervisors')
        self.supervisorsTable.setRowCount(cur.fetchone()[0])

        query = 'SELECT SupervisorName, Email, Phone, HireDate, EmploymentStatus, Username, Password FROM supervisors'
        results = cur.execute(query)
        for row in results:
            self.supervisorsTable.setItem(table_row, 0, QTableWidgetItem(row[0]))
            self.supervisorsTable.setItem(table_row, 1, QTableWidgetItem(row[1]))
            self.supervisorsTable.setItem(table_row, 2, QTableWidgetItem(row[2]))
            self.supervisorsTable.setItem(table_row, 3, QTableWidgetItem(row[3]))
            self.supervisorsTable.setItem(table_row, 4, QTableWidgetItem(row[4]))
            self.supervisorsTable.setItem(table_row, 5, QTableWidgetItem(row[5]))
            self.supervisorsTable.setItem(table_row, 6, QTableWidgetItem(row[6]))
            table_row += 1


class Supervisor(QDialog):
    def __init__(self):
        super(Supervisor, self).__init__()
        loadUi('supervisorpage.ui', self)


class AdministratorLogin(QDialog):
    def __init__(self):
        super(AdministratorLogin, self).__init__()
        loadUi('adminlogin.ui', self)
        self.btnCancel.clicked.connect(self.cancel)
        self.btnLogin.clicked.connect(self.login)

    def cancel(self):
        widget.setCurrentIndex(0)

        self.password.setText("")
        self.username.setText("")
        self.error.setText('')

    def login(self):
        username = self.username.text()
        password = self.password.text()

        if len(username) == 0 and len(password) == 0:
            self.error.setText("Empty Input Fields")
        else:
            query = 'SELECT Password FROM administrators WHERE Username = ?'
            cur.execute(query, (username,))
            results = cur.fetchone()[0]
            if self.password.text() == results:
                self.error.setText("")
                self.username.setText("")
                self.password.setText("")

                widget.setCurrentIndex(3)
            else:
                self.error.setText("Invalid password or username")


class SupervisorLogin(QDialog):
    def __init__(self):
        super(SupervisorLogin, self).__init__()
        loadUi('supervisorlogin.ui', self)
        self.btnCancel.clicked.connect(self.cancel)
        self.btnLogin.clicked.connect(self.login)

    def cancel(self):
        widget.setCurrentIndex(0)
        self.password.setText("")
        self.username.setText("")
        self.error.setText('')

    def login(self):
        username = self.username.text()
        password = self.password.text()

        if len(username) == 0 and len(password) == 0:
            self.error.setText("Empty Input Fields")
        elif len(username) == 0:
            self.error.setText("Input Username")
        elif len(password):
            self.error.setText("Input Password")
        else:
            query = 'SELECT Password FROM supervisors WHERE Username = ?'
            cur.execute(query, (username,))
            results = cur.fetchone()[0]
            if self.password.text() == results:
                widget.setCurrentIndex(4)
            else:
                self.error.setText("Invalid password or username")


class Janitor(QDialog):
    def __init__(self):
        super(Janitor, self).__init__()
        loadUi('janitorspage.ui')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = QStackedWidget()
    widget.setWindowTitle('Umma Janitors Management System')
    widget.setFixedWidth(1037)
    widget.setFixedHeight(692)

    # Welcome page
    mainApp = MainWindow()
    widget.addWidget(mainApp)  # index 0

    # admin login page
    admin_login = AdministratorLogin()
    widget.addWidget(admin_login)  # index 1

    # supervisor login
    supervisor_login = SupervisorLogin()
    widget.addWidget(supervisor_login)  # index 2

    # admin dashboard
    admin_dashboard = Administrator()
    widget.addWidget(admin_dashboard)  # index 3

    # supervisor dashboard
    supervisor_dashboard = Supervisor()
    widget.addWidget(supervisor_dashboard)  # index 4

    # janitor dashboard
    janitor_dashboard = Janitor()
    widget.addWidget(janitor_dashboard)  # index 5

    widget.show()

    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(str(e))

