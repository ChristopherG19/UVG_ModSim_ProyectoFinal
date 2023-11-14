class Point:
    """A 3D point/vector"""

    def __init__(self, x, y=None, z=None):
        """Construct a Point from an (x, y, z) tuple or an iterable"""
        try:
            # convert from an iterable
            ii = iter(x)
            self.x = next(ii)
            self.y = next(ii)
            self.z = next(ii)
        except TypeError:
            # not iterable
            self.x = x
            self.y = y
            self.z = z
        if any(val is None for val in self):
            raise ValueError(f"Point does not allow None values: {self}")

    def __str__(self):
        return str(tuple(self))

    def __repr__(self):
        return "Point" + str(self)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other, self.z * other)

    def dot(self, other):
        """Return the dot product"""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Point(self.y * other.z - self.z * other.y,
                     self.z * other.x - self.x * other.z,
                     self.x * other.y - self.y * other.x)

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z
        raise IndexError("Point index out of range")

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def count(self, val):
        return int(self.x == val) + int(self.y == val) + int(self.z == val)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __eq__(self, other):
        if isinstance(other, (tuple, list)):
            return self.x == other[0] and self.y == other[1] and self.z == other[2]
        return (isinstance(other, self.__class__) and self.x == other.x
                and self.y == other.y and self.z == other.z)

    def __ne__(self, other):
        return not (self == other)


class Matrix:
    """A 3x3 matrix"""

    def __init__(self, *args):
        """Matrix(1, 2, 3, 4, 5, 6, 7, 8, 9)
        Matrix([1, 2, 3, 4, 5, 6, 7, 8, 9])
        Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        Matrix(x for x in range(1, 10))
        """
        if len(args) == 9:
            self.vals = list(args)
        elif len(args) == 3:
            try:
                self.vals = [x for y in args for x in y]
            except Exception:
                self.vals = []
        else:
            self.__init__(*args[0])

        if len(self.vals) != 9:
            raise ValueError(f"Matrix requires 9 items, got {args}")

    def __str__(self):
        return ("[{}, {}, {},\n"
                " {}, {}, {},\n"
                " {}, {}, {}]".format(*self.vals))

    def __repr__(self):
        return ("Matrix({}, {}, {},\n"
                "       {}, {}, {},\n"
                "       {}, {}, {})".format(*self.vals))

    def __eq__(self, other):
        return self.vals == other.vals

    def __add__(self, other):
        return Matrix(a + b for a, b in zip(self.vals, other.vals))

    def __sub__(self, other):
        return Matrix(a - b for a, b in zip(self.vals, other.vals))

    def __iadd__(self, other):
        self.vals = [a + b for a, b in zip(self.vals, other.vals)]
        return self

    def __isub__(self, other):
        self.vals = [a - b for a, b in zip(self.vals, other.vals)]
        return self

    def __mul__(self, other):
        """Do Matrix-Matrix or Matrix-Point multiplication."""
        if isinstance(other, Point):
            return Point(other.dot(Point(row)) for row in self.rows())
        elif isinstance(other, Matrix):
            return Matrix(Point(row).dot(Point(col)) for row in self.rows() for col in other.cols())

    def rows(self):
        yield self.vals[0:3]
        yield self.vals[3:6]
        yield self.vals[6:9]

    def cols(self):
        yield self.vals[0:9:3]
        yield self.vals[1:9:3]
        yield self.vals[2:9:3]
        
import string

RIGHT = X_AXIS = Point(1, 0, 0)
LEFT           = Point(-1, 0, 0)
UP    = Y_AXIS = Point(0, 1, 0)
DOWN           = Point(0, -1, 0)
FRONT = Z_AXIS = Point(0, 0, 1)
BACK           = Point(0, 0, -1)

FACE = 'face'
EDGE = 'edge'
CORNER = 'corner'


# 90 degree rotations in the XY plane. CW is clockwise, CC is counter-clockwise.
ROT_XY_CW = Matrix(0, 1, 0,
                   -1, 0, 0,
                   0, 0, 1)
ROT_XY_CC = Matrix(0, -1, 0,
                   1, 0, 0,
                   0, 0, 1)

# 90 degree rotations in the XZ plane (around the y-axis when viewed pointing toward you).
ROT_XZ_CW = Matrix(0, 0, -1,
                   0, 1, 0,
                   1, 0, 0)
ROT_XZ_CC = Matrix(0, 0, 1,
                   0, 1, 0,
                   -1, 0, 0)

# 90 degree rotations in the YZ plane (around the x-axis when viewed pointing toward you).
ROT_YZ_CW = Matrix(1, 0, 0,
                   0, 0, 1,
                   0, -1, 0)
ROT_YZ_CC = Matrix(1, 0, 0,
                   0, 0, -1,
                   0, 1, 0)


def get_rot_from_face(face):
    """
    :param face: One of FRONT, BACK, LEFT, RIGHT, UP, DOWN
    :return: A pair (CW, CC) given the clockwise and counterclockwise rotations for that face
    """
    if face == RIGHT:   return "R", "Ri"
    elif face == LEFT:  return "L", "Li"
    elif face == UP:    return "U", "Ui"
    elif face == DOWN:  return "D", "Di"
    elif face == FRONT: return "F", "Fi"
    elif face == BACK:  return "B", "Bi"
    return None


