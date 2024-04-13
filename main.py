#This program will pop up a UI that allows you to input credentials for a password management system, and then stores the information in a text file.

import random, tkinter, tkinter.messagebox, pyperclip, json
FONT_NAME = "Arial"

#Creation of Window UI
window = tkinter.Tk()
window.title("Password Manager")
window.config(padx=20,pady=20)

#Adding in Lock Image
canvas = tkinter.Canvas(height=150, width=150)
lockImage = tkinter.PhotoImage(file="padlock.png")
lockImage = lockImage.subsample(3,3)
canvas.create_image(75,75,image=lockImage)
canvas.grid(column=1,row=0)


#Password Generator
def generatePassword():
    passwordOptions = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWYZ1234567890!@#$%^&*"
    passwordOptionsList = list(passwordOptions)
    generatedPassword = ""
    lastChar = None
    #Creates a 18 character long password that doesn't allow two same characters in a row
    for i in range(16):
        addedChar = random.choice(passwordOptionsList)
        while addedChar == lastChar:
            addedChar = random.choice(passwordOptionsList)
        generatedPassword += addedChar
        lastChar = addedChar
    passwordEntry.delete(0,'end')
    pyperclip.copy(generatedPassword)
    passwordEntry.insert(0,generatedPassword)

#Add credentials to a file
def addData():
    if len(websiteEntry.get()) == 0:
        popUpMessage("You forgot to enter a website name.")
    elif len(usernameEntry.get()) == 0:
        popUpMessage("You forgot to enter a username/email.")
    elif len(passwordEntry.get()) == 0:
        popUpMessage("You forgot to add a password.")
    else:
        newData = {
            websiteEntry.get(): {
                "email": usernameEntry.get(),
                "password": passwordEntry.get(),
            }
        }
        try:
            with open("data.json", "r") as dataFile:
                #puts json file into dict
                data = json.load(dataFile)
                #Puts new data into the dictionary
                data.update(newData)
        except FileNotFoundError:
            #If the file doesn't exist, just create a new one with this entry
            data = newData
        with open("data.json", "w") as dataFile:
            #Saves new data
            json.dump(data, dataFile, indent=4)
        #Empties the password and website entries
        passwordEntry.delete(0,'end')
        websiteEntry.delete(0,'end')


#Pop up message if there is an issue 
def popUpMessage(message):
    popUp = tkinter.messagebox.showinfo("Error", message)


def search():
    try:
        with open("data.json", "r") as dataFile:
            data = json.load(dataFile)
        website = websiteEntry.get()
        if website in data.keys():
            specificSite = data.get(website)
            user = specificSite.get("email")
            password = specificSite.get("password")
            tkinter.messagebox.showinfo("Credentials Info", "Email/Username: " + user + "\nPassword: " + password)
        elif len(websiteEntry.get()) == 0:
            pass
        else:
            tkinter.messagebox.showinfo("Entry not found", "There is no entry for " + website)

    except FileNotFoundError:
        tkinter.messagebox.showinfo("You do not have a data file.")



#Left Side Text
websiteText = tkinter.Label(text="Website:", font=(FONT_NAME, 10))
websiteText.grid(column=0, row=1)

usernameText = tkinter.Label(text="Username:", font=(FONT_NAME, 10))
usernameText.grid(column=0, row=2)

passwordText = tkinter.Label(text="Password:", font =(FONT_NAME, 10))
passwordText.grid(column=0,row=3)

#User Input Text Boxes
websiteEntry = tkinter.Entry(width=24)
websiteEntry.grid(column=1,row=1, columnspan=1)
websiteEntry.focus()
usernameEntry = tkinter.Entry(width=36)
usernameEntry.grid(column=1,row=2, columnspan=2)

passwordEntry = tkinter.Entry(width=24)
passwordEntry.grid(column=1,row=3)

#Search Button
searchButton = tkinter.Button(text="Search",font=(FONT_NAME,10), command=search)
searchButton.grid(column=2,row=1)
 
#Password Button
generatePasswordButton = tkinter.Button(text="Generate", font=(FONT_NAME, 10), command=generatePassword)
generatePasswordButton.grid(column=2,row=3)

addCredentialsButton = tkinter.Button(text="Add Account", font=(FONT_NAME, 10),width=18,command=addData)
addCredentialsButton.grid(column=1,row=4)




#Basically a while loop to keep the window open (without it, the window would just instantly close)
window.mainloop()