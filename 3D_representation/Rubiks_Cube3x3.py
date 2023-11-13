from ursina import *

class Game:
    def __init__(self):
        self.ursina_instance = Ursina()
        self.init_game()

    def init_game(self):
        # window.fullscreen = True
        Entity(model='quad', scale=60, texture='white_cube', texture_scale=(60, 60), rotation_x=90, y=-5, color=color.light_gray)  # plane
        Entity(model='sphere', scale=100, texture='sky0', double_sided=True)  # sky
        EditorCamera()
        
        self.movimientos = []
        self.movimientos_show = []
        camera.world_position = (0, 0, -15)
        self.model, self.texture = 'custom_cube', 'rubik_texture'

        # * Botones
        # Crear botones para rotar las caras
        button_scale = (0.30, 0.05)
        button_color = color.azure
        button_spacing = 0.06  # Espacio vertical entre los botones
        
        # Define las posiciones de las capas internas
        self.MIDDLE_X = {Vec3(0, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.MIDDLE_Y = {Vec3(x, 0, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.MIDDLE_Z = {Vec3(x, y, 0) for x in range(-1, 2) for y in range(-1, 2)}

        # Botón para rotar la cara derecha
        self.rotate_right_button = Button(text="Rotate Right Face", color=button_color, scale=button_scale, position=(0.7, 0.2))
        self.rotate_right_button.on_click = self.rotate_right_face

        # Botón para rotar la cara izquierda
        self.rotate_left_button = Button(text="Rotate Left Face", color=button_color, scale=button_scale, position=(0.7, 0.2 - button_spacing))
        self.rotate_left_button.on_click = self.rotate_left_face

        # Botón para rotar la cara superior
        self.rotate_top_button = Button(text="Rotate Top Face", color=button_color, scale=button_scale, position=(0.7, 0.2 - 2 * button_spacing))
        self.rotate_top_button.on_click = self.rotate_top_face

        # Botón para rotar la cara inferior
        self.rotate_bottom_button = Button(text="Rotate Bottom Face", color=button_color, scale=button_scale, position=(0.7, 0.2 - 3 * button_spacing))
        self.rotate_bottom_button.on_click = self.rotate_bottom_face

        # Botón para rotar la cara frontal
        self.rotate_face_button = Button(text="Rotate Front Face", color=button_color, scale=button_scale, position=(0.7, 0.2 - 4 * button_spacing))
        self.rotate_face_button.on_click = self.rotate_face_front

        # Botón para rotar la cara trasera
        self.rotate_back_button = Button(text="Rotate Back Face", color=button_color, scale=button_scale, position=(0.7, 0.2 - 5 * button_spacing))
        self.rotate_back_button.on_click = self.rotate_back_face
        
        # Agrega botones para rotar las capas internas
        self.rotate_middle_x_button = Button(text="Rotate Middle X Layer", color=button_color, scale=button_scale, position=(0.7, 0.2 - 6 * button_spacing))
        self.rotate_middle_x_button.on_click = self.rotate_middle_x_layer

        self.rotate_middle_y_button = Button(text="Rotate Middle Y Layer", color=button_color, scale=button_scale, position=(0.7, 0.2 - 7 * button_spacing))
        self.rotate_middle_y_button.on_click = self.rotate_middle_y_layer

        self.rotate_middle_z_button = Button(text="Rotate Middle Z Layer", color=button_color, scale=button_scale, position=(0.7, 0.2 - 8 * button_spacing))
        self.rotate_middle_z_button.on_click = self.rotate_middle_z_layer
        
        self.shuffle_button = Button(text="Shuffle Cube", color=button_color, scale=button_scale, position=(0.7, 0.2 - 10 * button_spacing))
        self.shuffle_button.on_click = self.shuffle_cube
        
        # Botón para reiniciar el cubo
        self.reset_button = Button(text="Reset Cube", color=button_color, scale=button_scale, position=(0.7, 0.2 - 11 * button_spacing))
        self.reset_button.on_click = self.reset_cube
        
        # Resolver
        self.solve_button = Button(text="Solve", color=button_color, scale=button_scale, position=(0.7, 0.2 - 9 * button_spacing))
        self.solve_button.on_click = self.rotate_to_solve
        
        self.move_text = Text(text='', origin=(0, 15), color=color.black)
        
        self.load_game()
        
    def update_move_text(self):
        moves_text = ' '.join(self.movimientos_show)
        self.move_text.text = f"Moves: {moves_text}"
        
    def reset_cube(self):
        # Eliminar todas las entidades del cubo
        for cube in self.CUBES:
            destroy(cube)
        destroy(self.PARENT)

        # Restaurar el plano de fondo
        Entity(model='quad', scale=60, texture='white_cube', texture_scale=(60, 60), rotation_x=90, y=-5, color=color.light_gray)

        self.movimientos = []
        self.movimientos_show = []
        self.move_text.text = ""

        # Volver a cargar el juego
        self.load_game()
        
    def to_rubik_notation(self, move):
        rubik_notation = {
            'LEFT': 'L', 'RIGHT': 'R', 'TOP': 'U', 'BOTTOM': 'D', 'FRONT': 'F', 'BACK': 'B',
            'MIDDLE_X': 'M', 'MIDDLE_Y': 'E', 'MIDDLE_Z': 'S'
        }
        return rubik_notation.get(move, move)
        
    def shuffle_cube(self):
        # Barajar el cubo realizando movimientos aleatorios con retraso
        possible_moves = ['LEFT', 'RIGHT', 'TOP', 'BOTTOM', 'FRONT', 'BACK', 'MIDDLE_X', 'MIDDLE_Y', 'MIDDLE_Z']
        num_moves = 20  # Puedes ajustar la cantidad de movimientos aleatorios
        delay_between_moves = 0.5  # Ajusta el retraso entre movimientos
        
        def shuffle_recursive():
            nonlocal num_moves
            if num_moves > 0:
                random_move = random.choice(possible_moves)
                self.rotate_side(random_move)
                self.movimientos.append(random_move)
                self.movimientos_show.append(self.to_rubik_notation(random_move))
                num_moves -= 1
                invoke(shuffle_recursive, delay=delay_between_moves)
                self.update_move_text()

        shuffle_recursive()

    def rotate_right_face(self):
        self.rotate_side('RIGHT')
        self.movimientos.append('RIGHT')
        self.movimientos_show.append(self.to_rubik_notation('RIGHT'))
        self.update_move_text()

    def rotate_left_face(self):
        self.rotate_side('LEFT')
        self.movimientos.append('LEFT')
        self.movimientos_show.append(self.to_rubik_notation('LEFT'))
        self.update_move_text()

    def rotate_top_face(self):
        self.rotate_side('TOP')
        self.movimientos.append('TOP')
        self.movimientos_show.append(self.to_rubik_notation('TOP'))
        self.update_move_text()

    def rotate_bottom_face(self):
        self.rotate_side('BOTTOM')
        self.movimientos.append('BOTTOM')
        self.movimientos_show.append(self.to_rubik_notation('BOTTOM'))
        self.update_move_text()

    def rotate_face_front(self):
        self.rotate_side('FRONT')
        self.movimientos.append('FRONT')
        self.movimientos_show.append(self.to_rubik_notation('FRONT'))
        self.update_move_text()

    def rotate_back_face(self):
        self.rotate_side('BACK')
        self.movimientos.append('BACK')
        self.movimientos_show.append(self.to_rubik_notation('BACK'))
        self.update_move_text()

    def rotate_middle_x_layer(self):
        self.rotate_side('MIDDLE_X')
        self.movimientos.append('MIDDLE_X')
        self.movimientos_show.append(self.to_rubik_notation('MIDDLE_X'))
        self.update_move_text()

    def rotate_middle_y_layer(self):
        self.rotate_side('MIDDLE_Y')
        self.movimientos.append('MIDDLE_Y')
        self.movimientos_show.append(self.to_rubik_notation('MIDDLE_Y'))
        self.update_move_text()

    def rotate_middle_z_layer(self):
        self.rotate_side('MIDDLE_Z')
        self.movimientos.append('MIDDLE_Z')
        self.movimientos_show.append(self.to_rubik_notation('MIDDLE_Z'))
        self.update_move_text()
            
    
    def rotate_to_solve(self):
        reverse_movements = self.movimientos[::-1]
        delay_between_moves = self.animation_time + random.uniform(0.5, 1.5)
        # delay_between_moves = self.animation_time + 0.11  # Delay de la función rotate_side_2

        def solve_recursive():
            if reverse_movements:
                movement = reverse_movements.pop(0)
                self.rotate_side_2(movement)
                invoke(solve_recursive, delay=delay_between_moves)

        solve_recursive()
        self.movimientos = []
        self.movimientos_show = []
        self.move_text.text = ""
            
    def load_game(self):
        self.create_cube_positions()
        self.CUBES = [Entity(model=self.model, texture=self.texture, position=pos) for pos in self.SIDE_POSITIONS]
        self.PARENT = Entity()
        self.rotation_axes = {'LEFT': 'x', 'RIGHT': 'x', 'TOP': 'y', 'BOTTOM': 'y', 'FRONT': 'z', 'BACK': 'z', 'MIDDLE_X': 'x', 'MIDDLE_Y': 'y', 'MIDDLE_Z': 'z'}  # Asegúrate de incluir los ejes para las capas internas
        self.cubes_side_positons = {'LEFT': self.LEFT, 'BOTTOM': self.BOTTOM, 'RIGHT': self.RIGHT, 'FRONT': self.FRONT, 'BACK': self.BACK, 'TOP': self.TOP, 'MIDDLE_X': self.MIDDLE_X, 'MIDDLE_Y': self.MIDDLE_Y, 'MIDDLE_Z': self.MIDDLE_Z}  # Incluye las capas internas
        self.animation_time = 0.35
        self.action_trigger = True
        self.action_mode = True
        self.message = Text(origin=(0, 19), color=color.black)
        self.toggle_game_mode()
        self.create_sensors()
        # self.random_state(rotations=3) # initial state of the cube, rotations - number of side turns

    def random_state(self, rotations=3):
        [self.rotate_side_without_animation(random.choice(list(self.rotation_axes))) for i in range(rotations)]

    def rotate_side_without_animation(self, side_name):
        cube_positions = self.cubes_side_positons[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                exec(f'self.PARENT.rotation_{rotation_axis} = 90')

    def create_sensors(self):
        '''detectors for each side, for detecting collisions with mouse clicks'''
        create_sensor = lambda name, pos, scale: Entity(name=name, position=pos, model='cube', color=color.dark_gray,
                                                        scale=scale, collider='box', visible=False)
        self.LEFT_sensor = create_sensor(name='LEFT', pos=(-0.99, 0, 0), scale=(1.01, 3.01, 3.01))
        self.FACE_sensor = create_sensor(name='FRONT', pos=(0, 0, -0.99), scale=(3.01, 3.01, 1.01))
        self.BACK_sensor = create_sensor(name='BACK', pos=(0, 0, 0.99), scale=(3.01, 3.01, 1.01))
        self.RIGHT_sensor = create_sensor(name='RIGHT', pos=(0.99, 0, 0), scale=(1.01, 3.01, 3.01))
        self.TOP_sensor = create_sensor(name='TOP', pos=(0, 1, 0), scale=(3.01, 1.01, 3.01))
        self.BOTTOM_sensor = create_sensor(name='BOTTOM', pos=(0, -1, 0), scale=(3.01, 1.01, 3.01))
        self.MIDDLE_X_sensor = create_sensor(name='MIDDLE_X', pos=(0, 0, 0), scale=(3.01, 3.01, 3.01))
        self.MIDDLE_Y_sensor = create_sensor(name='MIDDLE_Y', pos=(0, 0, 0), scale=(3.01, 3.01, 3.01))
        self.MIDDLE_Z_sensor = create_sensor(name='MIDDLE_Z', pos=(0, 0, 0), scale=(3.01, 3.01, 3.01))

    def toggle_game_mode(self):
        '''switching view mode or interacting with Rubik's cube'''
        self.action_mode = not self.action_mode
        msg = dedent(f"{'ACTION mode ON' if self.action_mode else 'VIEW mode ON'}" f" (to switch - press middle mouse button)").strip()
        self.message.text = msg

    def toggle_animation_trigger(self):
        '''prohibiting side rotation during rotation animation'''
        self.action_trigger = not self.action_trigger

    def rotate_side(self, side_name):
        self.action_trigger = False
        cube_positions = self.cubes_side_positons[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                eval(f'self.PARENT.animate_rotation_{rotation_axis}(90, duration=self.animation_time)')
        invoke(self.toggle_animation_trigger, delay=self.animation_time + 0.11)
        
    def rotate_side_2(self, side_name):
        self.action_trigger = False
        cube_positions = self.cubes_side_positons[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                eval(f'self.PARENT.animate_rotation_{rotation_axis}(-90, duration=self.animation_time)')
        invoke(self.toggle_animation_trigger, delay=self.animation_time + 0.11)

    def reparent_to_scene(self):
        for cube in self.CUBES:
            if cube.parent == self.PARENT:
                world_pos, world_rot = round(cube.world_position, 1), cube.world_rotation
                cube.parent = scene
                cube.position, cube.rotation = world_pos, world_rot
        self.PARENT.rotation = 0

    def create_cube_positions(self):
        self.LEFT = {Vec3(-1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.BOTTOM = {Vec3(x, -1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.FRONT = {Vec3(x, y, -1) for x in range(-1, 2) for y in range(-1, 2)}
        self.BACK = {Vec3(x, y, 1) for x in range(-1, 2) for y in range(-1, 2)}
        self.RIGHT = {Vec3(1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.TOP = {Vec3(x, 1, z) for x in range(-1, 2) for z in range(-1, 2)}

        # Agrega las nuevas posiciones de las capas internas
        self.MIDDLE_X = {Vec3(0, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.MIDDLE_Y = {Vec3(x, 0, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.MIDDLE_Z = {Vec3(x, y, 0) for x in range(-1, 2) for y in range(-1, 2)}

        # Actualiza self.positions con todas las posiciones
        self.SIDE_POSITIONS = self.LEFT | self.BOTTOM | self.FRONT | self.BACK | self.RIGHT | self.TOP | self.MIDDLE_X | self.MIDDLE_Y | self.MIDDLE_Z

    def input(self, key):
        if key in 'mouse1 mouse3' and self.action_mode and self.action_trigger:
            for hitinfo in mouse.collisions:
                collider_name = hitinfo.entity.name
                if (key == 'mouse1' and collider_name in 'LEFT RIGHT FRONT BACK' or
                        key == 'mouse3' and collider_name in 'TOP BOTTOM'):
                    self.rotate_side(collider_name)
                    break
        if key == 'mouse2':
            self.toggle_game_mode()

        super().input(key)


if __name__ == '__main__':
    game = Game()
    game.ursina_instance.run()
