# ═════════════════════════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════         Introduction          ═══════════════════════════════
# ═════════════════════════════════════════════════════════════════════════════════════════════
"""
INSA Hauts-de-France - Spécialité Informatique et Cybersécurité 
2025/2026 - Projet de Fondements de l'IA
Thomas Manche & Lavoisier Léandre
Jeu d'Othello : Implémentation du jeu et de différentes IA pour y jouer
"""

# ═════════════════════════════════════════════════════════════════════════════════════════════
# ═════════════════════════════  Conception des règles d'Othello  ═════════════════════════════
# ═════════════════════════════════════════════════════════════════════════════════════════════
# Import nécessaires pour le projet :
import numpy
import time
import copy
import random as rand
import threading

# plat représente le plateau d'Othello, matrice de 8x8 rempli de String.
plat = numpy.zeros((8,8),str)
# PionBlanc représente la valeur utilisée pour les pions blanc. Il peut être remplacé par "⚪" pour un aspect visuel plus fort ;)
PionBlanc = "B"
# PionNoir représente la valeur utilisée pour les pions noirs. Il peut être remplacé par "⚫" pour un aspect visuel plus fort ;)
PionNoir = "N"
# TourActuel représente le joueur qui doit jouer son coup. Il est initialisé au joueur de départ, soit PionNoir.
TourActuel=PionNoir

def InitialisePlateau():
    "Initialise le plateau d'Othello avec les 4 pions centrales de départ, et met les cases vides à ' ' pour une meilleure expérience visuelle."
    global plat
    plat=numpy.zeros((8,8),str)
    plat[3][3]=PionBlanc
    plat[4][4]=PionBlanc
    plat[3][4]=PionNoir
    plat[4][3]=PionNoir
    for i in range(0,8):
        for j in range(0,8):
            if plat[i][j]=='':
                plat[i][j]=' '

def checkCoup(x,y,incrementX, incrementY,plateau, joueur=None):
        """
        Regarde, à partir de la position (x,y), si le coup donné dans la direction (+incrementX, +incrementY) est jouable pour le joueur sur le plateau est autorisé.
        On regarde les cases dans la direction tant qu'elle n'est pas vide, n'est pas en dehors des limites et contient un pion adverse.
        Si au bout d'un moment, on trouve un pion allié, alors le coup est autorisé et on renvoie True. Sinon on renvoie False.
        """
        if joueur is None:
            joueur = TourActuel
        if plateau[x+incrementX][y+incrementY]==(PionNoir if joueur==PionBlanc else PionBlanc):
            if x+(incrementX*2)>-1 and x+(incrementX*2)<8 and y+(incrementY*2)<8 and y+(incrementY*2)>-1:
                if plateau[x+(incrementX*2)][y+(incrementY*2)]==joueur:
                    return True  
                return checkCoup(x+incrementX,y+incrementY,incrementX,incrementY, plateau, joueur)  
        return False

def CoupAutorise(i,j, plateau, joueur=None):
    """ 
    Regarde si le coup joué en (i,j) par joueur sur le plateau est autorisé selon les règles de l'Othello.
    Pour chaque direction (Nord - Est - Ouest - Sud) ainsi que leur combinaisons, on regarde si le coup est jouable avec checkCoup.
    Si au moins un coup est jouable, alors la fonction renvoie True, sinon elle renvoie False.
    """
    if joueur is None:
        joueur = TourActuel
    # Si la case n'est pas vide, on ne peut pas jouer dessus, on renvoie False
    if plateau[i][j]!=' ':
        return False
    if (i>1):
        #Ouest
        if checkCoup(i,j,-1,0,plateau,joueur):
            return True
        if (j>1):
            # Sud Ouest
            if checkCoup(i,j,-1,-1,plateau,joueur):
                return True
        if (j<6):
            # Sud Est
            if checkCoup(i,j,-1,1,plateau,joueur):
                return True
    if (i<6):
        # Est
        if checkCoup(i,j,1,0,plateau,joueur):
            return True
        if (j>1):
            # Sud Est
            if checkCoup(i,j,1,-1,plateau,joueur):
                return True
        if (j<6):
            # Nord Est
            if checkCoup(i,j,1,1,plateau,joueur):
                return True
    if (j>1):
        # Sud
        if checkCoup(i,j,0,-1,plateau,joueur):
            return True
    if (j<6):
        # Nord
        if checkCoup(i,j,0,1,plateau,joueur):
            return True
    return False

def ChangeCouleurCase(i,j,plateau):
    "Change la couleur de la case (i,j) du plateau par la couleur opposée."
    if plateau[i][j]==PionBlanc:
        plateau[i][j]=PionNoir
    elif plateau[i][j]==PionNoir:
        plateau[i][j]=PionBlanc

def ChangeCaseCoupAutorise(x,y,incrementX,incrementY,plateau, joueur=None):
    """ 
    A utiliser lorsque le coup est autorisé par la fonction coupAutorise.
    A partir de la position (x,y), on va continuer dans la direction (+incrementX, +incrementY) tant que l'on trouve des pions adverses.
    Lorsque l'on trouve un pion allié, on s'arrête.
    """
    if joueur is None:
        joueur = TourActuel
    case=plateau[x+incrementX][y+incrementY]
    while case!=TourActuel:
        ChangeCouleurCase(x+incrementX,y+incrementY,plateau)
        x=x+incrementX
        y=y+incrementY
        case=plateau[x+incrementX][y+incrementY]

def getAllPossibleHit(plateau,joueur):
    """
    Fonction qui renvoie un tableau contenant tout les coups possibles pour le joueur sur le plateau.
    """
    PossibleHit=[]
    for i in range(0,8):
        for j in range(0,8):
            if CoupAutorise(i,j,plateau,joueur):
                PossibleHit.append([i,j])
    return PossibleHit

def ChangeTour():
    "Permet de changer de tour automatiquement"
    global TourActuel
    TourActuel=PionNoir if TourActuel==PionBlanc else PionBlanc

def PosePion(i,j,plateau, joueur=None):
    """
    Fonction utilisée pour poser un pion sur le plateau.
    Elle va poser le pion du joueur sur la case (i,j).
    Pour chaque direction, elle va regarder ensuite si le coup est autorisé. 
    Si oui, alors elle retourne les cases dans la direction.
    """
    if joueur is None:
        joueur = TourActuel
    plateau[i][j]=joueur
    if (i>1):
        # Ouest
        if checkCoup(i,j,-1,0,plateau,joueur):
            ChangeCaseCoupAutorise(i,j,-1,0,plateau,joueur)
        if (j>1):
            # Sud Ouest
            if checkCoup(i,j,-1,-1,plateau,joueur):
                ChangeCaseCoupAutorise(i,j,-1,-1,plateau,joueur)
        if (j<6):
            #Nord Ouest
            if checkCoup(i,j,-1,1,plateau,joueur):
                ChangeCaseCoupAutorise(i,j,-1,1,plateau,joueur)
    if (i<6):
        # Est
        if checkCoup(i,j,1,0,plateau,joueur):
            ChangeCaseCoupAutorise(i,j,1,0,plateau,joueur)
        if (j>1):
            #Sud Est
            if checkCoup(i,j,1,-1,plateau,joueur):
                ChangeCaseCoupAutorise(i,j,1,-1,plateau,joueur)
        if (j<6):
            #Nord Est
            if checkCoup(i,j,1,1,plateau,joueur):
                ChangeCaseCoupAutorise(i,j,1,1,plateau,joueur)
    if (j>1):
        # Sud
        if checkCoup(i,j,0,-1,plateau,joueur):
                ChangeCaseCoupAutorise(i,j,0,-1,plateau,joueur)
    if (j<6):
        # Nord
        if checkCoup(i,j,0,1,plateau,joueur):
            ChangeCaseCoupAutorise(i,j,0,1,plateau,joueur)

