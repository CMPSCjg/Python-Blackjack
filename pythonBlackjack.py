import os
import os.path
import math
import datetime
import random

# Define the deck of cards
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*4

# Define the default amount of cash
defaultAmount = 500

# "deal": Function to deal two cards, at random, from a shuffled deck
# Inputs:
#     deck: Collection consisting of the numerical values of each card (4 each)
def deal(deck):
    hand = []
    random.shuffle(deck)
    for i in range(2):

        # "Draw" a card from the deck by popping the top card off the stack
        dealtCard = deck.pop()

        # Translate the numerical values into the face-card values
        if dealtCard == 11:
            dealtCard = "J"
        elif dealtCard == 12:
            dealtCard = "Q"
        elif dealtCard == 13:
            dealtCard = "K"
        elif dealtCard == 14:
            dealtCard = "A"

        # Add the card to the hand
        hand.append(dealtCard)

    return hand

# "hit": Function to give a card to the player.
# Inputs:
#     hand: Collection consisting of cards
def hit(hand):

    # "Draw" a card from the deck by popping the top card off the stack
    dealtCard = deck.pop()

    # Translate the numerical values into the face-card values
    if dealtCard == 11:
        dealtCard = "J"
    elif dealtCard == 12:
        dealtCard = "Q"
    elif dealtCard == 13:
        dealtCard = "K"
    elif dealtCard == 14:
        dealtCard = "A"

    # Add the card to the hand
    hand.append(dealtCard)

    return hand

# "getHandValue": Function to give the numerical total of the cards in the hand
# Inputs:
#     hand: Collection consisting of cards
def getHandValue(hand):
    handValue = 0
    aceCounter = 0

    # Loop through each card in the given hand
    for card in hand:

        # Translate the face-card values into numerical values and add them
        if card == "J" or card == "Q" or card == "K":
            handValue += 10
        elif card == "A":
            handValue += 11
            aceCounter += 1
        else:
            handValue += card

    # Translate the "Ace" card value from 11 to 1 if the hand exceeds 21
    while aceCounter > 0 and handValue > 21:
        aceCounter -= 1
        handValue -= 10
        
    return handValue

# "printHand": Function to display the current hand and its value
# Inputs:
#     hand: Collection consisting of cards
#     handValue: Numerical total of the cards in the hand
def printHand(hand, handValue):
    return (str(hand) + " (" + str(handValue) + ")")

# "gameOver": Function to update player data and see if player wants to play again
# Inputs:
#     userID: Unique ID of the player, used to pull the player's profile
#     currentBalance: Numerical value of the player's original balance before that game
#     newBalance: Numerical value to update the player data to
def gameOver(userID, currentBalance, newBalance):

    # Restart the player's progress if they lose all their money
    if newBalance <= 0:
        print("Your balance has reached $0. Your balance will be reset to the default amount.")
        newBalance = defaultAmount

    # Prompt the user to see whether he or she wants to play again, trapping incorrect responses as well
    userChoice = raw_input("Would you like to play again <Y or N>?: ").lower()
    while userChoice != "y" or userChoice != "n":
            if userChoice == "y" or userChoice == "n":
                break
            print("Invalid selection entered!")
            userChoice = raw_input("Would you like to play again <Y or N>?: ").lower()

    # If the user wants to play again, start a new game.
    # Otherwise, store the player's new cash balance and exit the program
    if userChoice == "y":
        blackjackGame(userID, newBalance)
    else:
        
        # Store the original text in the file
        file = r"./BlackjackPlayerData/" + userID + ".txt"
        profile = open(file, "r")
        with profile as filePointer:
            lines = filePointer.readlines()
        profile.close()

        # Re-write the text into the file, updating the balance line
        profile = open(file, "w")
        newBalanceLine = "Balance: $" + str(newBalance) + "\n"
        for line in lines:
            if "Balance: $" in line:
                line = newBalanceLine
            profile.write(line)
        profile.close()

# "loadPlayerData": Function to pull the player's data from their file
# Inputs:
#     file: The exact filepath to the player's data file      
def loadPlayerData(file):
    
    # Open the player's data file and parse their userID and current cash balance
    print ("Loading player data. . . DONE")
    profile = open(file, "r")
    with profile as filePointer:
        line = filePointer.readline()
        while line:
            if "UserID" in line:
                userID = line[8:].rstrip()
            elif "Balance: $" in line:
                currentBalance = line[10:].rstrip()
            line = filePointer.readline()
        profile.close()

    return userID, float(currentBalance)

