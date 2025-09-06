from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import uuid
import urllib.request
import os
from io import BytesIO
import asyncio


async def agree(text, husband, wife):
    temp_files = []
    
    img = Image.open("img\\agree.png")
                    
    def get_text_dimensions(text_string, font):
        draw = ImageDraw.Draw(img)
        bbox = draw.textbbox((140,35),text_string,font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        return (w,h)

    # Get the text multilined to fit into a box
    box = ((140,35,530,210))
    async def solve(text, font_size):
        await asyncio.sleep(0)
        size = None
        textsplit = text.split() #individual words
        font = ImageFont.truetype('arial.ttf',font_size)
        print("===== Trying with font size {}".format(font_size))
        r_txt = textsplit # r_txt is the remaining words in the entire string
        text_lines = []
        while len(r_txt) > 0:
            print("Remaining text: {}".format(" ".join(r_txt)))
            i = 0 # i is how many words it is trying to fit on the current line. Start at 0 because 1 gets added
            next_size = get_text_dimensions(r_txt[0],font) # try with just the first word
            if next_size[0] > box[2] - box[0]: # the first word is already too long, so split it
                j = 0
                f_txt1 = r_txt[0][0]
                next_size1 = get_text_dimensions(f_txt1,font)
                while next_size1[0] < box[2] - box[0] and j<len(r_txt[0]): 
                    j += 1    
                    f_txt1 = r_txt[0][:j] #f_txt1 is the text string it is trying to fit in the box. It is a substring of the first word in r_txt
                    print("Trying with text {}".format(f_txt1))
                    next_size1 = get_text_dimensions(f_txt1,font)
                    print("Size of string: {} compared to max size {}".format(next_size1[0],box[2] - box[0]))
                r_txt = [r_txt[0][:j-1],r_txt[0][j-1:]] + r_txt[1:]
            else: #first word isn't too long            
                while next_size[0] <= box[2] - box[0] and i<len(r_txt):# while the next_size is not too big, and we haven't fit all the words on the line  
                    i += 1    
                    size = next_size #the last "next_size" fit so make that the current size to use
                    txt = " ".join(r_txt[:i]) #txt is the text string it is trying to fit in the box
                    print("Trying with text {}".format(txt))
                    next_size = get_text_dimensions(txt,font)
                    print("Size of string: {} compared to max size {}".format(next_size[0],box[2] - box[0]))
                if i > 1:
                    i = i - 1
                    txt = " ".join(r_txt[:i])
                else:
                    txt = r_txt[0]
                next_size = get_text_dimensions(txt,font)
                print("Got it to fit with {} words in {} pixels".format(i,size))
                text_lines += [txt]
                print("Total text:\n" + "\n".join(text_lines))
                r_txt = r_txt[i:]
            
        # at this point, the text is split up so that it fits in the horizontal direction. Now we check if it is too tall.
        total_text = "\n".join(text_lines)
        next_size = get_text_dimensions(total_text,font)
        solved =  (next_size[1] <= box[3] - box[1])
        return (solved, total_text, next_size)
    
    font_size = 45
    solved = False
    while font_size>1 and not solved:
        (solved, total_text, next_size) = await solve(text, font_size)
        if next_size[1] > box[3] - box[1]:
            font_size -= 1
    print("Solved with font size {}".format(font_size))
    print("Total size: {}".format(next_size))
    print(total_text)

    font = ImageFont.truetype('arial.ttf',font_size)

    I1 = ImageDraw.Draw(img)
    I1.text((140,35), total_text ,font=font, fill = (0,0,0))
    
    
    
    
    def overlay(img,imgbytes,position,resize):
        img2 = Image.open(BytesIO(imgbytes)).convert("RGBA")
        img2 = img2.resize(resize,Image.LANCZOS)
        img.paste(img2,position,img2)
        
    overlay(img,husband,(80,280),(260,260))
    overlay(img,wife,(460,430),(260,260))
    filename = "tmp\\{}.png".format(str(uuid.uuid4()))
    img.save(filename)
    temp_files.append(filename)
    return (filename,temp_files)    

def where_banana(text):
    img = Image.open("img\\where.png")
    font = ImageFont.truetype('arial.ttf',40)
    temp_files = []
    imgd = ImageDraw.Draw(img)
    imgd.text((898, 59), text, font=font,fill=(0,0,0))
    filename = "tmp\\{}.png".format(str(uuid.uuid4()))
    img.save(filename)
    temp_files.append(filename)
    return (filename,temp_files)



def cleanup(temp_files):
    for file in temp_files:
        os.remove(file)