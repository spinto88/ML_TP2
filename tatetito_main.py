import tatetito_conVision as tttt
#import numpy as np
#import random
#from collections import defaultdict
#import pylab
from datetime import datetime
#import cPickle as pk
import dill
#import os
#os.chdir('/home/landfried/gaming/materias/aprendizaje_automatico/ML_TP2')

mundo = tttt.Tatetito(premio=1000)
d = datetime.now()
while d.day <= 21 and d.hour <= 9:
	d = datetime.now()
	mundo.learn()				
dill.dump(mundo, file('Modelo_entrenado.pk','w'))









# Jugar