# "printMainMenu": Function to display the main menu text
def printMainMenu():
    print("----------- BLACKJACK MENU -----------")
    print("1. Play the game")
    print("2. How to play")
    print("3. Quit")

# "printUI": Function to display pertinent information to the player
# Inputs:
#     userID: Unique ID of the player, used to pull the player's profile
#     currentBalance: Numerical value of the player's original balance before that game
#     currentBet: Amount placed by the player for this hand.
def printUI(userID, currentBalance, currentBet):
    print("--------------------------------------")
    print("  UserID: " + userID)
    print("  Balance: $" + str(currentBalance))
    print("")
    print("  Bet: $" + str(currentBet))
    print("--------------------------------------")

# "printHelpMenu": Function to display the "How to Play" menu text
def printHelpMenu():
    print("----------- HOW TO PLAY -----------")
    print("The rules of Blackjack are as follows:")
    print("You will be playing against the dealer.")
    print("If you win, you will receive double your bet amount.")
    print("If you get a Blackjack, you will receive 1.5x your bet amount.")
    print("Both you and the dealer will be dealt 2 cards at the start of the game.")
    print("You can choose to hit one or more times, or stand with any amount.")
    print("The dealer must hit if their cards total less than 17 and stand otherwise.")
    print("If your cards total over 21, tou bust and your turn is over. The same goes for the dealer.")
    print("If you or the dealer have 21 with the first 2 cards dealt, that player wins. If both have 21 at the start, they tie.")
    print("If both you and the dealer bust (go over 21), the dealer wins.")
    print("If both you and the dealer's hand total to the same amount, you both tie.")
    print("As the player, you will always take your turn before the dealer.")
    print("All cards count as their face value, but A can be 1 or 11 and J, Q, and K count as 10.")
    print("The deck will be shuffled before each game.")
    print("There will only be 1 deck used per game.")

    raw_input("Press Enter to return to the main menu. . .")
    mainMenu()

# "mainMenu": Function used as a starting point for the program/game
def mainMenu():
    
    # Create the player data directory if it doesn't exist.
    if not os.path.exists("./BlackjackPlayerData/"):
        os.makedirs("./BlackjackPlayerData/")

    # Define the menu choice
    menuChoice = 0

    # Print the main menu
    printMainMenu()

    # Prompt the user
    menuChoice = input("Enter selection --> ")
    while menuChoice < 1 or menuChoice > 3:
        print("Invalid selection!")
        printMainMenu()
        menuChoice = input("Enter selection --> ")

    # Determine what to do based on user choice
    if menuChoice == 1:

        ## PLAYER DATA FILE HANDLING
        
        # Check if user has played before.
        # If user hasn't played before, start new profile.
        fileName = raw_input("If you have played before, enter your ID. Otherwise, enter \'NEW\': ")
        if fileName == "NEW":

            # Write player data to player data file
            fileName = raw_input("Input a valid user ID: ")
            currentDate = datetime.datetime.now()
            newProfile = open("./BlackjackPlayerData/" + fileName + ".txt", "w+")
            newProfile.write("UserID: " + fileName + "\n")
            newProfile.write("Date Created: " + str(currentDate.month) + "/" + str(currentDate.day) + "/" + str(currentDate.year) + "\n")
            newProfile.write("Balance: $" + str(defaultAmount) + "\n")
            newProfile.close()

            # Store player data for game
            userID = fileName
            currentBalance = defaultAmount
        else:

            # If the player's data file exists, load the player's data.
            # Otherwise, prompt the user to enter their userID again.
            file = r"./BlackjackPlayerData/" + fileName + ".txt"
            if os.path.exists(file):

                # Load player data.
                [userID, currentBalance] = loadPlayerData(file)

            else:
                print("The userID: " + fileName + ", does not exist!")
                numAttempt = 1
                while numAttempt <= 3:
                    fileName = raw_input("Please enter a valid userID (Attempt #" + str(numAttempt) + " out of 3): ")
                    file = r"./BlackjackPlayerData/" + fileName + ".txt"
                    if os.path.exists(file):
                        [userID, currentBalance] = loadPlayerData(file)
                        break
                    else:
                        numAttempt += 1

                print("You have entered too many invalid userIDs. Please restart the program!")
                exit()

        # Start a new game
        blackjackGame(userID, currentBalance)

    elif menuChoice == 2:
        printHelpMenu()

    elif menuChoice == 3:
        exit()

    else:
        print("ERROR: This line should not be executed. Please restart the program!")

