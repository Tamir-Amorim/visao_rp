
from typing import List


def guerra_dos_numeros(matriz: List[List[int]]):


    par = 0
    impar = 0

    for linha in matriz:
        for coluna in linha:
            if type(coluna) != int or coluna < 0:
                return "Essa função só recebe números inteiros positivos"

            if coluna % 2 == 0:
                par+=coluna
            else:
                impar+=coluna     

   
   #qual número maior
    if impar > par:
        return impar - par
    elif impar == par:  
        return 0
    else:
        return par - impar 
