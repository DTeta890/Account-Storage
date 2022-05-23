from logging import root
from tkinter import *
from tkinter import messagebox
import tkinter.messagebox

# ****** GLOBAL VARIABLES ******

accounts = []
root = Tk()  # tkinter window
root.withdraw()  # Hides the window. Need to authenticate first
root.title('Account Manager')


class Pop_Up_Window:

    loop = False
    attempts = 0

    def __init__(self, master):  # Prepares the view
        top = self.top = Toplevel(master)
        top.title('Authentication')
        top.geometry('{}x{}'.format(300, 170))
        top.resizable(width=False, height=False)
        self.label = Label(top, text=" Password: ", font=(
            'Calibri', 14), justify=CENTER)
        self.label.pack(pady=10)
        self.entry = Entry(top, show='*', width=30)
        self.entry.pack(pady=15)
        self.button = Button(top, text='Submit',  # Submit button, on click callles submit_auth func.
                             command=self.submit_auth, font=('Calibri', 14))
        self.button.pack(pady=7)

    def submit_auth(self):
        self.value = self.entry.get()
        access = '1234'

        if self.value == access:  # If value entered matches 'access' => access the dashboard
            self.loop = True
            self.top.destroy()
            root.deiconify()  # Shows the window after authentication
        else:
            self.attempts += 1  # You can try 5 times than window will close
            if self.attempts == 5:
                root.quit()
            self.e .delete(0, 'end')
            messagebox.showerror(
                'Incorrect Password', 'Incorrect password, attempts remaining: ' + str(5 - self.attempts))


class Add_Account:

    def __init__(self, master, account_name, account_email, account_pass):
        self.root = master
        self.account_name = account_name
        self.account_email = account_email
        self.account_pass = account_pass

    def write(self):
        file_input = open('emails.txt', "a")
        acc_name = self.account_name
        acc_email = self.account_email
        acc_pass = self.account_pass

        encryptedAccountName = ""
        encryptedAccountEmail = ""
        encryptedAccountPass = ""
        # Account name encription
        for letter in acc_name:
            if letter == ' ':
                encryptedAccountName += ' '
            else:
                # Returns the unicode and adds 4 to the value
                encryptedAccountName += chr(ord(letter) + 4)
        # Account email encription
        for letter in acc_email:
            if letter == ' ':
                encryptedAccountEmail += ' '
            else:
                # Returns the unicode and adds 7 to the value
                encryptedAccountEmail += chr(ord(letter) + 7)
        # Account password encription
        for letter in acc_pass:
            if letter == ' ':
                encryptedAccountPass += ' '
            else:
                # Returns the unicode and adds 9 to the value
                encryptedAccountPass += chr(ord(letter) + 9)

        file_input.write(
            f'{encryptedAccountName},{encryptedAccountEmail},{encryptedAccountPass}, \n')
        file_input.close()


