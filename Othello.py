#Hello world 

import numpy
import time
import copy
import random as rand
import threading
# Jeu d'Othello : Variable

plat = numpy.zeros((8,8),str)
PionBlanc = "B"
PionNoir = "N"


def InitialisePlateau():
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
        if joueur is None:
            joueur = TourActuel

        if plateau[x+incrementX][y+incrementY]==("N" if joueur=="B" else "B"):
            if x+(incrementX*2)>-1 and x+(incrementX*2)<8 and y+(incrementY*2)<8 and y+(incrementY*2)>-1:
                if plateau[x+(incrementX*2)][y+(incrementY*2)]==joueur:
                    return True  
                return checkCoup(x+incrementX,y+incrementY,incrementX,incrementY, plateau, joueur)  
        return False


def CoupAutorise(i,j, plateau, joueur=None):
    if joueur is None:
        joueur = TourActuel
    #On doit check chaque diagonale & Chaque côté pour voir si le coup est autorisé
    if plateau[i][j]!=' ':
        return False
    if (i>1):
        #OOn prend le pion au dessus
        if checkCoup(i,j,-1,0,plateau,joueur):
            return True
        if (j>1):
            #Diagonale Gauche
            if checkCoup(i,j,-1,-1,plateau,joueur):
                return True
        if (j<6):
            #Diagonale droite
            if checkCoup(i,j,-1,1,plateau,joueur):
                return True
    if (i<6):
        #Pion en dessous
        if checkCoup(i,j,1,0,plateau,joueur):
            return True
        if (j>1):
            #Diagonale bas gauche
            if checkCoup(i,j,1,-1,plateau,joueur):
                return True
        if (j<6):
            #Diagonale bas droite
            if checkCoup(i,j,1,1,plateau,joueur):
                return True
    if (j>1):
        # Gauche
        if checkCoup(i,j,0,-1,plateau,joueur):
            return True
    if (j<6):
        # Droite
        if checkCoup(i,j,0,1,plateau,joueur):
            return True
    return False


def ChangeCaseCoupAutorise(x,y,incrementX,incrementY,plateau, joueur=None):
    if joueur is None:
        joueur = TourActuel
    case=plateau[x+incrementX][y+incrementY]
    while case!=TourActuel:
        ChangeCouleurCase(x+incrementX,y+incrementY,plateau)
        x=x+incrementX
        y=y+incrementY
        case=plateau[x+incrementX][y+incrementY]

def ChangeCouleurCase(i,j,plateau):
    if plateau[i][j]=="B":
        plateau[i][j]="N"
    elif plateau[i][j]=="N":
        plateau[i][j]="B"

def ChangeTour():
    global TourActuel
    TourActuel="N" if TourActuel=="B" else "B"

def PosePion(i,j,plateau, joueur=None):
    if joueur is None:
        joueur = TourActuel
    plateau[i][j]=joueur
    if (i>1):
        #On prend le pion au dessus
        if checkCoup(i,j,-1,0,plateau,joueur):
            ChangeCaseCoupAutorise(i,j,-1,0,plateau,joueur)
        if (j>1):
            #Diagonale Gauche
            if checkCoup(i,j,-1,-1,plateau,joueur):
                ChangeCaseCoupAutorise(i,j,-1,-1,plateau,joueur)
        if (j<6):
            #Diagonale droite
            if checkCoup(i,j,-1,1,plateau,joueur):
                ChangeCaseCoupAutorise(i,j,-1,1,plateau,joueur)
    if (i<6):
        #Pion en dessous
        if checkCoup(i,j,1,0,plateau,joueur):
            ChangeCaseCoupAutorise(i,j,1,0,plateau,joueur)
        if (j>1):
            #Diagonale bas gauche
            if checkCoup(i,j,1,-1,plateau,joueur):
                ChangeCaseCoupAutorise(i,j,1,-1,plateau,joueur)
        if (j<6):
            #Diagonale bas droite
            if checkCoup(i,j,1,1,plateau,joueur):
                ChangeCaseCoupAutorise(i,j,1,1,plateau,joueur)
    if (j>1):
        # Gauche
        if checkCoup(i,j,0,-1,plateau,joueur):
                ChangeCaseCoupAutorise(i,j,0,-1,plateau,joueur)
    if (j<6):
        # Droite
        if checkCoup(i,j,0,1,plateau,joueur):
            ChangeCaseCoupAutorise(i,j,0,1,plateau,joueur)