def isFinished(plateau, simulation=False):
    """
    Vérifie si la partie est terminée.
    Il va vérifier qu'au moins un joueur peut jouer un coup, que le plateau n'est pas rempli ou que les deux joueurs ont des deux pions.
    Si l'un des deux joueurs ne peut pas jouer, la fonction gère le changement de tour si l'adversaire peut jouer.
    """
    #Représente le remplissage du tableau
    condRemplissage=True
    #Représente la possibilité de jouer un coup pour au moins un des deux joueurs
    condCoupPossible=False
    for i in range(0,len(plateau)):
        for j in range(0,len(plateau[0])):
            if plateau[i][j]==' ':
                condRemplissage=False
                if CoupAutorise(i,j,plateau):
                    condCoupPossible=True
                    return False
    if condCoupPossible==False and condRemplissage==False:
        # Si le joueur actuel ne peut pas jouer mais le plateau n'est pas rempli, on regarde pour l'adversaire
        for i in range(0,len(plateau)):
            for j in range(0,len(plateau[0])):
                if CoupAutorise(i,j,plateau,PionBlanc if TourActuel==PionNoir else PionNoir) and simulation==False:
                    #print("Le joueur "+TourActuel+ " ne peut pas jouer, on repasse directement au joueur "+PionBlanc if TourActuel==PionNoir else PionNoir)
                    ChangeTour()
                    return False
    # Si une des conditions de victoire (Remplissage du plateau - Aucun coup possible - Aucun pion d'un des deux joueurs), alors on retourne True
    if condRemplissage==True or condCoupPossible==False or nombrePion(PionNoir, plat)==0 or nombrePion(PionBlanc,plat)==0:
        return True
    return False

# ═════════════════════════════════════════════════════════════════════════════════════════════
# ═════════════════════════════   Simulation de partie d'Othello  ═════════════════════════════
# ═════════════════════════════════════════════════════════════════════════════════════════════

" Variables de statistiques "
# Nombre de coup total joué dans la partie actuelle
pt=0
# Nombre de coups par couleur
BlackMoves=0
WhiteMoves=0

# Temps usé par couleur
BlackTimeUsed=0
WhitetimeUsed=0
# Nombre de noeuds total généré par IA
WhiteNumberOfNodes=0
BlackNumberOfNodes=0
# Nombre de noeuds par profondeur
BlackNodesPerDepth=[]
WhiteNodesPerDepth=[]
# Temps utilisé pour Montecarlo
tempsMontecarlo=0.5

" Variables de verboses "
# Variable représentant les tours
VerboseTourActuel=[PionNoir,PionBlanc]
# Variable représentant les IA disponibles
VerboseIA=["MinMaxV1MeilleurCoup","MinMaxMaximise","AlphaBeta","Montecarlo","Random","BetterMontecarlo"]
# Variable représentant les fonctions de score disponibles
VerboseScore=["Nombre de pions relatifs", "Poids des cases","scoreMobilite", "Mixte"]
# Variable représentant, pour BetterMontecarlo, les modes de preprocessing disponibles
VerbosePreProcessor=["FSP(Meilleurs coups fixes, NS=4)", "VSP(Coup au dessus seuil, PS=0.7)"]

"""
Conventions utilisés pour les statistiques écrites : 
i & j : IA utilisé pour respectivement les blancs et les noirs
k & l : Fonction de score utilisé pour respectivement les blancs et les noirs
m & n : Profondeur utilisée pour respectivement les blancs et les noirs (pour MinMaxMaximise et AlphaBeta) ou mode de preprocessing utilisé pour respectivement les blancs et les noirs (pour BetterMontecarlo)
"""

def writeStat(i,j,k,l,m,n):
    """
    Fonction utilisée pour écrire les paramètres de la partie dans le fichier resultat.txt.
    Elle va inscrire les IA utilisés, les fonctions de scores, et les paramètres importants de chaque IA.
    """
    with open('resultat.txt','a') as f:
        f.write("-----------------------\n")
        f.write(VerboseIA[i] + " (B) VS (N) "+ VerboseIA[j]+"\n")
        f.write(VerboseScore[k-1] + "(B) VS (N) "+ VerboseScore[l-1]+"\n")
        if VerboseIA[i]=="Montecarlo" or VerboseIA[i]=="BetterMontecarlo" or VerboseIA[j]=="BetterMontecarlo" or VerboseIA[j]=="Montecarlo":
            f.write("Temps pour Montecarlo : "+str(tempsMontecarlo) + "\n")
        if VerboseIA[i]=="BetterMontecarlo":
            f.write("Preprocessor Blanc :"+ VerbosePreProcessor[m-1] +"\n")
        if VerboseIA[j]=="BetterMontecarlo":
            f.write("Preprocessor Noir :"+ VerbosePreProcessor[n-1] + "\n")
        if VerboseIA[i]=="MinMaxMaximise" or VerboseIA[i]=="AlphaBeta":
            f.write("Profondeur Blanc (2 demi-coups) : "+ str(m)+ "\n")
        if VerboseIA[j]=="MinMaxMaximise" or VerboseIA[j]=="AlphaBeta":
            f.write("Profondeur Noir (2 demi-coups) : "+ str(n)+"\n")
        f.write(TourActuel + " commence.\n")

def writeStatisticTimeandNodes(i,j):
    """
    Fonction utilisée pour écrire les statistiques de la partie dans le fichier resultat.txt
    Elle va inscrire le temps moyen par coup, le nombre de noeuds total généré, le nombre de noeuds par coup & par profondeur pour chaque IA.
    """
    with open('resultat.txt','a',encoding='utf-8') as f:
        f.write("Temps moyen Noir :"+str(BlackTimeUsed/BlackMoves) + " sec\n")
        f.write("BlackNumberOfNodes:"+str(BlackNumberOfNodes)+"\n")
        f.write("BlackNumberOfNodesPerTurn:"+str(BlackNumberOfNodes/BlackMoves)+"\n")
        if j==1 or j==2:
            f.write("BlackNodesPerDepth:"+"\n")
            for i in range(0,len(BlackNodesPerDepth)):
                f.write("Profondeur "+str(i)+":"+str(BlackNodesPerDepth[i]/BlackMoves) + "("+str(BlackNodesPerDepth[i])+" Total)"+"\n")
        f.write("Temps moyen Blanc :"+str(WhitetimeUsed/WhiteMoves) + " sec\n")
        f.write("WhiteNumberOfNodes:"+str(WhiteNumberOfNodes)+"\n")
        f.write("WhiteNumberOfNodesPerTurn:"+str(WhiteNumberOfNodes/WhiteMoves)+"\n")
        if i==1 or i==2:
            f.write("WhiteNodesPerDepth:"+"\n")
            for i in range(0,len(WhiteNodesPerDepth)):
                f.write("Profondeur "+str(i+1)+":"+str(WhiteNodesPerDepth[i]/WhiteMoves) + "("+str(WhiteNodesPerDepth[i])+")"+"\n")

