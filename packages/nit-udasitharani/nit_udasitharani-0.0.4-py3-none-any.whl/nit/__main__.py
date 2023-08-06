import argparse, os, sys

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
