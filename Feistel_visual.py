from PySide6 import QtCore
from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QComboBox, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QStackedLayout,
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
            self.preLeft = res[:16]
            self.preRight = res[16:32]
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
        #self.RotateKey()
        self.roundNumber += 1
        self.left = self.preRight
        self.Fresult = self.xor(self.key, self.preRight)
        self.right = self.xor(self.preLeft, self.Fresult)
        self.RotateKey()
    def feistelRoundDecrypt(self):
        self.decryptRotateKey()
        self.preLeft = self.left
        self.preRight = self.right
        self.preKey = self.key
        self.roundNumber -= 1
        self.left = self.preRight
        self.Fresult = self.xor(self.key, self.preRight)
        self.right = self.xor(self.preLeft, self.Fresult)

    def binary32_to_text(self, binary_str):

        if len(binary_str) != 32 or not all(bit in '01' for bit in binary_str):
            raise ValueError("Input must be a 32-bit binary string (can include a space).")

        chars = [binary_str[i:i + 8] for i in range(0, 32, 8)]
        return ''.join(chr(int(b, 2)) for b in chars)


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
        self.begin_button.setMinimumSize(QSize(120, 40))
        self.begin_button.setEnabled(False)
        self.begin_button.clicked.connect(lambda: self.toEnc())

        self.layout.addWidget(self.round_label)
        self.layout.addWidget(self.round_dropdown)
        self.layout.addWidget(self.input_label)
        self.layout.addWidget(self.word)
        self.layout.addWidget(self.splitButton)
        self.layout.addWidget(self.begin_button)




        self.setLayout(self.layout)
    def splitButtonClicked(self):
        result = self.run.plaintext_preparer(self.word.text())
        self.run.rand_key()
        LRlabel = QLabel(str(result)+"\nKey: "+ self.run.key)
        self.layout.addWidget(LRlabel)
        self.validate_input()

    def validate_input(self):
        self.begin_button.setEnabled(len(self.word.text()) == 4)

    def toEnc(self):
        print("Begin")
        self.run.roundsToRun = int(self.round_dropdown.currentText())
        self.close()
        self.encryptionWindow = encryptGUI(self.run)
        self.encryptionWindow.show()

