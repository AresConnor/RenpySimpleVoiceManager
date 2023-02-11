import VoiceManager

if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = VoiceManager.VMMainWindow()
    win.show()
    app.exec()
