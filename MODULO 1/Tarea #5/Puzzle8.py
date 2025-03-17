#Ayon Zazueta Christian Natanael

import heapq

def resoluble(tablero):
    elementos = [num for fila in tablero for num in fila if num != 0]
    inversiones = 0
    for i in range(len(elementos)):
        for j in range(i + 1, len(elementos)):
            if elementos[i] > elementos[j]:
                inversiones += 1
    return inversiones % 2 == 0

def heuristica(estado):
    Pos_Obj = {
        1: (0, 0),
        2: (0, 1),
        3: (0, 2),
        4: (1, 0),
        0: (1, 1),
        5: (1, 2),
        6: (2, 0),
        7: (2, 1),
        8: (2, 2)
    }
    h = 0
    for fila in range(3):
        for columna in range(3):
            numero = estado[fila][columna]
            if numero != 0:
                fila_obj, col_obj = Pos_Obj[numero]
                h += abs(fila - fila_obj) + abs(columna - col_obj)
    return h

def encontrar_vacio(estado):
    for fila in range(3):
        for columna in range(3):
            if estado[fila][columna] == 0:
                return (fila, columna)
    return None

def obtener_estados_siguientes(estado):
    direcciones = [
        ('ARRIBA', -1, 0),
        ('ABAJO', 1, 0),
        ('IZQUIERDA', 0, -1),
        ('DERECHA', 0, 1)
    ]
    fila_emp, column_emp = encontrar_vacio(estado)
    sig_estd = []
    
    for movimiento, d_fila, d_column in direcciones:
        nueva_fila = fila_emp + d_fila
        nueva_columna = column_emp + d_column
        
        if 0 <= nueva_fila < 3 and 0 <= nueva_columna < 3:
            copia_estd = [list(fila) for fila in estado]
            copia_estd[fila_emp][column_emp], copia_estd[nueva_fila][nueva_columna] = copia_estd[nueva_fila][nueva_columna], copia_estd[fila_emp][column_emp]
            nuevo_estd = tuple(tuple(fila) for fila in copia_estd)
            sig_estd.append((nuevo_estd, movimiento))
    
    return sig_estd

def aplicar_movimiento(estado, movimiento):
    direcciones = {
        'ARRIBA': (-1, 0),
        'ABAJO': (1, 0),
        'IZQUIERDA': (0, -1),
        'DERECHA': (0, 1)
    }
    d_fila, d_column = direcciones[movimiento]
    fila_emp, column_emp = encontrar_vacio(estado)
    
    nueva_fila = fila_emp + d_fila
    nueva_columna = column_emp + d_column
    
    if 0 <= nueva_fila < 3 and 0 <= nueva_columna < 3:
        copia_estd = [list(fila) for fila in estado]
        copia_estd[fila_emp][column_emp], copia_estd[nueva_fila][nueva_columna] = copia_estd[nueva_fila][nueva_columna], copia_estd[fila_emp][column_emp]
        return tuple(tuple(fila) for fila in copia_estd)
    else:
        raise ValueError("Movimiento inválido")

def imprimir_puzzle(estado):
    for fila in estado:
        print(" ".join(str(num) if num != 0 else ' ' for num in fila))
    print()

def resolver_puzzle(estado_inicial):
    objetivo = (
        (1, 2, 3),
        (4, 0, 5),
        (6, 7, 8)
    )
    tupla_inicial = tuple(tuple(fila) for fila in estado_inicial)
    
    if tupla_inicial == objetivo:
        return []
    if not resoluble(estado_inicial):
        return None
    
    monticulo = []
    heapq.heappush(monticulo, (
        heuristica(tupla_inicial),
        0,
        heuristica(tupla_inicial),
        tupla_inicial,
        []
    ))
    visitados = set()
    
    while monticulo:
        costo_total, costo_real, heuristica_val, estado_actual, ruta = heapq.heappop(monticulo)
        
        if estado_actual == objetivo:
            return ruta
        if estado_actual in visitados:
            continue
        visitados.add(estado_actual)
        
        for estado_siguiente, movimiento in obtener_estados_siguientes(estado_actual):
            if estado_siguiente not in visitados:
                nuevo_costo_real = costo_real + 1
                nueva_heuristica = heuristica(estado_siguiente)
                nuevo_costo_total = nuevo_costo_real + nueva_heuristica
                heapq.heappush(monticulo, (
                    nuevo_costo_total,
                    nuevo_costo_real,
                    nueva_heuristica,
                    estado_siguiente,
                    ruta + [movimiento]
                ))
    
    return None

if __name__ == "__main__":
    estado_inicial = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]
    ]
    
    solucion = resolver_puzzle(estado_inicial)
    
    if solucion is not None:

        print("\nReconstrucción de los pasos:")
        
        estado_actual = tuple(tuple(fila) for fila in estado_inicial)
        
        for paso, movimiento in enumerate(solucion, 1):
            estado_actual = aplicar_movimiento(estado_actual, movimiento)
            print(f"Paso {paso}: {movimiento}")
            imprimir_puzzle(estado_actual)
    else:
        print("El puzzle no tiene solución.")