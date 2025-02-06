import tkinter
import random
from time import sleep


class fiestelRunEncryption():
    def __init__(self):
        self.roundNumber = 0
        self.key = ""
        self.left = ""
        self.right = ""

    def plaintext_preparer(self, plaintext):
        if len(plaintext) != 4:
            print("The plaintext must be 4 characters long")
            return
        else:
            res = ''.join(format(ord(i), '08b') for i in plaintext)
            self.left = res[:16]
            self.right = res[16:32]
            print("Left:", self.left, "Right:", self.right)


    def rand_key(self):
        self.key = ""
        for i in range(16):
            temp = random.randint(0, 1)
            self.key += str(temp)
        print("Random key:", self.key)

    def xor(self, i1, i2):
        temp = ""
        for i in range(len(i1)):  # iterate by index
            if i1[i] == i2[i]:
                temp += "0"
            else:
                temp += "1"
        return temp

    def feistelRound(self):
        self.roundNumber += 1




def encrypt():
    Run = fiestelRunEncryption()

    def on_submit_plaintext():
        plaintext = inputPlaintext.get()
        Run.plaintext_preparer(plaintext)  # Now passing the plaintext to the method
        Run.rand_key()

        inputPlaintext.delete(0, tkinter.END)
        sleep(0.5)
        outputLabel.config(text=f"Left: {Run.left}\nRight: {Run.right}\nKey: {Run.key}", fg="light blue")

    startScreen = tkinter.Tk()
    startScreen.resizable(True, True)
    startScreen.title("Setup Encryption")
    startScreen.geometry("400x400")
    startScreen.config(bg="white")

    inputPlaintext = tkinter.Entry(startScreen, width=40)
    inputPlaintext.pack(padx=5, pady=5)

    submitButton = tkinter.Button(startScreen, text="Submit", command=on_submit_plaintext)
    submitButton.pack(padx=5, pady=5)
    outputLabel = tkinter.Label(startScreen, text="", bg="white")
    outputLabel.pack(pady=10)

    startScreen.mainloop()
    runningScreen = tkinter.Tk()

    roundDisplay = tkinter.Label(runningScreen, text="Round " + str(Run.roundNumber))
    nextRound = tkinter.Button(runningScreen, text="Next Round", command=Run.feistelRound)
    roundDisplay.pack()
    nextRound.pack()

    #runningScreen.mainloop()
encrypt()

