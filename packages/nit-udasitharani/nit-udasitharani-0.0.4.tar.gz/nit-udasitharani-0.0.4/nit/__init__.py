from PIL import Image, ImageDraw, ImageFont

def generate_tile(initials, save_path, bgColor, fgColor):
    canvas_w, canvas_h = 400, 400
    poppinsFont = ImageFont.truetype("/home/udasitharani/Downloads/ttf/Poppins-Medium.ttf", 200)
    
    canvas = Image.new('RGBA', (canvas_w, canvas_h), color=bgColor)
    draw = ImageDraw.Draw(canvas)
    
    text_w, text_h = draw.textsize(initials, font=poppinsFont)
    draw.text(((canvas_w-text_w)/2, (canvas_h-text_h)/3), initials, fill=fgColor, font=poppinsFont)

    canvas.save(save_path)

def generate_initials_from_string(text):
    split_text = text.split(" ")
    if(len(split_text)):
        if(len(split_text)==1):
            return split_text[0][0].capitalize()
        else:
            return "".join([split_text[0][0].capitalize(), split_text[-1][0].capitalize()])

def generate_tile_from_initials(text, save_path, bgColor=(15,15,15), fgColor="white"):
    initials = generate_initials_from_string(text)
    generate_tile(initials, save_path, bgColor, fgColor)