class encryptGUI(QWidget):
    def __init__(self, feistel_instance):
        super().__init__()
        self.setWindowTitle("Feistel Cipher encryption in action")
        self.setGeometry(100, 100, 1920, 1080)
        self.layout = QVBoxLayout()
        self.feistel = feistel_instance
        self.keepGoingTF = "null"
        self.EncryptOrDecrypt = "E"


        container = QWidget()
        self.stacked_layout = QStackedLayout(container)

        self.bg_label = QLabel()
        self.bg_pixmap = QPixmap("feistel_bg4.png")
        self.bg_label.setPixmap(self.bg_pixmap)
        self.bg_label.setScaledContents(True)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.round_count = QLabel(f"Current Round: {self.feistel.roundNumber}\nPress Next Round to begin!")
        self.round_count.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 120); font-size: 20px;")
        self.round_count.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.round_count.setContentsMargins(0, 0, 0, 0)


        self.TopLeftScreen = QLabel(f"Current Left:\n{self.feistel.preLeft}")
        self.TopRightScreen = QLabel(f"Current Right:\n{self.feistel.preRight}")
        self.BottomLeftScreen = QLabel(f"Current Bottom:\nN/A")
        self.BottomRightScreen = QLabel(f"Current Bottom:\nN/A")
        for lbl in [self.TopLeftScreen, self.TopRightScreen, self.BottomLeftScreen, self.BottomRightScreen]:
            lbl.setMaximumWidth(290)
            lbl.setMinimumHeight(200)
            lbl.setStyleSheet("color: black; font-size: 20px; padding: 6px;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)
        top_layout.setContentsMargins(1, 40, 1, 40)
        top_layout.addWidget(self.TopLeftScreen)
        top_layout.addWidget(self.TopRightScreen)

        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(10)
        bottom_layout.setContentsMargins(1, 40, 1, 40)
        bottom_layout.addWidget(self.BottomLeftScreen)
        bottom_layout.addWidget(self.BottomRightScreen)

        self.ExitButton = QPushButton("Exit")
        self.ExitButton.setMinimumSize(QSize(160, 50))
        self.ExitButton.setEnabled(False)
        self.ExitButton.clicked.connect(lambda: self.keepGoing(False))

        self.NextRoundButton = QPushButton("Next Round")
        self.NextRoundButton.setMinimumSize(QSize(160, 50))
        self.NextRoundButton.clicked.connect(self.next_round_clicked)

        self.DecryptButton = QPushButton("Decrypt")
        self.DecryptButton.setMinimumSize(QSize(160, 50))
        self.DecryptButton.setEnabled(False)
        self.DecryptButton.clicked.connect(lambda: self.keepGoing(True))

        button_row = QHBoxLayout()
        button_row.addWidget(self.DecryptButton)
        button_row.addWidget(self.NextRoundButton)
        button_row.addWidget(self.ExitButton)
        for button in [self.DecryptButton, self.NextRoundButton, self.ExitButton]:
            button.setStyleSheet("color: green; font-size: 20px; background-color: rgba(0, 0, 0, 200);")
        button_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.content_layout.addWidget(self.round_count)
        self.content_layout.addLayout(top_layout)
        self.content_layout.addLayout(bottom_layout)
        self.content_layout.addLayout(button_row)
        #self.content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #self.content_layout.setContentsMargins(15, 50, 15, 50)
        #self.content_layout.setSpacing(70)


        self.stacked_layout.addWidget(self.bg_label)
        self.stacked_layout.addWidget(self.content_widget)
        self.stacked_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)


        self.setLayout(self.stacked_layout)


    def resizeEvent(self, event):
        self.bg_label.setPixmap(
            self.bg_pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio))
        self.bg_label.resize(self.size())
        return super().resizeEvent(event)
    def next_round_clicked(self):
        if self.EncryptOrDecrypt == "E":
            if self.feistel.roundNumber < self.feistel.roundsToRun:
                self.feistel.feistelRoundEncrypt()
                self.round_count.setText(f"Current Round: {self.feistel.roundNumber} \nCurrent Key: {self.feistel.key}")
                self.TopLeftScreen.setText(f"Current Left:\n {self.feistel.preLeft}")
                self.TopRightScreen.setText(f"Current Right:\n {self.feistel.preRight}")
                self.BottomLeftScreen.setText(f"New Left:\n {self.feistel.left}")
                self.BottomRightScreen.setText(f"New Right:\n {self.feistel.right}")
            else:
                self.ExitButton.setEnabled(True)
                self.DecryptButton.setEnabled(True)
                self.NextRoundButton.setEnabled(False)
        elif self.EncryptOrDecrypt == "D":
            if self.feistel.roundNumber > 0:
                self.feistel.feistelRoundDecrypt()
                print(self.feistel.key)
                self.round_count.setText(
                    f"Current Round (Reverse): {self.feistel.roundNumber}\n Current Key: {self.feistel.key}")
                self.TopLeftScreen.setText(f"Current Left:\n {self.feistel.preLeft}")
                self.TopRightScreen.setText(f"Current Right:\n {self.feistel.preRight}")
                self.BottomLeftScreen.setText(f"New Left:\n {self.feistel.left}")
                self.BottomRightScreen.setText(f"New Right:\n {self.feistel.right}")
                self.ExitButton.setEnabled(False)
                self.DecryptButton.setEnabled(False)
                self.NextRoundButton.setEnabled(True)
            if self.feistel.roundNumber == 0:
                final_binary = self.feistel.right+self.feistel.left 
                try:
                    decrypted_text = self.feistel.binary32_to_text(final_binary)
                except ValueError as e:
                    decrypted_text = f"Error: {e}"
                self.round_count.setText(f"Finished!\nDecrypted Result: {decrypted_text}")
                #to anyone reading this, The reason im setting left and right and right as left is to account for that last permutation after the last round, it works as it should
                print("Left: " + self.feistel.right)
                print("Right: " + self.feistel.left)
                self.ExitButton.setEnabled(True)
                self.DecryptButton.setEnabled(False)
                self.NextRoundButton.setEnabled(False)

    def keepGoing(self, TF):
        self.keepGoingTF = TF
        if self.keepGoingTF:
            self.EncryptOrDecrypt = "D"
            self.feistel.left, self.feistel.right = self.feistel.right, self.feistel.left
            self.TopLeftScreen.setText(f"Current Left:\n {self.feistel.left}")
            self.TopRightScreen.setText(f"Current Right:\n {self.feistel.right}")
            self.BottomLeftScreen.setText(f"N/A")
            self.BottomRightScreen.setText(f"N/A")
            self.NextRoundButton.setEnabled(True)
            self.DecryptButton.setEnabled(False)
            self.ExitButton.setEnabled(False)

        else:
            self.close()










if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BeginGUI()
    window.show()
    sys.exit(app.exec_())
