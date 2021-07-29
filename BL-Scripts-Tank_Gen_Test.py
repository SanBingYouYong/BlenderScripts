import bpy
import numpy as np
from random import randint


# hull -> cube -> bevel
# turret -> cube -> bevel
#hull_len = 4
#hull_wid = 3
#hull_hei = 1

#tur_len = 2
#tur_wid = 2
#tur_hei = 0.5

hull_len = randint(4, 8)
hull_wid = hull_len / 4 * 3
hull_hei = hull_len / 5

tur_len = hull_len / 2
tur_wid = hull_len / 2
tur_hei = hull_len / 6


def generate_hull():
    bpy.ops.mesh.primitive_cube_add(scale=(hull_len, hull_wid, hull_hei))
    bpy.ops.object.modifier_add(type="BEVEL")
    bpy.data.objects["Cube"].modifiers["Bevel"].width = hull_len

def generate_turret():
    # TODO find a way to use variables to substitue 1 and 3 in randint
    bpy.ops.mesh.primitive_cube_add(location=(hull_len-tur_len-randint(1, 3),0,hull_hei+tur_hei), 
                                    scale=(tur_len,tur_wid,tur_hei))
    bpy.ops.object.modifier_add(type="BEVEL")
    bpy.data.objects["Cube.001"].modifiers["Bevel"].width = tur_len

def generate_cannon():
    bpy.ops.mesh.primitive_cylinder_add(radius=tur_hei/4, 
                                        location=(bpy.data.objects["Cube.001"].location[0]+tur_len+0.5, 0, hull_hei+tur_hei), 
                                        rotation=(0, np.pi/2, 0), 
                                        scale=(1,1,2))


if __name__ == "__main__":
    generate_hull()
    generate_turret()
    generate_cannon()
