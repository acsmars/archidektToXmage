# importing the requests library
import requests
import os
import argparse


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


# parse input
parser = argparse.ArgumentParser(description='Public Deck ID')
parser.add_argument("deckID")
args = parser.parse_args()
print("Downloading deck with ID {}".format(args.deckID))

# api-endpoint

deckDirectory = "decks"
URL = "https://archidekt.com/api/decks/{}/".format(args.deckID)

try:
    data = requests.get(URL).json()
except:
    print("Exception getting deck {}. It likely doesn't exist, is private, or archidekt is down.")
    exit(1)

deckName = data.get("name")

mainboard = []
sideboard = []

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

with open("{}/{}.dck".format(deckDirectory, deckName), "w") as deckFile:
    for card in mainboard:
        deckFile.write(card.xmageFormat() + os.linesep)

    for card in sideboard:
        deckFile.write("SB: {}".format(card.xmageFormat()) + os.linesep)