class Piece:

    def __init__(self, pos, colors):
        """
        :param pos: A tuple of integers (x, y, z) each ranging from -1 to 1
        :param colors: A tuple of length three (x, y, z) where each component gives the color
            of the side of the piece on that axis (if it exists), or None.
        """
        assert all(type(x) == int and x in (-1, 0, 1) for x in pos)
        assert len(colors) == 3
        self.pos = pos
        self.colors = list(colors)
        self._set_piece_type()

    def __str__(self):
        colors = "".join(c for c in self.colors if c is not None)
        return f"({self.type}, {colors}, {self.pos})"

    def _set_piece_type(self):
        if self.colors.count(None) == 2:
            self.type = FACE
        elif self.colors.count(None) == 1:
            self.type = EDGE
        elif self.colors.count(None) == 0:
            self.type = CORNER
        else:
            raise ValueError(f"Must have 1, 2, or 3 colors - given colors={self.colors}")

    def rotate(self, matrix):
        """Apply the given rotation matrix to this piece."""
        before = self.pos
        self.pos = matrix * self.pos

        # we need to swap the positions of two things in self.colors so colors appear
        # on the correct faces. rot gives us the axes to swap between.
        rot = self.pos - before
        if not any(rot):
            return  # no change occurred
        if rot.count(0) == 2:
            rot += matrix * rot

        assert rot.count(0) == 1, (
            f"There is a bug in the Piece.rotate() method!"
            f"\nbefore: {before}"
            f"\nself.pos: {self.pos}"
            f"\nrot: {rot}"
        )

        i, j = (i for i, x in enumerate(rot) if x != 0)
        self.colors[i], self.colors[j] = self.colors[j], self.colors[i]


