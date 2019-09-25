# importing the requests library
import requests
import os
import argparse

deckDirectory = "decks"


class Card:
    quantity = 0
    setCode = ""
    setCollectorNumber = 0
    name = ""

    def xmageFormat(self):
        return "{} [{}:{}] {}".format(self.quantity, self.setCode, self.setCollectorNumber, self.name)

    def __repr__(self):
        return "Card(Name = {}, SetCode = {}, SetNumber = {}, Quantity = {})".format(self.name,
                                                                                     self.setCode,
                                                                                     self.setCollectorNumber,
                                                                                     self.quantity)


def downloadDeck(deckID):
    print("Downloading deck with ID {}".format(deckID))

    # deck api endpoint
    URL = "https://archidekt.com/api/decks/{}/".format(deckID)

    try:
        data = requests.get(URL).json()
    except:
        print("Exception getting deck {}. It likely doesn't exist, is private, or archidekt is down.")
        return

    deckName = data.get("name")

    mainboard = []
    sideboard = []

    if data.get("cards") == None:
        print("Deck is either private or contains no cards, skipping.")
        return

    for card in data.get("cards"):
        newCard = Card()

        newCard.name = card.get("card").get("oracleCard").get("name").split(" //")[0]
        newCard.quantity = card.get("quantity")
        newCard.setCollectorNumber = card.get("card").get("collectorNumber")
        newCard.setCode = card.get("card").get("edition").get("editioncode").upper()

        category = card.get("category")
        if (category == "Commander"):
            sideboard.append(newCard)
        elif (category == "Maybeboard"):
            pass
        else:
            mainboard.append(newCard)

    if not os.path.exists(deckDirectory):
        os.makedirs(deckDirectory)

    deckFilename = "".join([c for c in deckName if c.isalpha() or c.isdigit() or c == ' ']).rstrip()

    with open("{}/{}.dck".format(deckDirectory, deckFilename), "w") as deckFile:
        for card in mainboard:
            deckFile.write(card.xmageFormat() + os.linesep)

        for card in sideboard:
            deckFile.write("SB: {}".format(card.xmageFormat()) + os.linesep)


def getDecksByUserID(userID):
    # user ID api endpooint
    URL = "https://archidekt.com/api/users/{}/decks/".format(userID)
    try:
        data = requests.get(URL).json()
    except:
        print("Exception getting deck {}. It likely doesn't exist, is private, or archidekt is down.")
        return

    if data.get("decks") == None:
        print("Deck is either private or contains no cards, skipping.")
        return

    deckIDs = [x.get("id") for x in data.get("decks")]
    print("Found decks:{}".format(deckIDs))
    return deckIDs

def getDecksByUserName(username):
    # user ID api endpooint
    URL = "https://archidekt.com/api/decks/cards/?owner={}".format(username)
    try:
        data = requests.get(URL).json()
    except:
        print("Exception getting deck {}. It likely doesn't exist, is private, or archidekt is down.")
        return

    if data.get("results") == None:
        print("Deck is either private or contains no cards, skipping.")
        return

    deckIDs = [x.get("id") for x in data.get("results")]
    print("Found decks:{}".format(deckIDs))
    return deckIDs


# parse input
parser = argparse.ArgumentParser(description='Public Deck ID')
parser.add_argument("resourceID")
parser.add_argument('--user', dest='mode', action='store_const',
                    const="user", default="deck",
                    help='Fetch all decks by this user rather than a deck ID')
parser.add_argument('--userID', dest='mode', action='store_const',
                    const="userID", default="deck",
                    help='Fetch all decks by this user rather than a deck ID')
args = parser.parse_args()
if args.mode == "user":
    print("Downloading all decks from user with ID {}".format(args.resourceID))
    for deckID in getDecksByUserID(args.resourceID):
        downloadDeck(deckID)
elif args.mode == "userID":
    print("Downloading all decks from user with ID {}".format(args.resourceID))
    for deckID in getDecksByUserID(args.resourceID):
        downloadDeck(deckID)
elif args.mode == "deck":
    downloadDeck(args.resourceID)
else:
    print("Invalid Argument")
