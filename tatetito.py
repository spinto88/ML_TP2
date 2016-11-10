import numpy as np
import pandas as pd
import random
from collections import defaultdict
import pylab
from copy import deepcopy

        
class state(): 
    def __init__(self):
        self.tablero = np.array([[True,False,True,True,False,None,None],
                                  [True,True,False,None,None,None,None],
                                  [False,None,None,None,None,None,None],
                                  [None,None,None,None,None,None,None],
                                  [None,None,None,None,None,None,None],
                                  [None,None,None,None,None,None,None]])    

        # Diccionario de diccionarios
        self.Q = {}
        # Falta ver bien como inicializarlo
 
    
    def aString(self):
        row,col = self.tablero.shape
        res=""        
        for r in range(row):
            for c in range(col):
                if self.tablero[r,c]== True: res =res + "1"
                if self.tablero[r,c]== False: res =res + "2"
                if self.tablero[r,c]== None: res =res + "0"    
        return res


    def cuatro(self,lista):
        last=None
        count=0
        res=False
        for i in range(len(lista)):
            if count == 4: res = True
            if lista[i] == None: last=None; count=0
            if lista[i] == True and last != True: last = True; count = 1
            if lista[i] == True and last == True: count = count + 1
            if lista[i] == False and last != False: last = False; count =  1
            if lista[i] == False and last == False: count = count + 1
        return res
    
    def cuatroEnLinea(self,r,c):
        #c=4;r=3
        row,col = self.tablero.shape
        res = False
        res = res or self.cuatro(self.tablero[r,:])
        res = res or self.cuatro(self.tablero[:,c])
        if c-3<=0 and r-3 <=0: res = res or self.cuatro(self.tablero[r-3:r+1,c-3:c+1].diagonal())
        if c+3<=col and r-3 <=0: res = res or self.cuatro(rot90(self.tablero[r-3:r+1,c:c+3+1]).diagonal())
        return res        
        
    def isTerminal(self,r,c):
        if self.cuatroEnLinea(r,c) :
            return True
        else:
            return False

    """ Player es True o False, segun quien juegue """
    def accionesPosibles(self, player):

        res = list([])
        row,col = self.tablero.shape
        for c in range(col):
            for r in range(row):
                if self.tablero[r,c]== None: res.append([player,r,c]); break
        return res

    """ Actualiza sobre el tablero la accion realizada """
    def move(self, action):

        tablero_aux = deepcopy(self.tablero)

        row, col = action[1,2]
        tablero_aux[row][col] = action[0]

        return tablero_aux

    """ Funcion recompensa, tengo una reward positiva si desde state
    usando action llego a un estado terminal """
    def reward(self, state, action):

        if self.isTerminal(self.move(state,action)):
            return self.positive
        else:
            return 0
            
    def learn(self, state):

        self.learning_step += 1

        player = True

        # Repito hasta que state sea terminal
        while self.isTerminal(state) == False:

            # 1) Listo las posibles acciones que puedo hacer teniendo
                # en cuenta el estado de donde estoy
            actions = self.possibleActions(state, player)

            # LO MAS IMPORTANTE A CAMBIAR ESTA AQUI
            # 2) Elijo la accion con a con algun criterio, en principio al azar
	    # Aca discriminamos que jugador juega con temperatura alta o baja
            if player == True:
            # Aca ponemos la temperatura del player True
            action_best = random.choice(actions)
            else player == False:
            # Aca ponemos la temperatura del player False
            action_best = random.choice(actions)


            # 3) Calculo el nuevo valor de Q(s,a)
            new_state = self.move(action_best)
            
            new_actions = self.possibleActions(new_state)

            new_actions_Q = [[action, self.Q[new_state][action]] for action in new_actions]
            new_action_best = max(new_actions_Q, key = lambda x: x[1])[0]

            # Antes de pasar state a Q, convertirlo a string con el metodo definido

            # Aca hay que revisar si el - de gamma esta bien
            self.Q[state][action_best] += self.alpha*(self.reward(state, action_best) - self.gamma * (self.Q[new_state][new_action_best] - self.Q[state][action_best]))

            # 4) Actualizo s
            state = new_state

            # Cambia el jugador
            player = not player


   def draw(self):
       pass 
                                 
