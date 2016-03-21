# -*- coding: utf-8 -*-

from aktos_dcs import *
from aktos_dcs_lib import Qt
Qt.initialize()


class MainWindow(Actor, Qt.QtGui.QMainWindow):
    
    def __init__(self):
        Qt.QtGui.QMainWindow.__init__(self)
        Actor.__init__(self)
        self.ui = Qt.loadUI('qt-example.ui')

        self.guest_name = "stranger"

        # create signal-socket connections
        self.ui.say_hello.clicked.connect(self.say_hello)
        self.ui.get_name.clicked.connect(self.get_guest_name)
        self.ui.name_input.returnPressed.connect(self.get_guest_name)
        self.ui.show_popup.clicked.connect(self.show_popup)

    def handle_GuiMessage(self, msg_raw):
        msg = get_msg_body(msg_raw)
        print "gui received message: ", msg['text']
        self.ui.actor_msg.setText("msg received:  " + msg['text'])

    def say_hello(self):
        self.ui.hello_output.setText("hello " + self.guest_name + ", how are you?")

    def get_guest_name(self):
        self.guest_name = self.ui.name_input.text()

    def show_popup(self):
        modal = Modal()
        modal.ui.show()

class Modal(Actor, Qt.QtGui.QMainWindow):

    def __init__(self):
        Qt.QtGui.QMainWindow.__init__(self)
        Actor.__init__(self)
        self.ui = Qt.loadUI('qt-example.modal.ui')


    def handle_GuiMessage(self, msg_raw):
        msg = get_msg_body(msg_raw)
        print "gui received message: ", msg['text']
        self.ui.label.setText("msg received:  " + msg['text'])

class Test(Actor):
    def action(self):
        i = 0
        while True:
            print "sending gui message"
            self.send({'GuiMessage': {'text': str(i)}})
            i += 1
            sleep(1)


if __name__ == "__main__":
    import sys
    app = Qt.QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.ui.show()
    Test()
    Qt.greenlet_exec(app)

