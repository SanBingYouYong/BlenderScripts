import bpy
from random import randint


def generate():
    qrcode = bpy.data.objects["sample_pure_qr"]
    qrcodes = []
    for i in range(20):
        qrcodes.append(bpy.data.objects.new("qrcode" + str(i), qrcode.data))    
        qrcodes[-1].location = (randint(-6, 6), randint(-4, 4), randint(1, 10))
        bpy.data.collections["Collection"].objects.link(qrcodes[-1])

def clear():
    for object in bpy.data.objects:
        if "qrcode" in object.name:
            bpy.data.objects[object.name].select_set(state=True)
            bpy.ops.object.delete()

def output_coordinate():
    output_path = "F:/A-work/Tianyu/QRcode/blender_output/output.txt"
    coordinates = []
    for object in bpy.data.objects:
        if "qrcode" in object.name:
            coor = bpy.data.objects[object.name].location
            coordinates.append(coor)
    with open(output_path, 'w') as file:
        # file.write(str(coordinates))
        for coordinate in coordinates:
            file.writelines(str(coordinate) + "\n")


if __name__ == "__main__":
    # generate()
    # clear()
    output_coordinate()
