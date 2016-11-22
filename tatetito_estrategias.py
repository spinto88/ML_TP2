import numpy as np
import random
from collections import defaultdict
import pylab
import matplotlib.pyplot as plt

        
class Tatetito(object):

    def __init__(self, width = 7, height = 6, alpha = 0.01, gamma = 0.9, \
                 temp1 = 100.0, temp2 = 100.0, epsilon1 = 1.00, epsilon2 = 1.00):

	# Tablero
        self.width = width
        self.height = height
        self.tablero = np.zeros([height, width], dtype = np.int16)
        
        self.Q = defaultdict(lambda: defaultdict(lambda: random.random()))
        
	# Parametros del Q-learning
        self.alpha = alpha
        self.gamma = gamma

        # Estrategias: random, e-greedy, softmax 
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

    # Observa si hay cuatro en una linea
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

    # Observa si hay cuatro en linea en el tablero
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
        
    # Observa si el estado es terminal, 
    # si hay cuatro en linea o esta lleno
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


    # Funcion recompensa, obtengo si hago una jugada 
    # que me lleva al cuatro en linea
    def reward(self, action, player):
        
        self.move(action, player)
        if self.isTerminal(action) == 1 or self.isTerminal(action) == 2:
            res = 100
        else:
            res = 0

        # Desmueve: lleva al tablero a la misma posicion de antes
        for r in range(self.height):
            if self.tablero[r,action] == 0:
                r = r-1
                break    
        self.tablero[r,action] = 0
        return res
    
        
    # Algoritmo propio del aprendiza
    def learn(self, steps = np.inf):

        # Inicializo un jugador al azar y accion al azar

	player = random.choice([1,2])
        action_best = np.random.randint(self.width)
        step = 0

	# Tablero vacio
        self.tablero = np.zeros([self.height, self.width], dtype = np.int16)

        # Repito hasta que state sea terminal
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

	    # Veo si hay recompensa 
            recompensa = self.reward(action_best, player)
            
            # Realizo la accion
            self.move(action_best, player)

	    # Obtengo el nuevo estado
            new_state = self.aString()
            
            # Veo las nuevas acciones posibles
            new_actions = self.accionesPosibles()

            try:
                new_actions_Q = [[action, self.Q[new_state][action]] for action in new_actions]                
                new_action_best = max(new_actions_Q, key = lambda x: x[1])[0]          

                # Actualizacon del Q
                self.Q[state][action_best] += self.alpha*(recompensa - self.gamma * (
                    self.Q[new_state][new_action_best] - self.Q[state][action_best]))
    
                # Cambia el jugador
                if player == 1: player = 2
                else: player = 1
            except ValueError:
                pass
            
        # Si es terminal devuelvo quien gana o si hay empate
        return self.isTerminal(action_best)
        
        
    # Metodo dibujo el tablero
    def draw(self):        

        pylab.clf()
        color_dict = {0: 'white', 1: 'red', 2: 'green'}
        
        for row in range(self.height):
            for col in range(self.width):
                pylab.plot(col, row, '.', markersize=30, color=color_dict[self.tablero[row,col]])
        pylab.xlim([-0.5, self.width-1 + 0.5])
        pylab.ylim([-0.5, self.height-1 + 0.5])
        pylab.grid('on')
        pylab.show()



# Main del archivo
# Explora la evolucion del juego cuando el jugador 2 implementa
# una estrategia de e-greedy

j = 0

for epsilon2 in [0.00, 0.10, 0.20, 0.50, 1.00]:

   # Seteo las semillas
   random.seed(123458)
   np.random.seed(123458)

   tato = Tatetito()

   # El jugador 2 con e-greedy
   tato.strategy2 = 'e-greedy'
   tato.epsilon2 = epsilon2

   winners = []
   for k in range(1):
       winners.append(tato.learn())

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
   
   plt.figure(j)
   plt.plot(victorias1, '-', linewidth = 2, label = 'Jugador 1')
   plt.plot(victorias2, '-', linewidth = 2, label = 'Jugador 2')
   plt.axis([0, 100000, 0, 70000])
   plt.xlabel('Juegos')
   plt.ylabel('Victorias acumuladas')
   plt.legend(loc = 'best')
   plt.grid('on')
   plt.title('Epsilon jugador 2: ' + str(tato.epsilon2))
   plt.savefig('Epsilon' + str(epsilon2) + '.eps')
   j += 1
   

   # Grafico del tablero
   tato.draw()
