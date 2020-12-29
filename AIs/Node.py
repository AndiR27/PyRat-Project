class Node:

    def __init__(self, coordonneeX: int, coordonneeY: int):

        self.__coordonneeX = coordonneeX
        self.__coordonneeY = coordonneeY
        # 5-10
        self.__value = str(coordonneeX) + "-" + str(coordonneeY)
        self.__cheese = False
        # dicoCout : dict = {down : 1} { clé = noeud : value = coût (si 0, alors c'est un mur}

    def __str__(self):
        return "x: " + str(self.__coordonneeX) + ", y: " + str(self.__coordonneeY)

    def get_X(self) -> int:
        return self.__coordonneeX

    def get_Y(self) -> int:
        return self.__coordonneeY

    def get_value(self):
        return self.__value

    def set_value(self, value):
        self.__value = value
        return self


    def have_prev(self) -> bool:
        return self.__prev is not None



    def get_fromage(self):
        return self.__cheese

    def set_fromage(self):
        self.__cheese = True

    def __eq__(self, other):
        return other == self.__value

    def __hash__(self):
        return hash(self.__coordonneeX) ^ hash(self.__coordonneeY)
