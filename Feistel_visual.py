import tkinter
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

    def RotateKey(self):
        self.key = self.key[1:] + self.key[0]
    def feistelRound(self):
        self.preLeft = self.left
        self.preRight = self.right
        self.roundNumber += 1
        self.left = self.right
        self.right = self.xor(self.left, self.key)
        self.RotateKey()





def encrypt():
    Run = fiestelRun()

    def on_submit_plaintext():
        plaintext = inputPlaintext.get()
        error = Run.plaintext_preparer(plaintext)
        Run.rand_key()
        inputPlaintext.config(state=tkinter.DISABLED)
        submitButton.config(state=tkinter.DISABLED)
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
        roundOptions = {'4 Rounds': 4, '8 Rounds': 8}
        for text, value in roundOptions.items():
            radio_button = tkinter.Radiobutton(startScreen, text=text, variable=r, value=value, background="white")
            radio_button.pack(side=tkinter.TOP, ipady=5)

        beginButton = tkinter.Button(startScreen, text="Begin Encryption", command=setupComplete)
        beginButton.pack(side=tkinter.TOP, ipady=5)

    def setupComplete():
        startScreen.withdraw()
        runningScreen.deiconify()
        Run.roundsToRun = r.get()
        running()



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
    def running():

        if Run.roundNumber <= Run.roundsToRun:

            roundDisplay.config(text=f"Round {Run.roundNumber}")
            Run.feistelRound()
            leftInput.config(text=f"Left: {Run.left}")
            rightInput.config(text=f"Right: {Run.right}")
            leftResult.config(text=f"Left: {Run.preLeft}")
            rightResult.config(text=f"Right: {Run.preRight}")



        if Run.roundNumber > Run.roundsToRun:
            nextRound.config(state=tkinter.DISABLED)
            roundDisplay.config(text="Encryption Complete!")
            complete()
    def complete():
        startScreen.destroy()
        outputLabel3 = tkinter.Label(runningScreen, text="Do you want to close the program or decrypt the ciphertext you made?", bg="white")
        outputLabel3.grid(row=7, column=0)
        exitButton = tkinter.Button(runningScreen, text="Exit", command=runningScreen.destroy)
        decryptButton =tkinter.Button(runningScreen, text="Decrypt", command=runningScreen.destroy)
        exitButton.grid(row=8, column = 0, sticky = "w", padx=25, pady=5)
        decryptButton.grid(row=8, column = 1, sticky = "e", padx=25, pady=5)


    roundDisplay = tkinter.Label(runningScreen, text="Round " + str(Run.roundNumber), relief="ridge", height=5, width=20, font=("Harrington", 20))
    nextRound = tkinter.Button(runningScreen, text="Next Round", command=running, padx=5, pady=5)
    leftInput = tkinter.Label(runningScreen, text="Left Input: " + str(Run.preLeft), bg="Light blue", height=5, width=20, fg="green", relief="ridge", font=("Comic Sans MS", 14))
    rightInput = tkinter.Label(runningScreen, text="Right Input: " + str(Run.preRight), bg="Light blue", height=5, width=20, fg="green", relief="ridge", font=("Comic Sans MS", 14))
    leftResult = tkinter.Label(runningScreen, text="Left Result: " + str(Run.left), bg="Light blue", height=5, width=20, fg="green", relief="ridge", font=("Comic Sans MS", 14))
    rightResult = tkinter.Label(runningScreen, text = "Right Result" + str(Run.right), bg="Light blue", height=5, width=20, fg="green", relief="ridge", font=("Comic Sans MS", 14))
    keyCycle = tkinter.Label(runningScreen ,text = "Using a simple circular shift (For simplicity I am using a circular shift but there are may other ways you can change the key per round) you get from", bg="light blue", fg="green", relief="ridge", font=("Comic Sans MS", 14))
    roundDisplay.grid(row=0, column=0, columnspan=2, pady=10)
    leftInput.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    rightInput.grid(row=2, column=1, padx=10, pady=5, sticky="e")
    keyCycle.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    leftResult.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    rightResult.grid(row=4, column=1, padx=10, pady=5, sticky="e")
    nextRound.grid(row=6, column=0, columnspan=2, pady=10)
    runningScreen.grid_columnconfigure(0, weight=1)
    runningScreen.grid_columnconfigure(1, weight=1)
    runningScreen.withdraw()
    startScreen.mainloop()


encrypt()

