import numpy as np
import random

def animation_delay(level:str, mvmts = None):
    speed = 0
    mean_solving_time = 0 # 10 minutes
    std_deviation = 0 #  
    movimientos = 20 if mvmts is None else mvmts
    solved = 0

    print("average") if level == "a" else print("expert")

    if level == "a":
        while speed <= 0.30 or speed >= 30:
            mean_solving_time = 600 # 10 minuetes
            std_deviation = 300 

            solved = np.random.normal(mean_solving_time, std_deviation)
            speed = solved/movimientos
            
    elif level == "e":
        while (speed <= 0 or speed >= 5) or solved < 5:
            mean_solving_time = 5 # 10 minuetes
            std_deviation = 5 

            solved = np.random.normal(mean_solving_time, std_deviation)
            speed = solved/movimientos
            
#     print(f"speed: {movimientos}/")
    return speed, solved


def write_to_csv(cube_type, mvmts, time, player_type):
    
    with open("times.csv", '+a') as writer:
        writer.write(f"{cube_type}, {mvmts}, {time}, {player_type}\n")

        writer.close()


def gen_data():

    # options
    cube_types = ["3x3", "3x3V2", "floppy", "2x2"]
    player_types = ["a", "e"]
    ct = random.choice(cube_types)
    pt = random.choice(player_types)

    moves = 0

    if ct == "3x3" or ct == "3x3V2":
        moves = int(np.random.normal(20, 5))

    elif ct == "floppy":
        moves = int(np.random.normal(5, 1))

    elif ct == "2x2":
        moves = int(np.random.normal(15, 3))

    _, Stime = animation_delay(pt, moves)

    write_to_csv(ct, moves, Stime, pt)


# for _ in range(500):
#     gen_data()



