import pygame
import numpy as np
from random import randint

pygame.init()
clock = pygame.time.Clock()
negro=(0,0,0)
blanco=(255,255,255)
nReinas=8
dimension=65
ventanax=nReinas*dimension
ventanay=nReinas*dimension
ventana = pygame.display.set_mode((ventanax,ventanay))
tamanio_poblacion=100

fila=np.zeros(tamanio_poblacion,dtype=int)
filax=np.zeros(tamanio_poblacion,dtype=int)
columna=np.zeros(tamanio_poblacion,dtype=int)
columnax=np.zeros(tamanio_poblacion,dtype=int)
t_reinas=np.zeros(tamanio_poblacion,dtype=int)
total=np.zeros(tamanio_poblacion,dtype=int)
fitness=np.zeros(tamanio_poblacion,dtype=int)
aux1=np.zeros(tamanio_poblacion)
aux2=np.zeros(tamanio_poblacion)
auxi=np.zeros(tamanio_poblacion)
auxj=np.zeros(tamanio_poblacion)
porcentaje_de_vivir=np.zeros(tamanio_poblacion)

reina=pygame.image.load("Reina1.png")
reina=pygame.transform.scale(reina, (dimension, dimension))
poblacion=np.zeros((tamanio_poblacion,nReinas,nReinas),dtype=int)

aux=0
n_fila=0
n_col=0

for aux in range(tamanio_poblacion):
    for n_col in range(0,nReinas):
       poblacion[aux,randint(0,nReinas-1),n_col]=1

def imprimirReina(sujeto):   
    for n_fila in range(nReinas):
        for n_col in range(nReinas):
            if poblacion[sujeto,n_fila,n_col]==1:
                ventana.blit(reina,(n_col*dimension,n_fila*dimension))
    pygame.display.flip()    

def tablero(color):
    i=0
    j=0
    ventana.fill(color)
    pygame.display.flip()
    for j in range(0,nReinas):
        for i in range(0,nReinas):   
            if(i%2==0 and j%2!=0 or i%2!=0 and j%2==0):
               pygame.draw.rect(ventana, negro,(i*dimension, j*dimension, dimension, dimension))

