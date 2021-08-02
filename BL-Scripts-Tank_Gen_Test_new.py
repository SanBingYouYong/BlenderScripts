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

hull_len = randint(5, 10) 
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

def generate_wheels_tracks():
    num_wheels = randint(5, hull_len)
#    wheel_seg = (hull_len - 1) / num_wheels
#    wheel_radius = (wheel_seg - 0.2) / 2
    wheel_radius = hull_len / (num_wheels + 2)
    wheel_seg = (hull_len - num_wheels * wheel_radius) / (num_wheels)
    
    wheel_x_rear = -0.75 - (hull_len / 2)
    # TODO this wheel_x_front needs to be checked
    wheel_x_front = wheel_x_rear + (num_wheels - 1) * (wheel_seg + wheel_radius * 2)
    wheel_y_right = -0.5 - (hull_wid / 2)
    wheel_y_left = 0.5 + (hull_wid / 2)
    wheel_z = -0.5 - (hull_hei / 2)
    # y_right
    for i in range(num_wheels - 1):
        bpy.ops.mesh.primitive_cylinder_add(radius=wheel_radius,
                                            location=(wheel_x_rear + i * (wheel_seg + wheel_radius*2), wheel_y_right, wheel_z),
                                            rotation=(np.pi / 2, 0, 0),
                                            scale=(1, 1, 0.35))
        bpy.ops.object.mode_set(mode='EDIT')
        obj = bpy.context.active_object
        mes = obj.data
        bme = bmesh.from_edit_mesh(mes)
        # alt select: the ring
        for face in bme.faces:
            face.select = True
        bme.faces.ensure_lookup_table()
        print(len(bme.faces))
        bme.faces[30].select = False
    #    bme.faces[30].select = False  # WHY 30???????????????
        bpy.ops.mesh.inset(thickness=wheel_radius/3, depth=0, release_confirm=True)
        bpy.ops.mesh.inset(thickness=wheel_radius/12, depth=-wheel_radius/3, release_confirm=True)
        # select the outer surface
        for face in bme.faces:
            face.select = False
        bme.faces.ensure_lookup_table()
        bme.faces[30].select = True
        bpy.ops.mesh.inset(thickness=wheel_radius/6, depth=0, release_confirm=True)
        bpy.ops.mesh.inset(thickness=wheel_radius/12, depth=-wheel_radius/6, release_confirm=True)
        bpy.ops.mesh.inset(thickness=wheel_radius/6, depth=0, release_confirm=True)
        bpy.ops.mesh.inset(thickness=wheel_radius/6, depth=wheel_radius/6, release_confirm=True)
        bpy.ops.object.mode_set(mode='OBJECT')

    # y_left
    for i in range(num_wheels - 1):
        bpy.ops.mesh.primitive_cylinder_add(radius=wheel_radius,
                                            location=(wheel_x_rear + i * (wheel_seg + wheel_radius*2), wheel_y_left, wheel_z),
                                            rotation=(np.pi / 2, 0, 0),
                                            scale=(1, 1, 0.35))
        bpy.ops.object.mode_set(mode='EDIT')
        obj = bpy.context.active_object
        mes = obj.data
        bme = bmesh.from_edit_mesh(mes)
        # alt select: the ring
        for face in bme.faces:
            face.select = True
        bme.faces.ensure_lookup_table()
        print(len(bme.faces))
        bme.faces[33].select = False
    #    bme.faces[30].select = False  # WHY 30???????????????
        bpy.ops.mesh.inset(thickness=wheel_radius/3, depth=0, release_confirm=True)
        bpy.ops.mesh.inset(thickness=wheel_radius/12, depth=-wheel_radius/3, release_confirm=True)
        # select the outer surface
        for face in bme.faces:
            face.select = False
        bme.faces.ensure_lookup_table()
        bme.faces[33].select = True
        bpy.ops.mesh.inset(thickness=wheel_radius/6, depth=0, release_confirm=True)
        bpy.ops.mesh.inset(thickness=wheel_radius/12, depth=-wheel_radius/6, release_confirm=True)
        bpy.ops.mesh.inset(thickness=wheel_radius/6, depth=0, release_confirm=True)
        bpy.ops.mesh.inset(thickness=wheel_radius/6, depth=wheel_radius/6, release_confirm=True)
        bpy.ops.object.mode_set(mode='OBJECT')

    # TODO Guide Wheel not included! 
    # Guide Wheels:
    guide_radius = wheel_radius * 2 / 3 
    guide_x_rear = wheel_x_rear - wheel_radius * 2
    guide_x_front = wheel_x_front
    guide_z = wheel_z + wheel_radius * 2 / 3
    guide_wheels = []