def isFinished(plateau, simulation=False):
    condRemplissage=True
    condCoupPossible=False
    for i in range(0,len(plateau)):
        for j in range(0,len(plateau[0])):
            if plateau[i][j]==' ':
                condRemplissage=False
                if CoupAutorise(i,j,plateau):
                    condCoupPossible=True
    if condCoupPossible==False and condRemplissage==False:
        for i in range(0,len(plateau)):
            for j in range(0,len(plateau[0])):
                if CoupAutorise(i,j,plateau,"B" if TourActuel=="N" else "N") and simulation==False:
                    #print("Le joueur "+TourActuel+ " ne peut pas jouer, on repasse directement au joueur "+"B" if TourActuel=="N" else "N")
                    ChangeTour()
                    return False
    if condRemplissage==True or condCoupPossible==False or nombrePion("N", plat)==0 or nombrePion("B",plat)==0:
        return True
    return False
    

    # Rajouter le fait que si un des deux joueurs ne peut pas jouer, ca skip juste le tour ;)

TourActuel=PionNoir


VerboseTourActuel=["N","B"]
VerboseIA=["MinMaxV1MeilleurCoup","MinMaxMaximise","AlphaBeta","Montecarlo","Random"]
VerboseScore=["Nombre de pions relatifs", "Poids des cases","scoreMobilite", "Mixte"]

def writeStat(i,j,k,l,m,n):
    with open('resultat.txt','a') as f:
        f.write("-----------------------\n")
        f.write(VerboseIA[i] + " (B) VS (N) "+ VerboseIA[j]+"\n")
        f.write(VerboseScore[k-1] + "(B) VS (N) "+ VerboseScore[l-1]+"\n")
        if VerboseIA[i]=="Montecarlo" or VerboseIA[j]=="Montecarlo":
            f.write("Temps pour Montecarlo : "+str(tempsMontecarlo) + "\n")
        if VerboseIA[i]=="MinMaxMaximise" or VerboseIA[i]=="AlphaBeta":
            f.write("Profondeur Blanc (2 demi-coups) : "+ str(m)+ "\n")
        if VerboseIA[j]=="MinMaxMaximise" or VerboseIA[j]=="AlphaBeta":
            f.write("Profondeur Noir (2 demi-coups) : "+ str(n)+"\n")
        f.write(TourActuel + " commence.\n")

def writeStatisticTimeandNodes(i,j):
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

#Nombre de coups total
pt=0

#Nombre de coups par couleur
#Temps total pour le coup


BlackMoves=0
BlackNumberOfNodes=0
BlackNodesPerDepth=[]
BlackTimeUsed=0
#Nombre de récursivité faite & Nombre de noeuds par "étage"
WhiteNumberOfNodes=0
WhiteNodesPerDepth=[]
WhitetimeUsed=0
WhiteMoves=0


tempsMontecarlo=0.5

