import numpy as np
import subprocess, platform
from getAnswer import *
class Player():
    def __init__(self,name,bet,money=500):
        self.name=name
        self.hand=[]
        self.hand_split=None
        self.money=money
        self.bet=bet
    def __str__(self):
        return f'{self.name} has ${self.money}'
    def deal_hand(self,cards):
        #Gives player a card
        rand_num=np.random.randint(len(cards))
        self.hand.append(cards[rand_num])
        cards.pop(rand_num)
    def deal_hand_split(self,cards):
        #If player decides to split, gives the player's second hand a card
        rand_num=np.random.randint(len(cards))
        self.hand_split.append(cards[rand_num])
        cards.pop(rand_num)
    def get_val(self):
        #returns the value of the player's hand
        self.val=np.sum(list(zip(*self.hand))[1])
        return self.val
    def get_val_split(self):
        #If player decides to split, gives the value of the player's second hand
        self.val=np.sum(list(zip(*self.hand_split))[1])
        return self.val
    def bust(self):
        #Determines if player busted
        if self.get_val()>21:
            self.money-=self.bet
            print(f'{self.name} busted')
            input("Press enter to continue")
            return True
        return False
def clear():
#Clears the terminal
    if platform.system()=="Windows":
        subprocess.Popen("cls", shell=True).communicate()
        print('')
    else:
        print("\033c", end)
def init():
#Configure players and creates card deck
    clear()
    play_count=''
    players=[]
#Get number of players
    play_count=getAnsInt('Number of Players: ')
    clear()
#Gey player names
    for x in range(play_count):
        play_name='Player ' + str(x+1)
        chosen_name=input(f'{play_name} enter your character\'s name: ')
        players.append(Player(chosen_name,50))
#Create card deck
    cards=shuffle()
#Start game
    main(players,cards)
def shuffle():
#Shuffles deck
    cards=[("Ace Heart",11),("Ace Diamond",11),("Ace Spade",11),("Ace Clove",11),("Two Heart",2),("Two Diamond",2),("Two Spade",2),("Two Clove",2),("Three Heart",3),("Three Diamond",3),("Three Spade",3),("Three Clove",3),("Four Heart",4),("Four Diamond",4),("Four Spade",4),("Four Clove",4),("Five Heart",5),("Five Diamond",5),("Five Spade",5),("Five Clove",5),("Six Heart",6),("Six Diamond",6),("Six Spade",6),("Six Clove",6),("Seven Heart",7),("Seven Diamond",7),("Seven Spade",7),("Seven Clove",7),("Eight Heart",8),("Eight Diamond",8),("Eight Spade",8),("Eight Clove",8),("Nine Heart",9),("Nine Diamond",9),("Nine Spade",9),("Nine Clove",9),("Jack Heart",10),("Jack Diamond",10),("Jack Spade",10),("Jack Clove",10),("Queen Heart",10),("Queen Diamond",10),("Queen Spade",10),("Queen Clove",10),("King Heart",10),("King Diamond",10),("King Spade",10),("King Clove",10)]
    cards*=7
    return cards
def main(players,cards):
#Keeps track of turns and decides if needs to shuffle cards at beggining of a round
    clear()
#Determines if needs to shuffle cards
    if len(cards)==75:
        print("Shuffling Cards")
        cards=shuffle()
        input("Press enter to continue")
#Create dealer
    dealer=Player("Dealer",0)
    dealer.hand=[]
#Hand out cards
    dealer.deal_hand(cards)
    dealer.deal_hand(cards)
    for player_active in players:
        clear()
        player_active.hand=[]
        player_active.deal_hand(cards)
        player_active.deal_hand(cards)
#Get player's bet
        print(f'{player_active.name}\'s turn')
        print(player_active)
        player_active.bet=getAnsFlt('Enter bet: $',[0,player_active.money])
#Player split check
#Determines if hand can split
        if player_active.hand[0][1]!=player_active.hand[1][1]:
            player_turn(cards,player_active,dealer)
        else:
            split=getAnsStr("Would you like to split?",['Yes','No'])
            if split=='Yes':
#Creates second player hand
                player_active.hand_split=[player_active.hand[1]]
                player_active.hand.pop(1)
                player_active.deal_hand()
                player_active.deal_hand_split()
#Starts player's turn
                player_turn1(cards,player_active,dealer)
            else:
                player_turn(cards,player_active,dealer)
    clear()
    print("Dealer's Turn")
    dealer_turn(cards,players,dealer)
def player_turn(cards,player_active,dealer):
#Player's turn with no split
    clear()
#Show hands
    print(f'Your cards: {player_active.hand}')
    print(f'Dealer card: {dealer.hand[0]}')
#Player chooses action
    ans=getAnsStr('Hit or Stay: ',['Hit','Stay'])
    if ans=='Hit':
        player_active.deal_hand(cards)
