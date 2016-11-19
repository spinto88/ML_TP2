import numpy as np
import random
from collections import defaultdict
import pylab

        
class Tatetito(object): 

    def __init__(self, width = 7, height = 6, alpha = 0.01, gamma = 0.9, temp1 = 1.00, temp2 = 1.00):
        """
        self.tablero = np.array([[True,False,True,True,False,None,None],
                                  [True,True,False,None,None,None,None],
                                  [False,None,None,None,None,None,None],
                                  [None,None,None,None,None,None,None],
                                  [None,None,None,None,None,None,None],
                                  [None,None,None,None,None,None,None]])
        """

        # Q ya bien inicializado
        self.Q = defaultdict(lambda: defaultdict(lambda: random.random()))
        
        self.height = height
        self.width = width


        # Posicion inicial, creo q es lo que vamos a poner al final
        self.tablero = np.array([[None] * width] * height)


        # Temperaturas: 1.00 es temperatura infinita
        self.temp1 = temp1
        self.temp2 = temp2

        self.learning_step = 0
        
        self.alpha = alpha
        self.gamma = gamma
    
    # self.aString() devuelve el hash de la posicion del tablero actual
    def aString(self):
        row, col = self.tablero.shape
        res=""        
        for r in range(row):
            for c in range(col):
                if self.tablero[r,c]== True: res = res + "1"
                if self.tablero[r,c]== False: res = res + "2"
                if self.tablero[r,c]== None: res = res + "0"    
        return res

    
    def cuatro(self, lista):
        last=None
        count=0
        res=False
        for i in range(len(lista)):
            if count == 4: res = True
            if lista[i] == None: last=None; count=0
            if lista[i] == True and last != True: last = True; count = 1
            if lista[i] == True and last == True: count = count + 1
            if lista[i] == False and last != False: last = False; count = 1
            if lista[i] == False and last == False: count = count + 1
        return res
    
    def cuatroEnLinea(self,r,c):
        #c=4;r=3
        row,col = self.tablero.shape
        res = False
        res = res or self.cuatro(self.tablero[r,:])
        res = res or self.cuatro(self.tablero[:,c])
        if c-3<=0 and r-3 <=0: res = res or self.cuatro(self.tablero[r-3:r+1,c-3:c+1].diagonal())
        if c+3<=col and r-3 <=0: res = res or self.cuatro(np.rot90(self.tablero[r-3:r+1,c:c+3+1]).diagonal())
        return res        
        

    # VER BIEN ESTO, VER COMO ENTRA EN EL METODO learn !!!
    def isTerminal(self, c):
        """
        row, col = self.tablero.shape
        for r in range(row):
            if self.tablero[r][c] == None:
                r = r - 1
                break
            else:
                r = row - 1
                break
        """
        # Devuelve 2 si hay cuatro en linea y 1 si el tablero esta lleno
        #if self.cuatroEnLinea(r,c):
#            return 2
        # Si el tablero esta lleno, devuelve que es terminal
        if None not in self.tablero:
            return 1
        else:
            return False
        
    # Devuelve una lista de acciones posibles, 
    #    donde cada accion es la columna donde poner la ficha
    def accionesPosibles(self):

        res = []
        row, col = self.tablero.shape
        for c in range(col):
            for r in range(row):
                if self.tablero[r,c] == None: res.append(c); break
        return res

    """ Actualiza sobre el tablero la accion realizada """
    def move(self, action, player):

        row = self.tablero.shape[0]
        col_action = action
        for r in range(row):
            if self.tablero[r][col_action] == None:
                self.tablero[r][col_action] = player
                break
        return col_action


    # FALTA VER ESTA FUNCION, CREO QUE HAY QUE PASARLE PLAYER, 
    # Y QUE NO DE RECOMPENSA SI ES EMPATE!!!
    """ Funcion recompensa, tengo una reward positiva si desde state
    usando action llego a un estado terminal """
    def reward(self, action, player):
        row = self.tablero.shape[0]
        if self.isTerminal(self.move(action, player)) == 2:
            # Desmueve
            for r in range(row):
                if self.tablero[r][action] == None:
                    r = r-1
                    break    
            self.tablero[r,action] = None
            
            return self.positive
        else:
            return 0
            
    def learn(self):

        self.learning_step += 1

        # Inicializo
        player = True
        action_best = 0
        
        # Repito hasta que state sea terminal
        # VER ACA, QUE ES LO QUE LE PASAMOS COMO STATE!!!!!
        while self.isTerminal(action_best) == True:
            
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
                 if random.random() < self.temp1:
                      action_best = random.choice(actions)
                 else:
                      actions_Q = [[action, self.Q[state][action]] for action in actions]
                      action_best = max(actions_Q, key = lambda x: x[1])[0]
            
            if player == False:
                 # Aca ponemos la temperatura del player False
                 if random.random() < self.temp2:
                      action_best = random.choice(actions)
                 else:
                      actions_Q = [[action, self.Q[state][action]] for action in actions]
                      action_best = max(actions_Q, key = lambda x: x[1])[0]

            # 3) Calculo el nuevo valor de Q(s,a)
            # OJO: aca ya cambia el tablero
            self.move(action_best, player)
            new_state = self.aString()
            
            new_actions = self.accionesPosibles()

            new_actions_Q = [[action, self.Q[new_state][action]] for action in new_actions]
            new_action_best = max(new_actions_Q, key = lambda x: x[1])[0]

            # Aca hay que revisar conceptualmente si el - de gamma esta bien
            self.Q[state][action_best] += self.alpha*(self.reward(state, action_best)\
                    - self.gamma * (self.Q[new_state][new_action_best] - self.Q[state][action_best]))

            # Cambia el jugador
            player = not player
            print 1


    def draw(self):
       
        color_dict = {True: 'red', False: 'green', None: 'white'}
        
        for row in range(self.height):
            for col in range(self.width):
                pylab.plot(col, row, '.', markersize=30, color=color_dict[self.tablero[row,col]])
        pylab.xlim([-0.5, 6.5])
        pylab.ylim([-0.5, 5.5])


def __main__():                             
    seba_pinto = Tatetito()
    seba_pinto.learn()
    print seba_pinto.tablero
    print seba_pinto.Q
    seba_pinto.draw()

