from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QComboBox, QLineEdit, QPushButton, QMessageBox
)
import random
from time import sleep
import sys


class fiestelRun():
    def __init__(self):
        self.roundNumber = 0
        self.key = ""
        self.left = ""
        self.right = ""
        self.roundsToRun = 0
        self.preLeft = ""
        self.preRight = ""
        self.preKey = ""
        self.Fresult = ""
    def plaintext_preparer(self, plaintext):
        try:

            if len(plaintext) == 0:
                raise ValueError("The plaintext cannot be an empty string")

            if len(plaintext) != 4:
                raise ValueError("The plaintext must be 4 characters long")


            res = ''.join(format(ord(i), '08b') for i in plaintext)
            self.left = res[:16]
            self.right = res[16:32]
            print("Left:", self.left, "Right:", self.right)
            return "Left:", self.left, "Right:", self.right

        except ValueError as e:
            print(f"Error: {e}")
            return e
    def rand_key(self):
        self.key = ""
        for i in range(16):
            temp = random.randint(0, 1)
            self.key += str(temp)
        print("Random key:", self.key)

    def xor(self, i1, i2):
        temp = ""
        for i in range(len(i1)):
            if i1[i] == i2[i]:
                temp += "0"
            else:
                temp += "1"
        return temp

    def RotateKey(self):
        self.key = self.key[1:] + self.key[0]
    def decryptRotateKey(self):
        self.key = self.key[-1] + self.key[:-1]
    def feistelRoundEncrypt(self):
        self.preLeft = self.left
        self.preRight = self.right
        self.preKey = self.key
        self.RotateKey()
        self.roundNumber += 1
        self.left = self.right
        self.Fresult = self.xor(self.key, self.preRight)
        self.right = self.xor(self.preLeft, self.Fresult)
    def feistelRoundDecrypt(self):
        self.preLeft = self.left
        self.preRight = self.right
        self.preKey = self.key
        self.decryptRotateKey()
        self.roundNumber += 1
        self.left = self.preRight
        self.reverseFresult = self.xor(self.key, self.preRight)
        self.right = self.xor(self.preLeft, self.reverseFresult)

class BeginGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Feistel Cipher Visualized")
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()

        self.round_label = QLabel("Choose number of rounds:")
        self.round_dropdown = QComboBox()
        self.round_dropdown.addItems(["4", "8"])

        self.input_label = QLabel("Enter a 4-letter word:")
        self.word = QLineEdit()
        self.splitButton = QPushButton("Enter Word")
        self.splitButton.clicked.connect(self.splitButtonClicked)
        self.run = fiestelRun()



        self.begin_button = QPushButton("Begin")
        self.begin_button.clicked.connect(lambda: toEnc(self, self.run))
        self.layout.addWidget(self.round_label)
        self.layout.addWidget(self.round_dropdown)
        self.layout.addWidget(self.input_label)
        self.layout.addWidget(self.word)
        self.layout.addWidget(self.splitButton)
        self.layout.addWidget(self.begin_button)




        self.setLayout(self.layout)
    def splitButtonClicked(self):
        result = self.run.plaintext_preparer(self.word.text())
        LRlabel = QLabel(str(result))
        self.layout.addWidget(LRlabel)

class encryptGUI(QWidget):
    def __init__(self, feistel_instance):
        super().__init__()
        self.setWindowTitle("Feistel Cipher encryption in action")
        self.setGeometry(100, 100, 1920, 1080)
        self.layout = QVBoxLayout()
        self.feistel = feistel_instance
        self.round_count = QLabel("Current Round: ", feistel_instance.roundNumber)


def toEnc(window, feistel_instance):
    print("Begin")
    window.close()
    encryptionWindow = encryptGUI(feistel_instance)
    encryptionWindow.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BeginGUI()
    window.show()
    sys.exit(app.exec_())