def getResultat():
    """
    Fonction qui va tester tous les cas d'affrontement entre les différentes IA, fonctions de scores et paramètres importants.
    Elle va faire jouer les IA entre elles, et à la fin de chaque partie, elle va écrire les statistiques de la partie dans le fichier resultat.txt.
    """
    global pt, WhiteNumberOfNodes, WhiteNodesPerDepth, WhitetimeUsed, WhiteMoves, BlackMoves, BlackNumberOfNodes, BlackNodesPerDepth, BlackTimeUsed
    RecursiviteMax=3
    with open('resultat.txt','w') as f:
        f.write("Jeu d'Othello - Résultats \n")
    global TourActuel
    # t représente qui commence. 
    for t in range(0,4):
        # IA Blanc
        for i in range(0,6):
            #IA Noir
            #Normalement entre 0 - 6 ;)
            for j in range(0,6):
                #Score Blanc
                for k in range(1,5):
                    #Score Noir
                    for l in range(1,5):
                        #Profondeur pour Blanc ou paramètre de preprocessing pour BetterMontecarlo pour Blanc
                        for m in range(1,RecursiviteMax+1):
                            # Si on est pas dans AlphaBeta, MinMax ou Montecarlo, on break.
                            if m==2 and (i!=1 and i!=2 and i!=5):
                                break
                            #AlphaBeta a le droit a une profondeur de 3, seul lui.
                            if m==3 and i!=2:
                                break
                            #Profondeur pour Noir ou paramètre de preprocessing pour BetterMontecarlo pour Noir
                            for n in range(1,RecursiviteMax+1):
                                # Si on est pas dans AlphaBeta, MinMax ou Montecarlo, on break.
                                if n==2 and (j!=1 and j!=2 and j!=5):
                                    break
                                #AlphaBeta a le droit a une profondeur de 3, seul lui.
                                if n==3 and j!=2:
                                    break
                                InitialisePlateau()
                                pt=0
                                if t==0 or t==2:
                                    TourActuel=PionNoir
                                else:
                                    TourActuel=PionBlanc
                                writeStat(i,j,k,l,m,n)
                                WhiteNumberOfNodes=0
                                WhiteNodesPerDepth=[0]*m
                                WhitetimeUsed=0
                                WhiteMoves=0
                                BlackMoves=0
                                BlackNumberOfNodes=0
                                BlackNodesPerDepth=[0]*n
                                BlackTimeUsed=0
                                while True:
                                    if TourActuel==PionBlanc:
                                        timeStart=time.time()
                                        WhiteMoves+=1
                                        if i==0:
                                            (x,y)=MinMaxV1meilleurCoup(TourActuel,plat,k)
                                        elif i==1:
                                            (x,y),_=MinMaxMaximise(TourActuel,plat,m,k)
                                        elif i==2:
                                            (x,y),_=AlphaBetaMax(TourActuel,plat,m,float("-inf"),float("inf"),k)
                                        elif i==3:
                                            (x,y)=MonteCarloMain(TourActuel,plat,tempsMontecarlo)
                                        elif i==4:
                                            (x,y)=randomPlay(plat,TourActuel)
                                        elif i==5:
                                            (x,y)=BetterMonteCarloMain(TourActuel,plat,tempsMontecarlo,k,m,4,0.7)
                                        timeStop=time.time()
                                        WhitetimeUsed+=timeStop-timeStart
                                    else:
                                        timeStart=time.time()
                                        BlackMoves+=1
                                        if j==0:
                                            (x,y)=MinMaxV1meilleurCoup(TourActuel,plat,l)
                                        elif j==1:
                                            (x,y),_=MinMaxMaximise(TourActuel,plat,n,l)      
                                        elif j==2:
                                            (x,y),_=AlphaBetaMax(TourActuel,plat,n,float("-inf"),float("inf"),l)
                                        elif j==3:
                                            (x,y)=MonteCarloMain(TourActuel,plat,tempsMontecarlo)
                                        elif j==4:
                                            (x,y)=randomPlay(plat,TourActuel)
                                        elif j==5:
                                            (x,y)=BetterMonteCarloMain(TourActuel,plat,tempsMontecarlo,l,n,4,0.7)
                                        timeStop=time.time()
                                        BlackTimeUsed+=timeStop-timeStart
                                    if CoupAutorise(x,y,plat):
                                        pt+=1
                                        PosePion(x,y,plat)
                                        ChangeTour()
                                        if isFinished(plat):
                                            writeStatisticTimeandNodes(i,j)
                                            with open('resultat.txt','a') as f:
                                                f.write("Coup joué :"+str(pt)+ "\n")
                                                f.write("Score du joueur B : "+str(nombrePion(PionBlanc,plat))+"\n")
                                                f.write("Score du joueur N : " + str(nombrePion(PionNoir,plat))+"\n")
                                            break    

# ═════════════════════════════════════════════════════════════════════════════════════════════
# ══════════════════════════  Jouer & Afficher une partie d'Othello  ══════════════════════════
# ═════════════════════════════════════════════════════════════════════════════════════════════

"Variables des choix de la personne"
# IA Voulu pour le blanc & le noir
IAVouluBlanc=1
IAVouluNoir=1
# Fonction de score voulu pour le blanc & le noir
ScoreVouluNoir=1
ScoreVouluBlanc=1
# Profondeur voulu pour le blanc & le noir
profondeurBlanc=1
profondeurNoir=1
# Temps Montecarlo voulu pour le blanc & le noir
tempsMontecarloBlanc=0.5
tempsMontecarloNoir=0.5

def affichagePlat(plat):
    """
    Fonction qui va afficher le plateau de manière plus visuelle.
    Affiche notamment les coordonnées, et installe une grille.
    """
    plateau=numpy.zeros((9,9),str)
    for i in range(9):
        for j in range(9):
            if i==0 and j!=0:
                plateau[i][j]=j-1
            elif j==0 and i!=0:
                plateau[i][j]=i-1
            elif i==0 and j==0:
                plateau[i][j]=' '
                continue
            else:
                plateau[i][j]=plat[i-1][j-1]
            if plateau[i][j]=='':
                plateau[i][j]==' '
    for i in range(9):
        string= "| " 
        for j in range(9):
            string+=plateau[i][j] + " | "
        print(string)
        print("-------------------------------------")

def afficheInfoIA(Couleur):
    """
    Fonction qui affiche les paramètres de l'IA choisie pour la partie.
    """
    print("-----")
    print("Pour l'IA "+ Couleur+" :")
    print("| Modèle "+ VerboseIA[(IAVouluBlanc-1 if Couleur==PionBlanc else IAVouluNoir-1)])
    if (IAVouluBlanc if Couleur==PionBlanc else IAVouluNoir)==2 or (IAVouluBlanc if Couleur==PionBlanc else IAVouluNoir)==3:
        print("| Profondeur : " + str((profondeurBlanc if Couleur==PionBlanc else profondeurNoir)))
    if ((IAVouluBlanc if Couleur==PionBlanc else IAVouluNoir))!=4 and (IAVouluBlanc if Couleur==PionBlanc else IAVouluNoir)!=5:
        print("| Fonction de score utilisée : "+VerboseScore[(ScoreVouluBlanc-1 if Couleur==PionBlanc else ScoreVouluNoir-1)])
    if (IAVouluBlanc if Couleur==PionBlanc else IAVouluNoir)==4:
        print("| Temps de Montecarlo : "+ str((tempsMontecarloBlanc if Couleur==PionBlanc else tempsMontecarloNoir)))

