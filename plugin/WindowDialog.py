from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout

from ..utilities import translation

class WindowDialog(QDialog):
    """ Basic WindowDialog """

    def __init__(self, parent=None):
        super(WindowDialog, self).__init__(parent)

        self.setWindowTitle(translation.tr('windowDialogTitle'))
        self.__constructWidget()

    def __constructWidget(self):
        """ Construct dialog widgets """

        layout = QVBoxLayout()

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        buttonBox = QDialogButtonBox(QBtn)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        layout.addWidget(buttonBox)

        self.setLayout(layout)

        # self.setMinimumHeight(400)
        # self.setMinimumWidth(500)
