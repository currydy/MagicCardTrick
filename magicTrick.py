from tkinter import *
import speech_recognition as sr
from PIL import Image, ImageTk
from gtts import gTTS
from playsound import playsound
import random
import os


class MagicTrick:
    def __init__(self, mic, rec):
        self.mic = mic
        self.rec = rec
        self.cards = []
        self.choice = 0
        self.choice_count = 0
        self.answer = []


    def make_cards(self):
        cards = [
            [[1,"spades"], [7, "hearts"], [7, "diamonds"]],
            [[2, "clubs"], [2, "hearts"], [3, "clubs"]],
            [[1, "diamonds"], [3, "spades"], [8, "hearts"]],
            [[6, "hearts"], [4, "diamonds"], [1, "hearts"]],
            [[5, "spades"], [8, "clubs"], [5, "hearts"]],
            [[4, "hearts"], [9, "spades"], [6, "diamonds"]],
            [[3, "diamonds"], [4, "hearts"], [7, "spades"]],
            [[5, "clubs"], [3, "hearts"], [8, "diamonds"]],
            [[9, "hearts"], [6, "spades"], [9, "diamonds"]]
        ]
        for l in cards:
            random.shuffle(l)
        random.shuffle(cards)
        self.cards = cards


    def get_cards(self):
        return self.cards


    def get_speech(self):
        with self.mic as source:
            self.rec.adjust_for_ambient_noise(source)
            audio = self.rec.listen(source)

        try:
            speech_text = rec.recognize_google(audio)

        except sr.UnknownValueError:
            speech_text = "Error with speech recognition"

        except sr.RequestError:
            speech_text = "Error with API"

        return speech_text


    def show_answer(self, rt):
        x_pos = 10
        y_pos = 10
        path_string = "./cards/" + str(self.answer[0]) + "_" + self.answer[1] + ".png"
        image1 = Image.open(path_string)
        test = ImageTk.PhotoImage(image1)
        label1 = Label(image=test)
        label1.image = test
        label1.place(x=x_pos, y=y_pos)


    def show_cards(self, rt):
        x_pos = 10
        y_pos = 10
        for c in self.cards:
            for t in c:
                path_string = "./cards/" + str(t[0]) + "_" + t[1] + ".png"
                image1 = Image.open(path_string)
                test = ImageTk.PhotoImage(image1)
                label1 = Label(image=test)
                label1.image = test
                label1.place(x=x_pos, y=y_pos)
                x_pos += 300
            y_pos += 50
            x_pos = 10
        for c in self.cards:
            for t in c:
                print("{:14}".format(str(t[0]) + " " + t[1]), end=" ")
            print()


    def choose_column(self):
        speech = self.get_speech().lower()
        #speech = input("Enter column number: ")
        print("You said:", speech)
        while(1):
            if speech == "1":
                self.choice = 1
                break
            elif speech == "2":
                self.choice = 2
                break
            elif speech == "3":
                self.choice = 3
                break
            else:
                print("Not a valid column choice, try again")
                speech = self.get_speech().lower()
        self.choice_count += 1


    def shuffle(self):
        new_deck = [[[0, " "] for i in range(3)] for j in range(9)]
        if self.choice != 2:
            for r in range(len(self.cards)):
                for c in range(len(self.cards[r])):
                    if c == self.choice-1:
                        temp1 = self.cards[r][1]
                        new_deck[r][1][0] = self.cards[r][c][0]
                        new_deck[r][1][1] = self.cards[r][c][1]
                        new_deck[r][self.choice-1][0] = temp1[0]
                        new_deck[r][self.choice - 1][1] = temp1[1]
                    elif c != 1:
                        new_deck[r][c][0] = self.cards[r][c][0]
                        new_deck[r][c][1] = self.cards[r][c][1]

            self.cards = new_deck
        if self.choice_count == 3:
            self.answer = self.cards[4][1]


    def place_by_row(self):
        new_deck = [[[0, " "] for i in range(3)] for j in range(9)]
        column1 = []
        column2 = []
        column3 = []
        print(new_deck)
        for r in range(len(self.cards)):
            for c in range(len(self.cards[r])):
                if c == 0:
                    column1.append(self.cards[r][c])
                elif c == 1:
                    column2.append(self.cards[r][c])
                elif c == 2:
                    column3.append(self.cards[r][c])

        column1.extend(column2)
        column1.extend(column3)
        counter = 0
        for row in range(len(new_deck)):
            for i in range(3):
                new_deck[row][i] = column1[counter]
                counter += 1

        self.cards = new_deck


def speak(mytext):
    language = "en"

    myobj = gTTS(text=mytext, lang=language, slow=False)

    # Saving the converted audio in a mp3 file named
    # welcome
    os.remove("ai.mp3")
    myobj.save("ai.mp3")

    # Playing the converted file
    playsound("ai.mp3")


def close_window():
    root.destroy()


if __name__ == "__main__":

    rec = sr.Recognizer()
    mic = sr.Microphone()

    m_t = MagicTrick(mic, rec)
    m_t.make_cards()

    root = Tk()
    root.geometry("900x700")
    m_t.show_cards(root)
    speak("once the window pops up, please pick a card and take note of the column it is in")
    button = Button(text="click once card located", command=close_window)
    button.place(x=300, y=600)
    root.mainloop()

    #round 1
    root = Tk()
    root.geometry("900x700")
    speak("what column was your card in?")
    m_t.choose_column()
    print("Choice is:", m_t.choice)
    m_t.shuffle()
    m_t.place_by_row()
    m_t.show_cards(root)
    speak("please locate your card and note the column it is in")
    button = Button(text="click once card located", command=close_window)
    button.place(x=300, y=600)
    root.mainloop()

    #round 2
    root = Tk()
    root.geometry("900x700")
    speak("what column was your card in?")
    m_t.choose_column()
    print("Choice is:", m_t.choice)
    m_t.shuffle()
    m_t.place_by_row()
    m_t.show_cards(root)
    speak("please locate your card and note the column it is in")
    button = Button(text="click once card located", command=close_window)
    button.place(x=300, y=600)
    root.mainloop()

    #round3
    root = Tk()
    root.geometry("900x700")
    speak("what column was your card in?")
    m_t.choose_column()
    print("Choice is:", m_t.choice)
    m_t.shuffle()
    m_t.show_answer(root)
    speak("your card is " + str(m_t.answer[0]) + " of " + m_t.answer[1])
    print("your card is: ", m_t.answer)
    button = Button(text="click once card located", command=close_window)
    button.place(x=300, y=600)
    root.mainloop()







