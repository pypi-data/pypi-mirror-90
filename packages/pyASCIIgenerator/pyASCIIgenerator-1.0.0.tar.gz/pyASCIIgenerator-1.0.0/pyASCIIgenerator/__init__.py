import PIL.Image

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]


def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width / 1.65
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image


def grayify(image):
    grayscale_image = image.convert("L")
    return grayscale_image


def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    return characters


def asciify(path, new_width=100):
    try:
        image = PIL.Image.open(path)
    except:
        print(path, "is not a valid pathname to an image.")
        return

    new_image_data = pixels_to_ascii(grayify(resize_image(image)))

    pixel_count = len(new_image_data)
    ascii_image = "\n".join([new_image_data[index:(index + new_width)] for index in range(0, pixel_count, new_width)])

    print(ascii_image)


def help():
    print(
        "usage: \n\nimport pyASCIIgenerator\npyASCIIgenerator.asciify('path \\\ to \\\ file')\nREMEMBER TO USE DOUBLE BACKSLASHES^^^")

