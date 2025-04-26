import shutil
import os

def cp_dirtree(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
        os.mkdir(dst)
    for item in os.listdir(src):
        item_src = os.path.join(src, item) 
        item_dst = os.path.join(dst, item)
        if os.path.isfile(item_src):
            shutil.copy(item_src, item_dst)
        else:
            os.mkdir(item_dst)
            cp_dirtree(item_src, item_dst)