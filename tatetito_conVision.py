import numpy as np
import random
from collections import defaultdict
import pylab
#import cPickle as pk
import dill
#import os
#os.chdir('/home/landfried/gaming/materias/aprendizaje_automatico/ML_TP2')

        
class Tatetito(object):

    def __init__(self, width = 7, height = 6, alpha = 0.01, gamma = 0.9
				, premio=1000):

        self.width = width
        self.height = height
								
        self.premio =premio

        self.tablero = np.zeros([height, width], dtype = np.int16)
        
        self.Q = defaultdict(lambda: defaultdict(lambda: random.random()))
        
        self.alpha = alpha
        self.gamma = gamma

        # Temperaturas: 1.00 es temperatura infinita
        
        self.learning_step = 0
    
    
    # self.aString() devuelve el hash de la posicion del tablero actual
    def aString(self):

        res = ""
        for casilla in self.tablero.flatten():
            res += str(casilla)
        return res

    
    def cuatro(self, lista):

        lista_str = ''
        for i in lista:
            lista_str += str(i)
        
        if '1111' in lista_str or '2222' in lista_str:
            return True
        else:
            return False

    
    def cuatroEnLinea(self,r,c):

        res = False
        res = res or self.cuatro(self.tablero[r,:])
        res = res or self.cuatro(self.tablero[:,c])
        
        #diag1 = [self.tablero[i,j] for i in range(self.height) for j in [k in range(c-3, c+3) if k >= 0 and k < self.width]]  (SEBA PINTO)
        #diag2 = [self.tablero[i,j] for i in range(self.height) for j in [k in range(c-3, c+3).reverse if k >= 0 and k < self.width]]
        
        diag1 = []
        i = 0
        while r-i >= 0 and c-i >= 0:
            diag1.append(self.tablero[r-i,c-i])
            i += 1
        diag1.reverse()
        i = 1
        while r+i < self.height and c+i < self.width:
            diag1.append(self.tablero[r+i,c+i])
            i += 1

        diag2 = []
        i = 0
        while r-i >= 0 and c+i < self.width:
            diag2.append(self.tablero[r-i,c+i])            
            i += 1
        diag2.reverse()        
        i = 1
        while r+i < self.height and c-i >= 0:
            diag2.append(self.tablero[r+i,c-i])
            i += 1
            
        res = res or self.cuatro(diag1)
        res = res or self.cuatro(diag2)
        return res
        

    def isTerminal(self, c):
        
        if self.learning_step == 0: return "Falso"
        for r in range(self.height):
            if self.tablero[r,c] == 0:
                r = r - 1
                break
        
        # Devuelve 2 si hay cuatro en linea y 1 si el tablero esta lleno
        if self.cuatroEnLinea(r,c):
            return "4EnLinea"
        # Si el tablero esta lleno, devuelve que es terminal
        elif 0 not in self.tablero:
            return "Lleno"
        else:
            return "Falso"
            
        
    # Devuelve una lista de acciones posibles, donde cada accion es la columna donde poner la ficha
    def accionesPosibles(self):

        res = []
        for c in range(self.width):
            for r in range(self.height):
                if self.tablero[r,c] == 0: res.append(c); break
        return res

    def ultimaFilaLibre(self,action):
        res = self.height
        for r in range(self.height):
            if self.tablero[r,action] == 0:
                res= r
                break  
        return res    
    # Actualiza sobre el tablero la accion realizada
    def move(self, action, player):
        r = self.ultimaFilaLibre(action)
        self.tablero[r,action] = player
        
    def revert(self, action):
        r = self.ultimaFilaLibre(action)
        self.tablero[r-1,action] = 0
    
    # FALTA VER ESTA FUNCION, CREO QUE HAY QUE PASARLE PLAYER, 
    # Y QUE NO DE RECOMPENSA SI ES EMPATE!!!
    """ Funcion recompensa, tengo una reward positiva si desde state
    usando action llego a un estado terminal """
    def reward(self, action, player):
        
        self.move(action, player)
        if self.isTerminal(action) == "4EnLinea":
            res = self.premio
        else:
            res = 0
        # "Desmueve"
        self.revert(action)
        return res
    
        
    def learn(self, steps = np.inf, temp1=0, temp2=0):

        # Inicializo
        player = 1
        action_best = np.random.randint(self.width)
        step = 0
        self.tablero = np.zeros([self.height, self.width], dtype = np.int16)
        # Repito hasta que state sea terminal
        # VER ACA, QUE ES LO QUE LE PASAMOS COMO STATE!!!!!
        while self.isTerminal(action_best) == "Falso" and step < steps:

            self.learning_step += 1
            step += 1
            state = self.aString()
            # 1) Listo las posibles acciones que puedo hacer teniendo
                # en cuenta el estado de donde estoy, cargado en la matriz
            actions = self.accionesPosibles()
            # LO MAS IMPORTANTE A CAMBIAR ESTA AQUI
            # 2) Elijo la accion con a con algun criterio, en principio al azar
            # Aca discriminamos que jugador juega con temperatura alta o baja
            if player == 1:
                temp = temp1
                otro = 2
            else:
                otro = 1
                temp = temp2
            if random.random() < temp:
                action_best = random.choice(actions)
            else:
                for a in actions:
                    #a=0
                    r = self.ultimaFilaLibre(a)
                    self.move(a,player)
                    for b in self.accionesPosibles():
                        #b=3
                        s = self.ultimaFilaLibre(b) 
                        self.move(b,otro)
                        if self.cuatroEnLinea(s,b):
                            self.Q[state][a]=-self.premio
                        self.revert(b)
                    if self.cuatroEnLinea(r,a):
                        self.Q[state][a]=self.premio*2
                    self.revert(a)
                    #self.draw()
                actions_Q = [[action, self.Q[state][action]] for action in actions]
                action_best = max(actions_Q, key = lambda x: x[1])[0]                
            recompensa = self.reward(action_best, player)
            # 3) Calculo el nuevo valor de Q(s,a)
            # OJO: aca ya cambia el tablero
            self.move(action_best, player)
            #self.draw()
            new_state = self.aString()
            new_actions = self.accionesPosibles()
            try:
                new_actions_Q = [[action, self.Q[new_state][action]] for action in new_actions]                
                new_action_best = max(new_actions_Q, key = lambda x: x[1])[0]          
                # Aca hay que revisar conceptualmente si el - de gamma esta bien
                self.Q[state][action_best] += self.alpha*(recompensa - self.gamma * (
                    self.Q[new_state][new_action_best] - self.Q[state][action_best]))
                # Cambia el jugador
                if player == 1: player = 2
                else: player = 1
            except ValueError:
                pass
            
        #pylab.figure()
        #self.draw()

        
    def draw(self):        
        color_dict = {0: 'white', 1: 'red', 2: 'green'}
        
        for row in range(self.height):
            for col in range(self.width):
                pylab.plot(col, row, '.', markersize=30, color=color_dict[self.tablero[row,col]])
        pylab.xlim([-0.5, self.width-1 + 0.5])
        pylab.ylim([-0.5, self.height-1 + 0.5])









# Jugar
