import numpy as np
import pandas as pd
import random
from collections import defaultdict
import pylab
from copy import deepcopy

        
class Tatetito(object): 

    def __init__(self, width = 7, height = 6):
        self.tablero = np.array([[True,False,True,True,False,None,None],
                                  [True,True,False,None,None,None,None],
                                  [False,None,None,None,None,None,None],
                                  [None,None,None,None,None,None,None],
                                  [None,None,None,None,None,None,None],
                                  [None,None,None,None,None,None,None]])    

        # Q ya bien inicializado
        self.Q = defaultdict(lambda: defaultdict(lambda: random.random()))
        self.height = height
        self.width = width


        # Temperaturas 
        self.temp1 = 1.00
        self.temp2 = 1.00

        self.learning_step = 0
    
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
        

    # VER BIEN ESTO, VER COMO ENTRA EN EL METODO learn !!!
    def isTerminal(self, r, c):

        # CALCULAR ACA r y c, creo que hay que pasarle como el ultimo move

        if self.cuatroEnLinea(r,c) :
            return True
        # Si el tablero esta lleno, devuelve que es terminal
        elif None not in self.tablero:
            return True

        else:
            return False
        

    def accionesPosibles(self):

        res = list([])
        row,col = self.tablero.shape
        for c in range(col):
            for r in range(row):
                if self.tablero[r,c]== None: res.append(r,c]); break
        return res

    """ Actualiza sobre el tablero la accion realizada """
    def move(self, action, player):

        row, col = action
        self.tablero[row][col] = player


    # FALTA VER ESTA FUNCION, CREO QUE HAY QUE PASARLE PLAYER, 
    # Y QUE NO DE RECOMPENSA SI ES EMPATE!!!
    """ Funcion recompensa, tengo una reward positiva si desde state
    usando action llego a un estado terminal """
    def reward(self, state, action):

        if self.isTerminal(self.move(state,action)):
            return self.positive
        else:
            return 0
            
    def learn(self):

        self.learning_step += 1

        player = True

        state = self.aString()

        # Repito hasta que state sea terminal
        # VER ACA, QUE ES LO QUE LE PASAMOS COMO STATE!!!!!
        while self.isTerminal(...) == False:

            # Esta es la key
            state = self.aString()

            # 1) Listo las posibles acciones que puedo hacer teniendo
                # en cuenta el estado de donde estoy, cargado en la matriz
            actions = self.accionesPosibles()

            # LO MAS IMPORTANTE A CAMBIAR ESTA AQUI
            # 2) Elijo la accion con a con algun criterio, en principio al azar
	    # Aca discriminamos que jugador juega con temperatura alta o baja
            if player == True:
                 # Aca ponemos la temperatura del player True
                 if random() < self.temp1:
                      action_best = random.choice(actions)
                 else:
                      actions_Q = [[action, self.Q[state][action]] for action in new_actions]
                      action_best = max(actions_Q, key = lambda x: x[1])[0]
            
            if player == False:
                 # Aca ponemos la temperatura del player False
                 if random() < self.temp2:
                      action_best = random.choice(actions)
                 else:
                      actions_Q = [[action, self.Q[state][action]] for action in new_actions]
                      action_best = max(actions_Q, key = lambda x: x[1])[0]


            # 3) Calculo el nuevo valor de Q(s,a)
            # OJO: aca ya cambia el tablero
            self.move(action_best, player)
            new_state = aString()
            
            new_actions = self.accionesPosibles()

            new_actions_Q = [[action, self.Q[new_state][action]] for action in new_actions]
            new_action_best = max(new_actions_Q, key = lambda x: x[1])[0]

            # Aca hay que revisar conceptualmente si el - de gamma esta bien
            self.Q[state][action_best] += self.alpha*(self.reward(state, action_best)\
                    - self.gamma * (self.Q[new_state][new_action_best] - self.Q[state][action_best]))

            # Cambia el jugador
            player = not player


   def draw(self):
       
	color_dict = {True: 'red', False: 'green', None: 'white'}
        
        for row in range(6):
            for col in range(7):
                pylab.plot(col, row, '.', markersize=30, color=color_dict[self.tablero[row,col]])
        pylab.xlim([-0.5, 6.5])
        pylab.ylim([-0.5, 5.5])

                                 