###############################################################################################
    # rear
    bpy.ops.mesh.primitive_cylinder_add(radius=guide_radius, 
                                        location=(guide_x_rear, wheel_y_left, guide_z),
                                        rotation=(np.pi/2,0,0),
                                        scale=(1,1,0.35))
    guide_wheels.append(bpy.context.active_object)
    bpy.ops.object.mode_set(mode='EDIT')
    obj = bpy.context.active_object
    mes = obj.data
    bme = bmesh.from_edit_mesh(mes)
    # alt select: the ring
    for face in bme.faces:
        face.select = True
    bme.faces.ensure_lookup_table()
    print(len(bme.faces))
    bme.faces[33].select = False
#    bme.faces[30].select = False  # WHY 30???????????????
    bpy.ops.mesh.inset(thickness=guide_radius/3, depth=0, release_confirm=True)
    bpy.ops.mesh.inset(thickness=guide_radius/12, depth=-guide_radius/3, release_confirm=True)
    # select the outer surface
    for face in bme.faces:
        face.select = False
    bme.faces.ensure_lookup_table()
    bme.faces[33].select = True
    bpy.ops.mesh.inset(thickness=guide_radius/6, depth=0, release_confirm=True)
    bpy.ops.mesh.inset(thickness=guide_radius/12, depth=-guide_radius/6, release_confirm=True)
    bpy.ops.mesh.inset(thickness=guide_radius/6, depth=0, release_confirm=True)
    bpy.ops.mesh.inset(thickness=guide_radius/6, depth=guide_radius/6, release_confirm=True)
    bpy.ops.object.mode_set(mode='OBJECT')
###############################################################################################
    bpy.ops.mesh.primitive_cylinder_add(radius=guide_radius, 
                                        location=(guide_x_rear, wheel_y_right, guide_z),
                                        rotation=(np.pi/2,0,0),
                                        scale=(1,1,0.35))
    guide_wheels.append(bpy.context.active_object)
    bpy.ops.object.mode_set(mode='EDIT')
    obj = bpy.context.active_object
    mes = obj.data
    bme = bmesh.from_edit_mesh(mes)
    # alt select: the ring
    for face in bme.faces:
        face.select = True
    bme.faces.ensure_lookup_table()
    print(len(bme.faces))
    bme.faces[30].select = False
#    bme.faces[30].select = False  # WHY 30???????????????
    bpy.ops.mesh.inset(thickness=guide_radius/3, depth=0, release_confirm=True)
    bpy.ops.mesh.inset(thickness=guide_radius/12, depth=-guide_radius/3, release_confirm=True)
    # select the outer surface
    for face in bme.faces:
        face.select = False
    bme.faces.ensure_lookup_table()
    bme.faces[30].select = True
    bpy.ops.mesh.inset(thickness=guide_radius/6, depth=0, release_confirm=True)
    bpy.ops.mesh.inset(thickness=guide_radius/12, depth=-guide_radius/6, release_confirm=True)
    bpy.ops.mesh.inset(thickness=guide_radius/6, depth=0, release_confirm=True)
    bpy.ops.mesh.inset(thickness=guide_radius/6, depth=guide_radius/6, release_confirm=True)
    bpy.ops.object.mode_set(mode='OBJECT')
###############################################################################################
    # front
    bpy.ops.mesh.primitive_cylinder_add(radius=guide_radius, 
                                        location=(guide_x_front, wheel_y_left, guide_z),
                                        rotation=(np.pi/2,0,0),
                                        scale=(1,1,0.35))
    guide_wheels.append(bpy.context.active_object)
    bpy.ops.object.mode_set(mode='EDIT')
    obj = bpy.context.active_object
    mes = obj.data
    bme = bmesh.from_edit_mesh(mes)
    # alt select: the ring
    for face in bme.faces:
        face.select = True
    bme.faces.ensure_lookup_table()
    print(len(bme.faces))
    bme.faces[33].select = False
