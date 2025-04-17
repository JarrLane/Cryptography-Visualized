import PySimpleGUI as sg
import random
from time import sleep



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

class FeistelGUI:
    def __init__(self):
        self.beginning = sg.Window('Feistel Visual setup', resizable=True)