class Cube:
    """Stores Pieces which are addressed through an x-y-z coordinate system:
        -x is the LEFT direction, +x is the RIGHT direction
        -y is the DOWN direction, +y is the UP direction
        -z is the BACK direction, +z is the FRONT direction
    """

    def _from_cube(self, c):
        self.faces = [Piece(pos=Point(p.pos), colors=p.colors) for p in c.faces]
        self.edges = [Piece(pos=Point(p.pos), colors=p.colors) for p in c.edges]
        self.corners = [Piece(pos=Point(p.pos), colors=p.colors) for p in c.corners]
        self.pieces = self.faces + self.edges + self.corners

    def _assert_data(self):
        assert len(self.pieces) == 26
        assert all(p.type == FACE for p in self.faces)
        assert all(p.type == EDGE for p in self.edges)
        assert all(p.type == CORNER for p in self.corners)

    def __init__(self, cube_str):
        """
        cube_str looks like:
                UUU                       0  1  2
                UUU                       3  4  5
                UUU                       6  7  8
            LLL FFF RRR BBB      9 10 11 12 13 14 15 16 17 18 19 20
            LLL FFF RRR BBB     21 22 23 24 25 26 27 28 29 30 31 32
            LLL FFF RRR BBB     33 34 35 36 37 38 39 40 41 42 43 44
                DDD                      45 46 47
                DDD                      48 49 50
                DDD                      51 52 53
        Note that the back side is mirrored in the horizontal axis during unfolding.
        Each 'sticker' must be a single character.
        """
        if isinstance(cube_str, Cube):
            self._from_cube(cube_str)
            return

        cube_str = "".join(x for x in cube_str if x not in string.whitespace)
        import time
        
        print(cube_str)
        time.sleep(10)
        assert len(cube_str) == 54
        self.faces = (
            Piece(pos=RIGHT, colors=(cube_str[28], None, None)),
            Piece(pos=LEFT,  colors=(cube_str[22], None, None)),
            Piece(pos=UP,    colors=(None, cube_str[4],  None)),
            Piece(pos=DOWN,  colors=(None, cube_str[49], None)),
            Piece(pos=FRONT, colors=(None, None, cube_str[25])),
            Piece(pos=BACK,  colors=(None, None, cube_str[31])))
        self.edges = (
            Piece(pos=RIGHT + UP,    colors=(cube_str[16], cube_str[5], None)),
            Piece(pos=RIGHT + DOWN,  colors=(cube_str[40], cube_str[50], None)),
            Piece(pos=RIGHT + FRONT, colors=(cube_str[27], None, cube_str[26])),
            Piece(pos=RIGHT + BACK,  colors=(cube_str[29], None, cube_str[30])),
            Piece(pos=LEFT + UP,     colors=(cube_str[10], cube_str[3], None)),
            Piece(pos=LEFT + DOWN,   colors=(cube_str[34], cube_str[48], None)),
            Piece(pos=LEFT + FRONT,  colors=(cube_str[23], None, cube_str[24])),
            Piece(pos=LEFT + BACK,   colors=(cube_str[21], None, cube_str[32])),
            Piece(pos=UP + FRONT,    colors=(None, cube_str[7], cube_str[13])),
            Piece(pos=UP + BACK,     colors=(None, cube_str[1], cube_str[19])),
            Piece(pos=DOWN + FRONT,  colors=(None, cube_str[46], cube_str[37])),
            Piece(pos=DOWN + BACK,   colors=(None, cube_str[52], cube_str[43])),
        )
        self.corners = (
            Piece(pos=RIGHT + UP + FRONT,   colors=(cube_str[15], cube_str[8], cube_str[14])),
            Piece(pos=RIGHT + UP + BACK,    colors=(cube_str[17], cube_str[2], cube_str[18])),
            Piece(pos=RIGHT + DOWN + FRONT, colors=(cube_str[39], cube_str[47], cube_str[38])),
            Piece(pos=RIGHT + DOWN + BACK,  colors=(cube_str[41], cube_str[53], cube_str[42])),
            Piece(pos=LEFT + UP + FRONT,    colors=(cube_str[11], cube_str[6], cube_str[12])),
            Piece(pos=LEFT + UP + BACK,     colors=(cube_str[9], cube_str[0], cube_str[20])),
            Piece(pos=LEFT + DOWN + FRONT,  colors=(cube_str[35], cube_str[45], cube_str[36])),
            Piece(pos=LEFT + DOWN + BACK,   colors=(cube_str[33], cube_str[51], cube_str[44])),
        )

        self.pieces = self.faces + self.edges + self.corners

        self._assert_data()

    def is_solved(self):
        def check(colors):
            assert len(colors) == 9
            return all(c == colors[0] for c in colors)
        return (check([piece.colors[2] for piece in self._face(FRONT)]) and
                check([piece.colors[2] for piece in self._face(BACK)]) and
                check([piece.colors[1] for piece in self._face(UP)]) and
                check([piece.colors[1] for piece in self._face(DOWN)]) and
                check([piece.colors[0] for piece in self._face(LEFT)]) and
                check([piece.colors[0] for piece in self._face(RIGHT)]))

    def _face(self, axis):
        """
        :param axis: One of LEFT, RIGHT, UP, DOWN, FRONT, BACK
        :return: A list of Pieces on the given face
        """
        assert axis.count(0) == 2
        return [p for p in self.pieces if p.pos.dot(axis) > 0]

    def _slice(self, plane):
        """
        :param plane: A sum of any two of X_AXIS, Y_AXIS, Z_AXIS (e.g. X_AXIS + Y_AXIS)
        :return: A list of Pieces in the given plane
        """
        assert plane.count(0) == 1
        i = next((i for i, x in enumerate(plane) if x == 0))
        return [p for p in self.pieces if p.pos[i] == 0]

    def _rotate_face(self, face, matrix):
        self._rotate_pieces(self._face(face), matrix)

    def _rotate_slice(self, plane, matrix):
        self._rotate_pieces(self._slice(plane), matrix)

    def _rotate_pieces(self, pieces, matrix):
        for piece in pieces:
            piece.rotate(matrix)

    # Rubik's Cube Notation: http://ruwix.com/the-rubiks-cube/notation/
    def L(self):  self._rotate_face(LEFT, ROT_YZ_CC)
    def Li(self): self._rotate_face(LEFT, ROT_YZ_CW)
    def R(self):  self._rotate_face(RIGHT, ROT_YZ_CW)
    def Ri(self): self._rotate_face(RIGHT, ROT_YZ_CC)
    def U(self):  self._rotate_face(UP, ROT_XZ_CW)
    def Ui(self): self._rotate_face(UP, ROT_XZ_CC)
    def D(self):  self._rotate_face(DOWN, ROT_XZ_CC)
    def Di(self): self._rotate_face(DOWN, ROT_XZ_CW)
    def F(self):  self._rotate_face(FRONT, ROT_XY_CW)
    def Fi(self): self._rotate_face(FRONT, ROT_XY_CC)
    def B(self):  self._rotate_face(BACK, ROT_XY_CC)
    def Bi(self): self._rotate_face(BACK, ROT_XY_CW)
    def M(self):  self._rotate_slice(Y_AXIS + Z_AXIS, ROT_YZ_CC)
    def Mi(self): self._rotate_slice(Y_AXIS + Z_AXIS, ROT_YZ_CW)
    def E(self):  self._rotate_slice(X_AXIS + Z_AXIS, ROT_XZ_CC)
    def Ei(self): self._rotate_slice(X_AXIS + Z_AXIS, ROT_XZ_CW)
    def S(self):  self._rotate_slice(X_AXIS + Y_AXIS, ROT_XY_CW)
    def Si(self): self._rotate_slice(X_AXIS + Y_AXIS, ROT_XY_CC)
    def X(self):  self._rotate_pieces(self.pieces, ROT_YZ_CW)
    def Xi(self): self._rotate_pieces(self.pieces, ROT_YZ_CC)
    def Y(self):  self._rotate_pieces(self.pieces, ROT_XZ_CW)
    def Yi(self): self._rotate_pieces(self.pieces, ROT_XZ_CC)
    def Z(self):  self._rotate_pieces(self.pieces, ROT_XY_CW)
    def Zi(self): self._rotate_pieces(self.pieces, ROT_XY_CC)

    def sequence(self, move_str):
        """
        :param moves: A string containing notated moves separated by spaces: "L Ri U M Ui B M"
        """
        moves = [getattr(self, name) for name in move_str.split()]
        for move in moves:
            move()

    def find_piece(self, *colors):
        if None in colors:
            return
        for p in self.pieces:
            if p.colors.count(None) == 3 - len(colors) \
                and all(c in p.colors for c in colors):
                return p

    def get_piece(self, x, y, z):
        """
        :return: the Piece at the given Point
        """
        point = Point(x, y, z)
        for p in self.pieces:
            if p.pos == point:
                return p

    def __getitem__(self, *args):
        if len(args) == 1:
            return self.get_piece(*args[0])
        return self.get_piece(*args)

    def __eq__(self, other):
        return isinstance(other, Cube) and self._color_list() == other._color_list()

    def __ne__(self, other):
        return not (self == other)

    def colors(self):
        """
        :return: A set containing the colors of all stickers on the cube
        """
        return set(c for piece in self.pieces for c in piece.colors if c is not None)

    def left_color(self): return self[LEFT].colors[0]
    def right_color(self): return self[RIGHT].colors[0]
    def up_color(self): return self[UP].colors[1]
    def down_color(self): return self[DOWN].colors[1]
    def front_color(self): return self[FRONT].colors[2]
    def back_color(self): return self[BACK].colors[2]

    def _color_list(self):
        right = [p.colors[0] for p in sorted(self._face(RIGHT), key=lambda p: (-p.pos.y, -p.pos.z))]
        left  = [p.colors[0] for p in sorted(self._face(LEFT),  key=lambda p: (-p.pos.y, p.pos.z))]
        up    = [p.colors[1] for p in sorted(self._face(UP),    key=lambda p: (p.pos.z, p.pos.x))]
        down  = [p.colors[1] for p in sorted(self._face(DOWN),  key=lambda p: (-p.pos.z, p.pos.x))]
        front = [p.colors[2] for p in sorted(self._face(FRONT), key=lambda p: (-p.pos.y, p.pos.x))]
        back  = [p.colors[2] for p in sorted(self._face(BACK),  key=lambda p: (-p.pos.y, -p.pos.x))]

        return (up + left[0:3] + front[0:3] + right[0:3] + back[0:3]
                   + left[3:6] + front[3:6] + right[3:6] + back[3:6]
                   + left[6:9] + front[6:9] + right[6:9] + back[6:9] + down)

    def flat_str(self):
        return "".join(x for x in str(self) if x not in string.whitespace)

    def __str__(self):
        template = ("    {}{}{}\n"
                    "    {}{}{}\n"
                    "    {}{}{}\n"
                    "{}{}{} {}{}{} {}{}{} {}{}{}\n"
                    "{}{}{} {}{}{} {}{}{} {}{}{}\n"
                    "{}{}{} {}{}{} {}{}{} {}{}{}\n"
                    "    {}{}{}\n"
                    "    {}{}{}\n"
                    "    {}{}{}")

        return "    " + template.format(*self._color_list()).strip()


