import base64
from pathlib import Path

from setting.GLOBAL import BASE_DIR_PATH


# from setting.GLOBAL import PICS_DIR


def pic_to_py(picture_names):
    write_data = []
    write_data.append("oem_image_dic={")
    for picture_name in picture_names:
        filename = picture_name.stem
        # filename = picture_name.replace('.', '_')
        open_pic = open("%s" % picture_name, 'rb')
        b64str = base64.b64encode(open_pic.read())
        open_pic.close()
        write_data.append('"%s" : "%s",\n' % (filename, b64str.decode()))
    write_data.append("}")
    f = open('images_base.py', 'w+')
    for data in write_data:
        f.write(data)
    f.close()


def get_pic_names():
    pic_name_list = []
    print(BASE_DIR_PATH)

    filedir = BASE_DIR_PATH.parent.parent / "assets/logos"

    # filedir = Path(r"C:\Users\Administrator\PycharmProjects\index_invite_1128\oem\assets")
    for item in filedir.glob("**/*.png"):
        pic_name_list.append(item)

    return pic_name_list


pics = get_pic_names()
print(pics)
pic_to_py(pics)

# -*- coding: UTF8 -*-
# import pathlib
#
# path = pathlib.Path(r"C:\Users\Administrator\PycharmProjects\index_invite_1128\oem\assets")
# # print(dir(path))
# print("展示文件夹名：")
# print(path.name)
# print("展示整个路径：")
# print(path)
#
# print("\n展示直接下级:")
# for i in path.iterdir():
#     print(i)
# print("遍历所有下级:")
# for i in path.glob("**/*.png"):
#     print(i)
