import enchant
import random

board = [["a","t",""],["","h",""],["p","e","r"]]

def getWord(board):
	wordsList = []
	eh = set()
	for x in range(len(board)): #row
		for y in range(len(board[0])): #col
			if board[x][y] != "":
				if (y == 0 or board[x][y-1] == ""): #horizontal
					if y < (len(board)-1) and board[x][y+1] != "":
						word = []
						i = x
						j = y
						while j < len(board[0]) and  board[i][j] != "":
							word.append(board[i][j])
							j+= 1
						wordsList.append("".join(word))
				if (x == 0 or board[x-1][y] == ""): #vertical
					if x < (len(board[0])-1) and board[x+1][y] != "":
						word = []
						i = x
						j = y
						while i < len(board) and  board[i][j] != "":
							word.append(board[i][j])
							i+= 1
						wordsList.append("".join(word))
	return wordsList

def checkWords(board):
	toCheck = getWord(board)
	print(toCheck)
	d = enchant.Dict("en_US")
	correctWords = []
	falseWords = []
	for a in toCheck:
		if d.check(a):
			correctWords.append(a)
		else:
			falseWords.append(a)
	if correctWords == toCheck:
		return True
	else:
		return falseWords

class Letters(object):
	def __init__(self):
		pass

	d = {'A':13, 'B':3, 'C':3, 'D':6, 'E':18, 'F':3, 'G':4, 'H':3, 'I':12, 'J':2, 'K':2, 'L':5, 'M':3, 'N':8, 'O':11, 'P':3, 'Q':2, 'R':9, 'S':6, 'T':9, 'U':6, 'V':3, 'W':3, 'X':2, 'Y':3, 'Z':2}
	
	def peel(self):
		while True:
			n = random.randint(65,90)
			letter = chr(n)
			if Letters.d[letter] > 0:
				Letters.d[letter] -= 1
				break
		print(letter,Letters.d)
		return letter

	def start(self):
		pass
	def replace(self):
		pass

l1 = Letters()
l1.peel()