#    bme.faces[30].select = False  # WHY 30???????????????
    bpy.ops.mesh.inset(thickness=guide_radius/3, depth=0, release_confirm=True)
    bpy.ops.mesh.inset(thickness=guide_radius/12, depth=-guide_radius/3, release_confirm=True)
    # select the outer surface
    for face in bme.faces:
        face.select = False
    bme.faces.ensure_lookup_table()
    bme.faces[33].select = True
    bpy.ops.mesh.inset(thickness=guide_radius/6, depth=0, release_confirm=True)
    bpy.ops.mesh.inset(thickness=guide_radius/12, depth=-guide_radius/6, release_confirm=True)
    bpy.ops.mesh.inset(thickness=guide_radius/6, depth=0, release_confirm=True)
    bpy.ops.mesh.inset(thickness=guide_radius/6, depth=guide_radius/6, release_confirm=True)
    bpy.ops.object.mode_set(mode='OBJECT')
###############################################################################################
    bpy.ops.mesh.primitive_cylinder_add(radius=guide_radius, 
                                        location=(guide_x_front, wheel_y_right, guide_z),
                                        rotation=(np.pi/2,0,0),
                                        scale=(1,1,0.35))
    guide_wheels.append(bpy.context.active_object)
    bpy.ops.object.mode_set(mode='EDIT')
    obj = bpy.context.active_object
    mes = obj.data
    bme = bmesh.from_edit_mesh(mes)
    # alt select: the ring
    for face in bme.faces:
        face.select = True
    bme.faces.ensure_lookup_table()
    print(len(bme.faces))
    bme.faces[30].select = False