def demandeInfo(Couleur):
    """
    Fonction lancé si le joueur choisit de faire jouer une IA pour la couleur donnée.
    Elle permet de choisir :
    - Le type d'IA
    - La fonction de score
    - Les paramètres importants
    Le tout entièrement visuel"""
    global IAVouluBlanc, ScoreVouluBlanc, profondeurBlanc, tempsMontecarloBlanc, IAVouluNoir, ScoreVouluNoir, profondeurNoir, tempsMontecarloNoir
    print("-------------------------------------")
    print("Configuration pour " + Couleur)
    while True:
            print("Quel IA voulu pour les blancs ?")
            print("| 1: MinMaxV1MeilleurCoup : cherche le pire score pour vous ! ")
            print("| 2: MinMax : Cherche son meilleure score en minimisant le votre !")
            print("| 3: AlphaBeta : MinMax optimisé !")
            print("| 4: Montecarlo : Ces simulations vont vous détruire !")
            print("| 5: Random : Il ne réfléchit pas... Littéralement !")
            print("| 6: BetterMontecarlo : Simulation avec Preprocessin, et score... Ca pique !")
            if Couleur==PionBlanc:
                IAVouluBlanc=int(input("Votre choix :"))
                choix=IAVouluBlanc
            else:
                IAVouluNoir=int(input("Votre choix :"))
                choix=IAVouluNoir
            match choix:
                case 1:
                    while True:
                        print("Quel score voulez-vous ?")
                        print("|1: Score absolue : L'IA cherche à avoir plus de pions que vous")
                        print("|2: Score relatif : L'IA s'aide d'un tableau de poids")
                        print("|3: Score mobilité : L'IA cherche à limiter vos coups tout en augmentant ses possibilités")
                        print("|4: Score mixte : L'IA allie ses stratégies")
                        if Couleur==PionBlanc:
                            ScoreVouluBlanc=int(input("Votre choix :"))
                            if ScoreVouluBlanc >= 1 and ScoreVouluBlanc <= 4 : 
                                break
                        else:
                            ScoreVouluNoir=int(input("Votre choix :"))
                            if ScoreVouluNoir >= 1 and ScoreVouluNoir <= 4 : 
                                break
                    return
                case 2:
                    while True:
                        print("Quel score voulez-vous ?")
                        print("|1: Score absolue : L'IA cherche à avoir plus de pions que vous")
                        print("|2: Score relatif : L'IA s'aide d'un tableau de poids")
                        print("|3: Score mobilité : L'IA cherche à limiter vos coups tout en augmentant ses possibilités")
                        print("|4: Score mixte : L'IA allie ses stratégies")
                        if Couleur==PionBlanc:
                            ScoreVouluBlanc=int(input("Votre choix :"))
                            if ScoreVouluBlanc >= 1 and ScoreVouluBlanc <= 4 : 
                                break
                        else:
                            ScoreVouluNoir=int(input("Votre choix :"))
                            if ScoreVouluNoir >= 1 and ScoreVouluNoir <= 4 : 
                                break
                    print("Quel profondeur voulez-vous ? Chaque profondeur joue 2 demi-coups (1 coup allié, 1 coup adverse). Attention, pour MinMax, on conseille un max de 2 !")
                    if Couleur==PionBlanc:
                        profondeurBlanc=int(input("Votre choix :"))
                    else:
                        profondeurNoir=int(input("Votre choix :"))
                    return
                case 3:
                    while True:
                        print("Quel score voulez-vous ?")
                        print("|1: Score absolue : L'IA cherche à avoir plus de pions que vous")
                        print("|2: Score relatif : L'IA s'aide d'un tableau de poids")
                        print("|3: Score mobilité : L'IA cherche à limiter vos coups tout en augmentant ses possibilités")
                        print("|4: Score mixte : L'IA allie ses stratégies")
                        if Couleur==PionBlanc:
                            ScoreVouluBlanc=int(input("Votre choix :"))
                            if ScoreVouluBlanc >= 1 and ScoreVouluBlanc <= 4 : 
                                break
                        else:
                            ScoreVouluNoir=int(input("Votre choix :"))
                            if ScoreVouluNoir >= 1 and ScoreVouluNoir <= 4 : 
                                break
                    print("Quel profondeur voulez-vous ? Chaque profondeur joue 2 demi-coups (1 coup allié, 1 coup adverse).")
                    if Couleur==PionBlanc:
                        profondeurBlanc=int(input("Votre choix :"))
                    else:
                        profondeurNoir=int(input("Votre choix :"))
                    return
                case 4:
                    print("Quel temps voulez-vous pour le Montecarlo ? On conseille 0.5 ou 1. Merci de mettre un . et pas une virgule ! ")
                    if Couleur==PionBlanc:
                        tempsMontecarloBlanc=float(input("Votre choix:"))
                    else:
                        tempsMontecarloNoir=float(input("Votre choix : "))
                    return
                case 5:
                    return
                case 6:
                    while True:
                        print("Quel score voulez-vous ?")
                        print("|1: Score absolue : L'IA cherche à avoir plus de pions que vous")
                        print("|2: Score relatif : L'IA s'aide d'un tableau de poids")
                        print("|3: Score mobilité : L'IA cherche à limiter vos coups tout en augmentant ses possibilités")
                        print("|4: Score mixte : L'IA allie ses stratégies")
                        if Couleur==PionBlanc:
                            ScoreVouluBlanc=int(input("Votre choix :"))
                            if ScoreVouluBlanc >= 1 and ScoreVouluBlanc <= 4 : 
                                break
                        else:
                            ScoreVouluNoir=int(input("Votre choix :"))
                            if ScoreVouluNoir >= 1 and ScoreVouluNoir <= 4 : 
                                break
                    print("Quel mode de Preprocessing voulez vous ? ")
                    print("| 1: FSP : Va regarder les 4 (=Ns) meilleurs coups à converser au début")
                    print("| 2: VSP : Va garder les 30% (=ps) meilleurs coups par rapport à la moyenne")
                    if Couleur==PionBlanc:
                        profondeurBlanc=int(input("Votre choix :"))
                    else:
                        profondeurNoir=int(input("Votre choix :"))
                    print("Quel temps voulez-vous pour le Montecarlo ? On conseille 0.5 ou 1. Merci de mettre un . et pas une virgule ! ")
                    if Couleur==PionBlanc:
                        tempsMontecarloBlanc=float(input("Votre choix:"))
                    else:
                        tempsMontecarloNoir=float(input("Votre choix : "))
                    return
                case default:
                    return

