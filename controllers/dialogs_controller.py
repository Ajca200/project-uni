from PyQt5.QtWidgets import QDialog

class DialogController:
    @staticmethod
    def open_forgot_password_dialog(id,email,code):
        """ Abre el diálogo de olvido de contraseña """
        from views.dialogs.fogot_password_dialog import ForgotPasswordDialog  # Importación tardía

        dialog = ForgotPasswordDialog(id, email, code)
        status = dialog.exec_()

        if status == QDialog.Accepted:
            return True
        else:
            return False

    @staticmethod
    def open_new_password_dialog(id):
        """ Abre el diálogo para nueva contraseña """
        from views.dialogs.new_password_dialog import NewPasswordDialog  # Importación tardía
        dialog = NewPasswordDialog(id)
        dialog.exec_()

    @staticmethod
    def open_loading_dialog():
        """ abre el dialogo para loading (cargando...) """
        from views.dialogs.loading_dialog import LoadingDialog
        dialog = LoadingDialog()
        dialog.show()
        return dialog
