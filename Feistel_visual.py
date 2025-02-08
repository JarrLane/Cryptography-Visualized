import tkinter
import random
from time import sleep


class fiestelRunEncryption():
    def __init__(self):
        self.roundNumber = 0
        self.key = ""
        self.left = ""
        self.right = ""
        self.roundsToRun = 0

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
        error = Run.plaintext_preparer(plaintext)
        Run.rand_key()

        inputPlaintext.delete(0, tkinter.END)
        sleep(0.5)
        if error:
            outputLabel.config(text=error, fg="red")
            return
        else:
            outputLabel.config(text=f"Left: {Run.left}\nRight: {Run.right}\nKey: {Run.key}", fg="green")
            set_rounds()

    def set_rounds():
        outputLabel2.config(text="Choose how many rounds you wish to run the cipher")
        roundOptions = {'4 Rounds': 4, '8 Rounds': 8, '16 Rounds': 16}
        for text, value in roundOptions.items():
            radio_button = tkinter.Radiobutton(startScreen, text=text, variable=r, value=value, background="white")
            radio_button.pack(side=tkinter.TOP, ipady=5)

        beginButton = tkinter.Button(startScreen, text="Begin Encryption", command=setupComplete)
        beginButton.pack(side=tkinter.TOP, ipady=5)

    def setupComplete():
        startScreen.withdraw()
        runningScreen.deiconify()
        Run.roundsToRun = r.get()



    startScreen = tkinter.Tk()
    startScreen.resizable(True, True)
    startScreen.title("Setup Encryption")
    startScreen.geometry("600x600")
    startScreen.config(bg="white")

    inputPlaintext = tkinter.Entry(startScreen, width=40)
    inputPlaintext.pack(padx=5, pady=50)

    submitButton = tkinter.Button(startScreen, text="Submit", command=on_submit_plaintext)
    submitButton.pack(padx=5, pady=5)
    outputLabel = tkinter.Label(startScreen, text="", bg="white")
    outputLabel.pack(pady=10)
    outputLabel2 = tkinter.Label(startScreen, text="", bg="white")
    outputLabel2.pack(pady=10)
    r = tkinter.IntVar()

    runningScreen = tkinter.Tk()
    runningScreen.resizable(True, True)
    runningScreen.title("Encryption")
    runningScreen.geometry("600x600")
    roundDisplay = tkinter.Label(runningScreen, text="Round " + str(Run.roundNumber), relief="ridge", bg="white")
    nextRound = tkinter.Button(runningScreen, text="Next Round", command=Run.feistelRound)
    
    roundDisplay.pack()
    nextRound.pack()
    runningScreen.withdraw()
    startScreen.mainloop()


encrypt()

