# Crear un cubo de Rubik con colores
rubik_cube = [
    # Cara Blanca (Top)
    [
        [0,0,0], [0,0,1], [0,0,2],    
        [0,1,0], [0,1,1], [0,1,2],    
        [0,2,0], [0,2,1], [0,2,2]    
    ],
    # Cara Verde (Left)
    [
        [1,0,0], [1,0,1], [1,0,2],    
        [1,1,0], [1,1,1], [1,1,2],    
        [1,2,0], [1,2,1], [1,2,2]    
    ],
    # Cara Roja (Front)
    [
        [2,0,0], [2,0,1], [2,0,2],    
        [2,1,0], [2,1,1], [2,1,2],    
        [2,2,0], [2,2,1], [2,2,2]    
    ],
    # Cara Azul (Right)
    [
        [3,0,0], [3,0,1], [3,0,2],    
        [3,1,0], [3,1,1], [3,1,2],    
        [3,2,0], [3,2,1], [3,2,2]    
    ],
    # Cara Anaranjada (Back)
    [
        [4,0,0], [4,0,1], [4,0,2],    
        [4,1,0], [4,1,1], [4,1,2],    
        [4,2,0], [4,2,1], [4,2,2]    
    ],
    # Cara Amarilla (Bottom)
    [
        [5,0,0], [5,0,1], [5,0,2],    
        [5,1,0], [5,1,1], [5,1,2],    
        [5,2,0], [5,2,1], [5,2,2]    
    ]
]

colors = {0: 'Blanco', 1: 'Verde', 2: 'Roja', 3: 'Azul', 4: 'Anaranjada', 5: 'Amarilla'}

# Función para identificar si una pieza es un centro
def es_centro(coords):
    x, y, z = coords
    return (y == 1 and z == 1)

# Función para identificar si una pieza es una arista
def es_arista(coords):
    x, y, z = coords
    return (
        (y == 1 or z == 1) and
        not es_centro(coords)
    )

# Función para identificar si una pieza es una esquina
def es_esquina(coords):
    x, y, z = coords
    return (
        (y == 0 or y == 2) and
        (z == 0 or z == 2) and
        not es_centro(coords) and not es_arista(coords)
    )

# Identificar las piezas en el cubo
for x in range(6):
    for y in range(3):
        for z in range(3):
            coords = (x, y, z)
            if es_centro(coords):
                print(f"Centro {coords}: {colors[x]}")
            elif es_arista(coords):
                print(f"Arista {coords}: {colors[x]}")
            elif es_esquina(coords):
                print(f"Esquina {coords}: {colors[x]}")
    print()