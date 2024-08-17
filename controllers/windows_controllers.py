from views.windows.admin_window import AdminDashboard
from views.windows.teacher_window import TeacherWindow


class WindowsControllers:
    @staticmethod
    def open_admin_window(user_id):
        """ Open the admin window """
        window = AdminDashboard(user_id)
        window.showMaximized()

    @staticmethod
    def open_teacher_window():
        """ Open the teacher window """
        window = TeacherWindow()
        window.show()

    @staticmethod
    def open_forgot_password_window():
        """ Open the fogot password window """
        from views.windows.fogot_password_window import ForgotPasswordWindow

        window = ForgotPasswordWindow()
        window.show()

    @staticmethod
    def open_login_window():
        """ open the login window """
        from views.windows.login_window import LoginWindow
        
        window = LoginWindow()
        window.show()
