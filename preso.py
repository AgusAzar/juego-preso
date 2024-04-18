import numpy as np
import pickle
probabilidadDados = np.zeros(13,np.float32)
memo = {}

def llenar_probabilidad_memo():
    numeros = np.arange(1,10)
    for i in range(1,7):
        for j in range(i,7):
            buscar_mejor_eleccion(numeros, (i+j))

def llenar_probabilidad_dados():
    for i in range(1,7):
        for j in range(i,7):
            probabilidadDados[i+j] += 1/36

def puedo_formar_con_numeros(numeros,un_valor):
    for i in numeros:
        for j in numeros:
            if i != j and i+j == un_valor: return True
    return False

def calcular_esperanza_de_los_numeros(numeros):
    print("calculando esperanza para", numeros)
    if numeros.shape[0] == 0:
        return -10
    else:
        esperanza = 0
        for i in range(1,13):
            if not puedo_formar_con_numeros(numeros,i):
                esperanza += probabilidadDados[i] * np.sum(numeros)
            else:
                esperanza_i,n1,n2 = buscar_mejor_eleccion(numeros,i)
                esperanza += probabilidadDados[i] * esperanza_i
        return esperanza


def buscar_mejor_eleccion(numeros, valor):
    key = (tuple(numeros),valor)
    if not memo.get(key):
        esperanza_minima = float("inf")
        primer_numero_a_tachar = 0
        segundo_numero_a_tachar = 0
        for primer_numero in numeros:
            if primer_numero == valor:
                esperanza = calcular_esperanza_de_los_numeros(np.delete(numeros, np.where(numeros==valor)))
                if esperanza < esperanza_minima:
                    esperanza_minima = esperanza
                    primer_numero_a_tachar = primer_numero
                    segundo_numero_a_tachar = 0
            for segundo_numero in numeros:
                if primer_numero < segundo_numero and primer_numero+segundo_numero == valor:
                    esperanza = calcular_esperanza_de_los_numeros(np.setdiff1d(numeros,[primer_numero,segundo_numero]))
                    if esperanza < esperanza_minima:
                        esperanza_minima = esperanza
                        primer_numero_a_tachar = primer_numero
                        segundo_numero_a_tachar = segundo_numero
        memo[key] = (esperanza_minima,primer_numero_a_tachar,segundo_numero_a_tachar)
    return memo.get(key)

def main():
    global memo
    llenar_probabilidad_dados()
    numeros = np.arange(1,10)
    try:
        with open('esperanza.json','rb') as file:
            memo = pickle.load(file)
    except:
        memo = {}
    if not memo:
        llenar_probabilidad_memo()
        print("esperanza calculada")
        with open('esperanza.json','wb') as file:
            pickle.dump(memo,file)
    perdiste = False
    print("Jugando al Preso")
    while not perdiste:
        print("Ingrese la suma del dado:")
        suma = input()
        _,primer_numero_a_tachar,segundo_numero_a_tachar = buscar_mejor_eleccion(numeros,int(suma))
        numeros = np.setdiff1d(numeros,[primer_numero_a_tachar,segundo_numero_a_tachar])
        if primer_numero_a_tachar == segundo_numero_a_tachar == 0:
            perdiste = True
        else:
            print(f'Tache el {primer_numero_a_tachar} y el {segundo_numero_a_tachar}')
    print("perdiste")
    print("sumas: ", sum(numeros))
if __name__ == "__main__":
    main()
