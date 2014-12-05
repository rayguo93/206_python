#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import cgi
import cgitb

cgitb.enable()

form = cgi.FieldStorage()
username = form.getvalue('username')
productNames = []
productAmounts = []
maxIndex = 0

#get from the form which checkboxes with ticked and the quantities
if form.getvalue('dog1'):
	productNames.append('dog1')
	value = form.getvalue('numDog1')
	if value != None:
		productAmounts.append(int(value))
	else:
		productAmounts.append(0)
	maxIndex = maxIndex+1

if form.getvalue('dog2'):
	productNames.append('dog2')
	value = form.getvalue('numDog2')
	if value != None:
		productAmounts.append(int(value))
	else:
		productAmounts.append(0)

	maxIndex = maxIndex+1

if form.getvalue('dog3'):
	productNames.append('dog3')
	value = form.getvalue('numDog3')
	if value != None:
		productAmounts.append(int(value))
	else:
		productAmounts.append(0)

	maxIndex = maxIndex+1

isLogged = 0
totalCost = 0.0

#check if the user is logged in
import csv
with open('../data/LoggedIn.csv', 'rb') as loggedInUsersFile:
	reader = csv.reader(loggedInUsersFile)
	for row in reader:
		if row[0] == username:
			isLogged = 1

#if he is print a bill from the inventory file
if isLogged == 1:

	print "Content-Type: text/html;charset=us-ascii\n\n"
	print "<html>\n"
	print "<head>\n"
	print "<title>Your Bill</title>\n"
	print "</head>\n\n"
	print "<body>\n\n"
	print "<table cellspacing = '1' border = '1'>\n\n"
	print "<tr>\n"
	print "<td>Product Name</td>\n"
	print "<td>Number of units</td>\n"
	print "<td>Price</td>\n"
	print "</tr>"

	newRows = []
	index = 0

	with open('../data/Inventory.csv', 'rb') as inventoryFile:
		reader = csv.reader(inventoryFile)
		for row in reader:
			newRows.append(row)

	for i in range(0, maxIndex):
		index = 0
		with open('../data/Inventory.csv', 'rb') as inventoryFile:
			reader = csv.reader(inventoryFile)
			for row in reader:
				if row[0] == productNames[i]:
					if int(row[1]) < productAmounts[i]:
						productAmounts[i] = int(row[1])
					totalCost += (float(row[2]) * productAmounts[i])
					newRows[index][1] = int(row[1]) - productAmounts[i]
					print"<tr>\n"
					print "<td>%s</td>\n" % productNames[i]
					print "<td>%d</td>\n" % productAmounts[i]
					print "<td>%0.2f</td>\n" % (float(row[2]) * productAmounts[i])
					print "</tr>\n"
					break
				index = index + 1

	
	print "<tr>\n"
	print "<td>Total Cost</td>\n"
	print "<td colspan = '2' align='right'>%0.2f</td>\n" % totalCost
	print "</tr>\n"
	print"</table>\n\n"
	print"<a href='../index.html'><br><br>Home</a><br><br>\n"
	print"<a href='../catalogue.html'>Back to catalogue</a><br><br>\n"
	print"</body>\n"
	print"</html>\n"

	with open('../data/Inventory.csv', 'wb') as inv:
		writer = csv.writer(inv)
		writer.writerows(newRows)


else:
	#1.1 If not logged in then display error screen in HTML linking back to catalogue.

	print "Content-Type: text/html;charset=us-ascii\n\n"
	print "<html>\n"
	print "<head>\n"
	print"<title>Failure</title>\n"
	print"</head>\n\n"
	print"<body>\n\n"
	print"<b>Purchase Failed, you need to log in!<br><br></b>\n"
	print"<a href='../index.html'>Home</a><br><br>\n"
	print"<a href='../login.html'>Back to login</a><br><br>\n"
	print"</body>\n"
	print"</html>\n"



