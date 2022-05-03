#AC del modelo de Incendio forestal
#Modelo de Drossel y Schwabl(1992).
#Basado en el código de Christian Hill en https://scipython.com/blog/the-forest-fire-model/
'''Las funciones inicialize y update, así como las gráficas
 fueron agregadas por Octavio Rodríguez Vega'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors
from operator import itemgetter

'''Vecindad de Von Neumann '''
neighbourhood = ((0, 1),(0,-1),(-1,0), (1,0))
'''Los estados para las celdas en la retícula, vacío,
árbol y fuego'''
EMPTY, TREE, FIRE = 0, 1, 2 
'''usamos un color para cada celda, observe que hay que agregar uno más a la lista
con la intención de que el mapa de colores reconozca los tres que deseamos'''
colors_list = [(0.2,0,0), "lawngreen", "gray","darkorange" ]
cmap = colors.ListedColormap(colors_list)
bounds = [0,1,2,3]
norm = colors.BoundaryNorm(bounds, cmap.N)
'''se especifican la densidad inicial de árboles, density,
así como p, la probabilidad de que surja un árbol en una celda vacía y
f la probabilidad de que un árbol se incendie por causas naturales'''
density = 0.2
p, f = 0.05, 0.0001
'''las lista universeList contiene los estados de cada una de las celdas de la retícula, 
es un arreglo de 102 por 102, en donde la orilla no juega un papel en la dinámica.
La lista RES es el registro, en cada iteración(currentTimeStep), de árboles vivos y quemados, 
que se cuentan con la variable oneCount y twoCount, respectivamente '''
universeList,RES = [],[]
oneCount = 0
twoCount = 0
'''cellCountX y cellCountY son las dimensiones de la retícula'''
cellCountX, cellCountY = 102, 102
'''Inicialización de la retícula'''
def initialize():
	global currentTimeStep, universeList, RES
	currentTimeStep=0
	'''Se llena de celdas vacías primero, luego planta árboles de manera aleatoria
	y por último, de acuerdo a la densidad, va a acomodar a los árboles vivos, observe que si
	la condición es verdadera, dicha celda será un árbol vivo, de lo contrario un lugar vació'''
	universeList  = np.zeros((cellCountX, cellCountY))
	universeList[1:cellCountY-1, 1:cellCountX-1] = np.random.randint(0, 2, size=(cellCountY-2, cellCountX-2))
	universeList[1:cellCountY-1, 1:cellCountX-1] = np.random.random(size=(cellCountY-2, cellCountX-2)) < density
	'''se cuenta cuántos árboles vivos y quemados hay, 
	suponemos que en este paso la cantidad de árboles quemados es cero'''
	twoCount = np.count_nonzero(universeList==2)
	oneCount = np.count_nonzero(universeList==1)
	RES.append([currentTimeStep,oneCount,twoCount])

'''actualización de la retícula'''
def update(universeList):
	global X1, currentTimeStep, RES
	'''creamos una retícula espejo de la reticula universeList'''
	X1 = np.zeros((cellCountX, cellCountY))
	'''se incrementa el número de iteración'''
	currentTimeStep += 1
	'''recorrido de la retícula en donde se aplica la regla de evolución'''
	for ix in range (1,cellCountX-1):
		for iy in range (1,cellCountY-1):
			if universeList[iy,ix] == EMPTY and np.random.random() <= p:
				X1[iy,ix] = TREE
			elif universeList[iy,ix]==TREE:
				X1[iy,ix] = TREE
				for dx,dy in neighbourhood:
					if universeList[iy+dy,ix+dx] == FIRE:
						X1[iy,ix] = FIRE
						break
				else:
					if np.random.random() <= f:
						X1[iy,ix] = FIRE
	'''actualización del número de árboles vivos y quemados, 
	se ha comentado la impresión del número de iteraciones, podría servir como referencia'''					
	twoCount = np.count_nonzero(X1==2)
	oneCount = np.count_nonzero(X1==1)
	RES.append([currentTimeStep,oneCount,twoCount])
	#print(currentTimeStep)
	return X1


# la funcion de animación produce una instantánea de la retícula por unidad de tiempo
def animate(i):
    im.set_data(animate.universeList)
    animate.universeList = update(animate.universeList)

'''se llama a la función de inicialización de la retícula'''
initialize()
'''se crea la imagen de la retícula'''
fig = plt.figure(figsize=(25/3, 6.25))
ax = fig.add_subplot(111)
ax.set_axis_off()
im = ax.imshow(universeList, cmap=cmap, norm=norm)#, interpolation='nearest')
'''a la función de animación se le manda la retícula universeList'''
animate.universeList = universeList
interval = 100
anim = animation.FuncAnimation(fig, animate, interval=interval, frames=200)
plt.show()
'''se crean las gráficas del fenóḿeno'''
plt.plot(list(map(itemgetter(0),RES)),list(map(itemgetter(1),RES)),'-g', label='Vivos') 
plt.plot(list(map(itemgetter(0),RES)),list(map(itemgetter(2),RES)),'orange', label='En llamas')
plt.xlabel('Tiempo')
plt.ylabel('Árboles')
plt.legend(loc=0)
plt.title('AC del modelo de Incendio forestal estocástico')
plt.grid(True, linestyle='--', linewidth=0.4)
plt.xticks(np.arange(0, 400, step=50))
plt.xlim((0, 400))
plt.show()