def getResultat():
    global pt, WhiteNumberOfNodes, WhiteNodesPerDepth, WhitetimeUsed, WhiteMoves, BlackMoves, BlackNumberOfNodes, BlackNodesPerDepth, BlackTimeUsed
    RecursiviteMax=3
    compteurTour=1
    with open('resultat.txt','w') as f:
        f.write("Jeu d'Othello - Résultats \n")
    global TourActuel
    for t in range(0,2):
        for i in range(0,5):
            #Fonction pour B
            for j in range(0,5):
                #Fonction pour N
                for k in range(1,5):
                    #Score pour B
                    for l in range(1,5):
                        #Score pour N
                        for m in range(1,RecursiviteMax+1):
                            if m==2 and (i!=1 and i!=2):
                                break
                            #On fait MinMax a profondeur 2 max, car sinon cela prend trop de temps
                            if m==3 and i!=2:
                                break
                            for n in range(1,RecursiviteMax+1):
                                if n==2 and (j!=1 and j!=2):
                                    break
                                #On fait MinMax a profondeur 2 max, car sinon cela prend trop de temps
                                if n==3 and j!=2:
                                    break
                                InitialisePlateau()
                                pt=0
                                if t==0:
                                    TourActuel="N"
                                else:
                                    TourActuel="B"
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
                                    if TourActuel=="B":
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
                                        timeStop=time.time()
                                        BlackTimeUsed+=timeStop-timeStart
                                    if CoupAutorise(x,y,plat):
                                        pt+=1
                                        PosePion(x,y,plat)
                                        ChangeTour()
                                        if isFinished(plat):
                                            #print(plat)
                                            writeStatisticTimeandNodes(i,j)
                                            with open('resultat.txt','a') as f:
                                                f.write("Coup joué :"+str(pt)+ "\n")
                                                f.write("Score du joueur B : "+str(nombrePion("B",plat))+"\n")
                                                f.write("Score du joueur N : " + str(nombrePion("N",plat))+"\n")
                                            break    


def affichagePlat(plat):
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



IAVouluBlanc=1
ScoreVouluBlanc=1
profondeurBlanc=1
tempsMontecarloBlanc=0.5

IAVouluNoir=1
ScoreVouluNoir=1
profondeurNoir=1
tempsMontecarloNoir=0.5

def afficheInfoIA(Couleur):
    print("-----")
    print("Pour l'IA "+ Couleur+" :")
    print("| Modèle "+ VerboseIA[(IAVouluBlanc-1 if Couleur=="B" else IAVouluNoir-1)])
    if (IAVouluBlanc if Couleur=="B" else IAVouluNoir)==2 or (IAVouluBlanc if Couleur=="B" else IAVouluNoir)==3:
        print("| Profondeur : " + str((profondeurBlanc if Couleur=="B" else profondeurNoir)))
    if ((IAVouluBlanc if Couleur=="B" else IAVouluNoir))!=4 and (IAVouluBlanc if Couleur=="B" else IAVouluNoir)!=5:
        print("| Fonction de score utilisée : "+VerboseScore[(IAVouluBlanc-1 if Couleur=="B" else IAVouluNoir-1)])
    if (IAVouluBlanc if Couleur=="B" else IAVouluNoir)==4:
        print("| Temps de Montecarlo : "+ str((tempsMontecarloBlanc if Couleur=="B" else tempsMontecarloNoir)))

def demandeInfo(Couleur):
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
            if Couleur=="B":
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
                        if Couleur=="B":
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
                        if Couleur=="B":
                            ScoreVouluBlanc=int(input("Votre choix :"))
                            if ScoreVouluBlanc >= 1 and ScoreVouluBlanc <= 4 : 
                                break
                        else:
                            ScoreVouluNoir=int(input("Votre choix :"))
                            if ScoreVouluNoir >= 1 and ScoreVouluNoir <= 4 : 
                                break
                    print("Quel profondeur voulez-vous ? Chaque profondeur joue 2 demi-coups (1 coup allié, 1 coup adverse). Attention, pour MinMax, on conseille un max de 2 !")
                    if Couleur=="B":
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
                        if Couleur=="B":
                            ScoreVouluBlanc=int(input("Votre choix :"))
                            if ScoreVouluBlanc >= 1 and ScoreVouluBlanc <= 4 : 
                                break
                        else:
                            ScoreVouluNoir=int(input("Votre choix :"))
                            if ScoreVouluNoir >= 1 and ScoreVouluNoir <= 4 : 
                                break
                    print("Quel profondeur voulez-vous ? Chaque profondeur joue 2 demi-coups (1 coup allié, 1 coup adverse).")
                    if Couleur=="B":
                        profondeurBlanc=int(input("Votre choix :"))
                    else:
                        profondeurNoir=int(input("Votre choix :"))
                    return
                case 4:
                    print("Quel temps voulez-vous pour le Montecarlo ? On conseille 0.5 ou 1. Merci de mettre un . et pas une virgule ! ")
                    if Couleur=="B":
                        tempsMontecarloBlanc=float(input("Votre choix:"))
                    else:
                        tempsMontecarloNoir=float(input("Votre choix : "))
                    return
                case 5:
                    return
                case default:
                    return




