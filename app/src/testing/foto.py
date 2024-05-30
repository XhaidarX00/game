import os
from PIL import Image, ImageDraw, ImageFont

async def create_circle_mask(img):
    # Create a circular mask for the image
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)

    # Define the radius of the circle (half of the minimum dimension of the image)
    circle_radius = min(img.size) // 2

    # Calculate the coordinates for the bounding box of the circle
    circle_bbox = (
        img.size[0] // 2 - circle_radius,
        img.size[1] // 2 - circle_radius,
        img.size[0] // 2 + circle_radius,
        img.size[1] // 2 + circle_radius
    )

    # Draw the circle on the mask
    draw.ellipse(circle_bbox, fill=255)

    return mask

async def resize_and_create_circle_mask(photo_image_path):
    # Opening the secondary image (overlay image)
    img2 = Image.open(photo_image_path)
    img2 = img2.convert("RGBA")

    # Resize the overlay image with a suitable method (e.g., BICUBIC for smoother interpolation)
    resized_img2 = img2.resize((int(img2.size[0] * 1.31), int(img2.size[1] * 1.31)), Image.BICUBIC)

    # Create a circular mask for the resized overlay image
    mask = await create_circle_mask(resized_img2)

    # Apply the circular mask to the resized overlay image
    resized_img2.putalpha(mask)

    return resized_img2

async def merge_images(name, un, resized_overlay_image):
    # Opening the primary image (used in background)
    background_image_path = f"{current_path}/app/src/testing/background1.jpg"
    
    img1 = Image.open(background_image_path)

    # Pasting resized_overlay_image (with circular mask) on top of img1
    # starting at coordinates (0, 0)
    # x kiri kanan
    # y atas bawah
    img1.paste(resized_overlay_image, (1050, 813), mask=resized_overlay_image)
    
    
    # Load the font and resize it
    # font = ImageFont.truetype(f"{current_path}/app/src/testing/Kasper Lullaby.otf", size=font_size)

    # Call draw Method to add 2D graphics in an image
    I1 = ImageDraw.Draw(img1)

    # Add Text to an image with white color
    if len(name) <= 6:
        font_size = 120
        xn, yn = 590, 1100
    else:
        font_size = 120
        xn, yn = 400, 1100
    
    font = ImageFont.truetype(f"{current_path}/app/src/testing/arial-font/arial.ttf", size=font_size)
    I1.text((xn, yn), name, font=font, fill=(255, 255, 255))  # White color is (255, 255, 255)
    
    # I1.text((xn, yn), name, font=font, fill=(255, 255, 255))  # White color is (255, 255, 255)

    # font = ImageFont.truetype(f"{current_path}/app/src/testing/arial-font/arial.ttf", size=160)
    # I1.text((380, 1050), uid, font=font, fill=(255, 255, 255))
    
        
    if len(un) <= 6:
        font_size = 110
        xun, yun = 530, 1250
    else:
        font_size = 110
        xun, yun = 430, 1250
    
    font = ImageFont.truetype(f"{current_path}/app/src/testing/arial-font/arial.ttf", size=font_size)
    I1.text((xun, yun), un, font=font, fill=(255, 255, 255))
    
    # angle = 120
    # radians = math.radians(angle)
    # width, height = I1.textsize("MAYAWATI", font)
    # x = (img1.width - width) / 2
    # y = (img1.height - height) / 2
    # cx, cy = x + width / 2, y + height / 2
    # x, y = x - cx, y - cy
    # x, y = x * math.cos(radians) - y * math.sin(radians), x * math.sin(radians) + y * math.cos(radians)
    # x, y = x + cx, y + cy

    # I1.text((300, 1050), uid, font=font, fill=(255, 255, 255))
    
    output_image_path = f"{current_path}/app/src/testing/hasil.jpg"
    
    # Saving the merged image
    img1.save(output_image_path)
    
    return output_image_path

    # Displaying the image (optional)
    # img1.show()

current_path = os.getcwd()

# Example usage:
background_image_path = f"{current_path}/app/src/testing/background1.jpg"
photo_image_path = f"{current_path}/app/src/testing/foto.jpg"
output_image_path = f"{current_path}/app/src/testing/hasil.jpg"

# name = "˹ᴅɪꜰλᴍꜱ 𝓜𝓮𝓵𝓵 ;"
# un = "@Mellgbt"
name = "ʜᴀɪ"
uid = "1234567"
un = "@Ke"


# Resize and create circular mask for the photo image with suitable method
# resized_overlay_image = resize_and_create_circle_mask(photo_image_path)
# merge_images(name, un, resized_overlay_image)

# Merge resized overlay image into background image with resized font
# merge_images(name, uid, un, background_image_path, resized_overlay_image, output_image_path)
# merge_images(name, un, background_image_path, resized_overlay_image, output_image_path)