import math


# Class Morpion gérant l'ensemble de jeu Morpion
class Morpion:

    # Initialisation du Morpion :
    # - state pour l'état courant du Morpion
    # - human pour indiquer si c'est joueur vs IA
    # - currentPlayer pour indiquer le joueur qui joue (X ou O). None si c'est Joueur vs IA car on laisse l'humain choisir son joueur (X ou Y)
    def __init__(self, state, human=None, player=None):
        self.state = state
        self.human = human
        self.currentPlayer = player

    # Récupérer le boolean qui détermnine si c'est un humain qui joue.
    def get_human(self):
        return self.human

    def set_human(self, human):
        self.human = human

    # Récupérer le player courant.
    def get_currentPlayer(self):
        return self.currentPlayer

    # Modifier le player courant.
    def set_currentPlayer(self, player):
        self.currentPlayer = player

    # Récupérer l'état courant.
    def get_state(self):
        return self.state

    # Modifier l'état courant en lui passant un tuple de coordonnées et la valeur à y mettre.
    def set_state(self, key, value):
        self.state[key[0]][key[1]] = value

    # Vérifier si le Morpion à l'état courant est vide.
    def empty(self):
        for line in self.get_state():
            for value in line:
                if value == '_':
                    return True
        return False

    # Vérifier si le Morpion à un état courant correspond à un état final.
    def finalState(self):
        for i in range(len(self.state)):

            # Vérifier si tous les emplacements, pour une ligne du Morpion à un état courant, ont la même valeur.
            if self.state[i][0] == self.state[i][1] == self.state[i][2]:
                if self.state[i][0] == 'X':
                    return 1
                elif self.state[i][0] == 'O':
                    return -1

            # Vérifier si tous les emplacements, pour une colonne du Morpion à un état courant, ont la même valeur.
            if self.state[0][i] == self.state[1][i] == self.state[2][i]:
                if self.state[0][i] == 'X':
                    return 1
                elif self.state[0][i] == 'O':
                    return -1

        # Vérifier si tous les emplacements, pour la diagonale gauche du Morpion à un état courant, ont la même valeur.
        if self.state[0][0] == self.state[1][1] == self.state[2][2]:
            if self.state[0][0] == 'X':
                return 1
            elif self.state[0][0] == 'O':
                return -1

        # Vérifier si tous les emplacements, pour la diagonale droite du Morpion à un état courant, ont la même valeur.
        if self.state[0][2] == self.state[1][1] == self.state[2][0]:
            if self.state[0][2] == 'X':
                return 1
            elif self.state[0][2] == 'O':
                return -1

        # Vérifier s'il n'y a plus de cases vides mais que l'on a pas de gagnant
        if not self.empty():
            return 0
        return None

    # Lister les emplacements libres d'un Morpion à l'état courant.
    # Ils sont listés sous forme de tuple (coordonées) et renvoyer.
    def actions(self):
        actions = []
        for x in range(len(self.get_state())):
            for y in range(len(self.get_state()[0])):
                if self.state[x][y] == '_':
                    actions.append((x, y))
        return actions

    # Trouver le meilleur déplacement à faire
    def findAction(self):

        # Exécuter l'algorithme miniMax si on est le joueur est X (Max) afin de trouver la meilleur action possible
        if self.get_currentPlayer() == 'X':
            bestValue = -math.inf
            for action in self.actions():
                if self.state[action[0]][action[1]] == '_':
                    self.set_state(action, 'X')
                    self.set_currentPlayer('O')
                    score = self.miniMax(0)
                    self.set_state(action, '_')
                    if score > bestValue:
                        bestValue = score
                        bestMove = action
            return [bestMove, 'X']

        # Exécuter l'algorithme miniMax si on est le joueur est O (Min) afin de trouver la meilleur action possible
        else:
            bestValue = math.inf
            for action in self.actions():
                if self.state[action[0]][action[1]] == '_':
                    self.set_state(action, 'O')
                    self.set_currentPlayer('X')
                    score = self.miniMax(0)
                    self.set_state(action, '_')
                    if score < bestValue:
                        bestValue = score
                        bestMove = action
            return [bestMove, 'O']

    # Dessiner chaque état du Morpion
    def drawGame(self):
        for i in range(len(self.get_state())):
            for j in range(len(self.get_state())):
                print('{}|'.format(self.get_state()[i][j]), end=" ")
            print('\n')
        print('\n')

    # Algorithme MiniMax :
    def miniMax(self, depth):

        # Vérifier si on est pas dans un état final
        if self.finalState() is not None:
            return self.finalState()

        # Exécuter l'algorithme récursivement si on est le joueur est X (Max) et trouver le meilleur Score
        if self.get_currentPlayer() == 'X':
            bestScore = -math.inf
            for action in self.actions():
                self.set_state(action, 'X')
                self.set_currentPlayer('O')
                score = self.miniMax(depth + 1)
                self.set_state(action, '_')
                bestScore = (max(bestScore, score))
            return bestScore
        else:
            # Exécuter l'algorithme récursivement si on est le joueur est O (Min) et trouver le meilleur Score
            bestScore = math.inf
            for action in self.actions():
                self.set_state(action, 'O')
                self.set_currentPlayer('X')
                score = self.miniMax(depth + 1)
                self.set_state(action, '_')
                bestScore = (min(bestScore, score))
            return bestScore

    # Vérifier si un joueur peut rentrer une valeur à un emplacement défini dans le Morpion.
    def checkState(self, key):
        if self.state[key[0]][key[1]] == '_':
            return True
        else:
            return False

    # Vérifier si un joueur veut jouer sinon deux IA s'affrontent
    def checkPlayer(self):
        gameType = input('Do you want to play ? (yes or no) :')
        if gameType == 'yes':
            return True
        elif gameType == 'no':
            return False
        else:
            print('Entrez un choix valide !')
            self.checkPlayer(gameType)

    # Vérifier quel IA on fait commencer en premier (X ou O)
    def checkIA(self):
        iaStart = input('Qui commence en premier : (X ou O)')
        if iaStart == 'X' or iaStart == 'O':
            self.set_currentPlayer(iaStart)
        else:
            print('Entrez un choix valide !')
            self.checkIA()

    # Premettre à un joueur de jouer au Morpion contre une IA
    # Récupérer la position que rentre le joueur et insérer sa valeur si la position est valide
    def playHuman(self):
        x = int(input("Enter absciss :  "))
        y = int(input("Enter ordinate :  "))
        if self.checkState((x, y)):
            if self.get_currentPlayer() == 'X':
                return [(x, y), 'X', 'O']
            else:
                return [(x, y), 'O', 'X']
        else:
            print('Enter valide coordinates ! \n')
            self.playHuman()

    # Exécuter le jeu et remplir le Morpion en fonction des déplacements trouvés.
    # Lancer le jeu de manière différente si c'est IA vs IA ou Joueur vs IA
    def game(self):

        if self.human:
            playerChoose = input('Choose your player X ou O:')
            humanPlayer = playerChoose
            self.currentPlayer = playerChoose
            while True:
                self.drawGame()

                result = self.finalState()
                if result is not None:
                    if result == 1:
                        print('X a gagné !')
                    elif result == -1:
                        print('O a gagné !')
                    elif result == 0:
                        print('Match nul ! ')
                    return

                if humanPlayer == self.get_currentPlayer():
                    move = self.playHuman()
                    self.set_state(move[0], move[1])
                    self.set_currentPlayer(move[2])
                else:
                    if self.get_currentPlayer() == 'X':
                        move = self.findAction()
                        self.set_state(move[0], move[1])
                        self.set_currentPlayer('O')
                    else:
                        move = self.findAction()
                        self.set_state(move[0], move[1])
                        self.set_currentPlayer('X')
        else:
            self.checkIA()
            while True:
                self.drawGame()

                result = self.finalState()
                if result is not None:
                    if result == 1:
                        print('X a gagné !')
                    elif result == -1:
                        print('O a gagné !')
                    elif result == 0:
                        print('Match nul ! ')
                    return
                if self.get_currentPlayer() == 'X':
                    move = self.findAction()
                    self.set_state(move[0], move[1])
                    self.set_currentPlayer('O')
                else:
                    move = self.findAction()
                    self.set_state(move[0], move[1])
                    self.set_currentPlayer('X')


# Main du programme afin de lancer le Morpion
def main():
    morpion = Morpion([['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']])
    morpion.set_human(morpion.checkPlayer())
    morpion.game()

# Exécuter le main
if __name__ == "__main__":
    main()
