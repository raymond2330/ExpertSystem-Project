import os

from PIL.Image import NONE
from Card import Card
from GameState import GameState
from Action import Action


# Logic for the solitaire game #################################################################

class GameLogic:
    
    def PlaceAce(self, gs):
        a1 = Action()
        gs.ui_components_to_render = {}
        
        #############################
        # Move draw deck card to Deck
        #############################

        drawDeckCard = gs.draw_deck_top_card
        #integer substrisng of the card name, s1 is 1, h13, is 13 -scarr
        if int(drawDeckCard[0][1:]) == 1:
            a1.name = 'MoveCardToDeck'
            a1.cards.append(drawDeckCard)
            gs.ui_components_to_render['draw_deck'] = []
            gs.ui_components_to_render['top_deck'] = []
            return a1 , gs.ui_components_to_render
        return None
    
    
    def GetNextAction(self, gs, sv):
        a1 = Action()
        gs.ui_components_to_render = {}
        
        #############################
        # Move draw deck card to Deck
        #############################

        drawDeckCard = gs.draw_deck_top_card
        if len(drawDeckCard) > 0:
            ace=self.PlaceAce(gs)
            if(type(ace) is tuple):
                a1, gs.ui_components_to_render = ace
                return a1
            for deckCard in gs.deck_cards_top:
                #print("DeckCard: " + deckCard[0])
                
                #suit
                dcardChar = deckCard[0][0]
                #value
                dcardInd = int(deckCard[0][1:])
                reqCard = dcardChar + str(dcardInd+1)
                #checking if the int of the draw card is greater by 1 of the pile card and matches suit -scarr                                      
                if reqCard == drawDeckCard[0]:
                    #print(reqCard)
                    a1.name = 'MoveCardToDeck'
                    a1.cards.append(drawDeckCard)
                    gs.ui_components_to_render['draw_deck'] = []
                    gs.ui_components_to_render['top_deck'] = []
                    return a1 

        ######################################
        # Move card from draw deck to column
        ######################################
        
        drawDeckCard = gs.draw_deck_top_card
        if len(drawDeckCard) > 0:
            #a, h, s, d
            cardChar = drawDeckCard[0][0]
            #1-13                
            cardInd = int(drawDeckCard[0][1:])
            # If it's a king card, move it to empty column if possible
            if cardInd == 13:
                if len(gs.empty_column_indices) > 0:
                    a1.name = 'MoveCardToColumn'
                    a1.cards.append(drawDeckCard)                        
                    a1.cards.append(['empty_col',gs.empty_column_indices[0]])
                    gs.ui_components_to_render['draw_deck'] = []
                    gs.ui_components_to_render['columns'] = [gs.empty_column_indices[0]]
                    gs.empty_column_indices.remove(gs.empty_column_indices[0])
                    return a1    

            #lists the possible card to be stacked below, for a13 it would be [h12, d12] -scarr
            ToggledChars = self.GetToggledCardChar(cardChar)
            CandCardNames = []
            for tchar in ToggledChars:
                candCardName = tchar + str(cardInd+1)
                CandCardNames.append(candCardName)

            colInd = 1
            for anotherColCrd in gs.column_cards:
                if len(anotherColCrd) > 0:
                    if anotherColCrd[0] in CandCardNames:
                        a1.name = 'MoveCardToColumn'
                        #from
                        a1.cards.append(drawDeckCard)
                        #to
                        a1.cards.append(anotherColCrd)
                        gs.ui_components_to_render['draw_deck'] = []
                        gs.ui_components_to_render['columns'] = [colInd]
                        return a1  
                colInd += 1  

        ######################################
        # Move card from one column to another
        ######################################
        
        
        colInd = 1

        for allColCrds in gs.column_all_cards:
            if len(allColCrds) > 0:
                #print(allColCrds)                
                colCrd = allColCrds[-1:][0]
                #print(colCrd)            
                if len(colCrd) > 0:
                    #print(colCrd[0])
                    cardChar = colCrd[0][0]                
                    cardInd = int(colCrd[0][1:])
                    # If it's a king card, move it to empty column if possible
                    if cardInd == 13 and gs.new_cards_in_column[colInd-1] == 1:
                        if len(gs.empty_column_indices) > 0:
                            a1.name = 'MoveCardToColumn'
                            a1.cards.append(colCrd)                        
                            a1.cards.append(['empty_col',gs.empty_column_indices[0]])
                            gs.ui_components_to_render['columns'] = [colInd, gs.empty_column_indices[0]]
                            gs.empty_column_indices.remove(gs.empty_column_indices[0])
                            return a1  
                            
                    ToggledChars = self.GetToggledCardChar(cardChar)
                    CandCardNames = []
                    for tchar in ToggledChars:
                        candCardName = tchar + str(cardInd+1)
                        CandCardNames.append(candCardName)

                    otherColInd = 1
                    for anotherColCrd in gs.column_cards:
                        if len(anotherColCrd) > 0:
                            if anotherColCrd[0] in CandCardNames:
                                a1.name = 'MoveCardToColumn'
                                #from
                                a1.cards.append(colCrd)
                                #to
                                a1.cards.append(anotherColCrd)
                                gs.ui_components_to_render['columns'] = [colInd, otherColInd]
                                return a1
                        otherColInd += 1
            colInd += 1

        #############################
        # Move column cards to Deck
        #############################
        colInd = 1

        for colCrd in gs.column_cards:        
            #print(colCrd)
            if len(colCrd) > 0:
                if int(colCrd[0][1:]) == 1:
                    a1.name = 'MoveCardToDeck'
                    a1.cards.append(colCrd)                    
                    gs.ui_components_to_render['top_deck'] = []
                    gs.ui_components_to_render['columns'] = [colInd]
                    return a1
                for deckCard in gs.deck_cards_top:
                    #print("DeckCard: " + deckCard[0])
                    dcardChar = deckCard[0][0]
                    dcardInd = int(deckCard[0][1:])
                    reqCard = dcardChar + str(dcardInd+1)                                      
                    if reqCard == colCrd[0]:
                        #print(reqCard)
                        a1.name = 'MoveCardToDeck'
                        a1.cards.append(colCrd)
                        gs.ui_components_to_render['top_deck'] = []
                        gs.ui_components_to_render['columns'] = [colInd]
                        return a1 
            colInd += 1
        
        #############################
        # Move Deck card to column
        #############################
        colInd = 1
        for DeckCard in gs.deck_cards_top:
            if len(DeckCard) > 0:
                #a, h, s, d
                cardChar = DeckCard[0][0]
                #1-13                
                cardInd = int(DeckCard[0][1:])

                #queen
                queenCards = []
                lessCards = []

                #lists the possible card to be stacked below, for a13 it would be [h12, d12] -scarr
                ToggledChars = self.GetToggledCardChar(cardChar)
                CandCardNames = []
                for tchar in ToggledChars:
                    candCardName = tchar + str(cardInd+1)
                    CandCardNames.append(candCardName)
                    queenCards.append(tchar + str(12))
                    queenCards.append(tchar + str(cardInd-1))
                    
                colInd = 1
                for anotherColCrd in gs.column_all_cards:
                    if len(anotherColCrd) > 0:
                        # If it's a king card, move it to empty column if an opposite queen exists without a king
                        if anotherColCrd[0] in queenCards and cardInd == 13:
                            if len(gs.empty_column_indices) > 0: #and gs.column_cards:#
                                    a1.name = 'MoveCardToColumn'
                                    a1.cards.append(DeckCard)                        
                                    a1.cards.append(['empty_col',gs.empty_column_indices[0]])
                                    gs.ui_components_to_render['top_deck'] = []
                                    gs.ui_components_to_render['columns'] = [gs.empty_column_indices[0]]
                                    gs.empty_column_indices.remove(gs.empty_column_indices[0])
                                    return a1   
                        elif anotherColCrd[0] in CandCardNames:
                            #checks if a card below the current cardInd exists
                            lessIncluded = False
                            for lcard in lessCards:
                                if lcard in gs.column_all_cards:
                                    lessIncluded = True
                                    break
                            if lessIncluded:
                                a1.name = 'MoveCardToColumn'
                                #from
                                a1.cards.append(DeckCard)
                                #to
                                a1.cards.append(anotherColCrd)
                                gs.ui_components_to_render['top_deck'] = []
                                gs.ui_components_to_render['columns'] = [colInd]
                                return a1  
                    colInd += 1  
        #TODO modify a1 and UI.process action if card does not register

            
        # Default action will be to draw card
        a1.name = 'DrawNewCard'
        gs.ui_components_to_render['draw_deck'] = []
        return a1
        
    def GetToggledCardChar(self, curr):
        ToggledChars = []
        if curr == 'c' or curr == 's':
            ToggledChars = ['h','d']       
        elif curr == 'd' or curr == 'h':
            ToggledChars = ['c','s']        
        return ToggledChars        