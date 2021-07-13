from PIL import Image
from PIL import ImageEnhance
 
 
def adjust_brightness(input_image, output_image, factor):
    image = Image.open(input_image)
    enhancer_object = ImageEnhance.Contrast(image)
    out = enhancer_object.enhance(factor)
    out.save(output_image)
 
if __name__ == '__main__':
    adjust_brightness('form_2.jpg',
                      'enhance_op.jpg',
                      1.7)
