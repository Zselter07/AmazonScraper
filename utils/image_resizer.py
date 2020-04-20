from PIL import Image
from PIL import ImageFilter

def resize_image(image_file_path, target_height = 1080, target_width = 1920):
    image = Image.open(image_file_path, 'r')
    image_size = image.size
    width = image_size[0]
    height = image_size[1]
    
    if height == width:
        difference = target_height - height 
    else:
        difference = target_height - height if target_height - height < target_width - width else target_width - width 

    new_width = width + difference
    new_height = height + difference 

    correctly_resized_image = image.resize((new_width, new_height))
    full_hd_image = image.resize((target_width,target_height))
    offset = (int((target_width - correctly_resized_image.width)/2), int((target_height - correctly_resized_image.height)/2))
    
    gaussImage = full_hd_image.filter(ImageFilter.GaussianBlur(40))
    gaussImage.paste(correctly_resized_image, offset)
    gaussImage.save(image_file_path)

def resize_images(folder_path):

    for image in folder_path:
        resize_image(image)
