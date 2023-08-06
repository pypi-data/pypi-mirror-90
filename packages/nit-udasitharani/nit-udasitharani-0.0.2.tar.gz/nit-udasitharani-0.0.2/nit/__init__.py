from PIL import Image, ImageDraw, ImageFont
import argparse
import os, sys

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

def main():
    my_parser = argparse.ArgumentParser(prog="name initials tile generator",
                                        usage="$(prog)s [options] name save_path",
                                        description="Generate a name initials tile icon given name")

    my_parser.add_argument("Name", metavar="name", type=str, help="Name to generate initials.")
    my_parser.add_argument("Save_Path", metavar="save_path", type=str, help="Path where the generated tile should be saved.")
    my_parser.add_argument("-bg", "--bg_color", type=str, help="Background color to be used in tile.")
    my_parser.add_argument("-fg", "--fg_color", type=str, help="Color of the text to be used in tile.")

    args = my_parser.parse_args()

    if not os.path.isdir(os.path.split(args.Save_Path)[0]):
        print("The path does not exist.")
        sys.exit()
    kwargs = dict(text=args.Name, save_path=args.Save_Path, bgColor=args.bg_color, fgColor=args.fg_color)
    generate_tile_from_initials(**{k: v for k, v in kwargs.items() if v is not None})
