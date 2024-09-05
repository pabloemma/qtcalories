# my first qt application
# August 2024

#this gets us the widgets, The main modules for Qt are QtWidgets, QtGui and QtCore.

from PySide6.QtWidgets import QApplication, QWidget


import sys


# You need one (and only one) QApplication instance per application.
  # Pass in sys.argv to allow command line arguments for your app.
  
app = QApplication(sys.argv)
# without commandline args we could just instantiate like
#app = QApplication([])

  # Create a Qt widget, which will be our window.
window = QWidget()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.
#ak give it a title, this i a slot
# a slot is a function which can recieve a signal
# in python all functions can be considered slots
window.setWindowTitle("this is a title")

# now I want to move the window somewhere else, with adifferent size
# first lets do the size
basew = 1000
baseh = 800
window.setBaseSize(basew,baseh)

# now we move it
posx = 100
posy = 50

window.move(posx,posy)

# now I want a different background
# first we need to enable this
window.setAutoFillBackground(True)
# no we can fill the background through the stylesheeet
window.setStyleSheet("background-color: white")




# I can create as many windows (top) as I want; however if I don't give titles or coordinates they are
#indistinguishable.
#window1 = QWidget()
#window1.show()  # IMPORTANT!!!!! Windows are hidden by default.


  # Start the event loop.
app.exec()
# Your application won't reach here until you exit and the event
  # loop has stopped.