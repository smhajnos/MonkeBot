from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps
import uuid
import urllib.request
import os
from io import BytesIO
import asyncio
import pathlib


def idiocracy(img_in):
    
    temp_files = []
    img2 = Image.open(BytesIO(img_in)).convert("RGBA")
    img = Image.open("img\\idiocracy.png")
    
    def overlay(img,img2,position,resize):
        img2 = img2.resize(resize,Image.LANCZOS)
        img.paste(img2,position,img2)
        
    size = ((105,105))
    origin = ((195,160))
    overlay(img,img2,origin,size)

    
    filename = "tmp\\{}.png".format(str(uuid.uuid4()))
    img.save(filename)
    temp_files.append(filename)
    return (filename,temp_files) 

async def imgagree(img_in, husband, wife):
    
    temp_files = []
    img2 = Image.open(BytesIO(img_in)).convert("RGBA")
    img = Image.open("img\\agree.png")
    
    def overlay(img,img2,position,resize):
        img2 = img2.resize(resize,Image.LANCZOS)
        img.paste(img2,position,img2)
        
    size = ((530-140,210-35))
    origin = ((140,35))
    overlay(img,img2,origin,size)
    
    
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



async def spongebob(text1,text2,text3):
    temp_files = []
    text=text1
    for t in [text2, text3]:
        if t:
            text = "\n".join([text, t])
    img = Image.open("img/spongebob.png")
    
    font_size = 200
    font = ImageFont.truetype('res/Krabby Patty.ttf',font_size)

    I1 = ImageDraw.Draw(img)
    I1.text((597,447), text,font=font, fill = (0,0,0),anchor="mm")
    
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

async def monkeballs(txt):
    fnt = ImageFont.truetype('arial.ttf',15)
    def generate_image(text_rows):
        width = 500
        height = 657+25*text_rows+15
        composite = Image.new('RGBA', (width, height))
        y = 0
        timage = Image.open("img/balls/top.png")
        composite.paste(timage,(0,y))
        y += timage.height
        for x in range(0,text_rows):
            timage = Image.open("img/balls/middle.png")
            composite.paste(timage,(0,y))
            y += timage.height
        timage = Image.open("img/balls/bottom.png")
        composite.paste(timage,(0,y))
        y += timage.height
        return composite
    
    async def calculate_lines(text):
        async def get_text_width(text_in):
            await asyncio.sleep(0)
            text_to_calc = " ".join(text_in)
            print("Getting text width of {}".format(text_to_calc))
            img = Image.new('RGBA', (500, 25))
            draw = ImageDraw.Draw(img)

            bbox = draw.textbbox((0,0),text_to_calc,fnt)
            print(bbox[2] - bbox[0])
            return bbox[2] - bbox[0]
        total_text = text.split()
        finished_text = []
        remaining_text = total_text
        while len(remaining_text) > 0:
            i = 1 # How words we are trying to fit on this line
            cont = True
            while i < len(remaining_text) and cont:
                this_line = remaining_text[0:i]
                w = await get_text_width(this_line)
                if w < 475: # Add 1 to i and 
                    i += 1
                else: # the previous i was the one we want
                    i -= 1
                    cont = False
            if i == 0:
                this_line = remaining_text[0]
                # TODO: clip it at the right number of characters and continue on next line
            else:   
                this_line = remaining_text[0:i]
            finished_text.append(this_line)
            remaining_text = remaining_text[i:]
            print(finished_text)
            print(remaining_text)
        return finished_text
                    
    lines = await calculate_lines(txt)       
            
    img = generate_image(len(lines))
    
    i = 0
    for line in lines:
        line_text = " ".join(line)
        imgdraw = ImageDraw.Draw(img)
        imgdraw.text((10,i*25+10), line_text ,font=fnt, fill = (0,0,0))
    
        i += 1
    temp_files = []
    filename = "tmp\\{}.png".format(str(uuid.uuid4()))
    img.save(filename)
    temp_files.append(filename)
    return (filename,temp_files)  

def angst(pfp):
    temp_files = []
    img = Image.open("img/angst/back.png")
    img2 = Image.open(BytesIO(pfp)).convert("RGBA")
    img2 = img2.resize((750,750),Image.LANCZOS)
    img.paste(img2,(504,106),img2)
    img3 = Image.open("img/angst/front.png")
    img.paste(img3,(0,0),img3)
    filename = "tmp\\{}.png".format(str(uuid.uuid4()))
    img.save(filename)
    temp_files.append(filename)
    return (filename,temp_files)


async def typewriter(txt):
    temp_files = []
    fnt = ImageFont.truetype('arial.ttf',45)
    async def calculate_lines(text):
        async def get_text_width(text_in):
            await asyncio.sleep(0)
            text_to_calc = " ".join(text_in)
            print("Getting text width of {}".format(text_to_calc))
            img = Image.new('RGBA', (496, 177))
            draw = ImageDraw.Draw(img)

            bbox = draw.textbbox((0,0),text_to_calc,fnt)
            print(bbox[2] - bbox[0])
            return bbox[2] - bbox[0]
        total_text = text.split()
        finished_text = []
        remaining_text = total_text
        while len(remaining_text) > 0:
            i = 1 # How words we are trying to fit on this line
            cont = True
            while i < len(remaining_text) and cont:
                this_line = remaining_text[0:i]
                w = await get_text_width(this_line)
                if w < 496: # Add 1 to i and 
                    i += 1
                else: # the previous i was the one we want
                    i -= 1
                    cont = False
            if i == 0:
                this_line = remaining_text[0]
                # TODO: clip it at the right number of characters and continue on next line
            else:   
                this_line = remaining_text[0:i]
            finished_text.append(this_line)
            remaining_text = remaining_text[i:]
            print(finished_text)
            print(remaining_text)
        return finished_text
                    
    lines = await calculate_lines(txt)
    txt_list = []
    for line in lines:
        line_text = " ".join(line)
        txt_list.append(line_text)
    out_txt = "\n".join(txt_list)
    img = Image.open("img/typewriter.png")
    f = ImageFont.truetype('arial.ttf',45)
    txt_img = Image.new('L', (496,177))
    d = ImageDraw.Draw(txt_img)
    d.text( (0, 0),out_txt,  font=f, fill=255)
    w=txt_img.rotate(25.7,  expand=1)
    img.paste( ImageOps.colorize(w, (0,0,0), (255,255,84)), (125,-50),  w)
    filename = "tmp\\{}.png".format(str(uuid.uuid4()))
    img.save(filename)
    temp_files.append(filename)
    return (filename,temp_files)


def yugioh(img_in):
    
    temp_files = []
    img2 = Image.open(BytesIO(img_in)).convert("RGBA")
    img = Image.open("img/yugioh/back.png")
            
    size = ((208,208))
    origin = ((56,45))
    img2 = img2.rotate(10, expand=1)
    img2 = img2.resize(size,Image.LANCZOS)
    img.paste(img2,origin,img2)
    
    img3 = Image.open("img/yugioh/front.png")
    img.paste(img3,((0,0)),img3) 
    
    
    filename = "tmp\\{}.png".format(str(uuid.uuid4()))
    img.save(filename)
    temp_files.append(filename)
    return (filename,temp_files)    

def cleanup(temp_files):
    for file in temp_files:
        os.remove(file)