def PlayingOthello(Blanc,Noir):
    """
    Fonction qui simule une partie d'Othello entre deux joueurs, qui peuvent être soit humains, soit des IA.
    """
    global TourActuel, tempsMontecarlo, WhiteNodesPerDepth, WhiteNumberOfNodes, WhitetimeUsed, WhiteMoves, BlackNumberOfNodes, BlackNodesPerDepth, BlackTimeUsed, BlackMoves,pt
    WhiteNumberOfNodes=0
    WhiteNodesPerDepth=[0]*4
    WhitetimeUsed=0
    WhiteMoves=0
    BlackNumberOfNodes=0
    BlackNodesPerDepth=[0]*4
    BlackTimeUsed=0
    BlackMoves=0
    InitialisePlateau()
    numeroTour=0
    pt=0
    print("-------------------------------------")
    TourActuel=PionNoir
    while True:
        numeroTour+=1
        print("Tour n°"+str(numeroTour) + " : A "+TourActuel  + " de jouer !")
        affichagePlat(plat)
        if TourActuel==PionBlanc:
            if Blanc==0:
                x=int(input("Renseignez la coordonnée de x (Hauteur):"))
                y=int(input("Renseignez la coordonnée de y (Largeur):"))
            elif Blanc==1:
                if IAVouluBlanc==1:
                    (x,y)=MinMaxV1meilleurCoup(TourActuel,plat,ScoreVouluBlanc)
                elif IAVouluBlanc==2:
                    (x,y),_=MinMaxMaximise(TourActuel,plat,profondeurBlanc,ScoreVouluBlanc)
                elif IAVouluBlanc==3:
                    (x,y),_=AlphaBetaMax(TourActuel,plat,profondeurBlanc,float("-inf"),float("inf"),ScoreVouluBlanc)
                elif IAVouluBlanc==4:
                    (x,y)=MonteCarloMain(TourActuel,plat,tempsMontecarloBlanc)
                elif IAVouluBlanc==5:
                    (x,y)=randomPlay(plat,TourActuel)
                elif IAVouluBlanc==6:
                    (x,y)=BetterMonteCarloMain(TourActuel,plat,tempsMontecarloBlanc,ScoreVouluBlanc,profondeurBlanc)
        else:
            if Noir==0:
                x=int(input("Renseignez la coordonnée de x (Hauteur):"))
                y=int(input("Renseignez la coordonnée de y (Largeur):"))
            elif Noir==1:
                if IAVouluNoir==1:
                    (x,y)=MinMaxV1meilleurCoup(TourActuel,plat,ScoreVouluNoir)
                elif IAVouluNoir==2:
                    (x,y),_=MinMaxMaximise(TourActuel,plat,profondeurNoir,ScoreVouluNoir)
                elif IAVouluNoir==3:
                    (x,y),_=AlphaBetaMax(TourActuel,plat,profondeurNoir,float("-inf"),float("inf"),ScoreVouluNoir)
                elif IAVouluNoir==4:
                    (x,y)=MonteCarloMain(TourActuel,plat,tempsMontecarloNoir)
                elif IAVouluNoir==5:
                    (x,y)=randomPlay(plat,TourActuel)
                elif IAVouluNoir==6:
                    (x,y)=BetterMonteCarloMain(TourActuel,plat,tempsMontecarloNoir,ScoreVouluNoir,profondeurNoir)
        if CoupAutorise(x,y,plat):
            PosePion(x,y,plat)
            pt+=1
            ChangeTour()
            if isFinished(plat):
                print("Fin du jeu ! Baissez les armes !")
                print("-------------------------------------")
                affichagePlat(plat)
                if Blanc==0:
                    print("-----\n Pour le joueur B :")
                else:
                    afficheInfoIA(PionBlanc)
                print("-> Score (B) de "+str(nombrePion(PionBlanc,plat)))
                if Noir==0:
                    print("-----\n Pour le joueur N :")
                else:
                    afficheInfoIA(PionNoir)
                print("-> Score (N) de "+str(nombrePion(PionNoir,plat)))
                if (nombrePion(PionBlanc,plat)) > (nombrePion(PionNoir,plat)):
                    print(" \n Le joueur B a gagné ! Félicitations ! \n ")
                elif (nombrePion(PionBlanc,plat)) < (nombrePion(PionNoir,plat)):
                    print("\n Le joueur N a gagné ! Félicitations ! \n")
                else:
                    print("\n Match nul entre les joueurs ! Bien joué ! \n")
                return
        else:
            print("Le coup n'est pas autorisé suivant les règles de l'Othello !")

def OthelloGame():
    """
    Fonction qui lance le jeu d'Othello à l'affichage.
    """
    print("-------------------------------------")
    print("Un plateau de 8x8 😦 \n un jeu enflammé 😩 .... \n Bienvenue à l'Othello 😁 ! ")
    while True:
        print("-------------------------------------")
        print("Quel mode voulez-vous ?")
        print("| 1 : Humain (B) vs Humain (N)")
        print("| 2 : Humain (B) vs IA (N)")
        print("| 3 : IA (B) vs Humain (N)")
        print("| 4 : IA (B) vs IA (N)")
        print("| Tout autre valeur termine le programme.")
        valeur=int(input("Votre réponse : "))
        match valeur:
            case 1:
                PlayingOthello(0,0)
            case 2:
                demandeInfo(PionNoir)
                PlayingOthello(0,1)
            case 3:
                demandeInfo(PionBlanc)
                PlayingOthello(1,0)
            case 4:
                demandeInfo(PionBlanc)
                demandeInfo(PionNoir)
                PlayingOthello(1,1)
            case default:
                return





# ═════════════════════════════════════════════════════════════════════════════════════════════
# ══════════════════════════  MinMax Inversé  ═════════════════════════════════════════════════
# ═════════════════════════════════════════════════════════════════════════════════════════════
"""
Premier algorithme développé pour l'IA.
Dû à une erreur de conception, il s'ait d'un algorithme qui cherche à minimiser le meilleur score de l'adversaire.
"""

def MinMaxV1meilleurScoreAdversaire(joueur, plateauTemp,versionScore):
    global WhiteNumberOfNodes, WhiteNodesPerDepth, BlackNumberOfNodes, BlackNodesPerDepth
    if TourActuel==PionBlanc:
        WhiteNumberOfNodes+=1
    else:
        BlackNumberOfNodes+=1
    platTemp = copy.deepcopy(plateauTemp)
    scoreTemp = 0
    scoreMeilleur = float("-inf")
    coupPossible=False
    for i in range ( 0, len(platTemp)):
        for j in range ( 0, len(platTemp[i])):
            if CoupAutorise(i,j,platTemp):
                coupPossible=True
                PosePion(i,j,platTemp)
                if versionScore==1:
                    scoreTemp = score(joueur , platTemp)
                elif versionScore==2:
                    scoreTemp=scorePoidsCase(joueur, platTemp)
                elif versionScore==3:
                    scoreTemp=scoreMobilite(joueur, platTemp)
                elif versionScore==4:
                    scoreTemp=scoreMixte(joueur,platTemp)
                if scoreTemp > scoreMeilleur:
                    scoreMeilleur = scoreTemp
                platTemp = copy.deepcopy(plateauTemp)
    if coupPossible==False:
        if versionScore == 1:
            return score(joueur, plateauTemp)
        else:
            return scorePoidsCase(joueur, plateauTemp)
    return scoreMeilleur    
                

def MinMaxV1meilleurCoup(joueur, plateau,versionScore=1 ):
    global WhiteNumberOfNodes, WhiteNodesPerDepth, BlackNumberOfNodes, BlackNodesPerDepth
    if TourActuel==PionBlanc:
        WhiteNumberOfNodes+=1
    else:
        BlackNumberOfNodes+=1
    plateauTemp = copy.deepcopy(plateau)
    coupMeilleurs = None
    scoreTemp = 0
    scoreAdver = 999999999
    for i in range ( 0, len(plateauTemp)):
        for j in range ( 0, len(plateauTemp[i])):
            if CoupAutorise(i,j,plateauTemp):
                plateauCoupSimule=copy.deepcopy(plateauTemp)
                PosePion(i,j,plateauCoupSimule)
                scoreTemp =  MinMaxV1meilleurScoreAdversaire(PionNoir if joueur==PionBlanc else PionBlanc, plateauCoupSimule, versionScore)
                if scoreTemp <= scoreAdver:
                    scoreAdver = scoreTemp
                    coupMeilleurs = (i,j)
    return coupMeilleurs
    
# ═════════════════════════════════════════════════════════════════════════════════════════════
# ══════════════════════════     MinMax       ═════════════════════════════════════════════════
# ═════════════════════════════════════════════════════════════════════════════════════════════
"""
Algorithme MinMax.
Cherche à maximiser son score tout en minimisant le score de l'adversaire.
Il est implémenté en deux fonctions : MinMaxMaximise et MinMaxMinimise, qui s'appellent récursivement.
"""
def MinMaxMinimise(joueur, plateau,profondeur,versionScore):
    global WhiteNumberOfNodes, WhiteNodesPerDepth, BlackNumberOfNodes, BlackNodesPerDepth
    if joueur==PionBlanc:
        WhiteNumberOfNodes+=1
        WhiteNodesPerDepth[profondeur-1]+=1
    else:
        BlackNodesPerDepth[profondeur-1]+=1
        BlackNumberOfNodes+=1
    platTemp = copy.deepcopy(plateau)
    scoreTemp = 0
    scoreMeilleur = float("inf")
    coupPossible = False
    for i in range ( 0, len(platTemp)):
        for j in range ( 0, len(platTemp[i])):
            if CoupAutorise(i,j,platTemp,PionBlanc if joueur==PionNoir else PionNoir):
                coupPossible=True
                PosePion(i,j,platTemp,PionBlanc if joueur==PionNoir else PionNoir) 
                _,scoreTemp = MinMaxMaximise(joueur , platTemp, profondeur-1,versionScore) 
                if scoreTemp < scoreMeilleur:
                    scoreMeilleur = scoreTemp
                platTemp = copy.deepcopy(plateau)
    if coupPossible==False:
        if versionScore == 1:
            return score(joueur, plateau)
        else:
            return scorePoidsCase(joueur, plateau)
    return scoreMeilleur    
                
