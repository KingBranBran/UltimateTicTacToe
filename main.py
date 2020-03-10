import replit
import random

board = [[], [], [], [], [], [], [], [], []]
bigBoard = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
firstGame = False

# Settings used
rand = False
fillPercent = 50

# --------- #
# FUNCTIONS #
# --------- #

def StartScreen():
  replit.clear()
  PrintTitle()
  print("START => Start a game.\nOPTIONS => Show options screen.\nHELP => How to play.\n")

  while True:
    playerInput = raw_input("Type a command: ")
    if playerInput.lower() == "start":
      StartGame()
      ClearBoard()
    elif playerInput.lower() == "help":
      HelpScreen()
    elif playerInput.lower() == "options":
      OptionScreen() 

def PrintTitle():
  print("|======================|")
  print("| ULTIMATE TIC-TAC-TOE |")
  print("|======================|\n")

def HelpScreen():
  replit.clear()
  PrintTitle()
  print("HOW TO PLAY\n-----------\nThis is a two, layered tic-tac-toe. The first player gets to choose which box of tic-tac-toe you get to play in. The next mark's (X or O) location determines the next box that the next player plays in. If a box is finished, the next player gets to choose a box. To win, get three Xs or Os in a row in the big tic-tac-toe area. The boxes are numbered 1 though 9 in reading order, and so is the smaller boxes within each box.")
  print("\nBACK => Go back to main screen.\n")

  while True:    
    playerInput = raw_input("Type a command: ")

    if playerInput.lower() == "back":
      StartScreen()
      break
         
def OptionScreen():
  replit.clear()
  PrintTitle()
  print("RANDOM FILL => %s" % (str(rand).upper())) 
  print("FILL PERCENT => %s" % (fillPercent))
  print("\nBACK => Go back to main screen.\n")

  while True:    
    playerInput = raw_input("Type a command: ")

    if playerInput.lower() == "random fill":
      RandomFillOption()
    elif playerInput.lower() == "fill percent":
      FillPercentOption()
    elif playerInput.lower() == "back":
      StartScreen()
      break

def RandomFillOption():
  global rand
  while True:
    playerInput = raw_input("Choose an option: ")
    if playerInput.lower() == "true":
      rand = True
    elif playerInput.lower() == "false":
      rand = False
    else:
      continue
    OptionScreen()
    break

def FillPercentOption():
  global fillPercent
  while True:
    playerInput = raw_input("Choose an option: ")
    
    try:
      convertedInput = int(playerInput)
      if convertedInput < 0 or convertedInput > 100:
        print("Invalid number!")
        continue
    except ValueError:
      continue  

    fillPercent = convertedInput
    OptionScreen()
    break

# Main function that controls the game.
def StartGame():
  global firstGame
  global totalWin
  global totalTie
  global bigBoard
  bigBoard = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
  totalWin = False
  totalTie = False
  replit.clear()
  PrintTitle()
  if not firstGame:
    FillBoard()
    firstGame = True
  ClearBoard("-")
  if rand:
    FillBoardWithRandom()
  PrintBoard()

  while not (totalWin or totalTie):
    NextTurn()
    replit.clear()
    PrintTitle()
    PrintBoard()
  if totalWin:
    print("\n%s wins!" % (winner))
  elif totalTie:
    print("\nThere is a tie!")
  EndScreen()

# Append the board with empty strings.
def FillBoard():
  for i in range(9):
    for _ in range(9):
      board[i].append("-")

# Fill the EXISTING board with a string.
def ClearBoard(character = " "):
  for i in range(9):
    for j in range(9):
      board[i][j] = character

def FillBoardWithRandom():
  for i in range(9):
    for j in range(9):
      if random.randint(1, 100) <= fillPercent:
        board[i][j] = ('X', 'O')[random.randint(0, 1)]
      else:
        board[i][j] = '-'
  for box in range(9):
    CheckForWin(board[box], box)

