import bpy
from random import randint


def generate_cube():
    for a in range(0, 5):
        fa = a*2
        x = a
        y = fa
        for yi in range(fa):
            z = randint(2, 6)
            for zi in range(z):
                bpy.ops.mesh.primitive_cube_add(size=0.8, location=(x,yi,zi))
                set_rigid()
                print((x,y,z))

def generate_point():
    for i in range(10):
        x = randint(-10, 10)
        y = randint(-10, 10)
        z = randint(-10, 10)
        bpy.ops.object.light_add(type='POINT', location=(x,y,z))

def set_rigid():
    mass_rand = randint(20, 50)
    bpy.ops.rigidbody.object_add()
    bpy.context.object.rigid_body.mass = mass_rand
    bpy.context.object.rigid_body.collision_shape = 'BOX'
    bpy.context.object.rigid_body.friction = 1
    bpy.context.object.rigid_body.use_margin = True
    bpy.context.object.rigid_body.collision_margin = 0
    bpy.context.object.rigid_body.linear_damping = 0.35
    # print("added")


if __name__ == "__main__":
    # generate_point()
    generate_cube()
    # set_rigid()