def MinMaxMaximise(joueur, plateau,profondeur, versionScore=1 ):
    global WhiteNumberOfNodes, WhiteNodesPerDepth, BlackNumberOfNodes, BlackNodesPerDepth
    if joueur==PionBlanc:
        WhiteNumberOfNodes+=1
        WhiteNodesPerDepth[profondeur-1]+=1
    else:
        BlackNodesPerDepth[profondeur-1]+=1
        BlackNumberOfNodes+=1
    plateauTemp = None
    bestCoup = None
    scoreTemp = 0
    bestscore = float("-inf")
    if profondeur==0:
        if versionScore==1:
            return bestCoup,score(joueur,plateau)
        elif versionScore==2:
            return bestCoup,scorePoidsCase(joueur,plateau)
        elif versionScore==3:
            return bestCoup,scoreMobilite(joueur,plateau)
        elif versionScore==4:
            return bestCoup, scoreMixte(joueur,plateau)
    for i in range ( 0, len(plateau)):
        for j in range ( 0, len(plateau[i])):
            if CoupAutorise(i,j,plateau):
                plateauTemp=copy.deepcopy(plateau)
                PosePion(i,j,plateauTemp) 
                scoreTemp =  MinMaxMinimise(joueur, plateauTemp, profondeur, versionScore)
                if scoreTemp >= bestscore:
                    bestscore = scoreTemp
                    bestCoup = (i,j)
        
    return bestCoup, bestscore

# ═════════════════════════════════════════════════════════════════════════════════════════════
# ══════════════════════════    Alpha-Beta    ═════════════════════════════════════════════════
# ═════════════════════════════════════════════════════════════════════════════════════════════
"""
Algorithme Alpha-Beta.
Optimisation de l'algorithme MinMax, qui utilise deux variables alpha et beta pour éviter de parcourir des branches inutiles de l'arbre de recherche.
Permet d'atteindre des profondeurs plus importantes que MinMax, tout en gardant un temps de calcul raisonnable.
"""

def AlphaBetaMax(joueur, plateau, profondeur, alpha, beta,versionScore=1):
    global WhiteNumberOfNodes, WhiteNodesPerDepth, BlackNumberOfNodes, BlackNodesPerDepth
    if joueur==PionBlanc:
        WhiteNumberOfNodes+=1
        WhiteNodesPerDepth[profondeur-1]+=1
    else:
        BlackNodesPerDepth[profondeur-1]+=1
        BlackNumberOfNodes+=1
    # Cette fonction doit retourner le meilleur coup pour le joueur donné PionNoir ou PionBlanc
    #utilise les algorithmes de minimax avec élagage alpha-beta pour déterminer le meilleur coup pour le joueur donné PionNoir ou PionBlanc
    plateauTemp = None
    bestCoup = (None,None)
    v = 0
    if profondeur==0:
        #choix du score/strategie de recherche à utiliser pour évaluer le plateau à la profondeur 0
        if versionScore==1:
            return bestCoup,score(joueur,plateau)
        elif versionScore==2:
            return bestCoup,scorePoidsCase(joueur,plateau)
        elif versionScore==3:
            return bestCoup,scoreMobilite(joueur,plateau)
        elif versionScore==4:
            return bestCoup, scoreMixte(joueur,plateau)
    for i in range ( 0, len(plateau)):
        for j in range ( 0, len(plateau[i])):
            if CoupAutorise(i,j,plateau, joueur):
                #print("Coup autorisé pour i:"+str(i) + "et j : "+ str(j))
                plateauTemp=copy.deepcopy(plateau)
                PosePion(i,j,plateauTemp, joueur) # fonction plaçant le pion du joueur sur le plateau temporaire
                _, v =  AlphaBetaMin(joueur, plateauTemp, profondeur, alpha, beta, versionScore)
                if bestCoup==(None,None):
                    bestCoup=(i,j)
                if v > alpha :
                    alpha = v
                    bestCoup = (i,j)
                if alpha >= beta:
                    return bestCoup, alpha
    return bestCoup, alpha
    
def AlphaBetaMin(joueur, plateau, profondeur, alpha, beta, versionScore=1): 
    global WhiteNumberOfNodes, WhiteNodesPerDepth, BlackNumberOfNodes, BlackNodesPerDepth
    if joueur==PionBlanc:
        WhiteNumberOfNodes+=1
        WhiteNodesPerDepth[profondeur-1]+=1
    else:
        BlackNodesPerDepth[profondeur-1]+=1
        BlackNumberOfNodes+=1
    # Cette fonction doit retourner le meilleur coup pour le joueur donné PionNoir ou PionBlanc
    #utilise les algorithmes de minimax avec élagage alpha-beta pour déterminer le meilleur coup pour le joueur donné PionNoir ou PionBlanc
    plateauTemp = None
    bestCoup = (None,None)
    v = 0
    for i in range ( 0, len(plateau)):
        for j in range ( 0, len(plateau[i])):
            if CoupAutorise(i,j,plateau,PionBlanc if joueur==PionNoir else PionNoir):
                #print("Coup autorisé pour i:"+str(i) + "et j : "+ str(j))
                plateauTemp=copy.deepcopy(plateau)
                PosePion(i,j,plateauTemp,PionBlanc if joueur==PionNoir else PionNoir) # fonction plaçant le pion du joueur sur le plateau temporaire
                _, v =  AlphaBetaMax(joueur, plateauTemp, profondeur-1, alpha, beta, versionScore)
                if bestCoup==(None,None):
                    bestCoup=(i,j)
                if v < beta :
                    beta = v
                    bestCoup = (i,j)
                if alpha >= beta:
                    return bestCoup, beta
    return bestCoup, beta



# ═════════════════════════════════════════════════════════════════════════════════════════════
# ══════════════════════════    Montecarlo    ═════════════════════════════════════════════════
# ═════════════════════════════════════════════════════════════════════════════════════════════
"""
Algorithme de Montecarlo.
Il est confié un temps total pour faire des simulations, et il doit choisir le coup qui a la meilleure moyenne de score après avoir fait des simulations aléatoires à partir de ce coup.
"""

def MonteCarloMain(joueur,plateau,tempsSimulation):
    global WhiteNumberOfNodes, WhiteNodesPerDepth, BlackNumberOfNodes, BlackNodesPerDepth
    if joueur==PionBlanc:
        WhiteNumberOfNodes+=1
    else:
        BlackNumberOfNodes+=1
    PossibleHit=getAllPossibleHit(plateau,joueur)
    if len(PossibleHit)==0:
        return None
    if len(PossibleHit)==1:
        return PossibleHit[0][0], PossibleHit[0][1]
    BestScore=float("-inf")
    BestIndex=-1
    for i in range(0, len(PossibleHit)):
        platSimulation=copy.deepcopy(plateau)
        PosePion(PossibleHit[i][0],PossibleHit[i][1],platSimulation,joueur)
        AvgScoreSimulation=MonteCarloSimulation(platSimulation,joueur,tempsSimulation/float(len(PossibleHit)))
        if AvgScoreSimulation>BestScore:
            BestScore=AvgScoreSimulation
            BestIndex=i
    return PossibleHit[BestIndex][0],PossibleHit[BestIndex][1]

" Variable utilisé pour savoir si le temps accordé pour une simulation est écoulé "
SimulationTimeElapsed=False

