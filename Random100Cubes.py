import bpy
from random import randint

number = 100
for i in range(0, number):
    x = randint(-20, 20)
    y = randint(-20, 20)
    z = randint(-20, 20)
    bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
