import tatetito as tttt
#import numpy as np
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


file_ = open('SinVision_luchaNoLibre_QsinVison_reverse.csv', 'wb') 
file_writer = csv.writer(file_)
file_writer.writerow(['gana'])
d = datetime.now()
while d.day < 24 and d.hour < 16:
	res = mundo.learn(temp1=1, temp2=0)
	file_writer.writerow([res])
	d = datetime.now()
file_.close()