# Print out the whole board.
def PrintBoard():
  for big_row in range(3):
    for small_row in range(3):
      print(" %s %s %s | %s %s %s | %s %s %s" % (board[big_row * 3][small_row * 3], board[big_row * 3][small_row * 3 + 1], board[big_row * 3][small_row * 3 + 2], board[1 + big_row * 3][small_row * 3], board[1 + big_row * 3][small_row * 3 + 1], board[1 + big_row * 3][small_row * 3 + 2], board[2 + big_row * 3][small_row * 3], board[2 + big_row * 3][small_row * 3 + 1], board[2 + big_row * 3][small_row * 3 + 2]))

    if big_row < 2:
      print("-----------------------")

def EndScreen():
  print("\nBACK => Go back to main screen.\n")

  while True:    
    playerInput = raw_input("Type a command: ")
    if playerInput.lower() == "back":
      StartScreen()
      break

# Controls turn order and player input.
currentPlayer = 0
currentBox = -1
boxNames = ("top-left", "top-middle", "top-right", "middle-left", "middle", "middle-right", "bottom-left", "bottom-middle", "bottom-right")
def NextTurn():
  global currentPlayer
  global currentBox

  if currentBox == -1:
    currentBox = PickBox()

  while True:
    playerInput = raw_input("\nPlayer %d, please put an %s in the %s box.\n" % (currentPlayer + 1, ('X', 'O')[currentPlayer], boxNames[currentBox]))

    try:
      convertedInput = int(playerInput) - 1
      if convertedInput > 8 or convertedInput < 0:
        print("Invalid number!")
        continue
      elif board[currentBox][convertedInput] in ('X', 'O'):
        print("That spot is already filled!")
        continue
      break
    except ValueError:
      continue
  
  print("")
  board[currentBox][convertedInput] = ('X', 'O')[currentPlayer]
  currentPlayer = (currentPlayer + 1) % 2 # Flips the turn order.
  CheckForWin(board[currentBox], currentBox)
  currentBox = convertedInput # Set next box.
  if bigBoard[convertedInput] in ('X', 'O', '-'): # Check if the picked box is already won.
    currentBox = -1
  
# Allows players to pick a valid box.
def PickBox():
  while True:
    playerInput = raw_input("\nPlayer %d, please choose a box to play in.\n" % (currentPlayer + 1))
    try:
      convertedInput = int(playerInput) - 1
      if convertedInput > 8 or convertedInput < 0:
        print("Invalid number!")
        continue
      elif bigBoard[convertedInput] in ('X', 'O', '-'):
        print("That box is already finished!")
        continue

      return convertedInput
    except ValueError:
      continue
  
# Check for three in a row, if there is, then check the bigger one.
totalWin = False
totalTie = False
winner = ""
def CheckForWin(field, fieldNum, total = False):
  global totalWin
  global totalTie
  global winner

  for p in range(2):
    win = False
    sign = ('X', 'O')[p]
    for row in range(3):
      if all( c == sign for c in (field[row * 3], field[row * 3 + 1], field[row * 3 + 2])):
        win = True
    for col in range(3):
      if all( c == sign for c in (field[col], field[col + 3], field[col + 6])):
        win = True
    if all( c == sign for c in (field[0], field[4], field[8])):
        win = True
    if all( c == sign for c in (field[2], field[4], field[6])):
        win = True

    if win:
      if total:
        totalWin = True
        ClearBoard()
        board[4][4] = sign
        winner = sign
      else:
        bigBoard[fieldNum] = sign
        ChangeBoard(fieldNum, p)
        CheckForWin(bigBoard, -1, True)
    elif total:
      if all(c in ('X', 'O', '-') for c in field): # If there is a tie
        totalTie = True
        ClearBoard()
        board[4][4] = '-'
    else:
      if all(c in ('X', 'O') for c in field): # If there is a tie
        bigBoard[fieldNum] = '-'
        ChangeBoard(fieldNum, 2)
        CheckForWin(bigBoard, -1, True)

# Change a box for when a player wins or there is a tie.
def ChangeBoard(field, player):
  board[field][0:2] = [" ", " ", " "]
  board[field][3:5] = [" ", ('X', 'O', '-')[player], " "]
  board[field][6:8] = [" ", " ", " "]

# ---- #
# CODE #
# ---- #

StartScreen()