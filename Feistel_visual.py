import tkinter
import random
from time import sleep
from tkinter.constants import RIGHT


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
    def feistelRound(self):
        self.preLeft = self.left
        self.preRight = self.right
        self.preKey = self.key

        self.RotateKey()
        self.roundNumber += 1
        self.left = self.right
        self.Fresult = self.xor(self.key, self.preRight)
        self.right = self.xor(self.preLeft, self.Fresult)
    def Decrypt(self):


        self.roundNumber = self.roundNumber - 1






def encrypt():
    Run = fiestelRun()

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
            inputPlaintext.config(state=tkinter.DISABLED)
            submitButton.config(state=tkinter.DISABLED)
            outputLabel.config(text=f"Left: {Run.left}\nRight: {Run.right}\nKey: {Run.key}", fg="green", font=("Bookman old style", 12))
            set_rounds()

    def set_rounds():
        outputLabel2.config(text="Choose how many rounds you wish to run the cipher", fg="mint cream", font=("Bookman old style", 12))
        roundOptions = {'4 Rounds': 4, '8 Rounds': 8}
        for text, value in roundOptions.items():
            radio_button = tkinter.Radiobutton(startScreen, text=text, variable=r, value=value, background="grey21", foreground="mint cream", font=("Bookman old style", 12))
            radio_button.pack(ipady=25)

        beginButton = tkinter.Button(startScreen, text="Begin Encryption", command=setupComplete, background="mint cream")
        beginButton.pack(ipady=25)
        beginButton.pack(side=tkinter.TOP, ipady=5)

    def setupComplete():
        startScreen.withdraw()
        runningScreen.deiconify()
        Run.roundsToRun = r.get()
        initDisplay()

    def fromStarting():
        getStarted.config(state=tkinter.DISABLED)
        nextRound.config(state=tkinter.NORMAL)
        running()



    startScreen = tkinter.Tk()
    startScreen.resizable(True, True)
    startScreen.title("Setup Encryption")
    startScreen.geometry("600x800")
    startScreen.config(bg="grey21")
    titleLabel = tkinter.Label(startScreen, text="Fiestel Encryption", bg="grey21", font=("Bookman old style", 30), fg="bisque", relief="sunken")
    titleLabel.pack(pady=15)
    fourChars = tkinter.Label(startScreen, text="Please input a 4 character word", bg="grey21", fg="mint cream", font=("Bookman old style", 15), relief="sunken")
    fourChars.pack(pady=15)
    inputPlaintext = tkinter.Entry(startScreen, width=40, relief="sunken", bg="grey62", fg="bisque")
    inputPlaintext.pack(padx=5, pady=50)

    submitButton = tkinter.Button(startScreen, text="Submit", command=on_submit_plaintext)
    submitButton.pack(padx=5, pady=5)
    outputLabel = tkinter.Label(startScreen, text="", bg="grey21")
    outputLabel.pack(pady=10)
    outputLabel2 = tkinter.Label(startScreen, text="", bg="grey21")
    outputLabel2.pack(pady=10)
    r = tkinter.IntVar()

    runningScreen = tkinter.Tk()
    runningScreen.resizable(True, True)
    runningScreen.title("Encryption")
    runningScreen.geometry("1920x1080")
    runningScreen.config(bg="grey21")
    def running():

        if Run.roundNumber <= Run.roundsToRun:

            roundDisplay.config(text=f"Round {Run.roundNumber}")
            Run.feistelRound()
            keyCycle.config(text=f"Using a simple circular shift \n(For simplicity I am using a circular shift but there are may other ways you can change the key per round)\n you get from {Run.preKey} to {Run.key}")
            leftInput.config(text=f"Left input:\n {Run.preLeft}")
            rightInput.config(text=f"Right input:\n {Run.preRight}")
            leftResult.config(text=f"Left result:\n {Run.left}")
            rightResult.config(text=f"Right result:\n {Run.right}")
            showFxor.config(text=f"Xor {Run.preRight} to {Run.key} \nand you get {Run.Fresult}")
            showNextXor.config(text=f"Xor {Run.Fresult} to {Run.preLeft} \nand you get {Run.right}")

        elif Run.roundNumber > Run.roundsToRun:
            nextRound.config(state=tkinter.DISABLED)
            roundDisplay.config(text="Encryption Complete!")
            complete()
    def decrypt_running():
        pass
    def complete():
        startScreen.destroy()
        outputLabel3 = tkinter.Label(runningScreen, text="Do you want to close the \n program or decrypt the ciphertext you made?", bg="mint cream", fg="black", font=("Bookman old style", 14))
        outputLabel3.grid(row=8, columnspan=2)
        exitButton = tkinter.Button(runningScreen, text="Exit", command=runningScreen.destroy)
        decryptButton =tkinter.Button(runningScreen, text="Decrypt", command=decrypt)
        exitButton.grid(row=9, column = 0, sticky = "w", padx=25, pady=5)
        decryptButton.grid(row=9, column = 1, sticky = "e", padx=25, pady=5)

    def decrypt():
        decrypting = tkinter.Tk()
        decrypting.title("Decrypt")
        decrypting.config(bg="grey21")
        decrypting.geometry("1920x1080")
        decrypting.resizable(True, True)
        roundDisplayD = tkinter.Label(decrypting, text="Round 0", relief="ridge", height=5, width=20,
                                      font=("Harrington", 20), bg="mint cream", fg="dark blue")
        nextRoundD = tkinter.Button(decrypting, text="Next Round", command=running, padx=5, pady=5)
        leftInputD = tkinter.Label(runningScreen, text=f"Left Input:\n {Run.left}", bg="mint cream", height=5, width=20,
                                   fg="green", relief="ridge", font=("Comic Sans MS", 14))
        rightInputD = tkinter.Label(decrypting, text=f"Right Input:\n {Run.right}", bg="mint cream", height=5,
                                    width=20, fg="green", relief="ridge", font=("Comic Sans MS", 14))
        leftResultD = tkinter.Label(decrypting, text="Left Result: TBD", bg="mint cream", height=5, width=20,
                                    fg="green", relief="ridge", font=("Comic Sans MS", 14))
        rightResultD = tkinter.Label(decrypting, text="Right Result: TBD", bg="mint cream", height=5, width=20,
                                     fg="green", relief="ridge", font=("Comic Sans MS", 14))
        keyCycleD = tkinter.Label(decrypting, text=f"Your starting key is {Run.key}", bg="mint cream", fg="green",
                                  relief="ridge", font=("Comic Sans MS", 14))
        showFxorD = tkinter.Label(decrypting, text="Here in the F function we XOR\n the key and the right input",
                                  bg="mint cream", fg="green", relief="ridge", font=("Comic Sans MS", 14))
        showNextXorD = tkinter.Label(decrypting,
                                    text="Here is where the result of F()\n and the left input are Xored",
                                    bg="mint cream", fg="green", relief="ridge", font=("Comic Sans MS", 14))
        roundDisplayD.grid(row=0, column=0, columnspan=2, pady=10)
        leftInputD.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        rightInputD.grid(row=2, column=1, padx=10, pady=5, sticky="e")
        keyCycleD.grid(row=1, column=0, columnspan=2, pady=10)
        nextRoundD.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        showFxorD.grid(row=4, column=1, sticky="e", pady=10)
        showNextXorD.grid(row=4, columnspan=2, pady=10)
        nextRound.config(state=tkinter.DISABLED)
        leftResultD.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        rightResultD.grid(row=5, column=1, padx=10, pady=5, sticky="e")
        runningScreen.destroy()
        decrypting.mainloop()

    def initDisplay():
        leftInput.config(text=f"Left Input:\n {Run.left}")
        rightInput.config(text=f"Right Input:\n {Run.right}")
        keyCycle.config(text=f"Your starting key is {Run.key}")






    roundDisplay = tkinter.Label(runningScreen, text="Round 0", relief="ridge", height=5, width=20, font=("Harrington", 20), bg="mint cream", fg="dark blue")
    nextRound = tkinter.Button(runningScreen, text="Next Round", command=running, padx=5, pady=5)
    leftInput = tkinter.Label(runningScreen, text=f"Left Input:\n {Run.left}", bg="mint cream", height=5, width=20, fg="green", relief="ridge", font=("Comic Sans MS", 14))
    rightInput = tkinter.Label(runningScreen, text=f"Right Input:\n {Run.right}", bg="mint cream", height=5, width=20, fg="green", relief="ridge", font=("Comic Sans MS", 14))
    leftResult = tkinter.Label(runningScreen, text="Left Result: TBD", bg="mint cream", height=5, width=20, fg="green", relief="ridge", font=("Comic Sans MS", 14))
    rightResult = tkinter.Label(runningScreen, text = "Right Result: TBD", bg="mint cream", height=5, width=20, fg="green", relief="ridge", font=("Comic Sans MS", 14))
    keyCycle = tkinter.Label(runningScreen ,text =f"Your starting key is {Run.key}" , bg="mint cream", fg="green", relief="ridge", font=("Comic Sans MS", 14))
    showFxor = tkinter.Label(runningScreen, text="Here in the F function we XOR\n the key and the right input", bg="mint cream", fg="green", relief="ridge", font=("Comic Sans MS", 14))




    showNextXor =tkinter.Label(runningScreen, text="Here is where the result of F()\n and the left input are Xored", bg="mint cream", fg="green" , relief="ridge", font=("Comic Sans MS", 14))
    FCanvas = tkinter.Canvas(runningScreen, bg="grey21", height=50, width=50, bd=0, highlightthickness=0)
    arrowF = FCanvas.create_line(25,0,25,50, arrow=tkinter.LAST, fill="red2", width=7)
    keyCanvas = tkinter.Canvas(runningScreen, bg="grey21", height=210, width=450, bd=0 , highlightthickness=0)
    keyArrow = keyCanvas.create_line(10,10,400,200, arrow=tkinter.LAST, fill= "red2", width=7)
    nextXarr = tkinter.Canvas(runningScreen, bg="grey21", height=50, width=250, bd=0, highlightthickness=0)
    nextXarrow = nextXarr.create_line(10,25,245,25, fill="red2", width=7, arrow=tkinter.FIRST)
    finalArr = tkinter.Canvas(runningScreen, bg="grey21", height=50, width=300, bd=0, highlightthickness=0)
    finalArrow = finalArr.create_line(300,10,10,45, fill="red2", width=7, arrow=tkinter.LAST)


    getStarted = tkinter.Button(runningScreen, text = "Lets start Round 1", command=fromStarting)
    roundDisplay.grid(row=0, column=0, columnspan=2, pady=10)
    leftInput.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    rightInput.grid(row=2, column=1, padx=10, pady=5, sticky="e")
    keyCycle.grid(row=1, column = 0, columnspan = 2, padx=10, pady=20)
    leftResult.grid(row=6, column=0, padx=10, pady=5, sticky="w")
    rightResult.grid(row=6, column=1, padx=10, pady=5, sticky="e")
    nextRound.grid(row=7, column=0, columnspan=2, pady=10)
    showFxor.grid(row=4,column=1,sticky = "e", pady=10)
    showNextXor.grid(row=4, columnspan=2, pady=10)
    nextRound.config(state=tkinter.DISABLED)
    runningScreen.grid_columnconfigure(0, weight=1)
    runningScreen.grid_columnconfigure(1, weight=1)
    getStarted.grid(row=9, column=0, columnspan=2, pady=10)
    FCanvas.grid(row=3, column=1,padx = 60, pady=10, sticky="e")
    keyCanvas.grid(row=2, column = 1, pady=10, padx=100)
    nextXarr.grid(row=4, column=1, padx=12, pady=5)
    finalArr.grid(row=4, column=0, padx=15, pady=5)



    runningScreen.withdraw()
    startScreen.mainloop()




encrypt()

