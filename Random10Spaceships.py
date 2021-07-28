import bpy
from random import randint

number = 10
for i in range(0, number):
    x = randint(-20, 20)
    y = randint(-20, 20)
    z = randint(-20, 20)
    bpy.ops.mesh.generate_spaceship()
    if i == 0:
        ship_name = "Spaceship"
    elif i > 0 and i < 10:
        ship_name = "Spaceship.00" + str(i)
    else:  # more than 100 not inclueded
        ship_name = "Spaceship.0" + str(i)  # not tested
    bpy.data.objects[ship_name].location.x += x
    bpy.data.objects[ship_name].location.y += y
    bpy.data.objects[ship_name].location.z += z
