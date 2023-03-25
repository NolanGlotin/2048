import tkinter
from PIL import Image, ImageTk
import numpy as np
import random as rd

# Ajout d'un bloc au hasard
def NewBlock() :
    # On détermine tous les emplacements vides disponibles
    Pos = []
    for x in range(dim[0]):
        for y in range(dim[1]):
            pos = (x,y)
            if M[x][y]==0:
                Pos.append(pos)
    if len(Pos)==0:
        return False # Plus d'emplacement vide
    pos = Pos[rd.randint(0,len(Pos)-1)]
    if rd.randint(0,4)==0:
        block = 2 # Un bloc avec la valeur 4 peut apparaître avec une probabilité de une chance sur 5
    else:
        block = 1 # La majorité du temps le bloc apparaît avec la valeur 2
    M[pos[0]][pos[1]] = block

# Affichage du jeu
def Refresh() :
    win = False
    loose = True
    for i in Images:
        canvas.delete(i) # Suppression de tous les bloc
    for x in range(dim[0]) :
        for y in range(dim[1]) :
            if M[x][y]!=0:
                Images.append(canvas.create_image(x*size+5,y*size+5,image=Blocks[M[x][y]-1],anchor='nw')) # Affichage du bloc
            if M[x][y]==11:
                win = True # Le joueur a formé le nombre 2048 -> victoire !
            elif M[x][y]==0:
                loose = False # Au moins une des cases est vide -> pas de défaite
    tk.update()
    if win:
        Win()
    elif loose:
        Loose()

# Gestion de la victoire
def Win():
    global game
    game = False # Arrêt du jeu
    canvas.create_rectangle(100,250,300,150,fill='white',width=5)
    canvas.create_text(200,200,text='Bravo !',font=('Helevetica','30','bold'))
    tk.update()

# Gestion de la défaite
def Loose():
    global game
    game = False
    canvas.create_rectangle(100,250,300,150,fill='white',width=5)
    canvas.create_text(200,200,text='Perdu...',font=('Helevetica','30','bold'))
    tk.update()


# Gestion des mouvements :

# Mouvement vers le haut
def Up(event):
    if game:
        for x in range (dim[0]):
            for y in range (dim[1]):
                v = 1
                while y-v>=0 and M[x][y-v]==0:
                    M[x][y-v] = M[x][y-v+1]
                    M[x][y-v+1] = 0
                    v += 1
                if y-v>=0 and M[x][y-v]==M[x][y-v+1]:
                    M[x][y-v] += 1
                    M[x][y-v+1] = 0
        NewBlock()
        Refresh()

# Mouvement vers le bas
def Down(event):
    if game:
        for x in range (dim[0]):
            for y in range (dim[1],-1,-1):
                v = -1
                while y-v<dim[1] and M[x][y-v]==0:
                    M[x][y-v] = M[x][y-v-1]
                    M[x][y-v-1] = 0
                    v -= 1
                if y-v<dim[1] and M[x][y-v]==M[x][y-v-1]:
                    M[x][y-v] += 1
                    M[x][y-v-1] = 0
        NewBlock()
        Refresh()

# Mouvement vers la droite
def Right(event):
    if game:
        for y in range (dim[1]):
            for x in range (dim[0],-1,-1):
                v = -1
                while x-v<dim[0] and M[x-v][y]==0:
                    M[x-v][y] = M[x-v-1][y]
                    M[x-v-1][y] = 0
                    v -= 1
                if x-v<dim[0] and M[x-v][y]==M[x-v-1][y]:
                    M[x-v][y] += 1
                    M[x-v-1][y] = 0
        NewBlock()
        Refresh()

# Mouvement vers la gauche
def Left(event):
    if game:
        for y in range (dim[1]):
            for x in range (dim[0]):
                v = 1
                while x-v>=0 and M[x-v][y]==0:
                    M[x-v][y] = M[x-v+1][y]
                    M[x-v+1][y] = 0
                    v += 1
                if x-v>=0 and M[x-v][y]==M[x-v+1][y]:
                    M[x-v][y] += 1
                    M[x-v+1][y] = 0
        NewBlock()
        Refresh()


# Code principal

# Paramètres
dim = (4,4) # Dimension de la grille (en cellules)
size = 100 # Dimension d'une cellule

# Création de la fenêtre graphique
tk = tkinter.Tk()
canvas = tkinter.Canvas(tk,width=dim[0]*size,height=dim[1]*size,bg='white')
tk.title('2048')
for x in range(dim[0]):
    for y in range (dim[1]):
        canvas.create_rectangle(x*size+5,y*size+5,(x+1)*size-5,(y+1)*size-5,fill='grey',width=0)
canvas.pack()
tk.update()

# Création des images
Blocks = [ImageTk.PhotoImage(Image.open('Assets/'+str(2**i)+'.png').resize((size-10,size-10))) for i in range (1,12)]
Images = []

# Création du tableau
M = np.zeros(dim,dtype=int)

# Association des touches aux actions
canvas.bind_all('<Up>',Up)
canvas.bind_all('<Down>',Down)
canvas.bind_all('<Right>',Right)
canvas.bind_all('<Left>',Left)

# Lancement du jeu
NewBlock()
Refresh()
game = True

# Boucle principale
canvas.mainloop()