def PlayingOthello(Blanc,Noir):
    global TourActuel, tempsMontecarlo, WhiteNodesPerDepth, WhiteNumberOfNodes, WhitetimeUsed, WhiteMoves, BlackNumberOfNodes, BlackNodesPerDepth, BlackTimeUsed, BlackMoves
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
    print("-------------------------------------")
    TourActuel=PionNoir
    while True:
        numeroTour+=1
        print("Tour n°"+str(numeroTour) + " : A "+TourActuel  + " de jouer !")
        affichagePlat(plat)
        if TourActuel=="B":
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
        if CoupAutorise(x,y,plat):
            PosePion(x,y,plat)
            ChangeTour()
            if isFinished(plat):
                print("Fin du jeu ! Baissez les armes !")
                print("-------------------------------------")
                affichagePlat(plat)
                if Blanc==0:
                    print("-----\n Pour le joueur B :")
                else:
                    afficheInfoIA("B")
                print("-> Score (B) de "+str(nombrePion("B",plat)))
                if Noir==0:
                    print("-----\n Pour le joueur N :")
                else:
                    afficheInfoIA("N")
                print("-> Score (N) de "+str(nombrePion("N",plat)))
                if (nombrePion("B",plat)) > (nombrePion("N",plat)):
                    print(" \n Le joueur B a gagné ! Félicitations ! \n ")
                elif (nombrePion("B",plat)) < (nombrePion("N",plat)):
                    print("\n Le joueur N a gagné ! Félicitations ! \n")
                else:
                    print("\n Match nul entre les joueurs ! Bien joué ! \n")
                return
        else:
            print("Le coup n'est pas autorisé suivant les règles de l'Othello !")
def OthelloGame():
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
                demandeInfo("N")
                PlayingOthello(0,1)
            case 3:
                demandeInfo("B")
                PlayingOthello(1,0)
            case 4:
                demandeInfo("B")
                demandeInfo("N")
                PlayingOthello(1,1)
            case default:
                return




############################################################################################################
#==========================================================================================================#
#=========================== V1 : Min-max inversé de profondeur 1 =========================================#
#==========================================================================================================#
############################################################################################################
#Premiere version de l algorithme avec les min max inversés. 
# Le joueur choisit le coup qui minimise le meilleur score de l adversaire après que le joueur ait joué son coup.   
  