#    bme.faces[30].select = False  # WHY 30???????????????
    bpy.ops.mesh.inset(thickness=guide_radius/3, depth=0, release_confirm=True)
    bpy.ops.mesh.inset(thickness=guide_radius/12, depth=-guide_radius/3, release_confirm=True)
    # select the outer surface
    for face in bme.faces:
        face.select = False
    bme.faces.ensure_lookup_table()
    bme.faces[30].select = True
    bpy.ops.mesh.inset(thickness=guide_radius/6, depth=0, release_confirm=True)
    bpy.ops.mesh.inset(thickness=guide_radius/12, depth=-guide_radius/6, release_confirm=True)
    bpy.ops.mesh.inset(thickness=guide_radius/6, depth=0, release_confirm=True)
    bpy.ops.mesh.inset(thickness=guide_radius/6, depth=guide_radius/6, release_confirm=True)
    bpy.ops.object.mode_set(mode='OBJECT')
    ############################################################################################
    ############################################################################################
    # tracks - down
    track_len = guide_radius
    track_wid = guide_radius * 1.5
    track_hei = guide_radius/4
    track_x_rear = guide_x_rear + guide_radius/6
    track_x_down_rear = wheel_x_rear
    track_x_down_front = wheel_x_front - guide_radius * 2
    track_y_right = wheel_y_right - guide_radius/6
    track_y_left = wheel_y_left + guide_radius/6
    track_z_down = wheel_z - wheel_radius - track_hei / 2   
    xi = track_x_down_rear
    while xi <= track_x_down_front - track_len:
        bpy.ops.mesh.primitive_cube_add(size=1,
                                        location=(xi, track_y_right, track_z_down),
                                        scale=(track_len, track_wid, track_hei))
        xi += track_len
    # note: quan yi zhi ji, should be modified thoroughly
    bpy.ops.mesh.primitive_cube_add(size=1,
                                    location=(xi, track_y_right, track_z_down),
                                    scale=(track_len,track_wid,track_hei))
    # note: quan yi zhi ji, should be modified thoroughly
    bpy.ops.mesh.primitive_cube_add(size=1,
                                    location=(xi + track_len * 2 / 3, track_y_right, track_z_down),
                                    scale=(track_len / 2,track_wid,track_hei))
    # tracks - up
    track_x_up_rear = guide_x_rear
    track_x_up_front = guide_x_front + track_len
    track_z_up = guide_z + guide_radius + track_hei / 2
    xi = track_x_up_rear
    while xi <= track_x_up_front - track_len:
        bpy.ops.mesh.primitive_cube_add(size=1,
                                        location=(xi, track_y_right, track_z_up),
                                        scale=(track_len,track_wid, track_hei))
        xi += track_len
    # note: quan yi zhi ji, should be modified thoroughly
    bpy.ops.mesh.primitive_cube_add(size=1,
                                    location=(xi - track_len/ 3, track_y_right, track_z_up),
                                    scale=(track_len / 2,track_wid,track_hei))
    ######################################################################################
    bpy.ops.mesh.primitive_cube_add(size=1,
                                    location=(guide_x_rear - guide_radius - track_hei/2, track_y_right, guide_z),
                                    scale=(track_len,track_wid,track_hei),
                                    rotation=(0,np.pi/2,0))
    bpy.ops.mesh.primitive_cube_add(size=1,
                                    location=(guide_x_front + guide_radius + track_hei/2, track_y_right, guide_z),
                                    scale=(track_len,track_wid,track_hei),
                                    rotation=(0,np.pi/2,0))
    ###########################################################
    # Note: x * cos(45) == x / 2 * sqrt(2)
    bpy.ops.mesh.primitive_cube_add(size=1,
                                    location=(guide_x_rear - (guide_radius + track_hei) / 2 * np.sqrt(2) + track_hei / 2, track_y_right, guide_z + (guide_radius + track_hei) / 2 * np.sqrt(2) - track_hei / 2),
                                    scale=(track_len,track_wid,track_hei),
                                    rotation=(0, -np.pi/4, 0))
    bpy.ops.mesh.primitive_cube_add(size=1,
                                    location=(guide_x_rear - (guide_radius + track_hei) / 2 * np.sqrt(2) + track_hei / 2, track_y_right, guide_z - (guide_radius + track_hei) / 2 * np.sqrt(2) + track_hei / 2),
                                    scale=(track_len,track_wid,track_hei),
                                    rotation=(0, np.pi/4, 0))
    # Note: will be gap in the front tracks
    bpy.ops.mesh.primitive_cube_add(size=1,
                                    location=(guide_x_front + (guide_radius + track_hei) / 2 * np.sqrt(2) - track_hei / 2, track_y_right, guide_z + (guide_radius + track_hei) / 2 * np.sqrt(2) - track_hei / 2),
                                    scale=(track_len,track_wid,track_hei),
                                    rotation=(0, np.pi/4, 0))
    bpy.ops.mesh.primitive_cube_add(size=1,
                                    location=(guide_x_front + (guide_radius + track_hei) / 2 * np.sqrt(2) - track_hei / 2, track_y_right, guide_z - (guide_radius + track_hei) / 2 * np.sqrt(2) + track_hei / 2),
                                    scale=(track_len,track_wid,track_hei),
                                    rotation=(0, -np.pi/4, 0))
    ###########################################################
    # the final angled tracks
    temp_x_diff = (track_x_down_rear - track_len / 2) - (guide_x_rear - track_hei)
    temp_z_diff = (guide_z - guide_radius - track_hei) - track_z_down
    temp_third_leg = np.sqrt(temp_x_diff ** 2 + temp_z_diff ** 2)
    # temp_angle = (np.pi * np.arctan(temp_z_diff/temp_x_diff)) / 180
    temp_angle = np.arctan(temp_z_diff/temp_x_diff)
    bpy.ops.mesh.primitive_cube_add(size=1,
                                    location=(track_x_down_rear - track_len / 2 - temp_x_diff / 2, track_y_right, track_z_down + temp_z_diff / 2),
                                    scale=(temp_third_leg,track_wid, track_hei),
                                    rotation=(0, temp_angle, 0))

    temp_x_diff = (guide_x_front + track_hei) - (track_x_down_front + track_len / 2)
    temp_z_diff = (guide_z - guide_radius - track_hei) - track_z_down
    temp_third_leg = np.sqrt(temp_x_diff ** 2 + temp_z_diff ** 2)
    # temp_angle = (np.pi * np.arctan(temp_z_diff/temp_x_diff)) / 180
    temp_angle = np.arctan(temp_z_diff/temp_x_diff)
    bpy.ops.mesh.primitive_cube_add(size=1,
                                    location=(track_x_down_front + track_len / 2 + temp_x_diff / 2, track_y_right, track_z_down + temp_z_diff / 2),
                                    scale=(temp_third_leg,track_wid, track_hei),
                                    rotation=(0, -temp_angle, 0))

    ######################################################################################



if __name__ == "__main__":
    generate_hull()
    generate_turret()
    generate_cannon()
    generate_wheels_tracks()