def MonteCarloSimulation(plateau,joueur,tempsSimulation):
    global WhiteNumberOfNodes, WhiteNodesPerDepth, BlackNumberOfNodes, BlackNodesPerDepth
    global SimulationTimeElapsed
    SimulationTimeElapsed=False
    scoreActuel=0
    numberOfSimulation=0

    threading.Thread(target=MonteCarloThreadTime,args=(tempsSimulation,)).start()
    while SimulationTimeElapsed==False:
        plat=copy.deepcopy(plateau)
        ActuelJoueur=(PionBlanc if joueur==PionNoir else PionNoir)
        while True:
            if SimulationTimeElapsed==True:
                break
            PossibleHit=getAllPossibleHit(plat,ActuelJoueur)
            if len(PossibleHit)!=0:
                IndexPlayed=rand.randint(0,len(PossibleHit)-1)
            else:
                ActuelJoueur=(PionBlanc if ActuelJoueur==PionNoir else PionNoir)    
                continue
            PosePion(PossibleHit[IndexPlayed][0],PossibleHit[IndexPlayed][1],plat,ActuelJoueur)
            ActuelJoueur=(PionBlanc if ActuelJoueur==PionNoir else PionNoir)
            if isFinished(plat,True):
                scoreActuel+=score(joueur,plat)
                numberOfSimulation+=1
                break
    if numberOfSimulation!=0:
        if joueur==PionBlanc:
            WhiteNumberOfNodes+=numberOfSimulation
        else:
            BlackNumberOfNodes+=numberOfSimulation
        return scoreActuel/numberOfSimulation
    else:
        return 0

def MonteCarloThreadTime(tempsSimulation):
    global SimulationTimeElapsed
    time.sleep(tempsSimulation)
    SimulationTimeElapsed=True
    return

# ═════════════════════════════════════════════════════════════════════════════════════════════
# ══════════════════════════    Montecarlo    ═════════════════════════════════════════════════
# ═════════════════════════════════════════════════════════════════════════════════════════════
"""
Algorithme de Montecarlo amélioré.
Il est confié un temps total pour faire des simulations, et il doit choisir le coup qui a la meilleure moyenne de score après avoir fait des simulations aléatoires à partir de ce coup.
Il a également une capacité de faire un Preprocessing des coups possibles, en utilisant une fonction de score pour évaluer rapidement les coups et ne garder que les meilleurs pour faire les simulations.
"""
def Preprocessor(plateau, joueur, PossibleHit, modePreprocess, Ns=4, ps=0.7):
    """
    Va permettre d'obtenir les meilleurs coups selon le type d'alorithme : 
    - FSP : Full Search Preprocessing : va trier les coups par score décroissant et ne garder que les Ns meilleurs
    - VSP : Value Search Preprocessing : va calculer la moyenne des scores de tous
    Le Preprocessor utilise toujours le poids des cases, pour assurer une cohérence avec les positions.
    """
    # calculer le score de chaque coup directement
    coupsScores=[]
    for coup in PossibleHit:
        x,y = coup
        platTest=copy.deepcopy(plateau)
        PosePion(x,y,platTest,joueur)
        # bloc score en brut
        s=scorePoidsCase(joueur,platTest)
        coupsScores.append((s,coup))
    # appliquer le préprocessing
    if modePreprocess=="FSP":
        # trier par score décroissant et garder les Ns meilleurs
        coupsScores.sort(reverse=True,key=lambda x:x[0])
        coupsFiltres=[c[1] for c in coupsScores[:Ns]]
    elif modePreprocess=="VSP":
        moyenne=sum(c[0] for c in coupsScores)/len(coupsScores)
        seuil=ps*moyenne
        coupsFiltres=[c[1] for c in coupsScores if c[0]>=seuil]
        if len(coupsFiltres)==0:
            coupsFiltres=PossibleHit
    else:
        coupsFiltres=PossibleHit

    return coupsFiltres

def selectPseudoRandomMove(plat, joueur, PossibleHit, versionScore):
    """
    Fonction qui va réaliser une sélection pseudo-aléatoire pour les simulations avec une répartition : 
    - 30% aléatoire pur : pour garder une part d'exploration dans les simulations
    - 70% coup heuristique selon versionScore : pour favoriser les coups qui ont un meilleur score selon la fonction de score choisie, et ainsi améliorer la qualité des simulations
    Afin d'augmenter la rapidité de cette sélection, on ne va pas calculer le score de tous les coups possibles, mais seulement d'un échantillon aléatoire de ces coups, pour ensuite choisir le meilleur parmi cet échantillon.
    """
    if rand.random() < 0.3:
        return rand.randint(0, len(PossibleHit) - 1)
    sampleSize = min(3, len(PossibleHit))
    indicesToTest = rand.sample(range(len(PossibleHit)), sampleSize)
    bestScore = float("-inf")
    bestIndex = indicesToTest[0]
    for i in indicesToTest:
        x, y = PossibleHit[i]
        platTest = copy.deepcopy(plat)
        PosePion(x, y, platTest, joueur)
        if versionScore == 1:
            s = score(joueur, platTest)
        elif versionScore == 2:
            s = scorePoidsCase(joueur, platTest)
        elif versionScore == 3:
            s = scoreMobilite(joueur, platTest)
        elif versionScore == 4:
            s = scoreMixte(joueur, platTest)
        if s > bestScore:
            bestScore = s
            bestIndex = i    
    return bestIndex

def BetterMonteCarloMain(joueur,plateau,tempsSimulation,versionScore,modePreprocess="FSP",Ns=4,ps=0.7):
    """
    Pour la liste des coups, un preprocessor est appliqué, permettant de ne garder que les coups les plus intéressants pour faire les simulations, et ainsi améliorer la qualité des simulations.
    Ensuite, pour chaque coup, on fait des simulations en utilisant une sélection pseudo-aléatoire
    """
    global WhiteNumberOfNodes, WhiteNodesPerDepth, BlackNumberOfNodes, BlackNodesPerDepth
    if joueur==PionBlanc:
        WhiteNumberOfNodes+=1
    else:
        BlackNumberOfNodes+=1
    PossibleHit=getAllPossibleHit(plateau,joueur)
    if len(PossibleHit)==0:
        return None
    # appliquer le Preprocessor
    PossibleHit=Preprocessor(plateau,joueur,PossibleHit,modePreprocess,Ns,ps)
    if len(PossibleHit)==1:
        return PossibleHit[0][0],PossibleHit[0][1]
    BestScore=float("-inf")
    BestIndex=-1
    for i in range(len(PossibleHit)):
        platSimulation=copy.deepcopy(plateau)
        PosePion(PossibleHit[i][0],PossibleHit[i][1],platSimulation,joueur)
        AvgScoreSimulation=BetterMonteCarloSimulation(
            platSimulation,
            joueur,
            tempsSimulation/float(len(PossibleHit)),
            versionScore
        )
        if AvgScoreSimulation>BestScore:
            BestScore=AvgScoreSimulation
            BestIndex=i
    return PossibleHit[BestIndex][0],PossibleHit[BestIndex][1]

