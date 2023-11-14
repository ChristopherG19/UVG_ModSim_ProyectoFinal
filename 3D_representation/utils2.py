import numpy as np

def animation_delay(level:str):
    speed = 0
    mean_solving_time = 0 # 10 minutes
    std_deviation = 0 #  
    movimientos = 20

    print("average") if level == "a" else print("expert")

    if level == "a":
        while speed <= 0.30 or speed >= 30:
            mean_solving_time = 600 # 10 minuetes
            std_deviation = 300 

            solved = np.random.normal(mean_solving_time, std_deviation)
            speed = solved/movimientos
            
    elif level == "e":
        while speed <= 0 or speed >= 5 or solved > 5:
            mean_solving_time = 5 # 10 minuetes
            std_deviation = 5 

            solved = np.random.normal(mean_solving_time, std_deviation)
            speed = solved/movimientos
            
#     print(f"speed: {movimientos}/")
    return speed

# res = animation_delay("e")
# print(res)
