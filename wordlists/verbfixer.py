rawlistFile = open("verb list raw.txt", "rt")
rawlist = rawlistFile.read()

letters = '.1234567890 ABCDEFGHIJKLMNOPQRSTUVWXYZ+' # there are capital markers that have to be removed

newlist = rawlist

for char in letters:
    newlist = newlist.replace(char, '')

newlistFile = open("new verb list.txt", "wt")
newlistFile.write(newlist)
newlistFile.close()