def blackjackGame(userID, currentBalance):

        ## BLACKJACK GAME HANDLING

        # Clear the console screen
        os.system("cls")

        # Prompt user to place a bet
        print("Balance: $" + str(currentBalance))
        userBet = input("Enter your bet amount: ")
        while userBet > currentBalance:
            print("You do not have enough money to place that bet!")
            userBet = input("Enter your bet amount: ")
        newBalance = currentBalance - userBet

        # Setup console header to display user information
        printUI(userID, newBalance, userBet)

        # Deal cards to the player and the dealer
        print("Dealing cards now. . .")
        playerHand = deal(deck)
        playerHandValue = getHandValue(playerHand)
        print("\nYour hand: " + printHand(playerHand, playerHandValue))
        dealerHand = deal(deck)
        dealerHandValue = getHandValue(dealerHand)
        if dealerHandValue == 21:
            print("\nDealer's hand: " + printHand(dealerHand, dealerHandValue))
        else:
            print("Dealer's hand: [" + str(dealerHand[0]) + ", ??] (??)")

        # Check for blackjack(s)
        if playerHandValue == 21 and dealerHandValue == 21:
            print("The player and dealer both have a Blackjack. Tie!")
            newBalance = currentBalance + userBet
            gameOver(userID, currentBalance, newBalance)
            return
        elif playerHandValue == 21:
            print("The player has a Blackjack. You win!")
            newBalance = math.floor(currentBalance + userBet * 1.5)
            gameOver(userID, currentBalance, newBalance)
            return
        elif dealerHandValue == 21:
            print("The dealer has a Blackjack. You lose!")
            gameOver(userID, currentBalance, newBalance)
            return

        # Prompt the user to hit or stand
        userChoice = raw_input("Would you like to hit <h> or stand <s>?: ").lower()
        while userChoice != "h" or userChoice != "s":
            if userChoice == "h" or userChoice == "s":
                break
            print("Invalid selection entered!")
            userChoice = raw_input("Would you like to hit <h> or stand <s>?: ").lower()
            
        while True:
            if userChoice == "h":
                playerHand = hit(playerHand)
                playerHandValue = getHandValue(playerHand)
                print("\nYour hand: " + printHand(playerHand, playerHandValue))
                print("Dealer's hand: " + str(dealerHand[0]) + ", ?? (??)")
                if playerHandValue > 21:
                    playerBusted = 1
                    print("You have busted. You lose!")
                    gameOver(userID, currentBalance, newBalance)
                    return
                userChoice = raw_input("Would you like to hit <h> or stand <s>?: ")
            elif userChoice == "s":
                print("Your turn is over. The dealer will have his turn now!")
                break

        # Dealer's turn
        print("\nYour hand: " + printHand(playerHand, playerHandValue))
        print("Dealer's hand: " + printHand(dealerHand, dealerHandValue))
        while dealerHandValue < 17:
            dealerHand = hit(dealerHand)
            dealerHandValue = getHandValue(dealerHand)
            print("\nYour hand: " + printHand(playerHand, playerHandValue))
            print("Dealer's hand: " + printHand(dealerHand, dealerHandValue))
            if dealerHandValue > 21:
                dealerBusted = 1
                print("The dealer has busted. You win!")
                newBalance = currentBalance + userBet
                gameOver(userID, currentBalance, newBalance)
                return

        # Determine winner if neither party has busted
        if playerHandValue > dealerHandValue:
            print("Your hand is higher than the dealer's. You win!")
            newBalance = currentBalance + userBet
        elif dealerHandValue > playerHandValue:
            print("The dealer's hand is higher than yours. You lose!")
        else:
            print("Both hands were equal in value. Tie!")
            newBalance += userBet

        ## UPDATING PLAYER DATA HANDLING

        ## PROMPT USER TO PLAY AGAIN OR QUIT
        gameOver(userID, currentBalance, newBalance)
        return
    
if __name__ == "__main__":
    mainMenu()