pygame.display.set_caption('Algoritmo Genetico de las 8 Reinas')
pygame.display.flip()
close=False
generacion=0
fmax=8*(nReinas-1)
while(close==False):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close = True  
    #inicializar
    for aux in range(tamanio_poblacion):
        fila[aux]=0
        columna[aux]=0
        aux1[aux]=0
        aux2[aux]=0
        t_reinas[aux]=0
        filax[aux]=0
        columnax[aux]=0
        auxi[aux]=0
        auxj[aux]=0

    #Evaluacion de filas
    for aux in range(tamanio_poblacion):
        for n_fila in range(nReinas):        
            filax[aux]=fila[aux]        
            for n_col in range(nReinas):
                if poblacion[aux,n_fila,n_col]==1:
                    fila[aux]+=1
            if fila[aux] - filax[aux] != 0:
                fila[aux]-=1

    #evaluacion de columnas
    for aux in range(tamanio_poblacion):
        for n_col in range(nReinas):        
            columnax[aux]=columna[aux]        
            for n_fila in range(nReinas):
                if poblacion[aux,n_fila,n_col]==1:
                    columna[aux]+=1
            if columna[aux] - columnax[aux] != 0:
                columna[aux]-=1

    #evaluacion diagonal positiva    
    for aux in range(tamanio_poblacion):
        dp=0
        while  dp <= ((nReinas - 1) * 2):
            auxi[aux]=aux1[aux]
            for n_fila in range(nReinas):
                for n_col in range(nReinas):
                    if (n_fila+n_col) == dp:
                        if poblacion[aux,n_fila,n_col]==1 :
                            aux1[aux]+=1
            if aux1[aux] - auxi[aux] != 0:
                aux1[aux]-=1
            dp+=1
    
    #evaluacion en diagonal negativa    
    for aux in range(tamanio_poblacion):
        dn=1-nReinas
        while  dn <= nReinas-1:
            auxj[aux]=aux2[aux]
            for n_fila in range(nReinas):        
                for n_col in range(nReinas):
                    if poblacion[aux,n_fila,n_col]==1 and (n_col-n_fila)==dn:
                        aux2[aux]+=1
            if aux2[aux] - auxj[aux] != 0:
                aux2[aux]-=1
            dn+=1
            
    #evaluacion de total de reinas
    for aux in range(tamanio_poblacion):
        for n_fila in range(nReinas):
            for n_col in range(nReinas):
                if poblacion[aux,n_fila,n_col]==1:
                    t_reinas[aux]+=1
    
    #fitness
    for aux in range(tamanio_poblacion):
        total[aux] = fila[aux] + columna[aux] + aux1[aux] + aux2[aux]
        fitness[aux] = (fmax - total[aux]) + abs(0 - t_reinas[aux])
    
    #porcentajes de vivir
    porcentaje_total=0
    for aux in range(tamanio_poblacion):
        porcentaje_total+=fitness[aux]
    for aux in range(tamanio_poblacion):
        porcentaje_de_vivir[aux]=float((fitness[aux]*100)/porcentaje_total)
    
    # padres
    padre=0
    madre=0

    #busqueda para el padre
    for aux in range(tamanio_poblacion):
        if porcentaje_de_vivir[aux] >= porcentaje_de_vivir[padre]:
            padre=aux
            aux=tamanio_poblacion
    if generacion==10000:
        close=True
    for aux in range(tamanio_poblacion):
        if (fmax - total[aux]) + abs(t_reinas[aux]) == nReinas + fmax:
          close=True
          tablero(blanco)
          imprimirReina(padre)
          print("Solucion: ",generacion) 
   
    if close==False and generacion%1==0:
        print("Generación: ",generacion)
        tablero(blanco)
        imprimirReina(0)


    #'''busqueda para madre
    porcentaje_de_vivir[padre]=0
    for aux in range(tamanio_poblacion):
        if porcentaje_de_vivir[aux]>=porcentaje_de_vivir[madre] and (poblacion[padre,:,:]!=poblacion[aux,:,:]).any():
            madre=aux
            aux=tamanio_poblacion
    hijo=np.zeros((3,nReinas,nReinas),dtype=int)
    mejorsujeto=np.zeros((nReinas,nReinas),dtype=int)
    cruce=nReinas-1
    for _ in range(randint(1,nReinas)):
        cruce=randint(1,nReinas-1)
        
    #cruce 1° generacion
    for n_fila in range(nReinas):
        for n_col in range(nReinas):
            if n_col<cruce:
                hijo[0,n_fila,n_col]=poblacion[padre,n_fila,n_col]
                hijo[1,n_fila,n_col]=poblacion[padre,n_fila,n_col]
            if n_col>=cruce:
                hijo[2,n_fila,n_col]=poblacion[padre,n_fila,n_col]
            mejorsujeto[n_fila,n_col]=poblacion[padre,n_fila,n_col]
    
    #cruce 2° generacion
    for n_fila in range(nReinas):
        for n_col in range(nReinas):
            if n_col>=cruce:
                hijo[0,n_fila,n_col]=poblacion[madre,n_fila,n_col]
                hijo[1,n_fila,n_col]=poblacion[madre,n_fila,n_col]
            if n_col<cruce:
                hijo[2,n_fila,n_col]=poblacion[madre,n_fila,n_col]
            mejorsujeto[n_fila,n_col]=poblacion[madre,n_fila,n_col]
    
    #mutacion en el hijo
    for _ in range(2):
        for _ in range(randint(1,nReinas)):
            n_col=randint(0,nReinas-1)
            n_fila=randint(0,nReinas-1)
        if hijo[0,n_fila,n_col]==1:
            hijo[0,n_fila,n_col]=0
        else:
            hijo[0,n_fila,n_col]=1
    for n_fila in range(nReinas):
        for n_col in range(nReinas):
            poblacion[0,n_fila,n_col]=mejorsujeto[n_fila,n_col]
            poblacion[1,n_fila,n_col]=hijo[0,n_fila,n_col]
            poblacion[2,n_fila,n_col]=hijo[1,n_fila,n_col]
            poblacion[3,n_fila,n_col]=hijo[2,n_fila,n_col]
  
    if tamanio_poblacion>=8:
        for aux in range(8,tamanio_poblacion):
             for n_fila in range(nReinas):
                for n_col in range(nReinas):
                    poblacion[aux,n_fila,n_col]=mejorsujeto[n_fila,n_col]

    if tamanio_poblacion>=8:
        for _ in range(randint(1,2)):
            for aux in range(8,tamanio_poblacion):
                for _ in range(randint(1,nReinas)):
                    n_col=randint(0,nReinas-1)
                    n_fila=randint(0,nReinas-1)
                if poblacion[aux,n_fila,n_col]==1:
                    poblacion[aux,n_fila,n_col]=0
                else:
                    poblacion[aux,n_fila,n_col]=1
    generacion+=1
close=False
while(close==False):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close = True
pygame.quit()