import tatetito_conVision as tttt
import numpy as np
#import random
#from collections import defaultdict
#import pylab
from datetime import datetime
#import cPickle as pk
import dill
#import os
#os.chdir('/home/landfried/gaming/materias/aprendizaje_automatico/ML_TP2')
#files = [f for f in os.listdir('.') if os.path.isfile(f)]
#for f in files:
#	print f
with open('Modelo_entrenado_21dia_00hs.pk', 'rb') as in_strm:
	mundo = dill.load(in_strm)

timesLearn = 60*24
halflife = (timesLearn)/4
disipacion=0.01
b0=-halflife*disipacion


d = datetime.now()
while d.day < 23:
	d = datetime.now()
	t = d.hour*d.minute
	temp = 0.1+((1-0.1)/(1+np.e**(-(b0+disipacion*(timesLearn-t ) ) ) ))
	mundo.learn(temp1=temp, temp2=temp)				
dill.dump(mundo, file('Modelo_entrenado_23dia_00hs.pk','w'))
while d.day < 22:
	d = datetime.now()
	t= d.hour*d.minute
	temp = 0.1+((1-0.1)/(1+np.e**(-(b0+disipacion*(timesLearn-t ) ) ) ))
	mundo.learn(temp1=temp, temp2=temp)				
dill.dump(mundo, file('Modelo_entrenado_22dia_00hs.pk','w'))




# Jugar
