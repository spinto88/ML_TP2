import numpy as np
import random
from collections import defaultdict
import pylab
import matplotlib.pyplot as plt

        
class Tatetito(object):

    def __init__(self, width = 7, height = 6, alpha = 0.01, gamma = 0.9, \
                 temp1 = 100.0, temp2 = 100.0, epsilon1 = 1.00, epsilon2 = 1.00):

        self.width = width
        self.height = height

        self.tablero = np.zeros([height, width], dtype = np.int16)
        
        self.Q = defaultdict(lambda: defaultdict(lambda: random.random()))
        
        self.alpha = alpha
        self.gamma = gamma

        # Estrategias 
        self.strategy1 = 'random'
        self.strategy2 = 'random'

        # Temperaturas: 10.00 es temperatura alta, 0.01 es bien baja.
        self.temp1 = temp1
        self.temp2 = temp2

        # Epsilon de e-greedy
        self.epsilon1 = epsilon1
        self.epsilon2 = epsilon2
        
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
        
        if '1111' in lista_str:
            return 1
        elif '2222' in lista_str:
            return 2
        else:
            return False

    
    def cuatroEnLinea(self,r,c):

        res = False
        res = res or self.cuatro(self.tablero[r,:])
        res = res or self.cuatro(self.tablero[:,c])
         
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
            return self.cuatroEnLinea(r,c)
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


    # Actualiza sobre el tablero la accion realizada
    def move(self, action, player):

        for r in range(self.height):
            if self.tablero[r,action] == 0:
                self.tablero[r,action] = player
                break


    # FALTA VER ESTA FUNCION, CREO QUE HAY QUE PASARLE PLAYER, 
    # Y QUE NO DE RECOMPENSA SI ES EMPATE!!!
    """ Funcion recompensa, tengo una reward positiva si desde state
    usando action llego a un estado terminal """
    def reward(self, action, player):
        
        self.move(action, player)
        if self.isTerminal(action) == 1 or self.isTerminal(action) == 2:
            res = 100
        else:
            res = 0
        # "Desmueve"
        for r in range(self.height):
            if self.tablero[r,action] == 0:
                r = r-1
                break    
        self.tablero[r,action] = 0
        return res
    
        
    def learn(self, steps = np.inf):

        # Inicializo
	player = random.choice([1,2])
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

            # 2) Elijo la accion con a con algun criterio, en principio al azar
	       # Aca discriminamos que jugador juega con temperatura alta o baja

            # Jugador 1
            if player == 1:
                if self.strategy1 == 'random':
                    action_best = np.random.choice(actions)
                elif self.strategy1 == 'e-greedy':
	            if random.random() < self.epsilon1:
                        action_best = np.random.choice(actions)
	            else:
                        actions_Q = [[action, self.Q[state][action]] for action in actions]                
                        action_best = max(actions_Q, key = lambda x: x[1])[0] 
                elif self.strategy1 == 'softmax':
                    temp = self.temp1
                    p_actions = [np.exp(self.Q[state][action]/temp) for action in actions]
            
                    if np.sum(p_actions) == 0.00:
                        action_best = np.random.choice(actions)
                    else:
                        p_actions_norm = p_actions / np.sum(p_actions)                                  
                        try:
                            action_best = np.random.choice(actions, p = p_actions_norm)
                        except:
                            actions_Q = [[action, self.Q[state][action]] for action in actions]                
                            action_best = max(actions_Q, key = lambda x: x[1])[0]
            # Jugador 2
            if player == 2:
                if self.strategy2 == 'random':
                    action_best = np.random.choice(actions)
                elif self.strategy2 == 'e-greedy':
	            if random.random() < self.epsilon2:
                        action_best = np.random.choice(actions)
	            else:
                        actions_Q = [[action, self.Q[state][action]] for action in actions]                
                        action_best = max(actions_Q, key = lambda x: x[1])[0] 
                elif self.strategy2 == 'softmax':
                    temp = self.temp2
                    p_actions = [np.exp(self.Q[state][action]/temp) for action in actions]
            
                    if np.sum(p_actions) == 0.00:
                        action_best = np.random.choice(actions)
                    else:
                        p_actions_norm = p_actions / np.sum(p_actions)                                  
                        try:
                            action_best = np.random.choice(actions, p = p_actions_norm)
                        except:
                            actions_Q = [[action, self.Q[state][action]] for action in actions]                
                            action_best = max(actions_Q, key = lambda x: x[1])[0]

 
            recompensa = self.reward(action_best, player)
            
            # 3) Calculo el nuevo valor de Q(s,a)
            # OJO: aca ya cambia el tablero
            self.move(action_best, player)

            new_state = self.aString()
            
            new_actions = self.accionesPosibles()

            try:
                new_actions_Q = [[action, self.Q[new_state][action]] for action in new_actions]                
                new_action_best = max(new_actions_Q, key = lambda x: x[1])[0]          

                # Aca hay que revisar conceptualmente si el - de gamma esta bien
                self.Q[state][action_best] += self.alpha*(recompensa - self.gamma * (
                    self.Q[new_state][new_action_best] + self.Q[state][action_best]))
    
                # Cambia el jugador
                if player == 1: player = 2
                else: player = 1
            except ValueError:
                pass
            
        return self.isTerminal(action_best)
        
        
    def draw(self):        
        color_dict = {0: 'white', 1: 'red', 2: 'green'}
        
        for row in range(self.height):
            for col in range(self.width):
                pylab.plot(col, row, '.', markersize=30, color=color_dict[self.tablero[row,col]])
        pylab.xlim([-0.5, self.width-1 + 0.5])
        pylab.ylim([-0.5, self.height-1 + 0.5])
        pylab.show()



# Los dos random
random.seed(123457)
seba_pinto = Tatetito()
winners = []
for k in range(10000):
    winners.append(seba_pinto.learn())


# El jugador 2 con e-greedy
random.seed(123457)
seba_pinto = Tatetito()
winners = []
seba_pinto.strategy2 = 'e-greedy'
seba_pinto.epsilon2 = 0.25
for k in range(10000):
    winners.append(seba_pinto.learn())








# Cuento las victorias
victorias1 = []
acum = 0
for i in winners:
    if i == 1:
        acum += 1
    victorias1.append(acum)

victorias2 = []
acum = 0
for i in winners:
    if i == 2:
        acum += 1
    victorias2.append(acum)


plt.plot(victorias1, label = 'Jugador 1')
plt.plot(victorias2, label = 'Jugador 2')
plt.xlabel('Juegos')
plt.ylabel('Victorias acumuladas')
plt.legend(loc = 'best')
plt.grid('on')
plt.show()
