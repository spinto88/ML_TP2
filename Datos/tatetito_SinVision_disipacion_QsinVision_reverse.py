import tatetito as tttt
import numpy as np
import csv 
#import random
#from collections import defaultdict
#import pylab
from datetime import datetime
#import cPickle as pk
import dill
#import os
#os.chdir('/home/landfried/gaming/materias/aprendizaje_automatico/ML_TP2/Datos')
#files = [f for f in os.listdir('.') if os.path.isfile(f)]
#for f in files:
#	print f
with open('Modelo_entrenado.pk', 'rb') as in_strm:
	mundo = dill.load(in_strm)



file_ = open('SinVision_disipacion_QsinVison_reverse.csv', 'wb') 
file_writer = csv.writer(file_)
file_writer.writerow(['gana'])
t = 0

timesLearn = 5000
halflife = ((timesLearn)*2)/5
disipacion=0.005
b0=-halflife*disipacion


while t < timesLearn :
	t+=1
	temp = ((1)/(1+np.e**(-(b0+disipacion*(timesLearn-t ) ) ) ))
	res = mundo.learn(temp1=1, temp2=temp)
	file_writer.writerow([res])
file_.close()