# if __name__ == '__main__':
#     cube = Cube("    DLU\n"
#                 "    RRD\n"
#                 "    FFU\n"
#                 "BBL DDR BRB LDL\n"
#                 "RBF RUU LFB DDU\n"
#                 "FBR BBR FUD FLU\n"
#                 "    DLU\n"
#                 "    ULF\n"
#                 "    LFR")
#     print(cube)

X_ROT_CW = {
    'U': 'F',
    'B': 'U',
    'D': 'B',
    'F': 'D',
    'E': 'Si',
    'S': 'E',
    'Y': 'Z',
    'Z': 'Yi',
}
Y_ROT_CW = {
    'B': 'L',
    'R': 'B',
    'F': 'R',
    'L': 'F',
    'S': 'Mi',
    'M': 'S',
    'Z': 'X',
    'X': 'Zi'
}
Z_ROT_CW = {
    'U': 'L',
    'R': 'U',
    'D': 'R',
    'L': 'D',
    'E': 'Mi',
    'M': 'E',
    'Y': 'Xi',
    'X': 'Y',
}
X_ROT_CC = {v: k for k, v in X_ROT_CW.items()}
Y_ROT_CC = {v: k for k, v in Y_ROT_CW.items()}
Z_ROT_CC = {v: k for k, v in Z_ROT_CW.items()}


def get_rot_table(rot):
    if rot == 'X': return X_ROT_CW
    elif rot == 'Xi': return X_ROT_CC
    elif rot == 'Y': return Y_ROT_CW
    elif rot == 'Yi': return Y_ROT_CC
    elif rot == 'Z': return Z_ROT_CW
    elif rot == 'Zi': return Z_ROT_CC


def _invert(move):
    if move.endswith('i'):
        return move[:1]
    return move + 'i'


def apply_repeat_three_optimization(moves):
    """ R, R, R --> Ri """
    changed = False
    i = 0
    while i < len(moves) - 2:
        if moves[i] == moves[i+1] == moves[i+2]:
            moves[i:i+3] = [_invert(moves[i])]
            changed = True
        else:
            i += 1
    if changed:
        apply_repeat_three_optimization(moves)


def apply_do_undo_optimization(moves):
    """ R Ri --> <nothing>, R R Ri Ri --> <nothing> """
    changed = False
    i = 0
    while i < len(moves) - 1:
        if _invert(moves[i]) == moves[i+1]:
            moves[i:i+2] = []
            changed = True
        else:
            i += 1
    if changed:
        apply_do_undo_optimization(moves)


def _unrotate(rot, moves):
    rot_table = get_rot_table(rot)
    result = []
    for move in moves:
        if move in rot_table:
            result.append(rot_table[move])
        elif _invert(move) in rot_table:
            result.append(_invert(rot_table[_invert(move)]))
        else:
            result.append(move)
    return result


def apply_no_full_cube_rotation_optimization(moves):
    rots = {'X', 'Y', 'Z', 'Xi', 'Yi', 'Zi'}
    changed = False
    i = 0
    while i < len(moves):
        if moves[i] not in rots:
            i += 1
            continue

        for j in reversed(range(i + 1, len(moves))):
            if moves[j] == _invert(moves[i]):
                moves[i:j+1] = _unrotate(moves[i], moves[i+1:j])
                changed = True
                break
        i += 1
    if changed:
        apply_no_full_cube_rotation_optimization(moves)