def BetterMonteCarloSimulation(plateau,joueur,tempsSimulation,versionScore):
    """
    Sur les 5 premiers coups de la simulation, on utilise une sélection pseudo-aléatoire pour favoriser les coups qui ont un meilleur score selon la fonction de score choisie, afin d'améliorer la qualité des simulations.
    Après les 5 premiers coups, on utilise une sélection aléatoire pur pour garder une part d'exploration dans les simulations, et aussi pour accélérer la sélection des coups, afin de faire plus de simulations dans le temps imparti.
    """
    global WhiteNumberOfNodes, WhiteNodesPerDepth, BlackNumberOfNodes, BlackNodesPerDepth
    global SimulationTimeElapsed
    SimulationTimeElapsed=False
    scoreActuel=0
    numberOfSimulation=0
    threading.Thread(target=MonteCarloThreadTime,args=(tempsSimulation,)).start()
    while SimulationTimeElapsed==False:
        plat=copy.deepcopy(plateau)
        ActuelJoueur=(PionBlanc if joueur==PionNoir else PionNoir)
        tourSimulation=0
        while True:
            if SimulationTimeElapsed==True:
                break
            PossibleHit=getAllPossibleHit(plat,ActuelJoueur)
            if len(PossibleHit)!=0:
                if tourSimulation<9 and tourSimulation%2==0:
                    IndexPlayed=selectPseudoRandomMove(plat,ActuelJoueur,PossibleHit,versionScore)
                else:
                    IndexPlayed=rand.randint(0,len(PossibleHit)-1)
            else:
                ActuelJoueur=(PionBlanc if ActuelJoueur==PionNoir else PionNoir)
                continue
            tourSimulation+=1
            PosePion(PossibleHit[IndexPlayed][0],PossibleHit[IndexPlayed][1],plat,ActuelJoueur)
            ActuelJoueur=(PionBlanc if ActuelJoueur==PionNoir else PionNoir)
            if isFinished(plat,True):
                scoreActuel+=score(joueur,plat)
                numberOfSimulation+=1
                break
    if numberOfSimulation!=0:
        if joueur==PionBlanc:
            WhiteNumberOfNodes+=numberOfSimulation
        else:
            BlackNumberOfNodes+=numberOfSimulation
        return scoreActuel/numberOfSimulation
    else:
        return 0
    
# ═════════════════════════════════════════════════════════════════════════════════════════════
# ══════════════════════════      Random      ═════════════════════════════════════════════════
# ═════════════════════════════════════════════════════════════════════════════════════════════
"""
Algorithme RANDOM.
Il choisit un coup aléatoire parmi les coups possibles, sans faire de simulation ni de préprocessing.
Permet de faire un benchmark pour les autres algorithmes, et de vérifier que les autres algorithmes font mieux que le hasard.
"""

def randomPlay(plateau,joueur):
    global WhiteNumberOfNodes, WhiteNodesPerDepth, BlackNumberOfNodes, BlackNodesPerDepth
    if joueur==PionBlanc:
        WhiteNumberOfNodes+=1
    else:
        BlackNumberOfNodes+=1
    PossibleHit=getAllPossibleHit(plateau,joueur)
    if len(PossibleHit)!=0:
        IndexPlayed=rand.randint(0,len(PossibleHit)-1)
    return PossibleHit[IndexPlayed][0],PossibleHit[IndexPlayed][1]

# ═════════════════════════════════════════════════════════════════════════════════════════════
# ════════════════════════  Fonction de score   ═══════════════════════════════════════════════
# ═════════════════════════════════════════════════════════════════════════════════════════════

def nombrePion(joueur,plat):
    """
    Permet d'obtenir le nombre de pion d'un joueur ainsi que le score associé (Si le plateau est vide alors on considère qu'il a 64 pions)
    """
    score=0
    scoreAdversaire=0
    for i in range(0,len(plat)):
        for j in range(0,len(plat[i])):
            if plat[i][j]==joueur:
                score+=1
            elif plat[i][j]==(PionBlanc if joueur==PionNoir else PionNoir):
                scoreAdversaire+=1
    if scoreAdversaire==0:
        score=64
    return score
nombrePion

def score(joueur, plat):
    """
    Permet d'obtenir le score absolu d'un joueur
    """
    score = 0
    scoreAdversaire=0
    for i in range ( 0, len(plat)):
        for j in range ( 0, len(plat[i])):
            if (plat[i][j] == joueur):
                score+=1
            elif (plat[i][j] == (PionBlanc if joueur==PionNoir else PionNoir)):
                scoreAdversaire+=1
    if scoreAdversaire==0:
        score=64
    return score - scoreAdversaire


tableauPoids = [
[500,-150,30,10,10,30,-150,500],
[-150,-250,0,0,0,0,-250,-150],
[30,0,1,2,2,1,0,30],
[10,0,2,16,16,2,0,10],
[10,0,2,16,16,2,0,10],
[30,0,1,2,2,1,0,30],
[-150,-250,0,0,0,0,-250,-150],
[500,-150,30,10,10,30,-150,500]]

def scorePoidsCase(joueur, plat):
    """
    Permet d'obtenir le score relatif d'un joueur en fonction des positions qu'il occupe.
    """
    # Cette fonction doit retourner le score du joueur donné PionNoir ou PionBlanc
    # Le score est défini comme le nombre de pions du joueur sur le plateau - le nombre de pions de l'adversaire, suivant le poids actif
    score = 0
    scoreAdversaire=0
    for i in range ( 0, len(plat)):
        for j in range ( 0, len(plat[i])):
            if (plat[i][j] == joueur):
                score+=tableauPoids[i][j]
            elif (plat[i][j] == (PionBlanc if joueur==PionNoir else PionNoir)):
                scoreAdversaire+=tableauPoids[i][j]
    if scoreAdversaire==0:
        score=0
        for i in range(0, len(plat)):
            for j in range(0,len(plat[i])):
                score+=tableauPoids[i][j]
    return score - scoreAdversaire

def scoreMobilite(joueur, plat): 
    """
    Permet d'obtenir le score de mobilité d'un joueur, c'est à dire le nombre de coups possibles pour ce joueur, moins le nombre de coups possibles pour l'adversaire.
    """
    score = 0
    scoreAdversaire=0
    for i in range ( 0, len(plat)):
        for j in range ( 0, len(plat[i])):
            if CoupAutorise(i,j,plat,joueur):#on verifie les coups possibles pour le joueur
                score+=1
                if (i,j) in [(0,0),(0,7),(7,0),(7,7)]:#on donne aux coins un poid plus important car ils sont avantageux pour le joueur
                    score+=10 
            #comme une case peut être jouable pour les deux joueurs, on ne met pas de elif, mais un if séparé pour vérifier les coups possibles pour l'adversaire
            if CoupAutorise(i,j,plat,PionBlanc if joueur==PionNoir else PionNoir):#on verifie les coups possibles pour l'adversaire
                scoreAdversaire+=1
                if (i,j) in [(0,0),(0,7),(7,0),(7,7)]:# on donne aux coins un poid plus important
                    scoreAdversaire+=10
    return score - scoreAdversaire

def scoreMixte(joueur, plat):
    """
    Va permettre d'obtenir un score mixte, qui combine les différentes fonctions de score en fonction du nombre de pions sur le plateau :
    - Si il y a moins de 20 pions sur le plateau, on utilise le score de poids de case, pour favoriser les positions stratégiques
    - Si il y a entre 20 et 50 pions sur le plateau, on utilise le score de mobilité, pour favoriser les coups qui offrent plus de possibilités de jeu
    - Si il y a plus de 50 pions sur le plateau, on utilise le score de nombre de pions, pour favoriser les coups qui permettent de gagner la partie
    """
    global pt
    if pt<20:
        return scorePoidsCase(joueur,plat)
    elif pt<50:
        return scoreMobilite(joueur,plat)
    else:
        return nombrePion(joueur,plat)

# ═════════════════════════════════════════════════════════════════════════════════════════════
# ════════════════════════  Lancement du jeu    ═══════════════════════════════════════════════
# ═════════════════════════════════════════════════════════════════════════════════════════════

print("Quel mode voulez-vous ? Génération de stat (Tapez 0) ou Othello Game (Tapez n'importe quel autre chiffre)?\n")
Choix=int(input("Votre choix : "))
if Choix==0:
    
    getResultat()
else:
    OthelloGame()