def MinMaxV1meilleurScoreAdversaire(joueur, plateauTemp,versionScore):
    global WhiteNumberOfNodes, WhiteNodesPerDepth, BlackNumberOfNodes, BlackNodesPerDepth
    if TourActuel=="B":
        WhiteNumberOfNodes+=1
    else:
        BlackNumberOfNodes+=1
    # Cette fonction doit retourner le meilleur coup pour l'adversaire donné "N" ou "B"
    platTemp = copy.deepcopy(plateauTemp)
    scoreTemp = 0
    scoreMeilleur = float("-inf")
    coupPossible=False
    for i in range ( 0, len(platTemp)):
        for j in range ( 0, len(platTemp[i])):
            if CoupAutorise(i,j,platTemp):
                coupPossible=True
                PosePion(i,j,platTemp) # fonction plaçant le pion de l'adversaire sur le plateau temporaire
                #choix du score/strategie de recherche à utiliser pour évaluer le plateau après que l adversaire ait joué son coup
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
    if TourActuel=="B":
        WhiteNumberOfNodes+=1
    else:
        BlackNumberOfNodes+=1
    # Cette fonction doit retourner le meilleur coup pour le joueur donné "N" ou "B"
    #le meilleure coup est déterminé comme le coup qui minimise le meillescore de l'adversaire après que le joueur ait joué son coup
    plateauTemp = copy.deepcopy(plateau)
    coupMeilleurs = None
    scoreTemp = 0
    scoreAdver = 999999999
    for i in range ( 0, len(plateauTemp)):
        for j in range ( 0, len(plateauTemp[i])):
            if CoupAutorise(i,j,plateauTemp):
                #print("Coup autorisé pour i:"+str(i) + "et j : "+ str(j))
                plateauCoupSimule=copy.deepcopy(plateauTemp)
                PosePion(i,j,plateauCoupSimule) # fonction plaçant le pion du joueur sur le plateau temporaire
                scoreTemp =  MinMaxV1meilleurScoreAdversaire("N" if joueur=="B" else "B", plateauCoupSimule, versionScore)
                if scoreTemp <= scoreAdver:
                    scoreAdver = scoreTemp
                    coupMeilleurs = (i,j)
    
    return coupMeilleurs
    
############################################################################################################
#==========================================================================================================#
#================================== V2 : Min-max de profondeur n  =========================================#
#==========================================================================================================#
############################################################################################################

def MinMaxMinimise(joueur, plateau,profondeur,versionScore):
    global WhiteNumberOfNodes, WhiteNodesPerDepth, BlackNumberOfNodes, BlackNodesPerDepth
    if joueur=="B":
        WhiteNumberOfNodes+=1
        WhiteNodesPerDepth[profondeur-1]+=1
    else:
        BlackNodesPerDepth[profondeur-1]+=1
        BlackNumberOfNodes+=1
    # Cette fonction doit retourner le meilleur coup pour le joueur  donné "N" ou "B"
    platTemp = copy.deepcopy(plateau)
    scoreTemp = 0
    scoreMeilleur = float("inf")
    coupPossible = False
    for i in range ( 0, len(platTemp)):
        for j in range ( 0, len(platTemp[i])):
            if CoupAutorise(i,j,platTemp,"B" if joueur=="N" else "N"):
                coupPossible=True
                PosePion(i,j,platTemp,"B" if joueur=="N" else "N") 
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
    if joueur=="B":
        WhiteNumberOfNodes+=1
        WhiteNodesPerDepth[profondeur-1]+=1
    else:
        BlackNodesPerDepth[profondeur-1]+=1
        BlackNumberOfNodes+=1
    # Cette fonction doit retourner le meilleur coup pour le joueur donné "N" ou "B"
    #le meilleure coup est déterminé comme le coup qui minimise le meillescore de l'adversaire après que le joueur ait joué son coup
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
                #print("Coup autorisé pour i:"+str(i) + "et j : "+ str(j))
                plateauTemp=copy.deepcopy(plateau)
                PosePion(i,j,plateauTemp) # fonction plaçant le pion du joueur sur le plateau temporaire
                scoreTemp =  MinMaxMinimise(joueur, plateauTemp, profondeur, versionScore)
                if scoreTemp >= bestscore:
                    bestscore = scoreTemp
                    bestCoup = (i,j)
        
    return bestCoup, bestscore



############################################################################################################
#==========================================================================================================#
#================================== V3: Score au poids des cases  =========================================#
#==========================================================================================================#
############################################################################################################

tableauPoids = [
[500,-150,30,10,10,30,-150,500],
[-150,-250,0,0,0,0,-250,-150],
[30,0,1,2,2,1,0,30],
[10,0,2,16,16,2,0,10],
[10,0,2,16,16,2,0,10],
[30,0,1,2,2,1,0,30],
[-150,-250,0,0,0,0,-250,-150],
[500,-150,30,10,10,30,-150,500]]

