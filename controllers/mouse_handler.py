from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtWidgets import QWidget

class MouseHandler(QWidget):
    def __init__(self):
        super().__init__()
        self.drag_position = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()