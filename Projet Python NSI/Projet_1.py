#Projet Python : Arborescence de fichier.
import subprocess
from tkinter import *
import json


with open("save.json") as file: #charge l'ancienne sauvegarde du tableau root.
    root = json.load(file)
chemin = ['root']
here = root[1]
historique = [root[1]] 

def ouvrir(nom): #permet d'ouvrir un fichier ou un dossier.
    global here
    nomTXT = nom+'.txt'
    for j in range(len(here)) : #cherche l'indice du nom passé en parametres de la fonction
        if type(here[j]) is list : 
            if here[j][0] == nom :
                index = j
        elif type(here[j]) is str and ((here[j] == nom) or (here[j] == nomTXT)): 
            index=j
            
    try :
        if type(here[index]) is list: 
            chemin.append(here[index][0]) 
            historique.append(here[index][1])
            here = here[index][1] #change notre emplacement actuel
        elif type(here[index]) is str : 
            subprocess.run('notepad.exe '+here[index]) #le fichier texte choisi est ouvert avec le bloc-note de windows.
    except UnboundLocalError :
        print("ce n'est ni un fichier texte ni un dossier ou le dossier/fichier ne s'appelle pas comme ça")
    afficher()
    

def retour(): #cette fonction permet de revenir au fichier précédent
    """
    utilistataion de la fonction
    """
    global here
    if len(historique) == 1 : #empeche l'utilisateur de reculer s'il se trouve dans le premier dossier
        print("vous ne pouvez pas reculer plus !")
    else :
        historique.pop()
        chemin.pop() 
        here = historique[-1] #change l'emplacement de l'utilisateur et l'emmene au dossier précédent
    afficher()
    

def c_fichier(nom): #permet de creer un fichier texte
    nomfichier = str(nom) + '.txt' 
    try:
        fichier = open(nomfichier,'x') #cree un fichier qui s'appelle nomfichier seulement si le nom de ce fichier n'existe pas encore
        fichier.close()
        here.append(nomfichier) 
        with open("save.json", "w") as file: #ecrase l'ancienne sauvegarde du tableau root
            json.dump(root, file) #cree une nouvelle sauvegarde du tableau root
    except FileExistsError : 
        print("ce nom de fichier est deja utilisé") #précise a l'utilisateur que le nom du fichier est deja utilisé
    afficher()
    
    
def suppr(nom): #permet de supprimer un fichier texte ou un dossier
    global here
    nomTXT = nom+'.txt'
    for j in range(len(here)) : #cherche l'indice du str passé en parametres de la fonction
        if type(here[j]) is list : 
            if here[j][0] == nom : 
                index = j
                break #evite une erreur IndexOutOFRange et optimisation du temps pris par cette fonction
        elif type(here[j]) is str and here[j] == nom or here[j] == nomTXT: 
            index=j
    try:
        here.pop(index) #supprime l'élément voulu
    except UnboundLocalError :
        print("Ce nom de fichier n'existe pas")
    with open("save.json", "w") as file:  
        json.dump(root, file) 
    afficher() 


def afficher(): #liste les dossiers/fichiers 
    for i in here: #pour chaque élément présent a l'emplacement actuel de l'utilisateur
        if type(i) is list : 
            print('Dossier : {}'.format(i[0])) #Affiche 'Dossier :' accompagné du nom du dossier
        elif type(i) is str : 
            print('Fichier : {}'.format(i)) #Affiche 'Fichier :' accompagné du nom du fichier
            
    
def recherche_dossier(nom): #recherche si un nom de dossierexiste deja à l'emplacement actuel de l'utilisateur
    existe=False 
    for i in here:
        if type(i) is list : #on cherche des noms de dossiers, on verifie donc seulement les listes
            if i[0] == nom: 
                existe = True 
    return existe #renvoie la valeur de existe

    
def c_dos(nom): #permet de creer un dossier
    existe = recherche_dossier(nom) 
    if not(existe) : #si le nom n'existe pas deja
        here.append([nom,[]]) #on crée un dossier s'appelant 'nom' et dont le contenu est vide
        with open("save.json", "w") as file:
            json.dump(root, file)  
        afficher() 
    else :
        print('un fichier est deja nommé comme ceci') #si le nom du fichier existe deja, cela prévient l'utilisateur
        

def formater_tous_les_dossiers(): #permet de supprimer la sauvegarde du tableau root et de la reinitialiser comme etant vide. Toutefois, les fichiers ne sont pas supprimés des dossiers de l'ordinateur.
    global root
    root=['root',[]] #reinitialise la valuer de root
    with open("save.json", "w") as file: 
        json.dump(root, file) #cree une nouvelle sauvegarde du tableau root qui a été reinitialiséNo
        

def cmd(): #permet d'afficher les commandes disponibles
    fen = Tk() 
    fen.title('Python') 
    fen.geometry("550x180") 
    frame = LabelFrame(fen, text="Commandes Disponibles") 
    frame.pack() 
    l_ouvrir = Label(frame, text='- ouvrir("nom") : ouvre le tableau ou le fichier texte s\'appellant "nom" /!\ pensez a mettre les guillemets') 
    l_retour = Label(frame, text='- retour() : revient dans le dossier précédent')
    l_c_fichier = Label(frame, text='- c_fichier("nom") : creer un fichier texte nom.txt, /!\ pensez a mettre les guillemets') 
    l_c_dos = Label(frame, text='- c_dos("nom") : creer un dossier portant le nom "nom", /!\ pensez a mettre les guillemets') 
    l_afficher = Label(frame, text="- afficher() : affiche le contenu du dossier ou l'on se trouve actuellement") 
    l_del = Label(frame, text="- suppr('nom') : supprime le fichier s'appelant 'nom' /!\ pensez a mettre les guillemets") 
    l_cmd = Label(frame, text="- cmd() : réaffiche ce message") 
    l_ouvrir.pack(anchor=W, padx=5)
    l_retour.pack(anchor=W, padx=5)
    l_c_fichier.pack(anchor=W, padx=5)
    l_c_dos.pack(anchor=W, padx=5)
    l_afficher.pack(anchor=W, padx=5)
    l_del.pack(anchor=W, padx=5)
    l_cmd.pack(anchor=W, padx=5)

cmd() #lance la fonction cmd() au démarrage
afficher() #lance la fonction afficher() au démarrage