def nombrePion (joueur,plat):
    score=0
    scoreAdversaire=0
    for i in range(0,len(plat)):
        for j in range(0,len(plat[i])):
            if plat[i][j]==joueur:
                score+=1
            elif plat[i][j]==("B" if joueur=="N" else "N"):
                scoreAdversaire+=1
    if scoreAdversaire==0:
        score=64
    return score


def score(joueur, plat):
    # Cette fonction doit retourner le score du joueur donné "N" ou "B"
    # Le score est défini comme le nombre de pions du joueur sur le plateau - le nombre de pions de l'adversaire

    score = 0
    scoreAdversaire=0
    for i in range ( 0, len(plat)):
        for j in range ( 0, len(plat[i])):
            if (plat[i][j] == joueur):
                score+=1
            elif (plat[i][j] == ("B" if joueur=="N" else "N")):
                scoreAdversaire+=1
    if scoreAdversaire==0:
        score=64
    return score - scoreAdversaire


def scorePoidsCase(joueur, plat):
    # Cette fonction doit retourner le score du joueur donné "N" ou "B"
    # Le score est défini comme le nombre de pions du joueur sur le plateau - le nombre de pions de l'adversaire, suivant le poids actif
    score = 0
    scoreAdversaire=0
    for i in range ( 0, len(plat)):
        for j in range ( 0, len(plat[i])):
            if (plat[i][j] == joueur):
                score+=tableauPoids[i][j]
            elif (plat[i][j] == ("B" if joueur=="N" else "N")):
                scoreAdversaire+=tableauPoids[i][j]
    if scoreAdversaire==0:
        score=0
        for i in range(0, len(plat)):
            for j in range(0,len(plat[i])):
                score+=tableauPoids[i][j]
    return score - scoreAdversaire

def scoreMobilite(joueur, plat): # peut rendre un entier négatif, positif ou nul
    # Cette fonction doit retourner le score du joueur donné "N" ou "B"
    # Le score est défini comme le nombre de coups possibles pour le joueur - le nombre de coups possibles pour l'adversaire
    score = 0
    scoreAdversaire=0
    for i in range ( 0, len(plat)):
        for j in range ( 0, len(plat[i])):
            if CoupAutorise(i,j,plat,joueur):#on verifie les coups possibles pour le joueur
                score+=1
                if (i,j) in [(0,0),(0,7),(7,0),(7,7)]:#on donne aux coins un poid plus important car ils sont avantageux pour le joueur
                    score+=10 
            #comme une case peut être jouable pour les deux joueurs, on ne met pas de elif, mais un if séparé pour vérifier les coups possibles pour l'adversaire
            if CoupAutorise(i,j,plat,"B" if joueur=="N" else "N"):#on verifie les coups possibles pour l'adversaire
                scoreAdversaire+=1
                if (i,j) in [(0,0),(0,7),(7,0),(7,7)]:# on donne aux coins un poid plus important
                    scoreAdversaire+=10
    return score - scoreAdversaire

def scoreMixte(joueur, plat):
    global pt
    if pt<20:
        return scorePoidsCase(joueur,plat)
    elif pt<50:
        return scoreMobilite(joueur,plat)
    else:
        return nombrePion(joueur,plat)
############################################################################################################
#==========================================================================================================#
#================================== V4: Algo Alpha-Beta  =========================================#
#==========================================================================================================#
############################################################################################################



