from matplotlib import image as mp_image
import numpy as np
import torchvision, torch
import PIL

array_to_byte = lambda v: chr(v[0] | v[1]<<3 | v[2]<<6)
load_img = lambda filename: torchvision.transforms.PILToTensor()(PIL.Image.open(filename).convert('RGB')).permute(1,2,0)

def txt_in_img(text,imgD):
    res = torch.zeros_like(imgD).type(torch.uint8)
    i, j = 0, 0
    collen = imgD.shape[1]
    text += '\x00'
    for word in text:
        res[i,j%collen] = torch.tensor(byte_to_array(word))
        i = j//collen # riga
        j = (j+1)     # colonna
    imgD = (imgD&(255-7))|res
    return imgD

def txt_from_img(img):
    lsb_img = img&7
    txt = ''
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if lsb_img[i,j][0] == 0 and lsb_img[i,j][1] == 0 and lsb_img[i,j][2] == 0:
                break
            word = array_to_byte(lsb_img[i,j])
            txt += word
    return txt

"""
Per leggere il messaggio:
txt_from_img(load_img(percorso_immagine_png))

Per scrivere il messaggio:
img = load_img(foto_png_target)
img_s = txt_in_img(testo,img)
dst = torchvision.transforms.ToPILImage()(img_s.permute(2,0,1))
dst.save(percorso_nuova_immagine_png)
"""

import os
def write_and_export(filename,txt):
    img = load_img(filename)
    img_s = txt_in_img(txt,img)
    dst = torchvision.transforms.ToPILImage()(img_s.permute(2,0,1))
    out = os.path.split(filename)
    dst.save(os.path.join(out[0],'stego_'+out[1]))

def read_from_img(filename):
    return txt_from_img(load_img(filename))