def optimize_moves(moves):
    result = list(moves)
    apply_no_full_cube_rotation_optimization(result)
    apply_repeat_three_optimization(result)
    apply_do_undo_optimization(result)
    return result

DEBUG = False

class Solver:

    def __init__(self, c):
        self.cube = c
        self.colors = c.colors()
        self.moves = []

        self.left_piece  = self.cube.find_piece(self.cube.left_color())
        self.right_piece = self.cube.find_piece(self.cube.right_color())
        self.up_piece    = self.cube.find_piece(self.cube.up_color())
        self.down_piece  = self.cube.find_piece(self.cube.down_color())

        self.inifinite_loop_max_iterations = 12

    def solve(self):
        if DEBUG: print(self.cube)
        self.cross()
        if DEBUG: print('Cross:\n', self.cube)
        self.cross_corners()
        if DEBUG: print('Corners:\n', self.cube)
        self.second_layer()
        if DEBUG: print('Second layer:\n', self.cube)
        self.back_face_edges()
        if DEBUG: print('Last layer edges\n', self.cube)
        self.last_layer_corners_position()
        if DEBUG: print('Last layer corners -- position\n', self.cube)
        self.last_layer_corners_orientation()
        if DEBUG: print('Last layer corners -- orientation\n', self.cube)
        self.last_layer_edges()
        if DEBUG: print('Solved\n', self.cube)

    def move(self, move_str):
        self.moves.extend(move_str.split())
        self.cube.sequence(move_str)

    def cross(self):
        if DEBUG: print("cross")
        # place the UP-LEFT piece
        fl_piece = self.cube.find_piece(self.cube.front_color(), self.cube.left_color())
        fr_piece = self.cube.find_piece(self.cube.front_color(), self.cube.right_color())
        fu_piece = self.cube.find_piece(self.cube.front_color(), self.cube.up_color())
        fd_piece = self.cube.find_piece(self.cube.front_color(), self.cube.down_color())

        self._cross_left_or_right(fl_piece, self.left_piece, self.cube.left_color(), "L L", "E L Ei Li")
        self._cross_left_or_right(fr_piece, self.right_piece, self.cube.right_color(), "R R", "Ei R E Ri")

        self.move("Z")
        self._cross_left_or_right(fd_piece, self.down_piece, self.cube.left_color(), "L L", "E L Ei Li")
        self._cross_left_or_right(fu_piece, self.up_piece, self.cube.right_color(), "R R", "Ei R E Ri")
        self.move("Zi")

    def _cross_left_or_right(self, edge_piece, face_piece, face_color, move_1, move_2):
        # don't do anything if piece is in correct place
        if (edge_piece.pos == (face_piece.pos.x, face_piece.pos.y, 1)
                and edge_piece.colors[2] == self.cube.front_color()):
            return

        # ensure piece is at z = -1
        undo_move = None
        if edge_piece.pos.z == 0:
            pos = Point(edge_piece.pos)
            pos.x = 0  # pick the UP or DOWN face
            cw, cc = get_rot_from_face(pos)

            if edge_piece.pos in (LEFT + UP, RIGHT + DOWN):
                self.move(cw)
                undo_move = cc
            else:
                self.move(cc)
                undo_move = cw
        elif edge_piece.pos.z == 1:
            pos = Point(edge_piece.pos)
            pos.z = 0
            cw, cc = get_rot_from_face(pos)
            self.move("{0} {0}".format(cc))
            # don't set the undo move if the piece starts out in the right position
            # (with wrong orientation) or we'll screw up the remainder of the algorithm
            if edge_piece.pos.x != face_piece.pos.x:
                undo_move = "{0} {0}".format(cw)

        assert edge_piece.pos.z == -1

        # piece is at z = -1, rotate to correct face (LEFT or RIGHT)
        count = 0
        while (edge_piece.pos.x, edge_piece.pos.y) != (face_piece.pos.x, face_piece.pos.y):
            self.move("B")
            count += 1
            if count >= self.inifinite_loop_max_iterations:
                raise Exception("Stuck in loop - unsolvable cube?\n" + str(self.cube))

        # if we moved a correctly-placed piece, restore it
        if undo_move:
            self.move(undo_move)

        # the piece is on the correct face on plane z = -1, but has two orientations
        if edge_piece.colors[0] == face_color:
            self.move(move_1)
        else:
            self.move(move_2)

    def cross_corners(self):
        if DEBUG: print("cross_corners")
        fld_piece = self.cube.find_piece(self.cube.front_color(), self.cube.left_color(), self.cube.down_color())
        flu_piece = self.cube.find_piece(self.cube.front_color(), self.cube.left_color(), self.cube.up_color())
        frd_piece = self.cube.find_piece(self.cube.front_color(), self.cube.right_color(), self.cube.down_color())
        fru_piece = self.cube.find_piece(self.cube.front_color(), self.cube.right_color(), self.cube.up_color())

        self.place_frd_corner(frd_piece, self.right_piece, self.down_piece, self.cube.front_color())
        self.move("Z")
        self.place_frd_corner(fru_piece, self.up_piece, self.right_piece, self.cube.front_color())
        self.move("Z")
        self.place_frd_corner(flu_piece, self.left_piece, self.up_piece, self.cube.front_color())
        self.move("Z")
        self.place_frd_corner(fld_piece, self.down_piece, self.left_piece, self.cube.front_color())
        self.move("Z")

    def place_frd_corner(self, corner_piece, right_piece, down_piece, front_color):
        # rotate to z = -1
        if corner_piece.pos.z == 1:
            pos = Point(corner_piece.pos)
            pos.x = pos.z = 0
            cw, cc = get_rot_from_face(pos)

            # be careful not to screw up other pieces on the front face
            count = 0
            undo_move = cc
            while corner_piece.pos.z != -1:
                self.move(cw)
                count += 1

            if count > 1:
                # go the other direction because I don't know which is which.
                # we need to do only one flip (net) or we'll move other
                # correctly-placed corners out of place.
                for _ in range(count):
                    self.move(cc)

                count = 0
                while corner_piece.pos.z != -1:
                    self.move(cc)
                    count += 1
                undo_move = cw
            self.move("B")
            for _ in range(count):
                self.move(undo_move)

        # rotate piece to be directly below its destination
        while (corner_piece.pos.x, corner_piece.pos.y) != (right_piece.pos.x, down_piece.pos.y):
            self.move("B")

        # there are three possible orientations for a corner
        if corner_piece.colors[0] == front_color:
            self.move("B D Bi Di")
        elif corner_piece.colors[1] == front_color:
            self.move("Bi Ri B R")
        else:
            self.move("Ri B B R Bi Bi D Bi Di")

    def second_layer(self):
        rd_piece = self.cube.find_piece(self.cube.right_color(), self.cube.down_color())
        ru_piece = self.cube.find_piece(self.cube.right_color(), self.cube.up_color())
        ld_piece = self.cube.find_piece(self.cube.left_color(), self.cube.down_color())
        lu_piece = self.cube.find_piece(self.cube.left_color(), self.cube.up_color())

        self.place_middle_layer_ld_edge(ld_piece, self.cube.left_color(), self.cube.down_color())
        self.move("Z")
        self.place_middle_layer_ld_edge(rd_piece, self.cube.left_color(), self.cube.down_color())
        self.move("Z")
        self.place_middle_layer_ld_edge(ru_piece, self.cube.left_color(), self.cube.down_color())
        self.move("Z")
        self.place_middle_layer_ld_edge(lu_piece, self.cube.left_color(), self.cube.down_color())
        self.move("Z")

    def place_middle_layer_ld_edge(self, ld_piece, left_color, down_color):
        # move to z == -1
        if ld_piece.pos.z == 0:
            count = 0
            while (ld_piece.pos.x, ld_piece.pos.y) != (-1, -1):
                self.move("Z")
                count += 1

            self.move("B L Bi Li Bi Di B D")
            for _ in range(count):
                self.move("Zi")

        assert ld_piece.pos.z == -1

        if ld_piece.colors[2] == left_color:
            # left_color is on the back face, move piece to to down face
            while ld_piece.pos.y != -1:
                self.move("B")
            self.move("B L Bi Li Bi Di B D")
        elif ld_piece.colors[2] == down_color:
            # down_color is on the back face, move to left face
            while ld_piece.pos.x != -1:
                self.move("B")
            self.move("Bi Di B D B L Bi Li")
        else:
            raise Exception("BUG!!")

    def back_face_edges(self):
        # rotate BACK to FRONT
        self.move("X X")

        # States:  1     2     3     4
        #         -B-   -B-   ---   ---
        #         BBB   BB-   BBB   -B-
        #         -B-   ---   ---   ---
        def state1():
            return (self.cube[0, 1, 1].colors[2] == self.cube.front_color() and
                    self.cube[-1, 0, 1].colors[2] == self.cube.front_color() and
                    self.cube[0, -1, 1].colors[2] == self.cube.front_color() and
                    self.cube[1, 0, 1].colors[2] == self.cube.front_color())

        def state2():
            return (self.cube[0, 1, 1].colors[2] == self.cube.front_color() and
                    self.cube[-1, 0, 1].colors[2] == self.cube.front_color())

        def state3():
            return (self.cube[-1, 0, 1].colors[2] == self.cube.front_color() and
                    self.cube[1, 0, 1].colors[2] == self.cube.front_color())

        def state4():
            return (self.cube[0, 1, 1].colors[2] != self.cube.front_color() and
                    self.cube[-1, 0, 1].colors[2] != self.cube.front_color() and
                    self.cube[0, -1, 1].colors[2] != self.cube.front_color() and
                    self.cube[1, 0, 1].colors[2] != self.cube.front_color())

        count = 0
        while not state1():
            if state4() or state2():
                self.move("D F R Fi Ri Di")
            elif state3():
                self.move("D R F Ri Fi Di")
            else:
                self.move("F")
            count += 1
            if count >= self.inifinite_loop_max_iterations:
                raise Exception("Stuck in loop - unsolvable cube\n" + str(self.cube))

        self.move("Xi Xi")

    def last_layer_corners_position(self):
        self.move("X X")
        # UP face:
        #  4-3
        #  ---
        #  2-1
        move_1 = "Li Fi L D F Di Li F L F F "  # swaps 1 and 2
        move_2 = "F Li Fi L D F Di Li F L F "  # swaps 1 and 3

        c1 = self.cube.find_piece(self.cube.front_color(), self.cube.right_color(), self.cube.down_color())
        c2 = self.cube.find_piece(self.cube.front_color(), self.cube.left_color(), self.cube.down_color())
        c3 = self.cube.find_piece(self.cube.front_color(), self.cube.right_color(), self.cube.up_color())
        c4 = self.cube.find_piece(self.cube.front_color(), self.cube.left_color(), self.cube.up_color())

        # place corner 4
        if c4.pos == Point(1, -1, 1):
            self.move(move_1 + "Zi " + move_1 + " Z")
        elif c4.pos == Point(1, 1, 1):
            self.move("Z " + move_2 + " Zi")
        elif c4.pos == Point(-1, -1, 1):
            self.move("Zi " + move_1 + " Z")
        assert c4.pos == Point(-1, 1, 1)

        # place corner 2
        if c2.pos == Point(1, 1, 1):
            self.move(move_2 + move_1)
        elif c2.pos == Point(1, -1, 1):
            self.move(move_1)
        assert c2.pos == Point(-1, -1, 1)

        # place corner 3 and corner 1
        if c3.pos == Point(1, -1, 1):
            self.move(move_2)
        assert c3.pos == Point(1, 1, 1)
        assert c1.pos == Point(1, -1, 1)

        self.move("Xi Xi")

    def last_layer_corners_orientation(self):
        self.move("X X")

        # States:  1        2      3      4      5      6      7      8
        #           B      B             B      B        B
        #         BB-      -B-B   BBB    -BB    -BB   B-B-   B-B-B   BBB
        #         BBB      BBB    BBB    BBB    BBB    BBB    BBB    BBB
        #         -B-B     BB-    -B-    -BB    BB-B  B-B-   B-B-B   BBB
        #         B          B    B B    B               B
        def state1():
            return (self.cube[ 1,  1, 1].colors[1] == self.cube.front_color() and
                    self.cube[-1, -1, 1].colors[1] == self.cube.front_color() and
                    self.cube[ 1, -1, 1].colors[0] == self.cube.front_color())

        def state2():
            return (self.cube[-1,  1, 1].colors[1] == self.cube.front_color() and
                    self.cube[ 1,  1, 1].colors[0] == self.cube.front_color() and
                    self.cube[ 1, -1, 1].colors[1] == self.cube.front_color())

        def state3():
            return (self.cube[-1, -1, 1].colors[1] == self.cube.front_color() and
                    self.cube[ 1, -1, 1].colors[1] == self.cube.front_color() and
                    self.cube[-1,  1, 1].colors[2] == self.cube.front_color() and
                    self.cube[ 1,  1, 1].colors[2] == self.cube.front_color())

        def state4():
            return (self.cube[-1,  1, 1].colors[1] == self.cube.front_color() and
                    self.cube[-1, -1, 1].colors[1] == self.cube.front_color() and
                    self.cube[ 1,  1, 1].colors[2] == self.cube.front_color() and
                    self.cube[ 1, -1, 1].colors[2] == self.cube.front_color())

        def state5():
            return (self.cube[-1,  1, 1].colors[1] == self.cube.front_color() and
                    self.cube[ 1, -1, 1].colors[0] == self.cube.front_color())

        def state6():
            return (self.cube[ 1,  1, 1].colors[1] == self.cube.front_color() and
                    self.cube[ 1, -1, 1].colors[1] == self.cube.front_color() and
                    self.cube[-1, -1, 1].colors[0] == self.cube.front_color() and
                    self.cube[-1,  1, 1].colors[0] == self.cube.front_color())

        def state7():
            return (self.cube[ 1,  1, 1].colors[0] == self.cube.front_color() and
                    self.cube[ 1, -1, 1].colors[0] == self.cube.front_color() and
                    self.cube[-1, -1, 1].colors[0] == self.cube.front_color() and
                    self.cube[-1,  1, 1].colors[0] == self.cube.front_color())

        def state8():
            return (self.cube[ 1,  1, 1].colors[2] == self.cube.front_color() and
                    self.cube[ 1, -1, 1].colors[2] == self.cube.front_color() and
                    self.cube[-1, -1, 1].colors[2] == self.cube.front_color() and
                    self.cube[-1,  1, 1].colors[2] == self.cube.front_color())

        move_1 = "Ri Fi R Fi Ri F F R F F "
        move_2 = "R F Ri F R F F Ri F F "

        count = 0
        while not state8():
            if state1(): self.move(move_1)
            elif state2(): self.move(move_2)
            elif state3(): self.move(move_2 + "F F " + move_1)
            elif state4(): self.move(move_2 + move_1)
            elif state5(): self.move(move_1 + "F " + move_2)
            elif state6(): self.move(move_1 + "Fi " + move_1)
            elif state7(): self.move(move_1 + "F F " + move_1)
            else:
                self.move("F")

            count += 1
            if count >= self.inifinite_loop_max_iterations:
                raise Exception("Stuck in loop - unsolvable cube:\n" + str(self.cube))

        # rotate corners into correct locations (cube is inverted, so swap up and down colors)
        bru_corner = self.cube.find_piece(self.cube.front_color(), self.cube.right_color(), self.cube.up_color())
        while bru_corner.pos != Point(1, 1, 1):
            self.move("F")

        self.move("Xi Xi")

    def last_layer_edges(self):
        self.move("X X")

        br_edge = self.cube.find_piece(self.cube.front_color(), self.cube.right_color())
        bl_edge = self.cube.find_piece(self.cube.front_color(), self.cube.left_color())
        bu_edge = self.cube.find_piece(self.cube.front_color(), self.cube.up_color())
        bd_edge = self.cube.find_piece(self.cube.front_color(), self.cube.down_color())

        # States:
        #       1              2
        #      ---            ---
        #      ---            ---
        #      -B-            -a-
        #  --- B-B ---    aaa BBB ---
        #  --B -B- B--    aaB -B- B--
        #  --- B-B ---    aaa B-B ---
        #      -B-            -B-
        #      ---            ---
        #      ---            ---
        #              (aB edge on any FRONT)
        def state1():
            return (bu_edge.colors[2] != self.cube.front_color() and
                    bd_edge.colors[2] != self.cube.front_color() and
                    bl_edge.colors[2] != self.cube.front_color() and
                    br_edge.colors[2] != self.cube.front_color())

        def state2():
            return (bu_edge.colors[2] == self.cube.front_color() or
                    bd_edge.colors[2] == self.cube.front_color() or
                    bl_edge.colors[2] == self.cube.front_color() or
                    br_edge.colors[2] == self.cube.front_color())


        cycle_move = "R R F D Ui R R Di U F R R"
        h_pattern_move = "Ri S Ri Ri S S Ri Fi Fi R Si Si Ri Ri Si R Fi Fi "
        fish_move = "Di Li " + h_pattern_move + " L D"

        if state1():
            # ideally, convert state1 into state2
            self._handle_last_layer_state1(br_edge, bl_edge, bu_edge, bd_edge, cycle_move, h_pattern_move)
        if state2():
            self._handle_last_layer_state2(br_edge, bl_edge, bu_edge, bd_edge, cycle_move)

        def h_pattern1():
            return (self.cube[-1,  0, 1].colors[0] != self.cube.left_color() and
                    self.cube[ 1,  0, 1].colors[0] != self.cube.right_color() and
                    self.cube[ 0, -1, 1].colors[1] == self.cube.down_color() and
                    self.cube[ 0,  1, 1].colors[1] == self.cube.up_color())

        def h_pattern2():
            return (self.cube[-1,  0, 1].colors[0] == self.cube.left_color() and
                    self.cube[ 1,  0, 1].colors[0] == self.cube.right_color() and
                    self.cube[ 0, -1, 1].colors[1] == self.cube.front_color() and
                    self.cube[ 0,  1, 1].colors[1] == self.cube.front_color())

        def fish_pattern():
            return (self.cube[FRONT + DOWN].colors[2] == self.cube.down_color() and
                    self.cube[FRONT + RIGHT].colors[2] == self.cube.right_color() and
                    self.cube[FRONT + DOWN].colors[1] == self.cube.front_color() and
                    self.cube[FRONT + RIGHT].colors[0] == self.cube.front_color())

        count = 0
        while not self.cube.is_solved():
            for _ in range(4):
                if fish_pattern():
                    self.move(fish_move)
                    if self.cube.is_solved():
                        return
                else:
                    self.move("Z")

            if h_pattern1():
                self.move(h_pattern_move)
            elif h_pattern2():
                self.move("Z " + h_pattern_move + "Zi")
            else:
                self.move(cycle_move)
            count += 1
            if count >= self.inifinite_loop_max_iterations:
                raise Exception("Stuck in loop - unsolvable cube:\n" + str(self.cube))

        self.move("Xi Xi")


    def _handle_last_layer_state1(self, br_edge, bl_edge, bu_edge, bd_edge, cycle_move, h_move):
        if DEBUG: print("_handle_last_layer_state1")
        def check_edge_lr():
            return self.cube[LEFT + FRONT].colors[2] == self.cube.left_color()

        count = 0
        while not check_edge_lr():
            self.move("F")
            count += 1
            if count == 4:
                raise Exception("Bug: Failed to handle last layer state1")

        self.move(h_move)

        for _ in range(count):
            self.move("Fi")


    def _handle_last_layer_state2(self, br_edge, bl_edge, bu_edge, bd_edge, cycle_move):
        if DEBUG: print("_handle_last_layer_state2")
        def correct_edge():
            piece = self.cube[LEFT + FRONT]
            if piece.colors[2] == self.cube.front_color() and piece.colors[0] == self.cube.left_color():
                return piece
            piece = self.cube[RIGHT + FRONT]
            if piece.colors[2] == self.cube.front_color() and piece.colors[0] == self.cube.right_color():
                return piece
            piece = self.cube[UP + FRONT]
            if piece.colors[2] == self.cube.front_color() and piece.colors[1] == self.cube.up_color():
                return piece
            piece = self.cube[DOWN + FRONT]
            if piece.colors[2] == self.cube.front_color() and piece.colors[1] == self.cube.down_color():
                return piece

        count = 0
        while True:
            edge = correct_edge()
            if edge is None:
                self.move(cycle_move)
            else:
                break

            count += 1

            if count % 3 == 0:
                self.move("Z")

            if count >= self.inifinite_loop_max_iterations:
                raise Exception("Stuck in loop - unsolvable cube:\n" + str(self.cube))

        while edge.pos != Point(-1, 0, 1):
            self.move("Z")

        assert self.cube[LEFT + FRONT].colors[2] == self.cube.front_color() and \
               self.cube[LEFT + FRONT].colors[0] == self.cube.left_color()