def AlphaBetaMax(joueur, plateau, profondeur, alpha, beta,versionScore=1):
    global WhiteNumberOfNodes, WhiteNodesPerDepth, BlackNumberOfNodes, BlackNodesPerDepth
    if joueur=="B":
        WhiteNumberOfNodes+=1
        WhiteNodesPerDepth[profondeur-1]+=1
    else:
        BlackNodesPerDepth[profondeur-1]+=1
        BlackNumberOfNodes+=1
    # Cette fonction doit retourner le meilleur coup pour le joueur donné "N" ou "B"
    #utilise les algorithmes de minimax avec élagage alpha-beta pour déterminer le meilleur coup pour le joueur donné "N" ou "B"
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
    if joueur=="B":
        WhiteNumberOfNodes+=1
        WhiteNodesPerDepth[profondeur-1]+=1
    else:
        BlackNodesPerDepth[profondeur-1]+=1
        BlackNumberOfNodes+=1
    # Cette fonction doit retourner le meilleur coup pour le joueur donné "N" ou "B"
    #utilise les algorithmes de minimax avec élagage alpha-beta pour déterminer le meilleur coup pour le joueur donné "N" ou "B"
    plateauTemp = None
    bestCoup = (None,None)
    v = 0
    for i in range ( 0, len(plateau)):
        for j in range ( 0, len(plateau[i])):
            if CoupAutorise(i,j,plateau,"B" if joueur=="N" else "N"):
                #print("Coup autorisé pour i:"+str(i) + "et j : "+ str(j))
                plateauTemp=copy.deepcopy(plateau)
                PosePion(i,j,plateauTemp,"B" if joueur=="N" else "N") # fonction plaçant le pion du joueur sur le plateau temporaire
                _, v =  AlphaBetaMax(joueur, plateauTemp, profondeur-1, alpha, beta, versionScore)
                if bestCoup==(None,None):
                    bestCoup=(i,j)
                if v < beta :
                    beta = v
                    bestCoup = (i,j)
                if alpha >= beta:
                    return bestCoup, beta
    return bestCoup, beta




############################################################################################################
#==========================================================================================================#
#================================== V5: Monte-Carlo Algorithm  =========================================#
#==========================================================================================================#
############################################################################################################

#First version of the MonteCarlo algorithm, where each move is simulated during the lapse accorded, and we take the best score, all of that randomly :)
def getAllPossibleHit(plateau,joueur):
    PossibleHit=[]
    for i in range(0,8):
        for j in range(0,8):
            if CoupAutorise(i,j,plateau,joueur):
                PossibleHit.append([i,j])
    return PossibleHit


def MonteCarloMain(joueur,plateau,tempsSimulation):
    global WhiteNumberOfNodes, WhiteNodesPerDepth, BlackNumberOfNodes, BlackNodesPerDepth
    if joueur=="B":
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
        ActuelJoueur=("B" if joueur=="N" else "N")
        while True:
            if SimulationTimeElapsed==True:
                break
            PossibleHit=getAllPossibleHit(plat,ActuelJoueur)
            if len(PossibleHit)!=0:
                IndexPlayed=rand.randint(0,len(PossibleHit)-1)
            else:
                ActuelJoueur=("B" if ActuelJoueur=="N" else "N")    
                continue
            PosePion(PossibleHit[IndexPlayed][0],PossibleHit[IndexPlayed][1],plat,ActuelJoueur)
            ActuelJoueur=("B" if ActuelJoueur=="N" else "N")
            if isFinished(plat,True):
                scoreActuel+=score(joueur,plat)
                numberOfSimulation+=1
                break
    if numberOfSimulation!=0:
        if joueur=="B":
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

############################################################################################################
#==========================================================================================================#
#================================== V6: Random algorithm  =========================================#
#==========================================================================================================#
############################################################################################################
#Algorithm that make all of his choices RANDOMLY ! Used not for performance, but to check mostly the adaptability of each program

def randomPlay(plateau,joueur):
    global WhiteNumberOfNodes, WhiteNodesPerDepth, BlackNumberOfNodes, BlackNodesPerDepth
    if joueur=="B":
        WhiteNumberOfNodes+=1
    else:
        BlackNumberOfNodes+=1
    PossibleHit=getAllPossibleHit(plateau,joueur)
    if len(PossibleHit)!=0:
        IndexPlayed=rand.randint(0,len(PossibleHit)-1)
    return PossibleHit[IndexPlayed][0],PossibleHit[IndexPlayed][1]

#TestFonction()
#getResultat()

OthelloGame()
