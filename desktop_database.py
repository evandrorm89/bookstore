'''This program uses the tkinter and sqlite3 modules to create and manipulate a database based on a booklist where the
user can add, delete or update information of books using the Tkinter GUI'''

from tkinter import *
import sqlite3

window = Tk()

window.wm_title("Bookstore")

#Here are some functions to implement the buttons in the Tkinter GUI

#function to get the row the user has clicked and put it in the titles as well
def get_selected_row(event):
	try:	
		global selected_tuple

		index = l1.curselection()[0]
		selected_tuple = l1.get(index)

		entry1.delete(0, END)
		entry1.insert(END, selected_tuple[1])
		entry2.delete(0, END)
		entry2.insert(END, selected_tuple[2])
		entry3.delete(0, END)
		entry3.insert(END, selected_tuple[3])
		entry4.delete(0, END)
		entry4.insert(END, selected_tuple[4])
	except IndexError:
		pass
	

def create_table():
	con = sqlite3.connect("books.db")
	cur = con.cursor()

	cur.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INT, isbn INT)")

	con.commit()
	con.close()


def view_all():
	con = sqlite3.connect("books.db")
	cur = con.cursor()

	cur.execute("SELECT * FROM books")
	rows = cur.fetchall()
	l1.delete(0, END)
	for i in rows:
		l1.insert(END, i)

	con.close()

def search():
	con = sqlite3.connect("books.db")
	cur = con.cursor()

	cur.execute("SELECT * FROM books WHERE title = ? OR author = ? OR year = ? OR isbn = ?", (e1_value.get(), e2_value.get(), e3_value.get(), e4_value.get()))
	rows = cur.fetchall()
	l1.delete(0, END)
	for i in rows:
		l1.insert(END, i)

	con.close()

def add():
	con = sqlite3.connect("books.db")
	cur = con.cursor()

	cur.execute("INSERT INTO books VALUES (NULL, ?, ?, ?, ?)", (e1_value.get(), e2_value.get(), e3_value.get(), e4_value.get()))
	
	con.commit()
	con.close()
	l1.delete(0, END)
	l1.insert(END, (e1_value.get(), e2_value.get(), e3_value.get(), e4_value.get()))

def update():
	con = sqlite3.connect("books.db")
	cur = con.cursor()

	cur.execute("UPDATE books SET title = ?, author = ?, year = ?, isbn = ? WHERE id = ?", (e1_value.get(), e2_value.get(), e3_value.get(), e4_value.get(), selected_tuple[0]))
	
	con.commit()
	con.close()
	view_all()

def delete():
	con = sqlite3.connect("books.db")
	cur = con.cursor()

	cur.execute("DELETE FROM books WHERE id = ? ", (selected_tuple[0], ))
	
	con.commit()
	con.close()
	view_all()

create_table()

#Entries

e1_value = StringVar()
e1 = Label(window, text = "Title")
e1.grid(row = 0, column = 0)
entry1 = Entry(window, textvariable = e1_value)
entry1.grid(row = 0, column = 1)

e2_value = StringVar()
e2 = Label(window, text = "Author")
e2.grid(row = 0, column = 2)
entry2 = Entry(window, textvariable = e2_value)
entry2.grid(row = 0, column = 3)

e3_value = StringVar()
e3 = Label(window, text = "Year")
e3.grid(row = 1, column = 0)
entry3 = Entry(window, textvariable = e3_value)
entry3.grid(row = 1, column = 1)

e4_value = StringVar()
e4 = Label(window, text = "ISBN")
e4.grid(row = 1, column = 2)
entry4 = Entry(window, textvariable = e4_value)
entry4.grid(row = 1, column = 3)

#Buttons

b1 = Button(window, text = "View All", width = 12, command = view_all)
b1.grid(row = 2, column = 3)

b2 = Button(window, text = "Search Entry", width = 12, command = search)
b2.grid(row = 3, column = 3)

b3 = Button(window, text = "Add Entry", width = 12, command = add)
b3.grid(row = 4, column = 3)

b4 = Button(window, text = "Update Selected", width = 12, command = update)
b4.grid(row = 5, column = 3)

b5 = Button(window, text = "Delete Selected", width = 12, command = delete)
b5.grid(row = 6, column = 3)

b6 = Button(window, text = "Close", width = 12, command = window.destroy)
b6.grid(row = 7, column = 3)

#Output

l1 = Listbox(window, height = 6, width = 40)
l1.grid(row = 2, column = 0, rowspan = 6, columnspan = 2)

#Scrollbar for the listbox
sb1 = Scrollbar(window)
sb1.grid(row = 2, column = 2, rowspan = 6)

#Configuring the scrollbar to the listbox
l1.configure(yscrollcommand = sb1.set)
sb1.configure(command = l1.yview)

#get the event of clicking on the selected row in the listbox
l1.bind('<<ListboxSelect>>', get_selected_row)

window.mainloop()