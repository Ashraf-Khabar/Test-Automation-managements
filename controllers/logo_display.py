from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap

class LogoDisplay:
    def __init__(self, parent):
        self.parent = parent
        self.logo_label = QLabel(parent)
        self.show_logo()

    def show_logo(self):
        """ Affiche le logo pendant quelques secondes au démarrage """
        logo_pixmap = QPixmap("../icons/Robot.png")
        self.logo_label.setPixmap(logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setGeometry(self.parent.rect()) 
        self.logo_label.show()
        QTimer.singleShot(4000, self.hide_logo)

    def hide_logo(self):
        """ Masque le logo après 3 à 5 secondes """
        self.logo_label.hide()
