import pandas as pd
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
import torch
from PIL import Image
# from IPython.display import display
import os

__version__ = "1.0.0"

model_id = "stabilityai/stable-diffusion-2"
DIRP = "D:\\Greeting card\\app"
scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, torch_dtype=torch.float16)

device = " "
if torch.cuda.is_available():
    device = "cude"
else:
    device = "cpu"
# #pipe = pipe.to("cuda")
pipe = pipe.to(device)

excel_path = os.path.join(DIRP,"data","EmployeeDatabase3.xlsx")
df = pd.read_excel(excel_path, engine='openpyxl')

# Function to generate birthday greeting card based on NGS
def generate_birthday_card(ngs):
    if ngs not in df['NGS'].values:
        return "NGS not found in the database. Please enter a valid NGS."

    employee_data = df[df['NGS'] == ngs].iloc[0]

    greeting_card = (
        f"Create a heartwarming and visually appealing image that captures the essence of "
        f"{employee_data['RITU']} in a {employee_data['TRAVEL']} incorporating {employee_data['COLOUR']} as backgorund colour "
        f"and {employee_data['ACTIVITY']} as activity. "
        f"The image should radiate positivity and excitement."
    )

    return greeting_card

def generate_card(user_ngs,occasion,num_images):
    # Get NGS from user
    # user_ngs = int(input("Enter the NGS of the employee: "))

    # Generate birthday greeting card and store it in the 'prompt' variable
    prompt = generate_birthday_card(user_ngs)

    # Print the generated string or error message
    print(prompt)



    # print("Choose Occasion, Birthday or Work Anniversary")
    # occasion = input()
    # occasion = occasion.lower()
    # num_images = int(input("Enter Number of Images between o and 7: "))
    # user_ngs = int(input("enter ngs: "))

    # Load the top and bottom images (assuming fixed paths for them)
    if occasion == 0:
        user_img = os.path.join(DIRP,"data","hbd.png")
        top_img = Image.open(user_img)
    elif occasion == 1:
        work_img = os.path.join(DIRP,"data","workann.png")
        top_img = Image.open(work_img)

    ngs_img = os.path.join(DIRP,"data","images",user_ngs+".png")
    bottom_img = Image.open(ngs_img)

    if 0 <= num_images <= 6:
        for i in range(num_images):
            # Generate the background image (assuming this part is working correctly)
            image = pipe(prompt).images[0]
            image.save(f"{user_ngs}Image{i+1}.png")

            # Load the generated background image
            background_img = Image.open(f"/content/{user_ngs}Image{i+1}.png")

            # Resize the top and bottom images to fit within the background
            top_img_resized = top_img.resize((int(background_img.width * 0.6), int(background_img.height * 0.35)))  # Adjust proportions as needed
            bottom_img_resized = bottom_img.resize((int(background_img.width * 0.5), int(background_img.height * 0.8)))  # Adjust proportions as needed

            # Calculate positions for top and bottom images dynamically based on index i
            if i == 0:
                # 1st image: top_img center aligned, bot_img center aligned
                top_x = (background_img.width - top_img_resized.width) // 2
                bottom_x = (background_img.width - bottom_img_resized.width) // 2
                top_y = (background_img.height - top_img_resized.height) // 100
                bottom_y = 230  # Adjust as needed
            elif i == 1:
                # 2nd image: top_img top right corner, bot_img bottom left corner
                top_x = background_img.width - top_img_resized.width
                bottom_x = 0
                top_y = 0
                bottom_y = background_img.height - bottom_img_resized.height
            elif i == 2:
                # 3rd image: top_img center aligned, bot_img lower the top_img
                top_x = (background_img.width - top_img_resized.width) // 2
                bottom_x = (background_img.width - bottom_img_resized.width) // 2
                top_y = (background_img.height - top_img_resized.height) // 2
                bottom_y = top_y + top_img_resized.height + 10  # Adjust as needed
            elif i % 2 == 0:
                # Even indexed images: top_img left center aligned, bot_img right center aligned
                top_x = 10
                bottom_x = background_img.width - bottom_img_resized.width - 10
                top_y = (background_img.height - top_img_resized.height) // 2
                bottom_y = (background_img.height - bottom_img_resized.height) // 2
            else:
                # Odd indexed images: top_img right center aligned, bot_img left center aligned
                top_x = background_img.width - top_img_resized.width - 10
                bottom_x = 10
                top_y = (background_img.height - top_img_resized.height) // 2
                bottom_y = (background_img.height - bottom_img_resized.height) // 2

            # Paste the top and bottom images onto the background
            background_img.paste(top_img_resized, (top_x, top_y), top_img_resized)
            background_img.paste(bottom_img_resized, (bottom_x, bottom_y), bottom_img_resized)

            # Display or save the combined image
            background_img.save(f"combined1_image_{i+1}.jpg")
        return background_img

    else:
        # print("Please enter a number between 1 and 7.")
        return None