class Account_Display:

    def __init__(self, master, account_name, account_email, account_pass, index):
        self.root = master
        self.account_name = account_name
        self.account_email = account_email
        self.account_pass = account_pass
        self.index = index

        dencryptedAccountName = ""
        dencryptedAccountEmail = ""
        dencryptedAccountPass = ""
        # Account name decription
        for letter in self.account_name:
            if letter == ' ':
                dencryptedAccountName += ' '
            else:
                # Substracts unicode by 4 and returns the character
                dencryptedAccountName += chr(ord(letter) - 4)
        # Account email decription
        for letter in self.account_email:
            if letter == ' ':
                dencryptedAccountEmail += ' '
            else:
                # Substracts unicode by 7 and returns the character
                dencryptedAccountEmail += chr(ord(letter) - 7)
        # Account password decription
        for letter in self.account_pass:
            if letter == ' ':
                dencryptedAccountPass += ' '
            else:
                # Substracts unicode by 9 and returns the character
                dencryptedAccountPass += chr(ord(letter) - 9)

        # Sets the view components texts
        self.label_name = Label(
            self.root, text=dencryptedAccountName, font=('Calibri', 14))
        self.label_email = Label(
            self.root, text=dencryptedAccountEmail, font=('Calibri', 14))
        self.label_pass = Label(
            self.root, text=dencryptedAccountPass, font=('Calibri', 14))
        self.deleteButton = Button(
            self.root, text='Del', fg='red', command=self.delete)

    def display(self):
        # Displayes the view components
        self.label_name.grid(row=6 + self.index, sticky=W)
        self.label_email.grid(row=6 + self.index, column=1)
        self.label_pass.grid(row=6 + self.index, column=2, sticky=E)
        self.deleteButton.grid(row=6 + self.index, column=3, sticky=E)

    def delete(self):
        # Asks the user if sure to delete the account
        answer = tkinter.messagebox.askquestion(
            'Delete', 'Are you sure you want to delete this entry?')

        if answer == 'yes':
            # Removes all accounts from the list
            for item in accounts:
                item.destroy()

            file_input = open('emails.txt', 'r')
            lines = file_input.readlines()
            file_input.close()

            file_input = open('emails.txt', "w")
            index = 0

            # After reading file lines, overwrite all except the one with the deleted index
            for line in lines:
                if index != self.index:
                    file_input.write(line)
                index += 1

            file_input.close()
            # Reloads the list of accounts displayed
            readfile()

    def destroy(self):
        self.label_name.destroy()
        self.label_email.destroy()
        self.label_pass.destroy()
        self.deleteButton.destroy()


# ******* FUNCTIONS *********


def onsubmit():
    input_acc_name = acc_name.get()
    input_email = email.get()
    input_pass = password.get()
    account = Add_Account(root, input_acc_name, input_email, input_pass)
    account.write()
    # Resets the input fields
    acc_name.delete(0, 'end')
    email.delete(0, 'end')
    password.delete(0, 'end')
    messagebox.showinfo(
        'Added Entity', f'Successfully Added,\nAcc. Name: {input_acc_name}\nEmail: {input_email}\nPassword: {input_pass}')
    # Reloads the list of accounts displayed after new one added
    readfile()


def readfile():
    file_input = open('emails.txt', 'r')
    index = 0

    for line in file_input:
        account_list = line.split(',')
        # After spliting by comma displayes the rows also resets the indexes after delite
        e = Account_Display(
            root, account_list[0], account_list[1], account_list[2], index)
        accounts.append(e)
        e.display()
        index += 1
    file_input.close()


# ******* GRAPHICS *********

window = Pop_Up_Window(root)

entity_label = Label(root, text='Add Account', font=('Calibri', 18))
name_label = Label(root, text='Acc. Name: ', font=('Calibri', 14))
email_label = Label(root, text='Email: ', font=('Calibri', 14))
pass_label = Label(root, text='Password: ', font=('Calibri', 14))
acc_name = Entry(root, font=('Calibri', 14))
email = Entry(root, font=('Calibri', 14))
password = Entry(root, show='*', font=('Calibri', 14))
submit = Button(root, text='Insert',
                command=onsubmit, font=('Calibri', 14))

entity_label.grid(columnspan=3, row=0)
name_label.grid(row=1, sticky=E, padx=3)
email_label.grid(row=2, sticky=E, padx=3)
pass_label.grid(row=3, sticky=E, padx=3)

acc_name.grid(columnspan=3, row=1, column=1, padx=2, pady=2, sticky=W)
email.grid(columnspan=3, row=2, column=1, padx=2, pady=2, sticky=W)
password.grid(columnspan=3, row=3, column=1, padx=2, pady=2, sticky=W)

submit.grid(columnspan=3, pady=4)

name_label2 = Label(root, text='Acc. Name: ', font=('Calibri', 14))
email_label2 = Label(root, text='Email: ', font=('Calibri', 14))
pass_label2 = Label(root, text='Password: ', font=('Calibri', 14))

name_label2.grid(row=5)
email_label2.grid(row=5, column=1)
pass_label2.grid(row=5, column=2)

readfile()

root.mainloop()
