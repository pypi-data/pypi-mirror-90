from PIL import Image, ImageFilter

def main():
    path = input("Enter the image location : ")
    name = input("Enter the name of your new thumbnail image name : ")
    image = Image.open(path)
    image.thumbnail((2592, 3000))
    image.save(name)


if __name__=='__main__':
    exit(main)
