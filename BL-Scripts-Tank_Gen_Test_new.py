import bpy
import bmesh
import numpy as np
from random import randint
#from random import random


# hull -> cube -> bevel
# turret -> cube -> bevel
#hull_len = 4
#hull_wid = 3
#hull_hei = 1

#tur_len = 2
#tur_wid = 2
#tur_hei = 0.5

hull_len = randint(4, 8) 
hull_wid = hull_len / 4 * 2
hull_hei = hull_len / 5

tur_len = hull_len / 2
tur_wid = hull_wid - hull_hei / 2
tur_hei = hull_len / 6
# test test test 

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
    bpy.ops.mesh.primitive_cylinder_add(radius=tur_hei/5, 
                                        location=(bpy.data.objects["Cube.001"].location[0]+tur_len+0.5, 0, hull_hei+tur_hei), 
                                        rotation=(0, -np.pi/2, 0), 
                                        scale=(1,1,2))
    bpy.ops.object.mode_set(mode='EDIT')
    obj = bpy.context.active_object
    mes = obj.data
    bme = bmesh.from_edit_mesh(mes)
    for face in bme.faces:
        face.select = False
#    bpy.ops.mesh.select_all(action='INVERT')
    bme.faces.ensure_lookup_table()
    bme.faces[33].select = True
#    print(len(bme.faces))
#    bpy.ops.wm.tool_set_by_id(name="builtin.inset_faces")
    bpy.ops.mesh.inset(thickness=0.05, depth=0, release_confirm=True)
    bpy.ops.mesh.inset(thickness=0.02, depth=-tur_hei*2, release_confirm=True)
    bpy.ops.object.mode_set(mode='OBJECT')

def generate_tracks():
    num_wheels = randint(4, hull_len)
#    wheel_seg = (hull_len - 1) / num_wheels
#    wheel_radius = (wheel_seg - 0.2) / 2
    wheel_radius = hull_len / (num_wheels + 2)
    wheel_seg = (hull_len - num_wheels * wheel_radius) / (num_wheels)
    
    wheel_x_rear = -0.75 - (hull_len / 2)
    wheel_x_front = (num_wheels - 1) * wheel_seg
    wheel_y_left = -0.5 - (hull_wid / 2)
    wheel_y_right = 0.5 + (hull_wid / 2)
    wheel_z = -0.5 - (hull_hei / 2)
    # y_left
    for i in range(num_wheels):
        bpy.ops.mesh.primitive_cylinder_add(radius=wheel_radius,
                                            location=(wheel_x_rear + i * (wheel_seg + wheel_radius*2), wheel_y_left, wheel_z),
                                            rotation=(np.pi / 2, 0, 0),
                                            scale=(1, 1, 0.35))
    # y_right
    for i in range(num_wheels):
        bpy.ops.mesh.primitive_cylinder_add(radius=wheel_radius,
                                            location=(wheel_x_rear + i * (wheel_seg + wheel_radius*2), wheel_y_right, wheel_z),
                                            rotation=(np.pi / 2, 0, 0),
                                            scale=(1, 1, 0.35))
    
    
#    print(hull_len, num_wheels, wheel_seg, wheel_radius, wheel_z)


if __name__ == "__main__":
    generate_hull()
    generate_turret()
    generate_cannon()
    generate_tracks()