#Check for bust
        if ace_switch(player_active):
            print('Player Busted')
            print(player_active.hand)
            pass
#Restart turn
        else:
            player_turn(cards,player_active,dealer)
def ace_switch(player_active):
#Turns an ace from being worth 11 to 1
#Check if player busted
    if player_active.get_val()>21:
        for x,v in enumerate(player_active.hand):
#Check if any aces
                if v[1]==11:
#Switch ace value from 11 to 1
                    player_active.hand[x]=(v[0],1)
                    ace_switch(player_active)
                    return None
        return True
    return False
def player_turn1(cards,player_active,dealer):
#Player's first hand if split
    clear()
#Show cards
    print(f'Your first hand:{player_active.hand}')
    print(f'Dealer card: {dealer.hand[0]}')
#Player decides action
    ans=getAnsStr('Hit or Stay: ',['Hit','Stay'])
    if ans=='Hit':
#Deal first hand
        player_active.deal_hand(cards)
#Check if bust
        if ace_switch(player_active):
            print('Player Busted')
            print(player_active.hand)
            pass
#Restart turn
        else:
            player_turn(cards,player_active,dealer)
def player_turn2(cards,player_active,dealer):
#Player's second hand if split
    clear()
#Show cards
    print(f'Your second hand:{player_active.hand_split}')
    print(f'Dealer card: {dealer.hand[0]}')
#Player decides action
    ans=getAnsStr('Hit or Stay: ',['Hit','Stay'])
    if ans=='Hit':
#Deal first action
        player_active.deal_hand(cards)
#Check if bust
        if ace_switch(player_active):
            print('Player Busted')
            print(player_active.hand)
            pass
#Restart turn
        else:
            player_turn(cards,player_active,dealer) 
def dealer_turn(cards,players,dealer):
#Plays for the dealer
    val=dealer.get_val()
#Check if dealer busted
    if ace_switch(dealer): 
        print(f'Dealer\'s hand: {dealer.hand}')
        print("Dealer Busted")
        game_over(players,dealer,cards)
#Dealer deals until his hand is at least worth 17 points
    elif val<17:
        dealer.deal_hand(cards)
        dealer_turn(cards,players,dealer)
        return None
#Once hand is worth 17 ends game
    else:
        print(f'Dealer\'s hand: {dealer.hand}')
        game_over(players,dealer,cards)
def game_over(players,dealer,cards):
#Determines who won and determines new player balances
    for player_active in players:
        print(f'{player_active.name}\'s hand: {player_active.hand}')
#Checks values if player didn't split
        if player_active.hand_split==None:
#Checks if player busted
            if player_active.get_val()<22:
#Win
                if (player_active.val>dealer.val):
                    print(f'{player_active.name} beat the dealer')
                    player_active.money+=player_active.bet
#Push
                elif player_active.val is dealer.val:
                    print(f'{player_active.name} pushed')
#Loss
                elif dealer.val<22:
                    print(f'The dealer beat {player_active.name}')
                    player_active.money-=player_active.bet
                else:
#Win
                    print(f'{player_active.name} won')
                    player_active.money+=player_active.bet
#Bust
            else:
                print(f'{player_active.name} Busted')
                player_active.money-=player_active.bet
#Checks values if player did split
        else:
#Player's 1st hand
            if player_active.get_val()<22:
#Win
                if (player_active.val>dealer.val):
                    print(f'{player_active.name}\'s first hand beat the dealer')
                    player_active.money+=player_active.bet
#Push
                elif player_active.val is dealer.val:
                    print(f'{player_active.name}\'s first hand pushed')
#Loss
                elif dealer.val<22:
                    print(f'The dealer beat {player_active.name}\'s first hand')
                    player_active.money-=player_active.bet
                else:
#Win
                    print(f'{player_active.name}\'s first hand won')
                    player_active.money+=player_active.bet
#Bust
            else:
                print(f'{player_active.name}\'s first hand lost')
#Player's 2nd hand
            if player_active.get_val_split()<22:
#Win
                if (player_active.val>dealer.val):
                    print(f'{player_active.name}\'s second hand beat the dealer')
                    player_active.money+=player_active.bet
#Push
                elif player_active.val is dealer.val:
                    print(f'{player_active.name}\'s second hand pushed')
#Loss
                elif dealer.val<22:
                    print(f'The dealer beat {player_active.name}\'s second hand')
                    player_active.money-=player_active.bet
#Win
                else:
                    print(f'{player_active.name}\'s Second hand won')
                    player_active.money+=player_active.bet
#Bust
            else:
                print(f'{player_active.name}\'s second hand lost')
        print(player_active)
#Determines if going to play again
    play=''
    while play not in ['Yes','No']:
        print("Would you like to play again?")
        play=input("Yes or No: ")
    if play=='Yes':
        main(players,cards)
    clear()
init()