from PIL import ImageGrab, ImageDraw, ImageFont
import requests
import io
import base64
from config import API_KEY

def capture_screenshot_with_grid(filename='screenshot_with_grid.png',
                                 grid_columns=25, grid_rows=13,
                                 line_color=(255, 0, 0), line_width=3):
    # Define the font for the numbers
    font = ImageFont.truetype("arialbd.ttf", 20)

    # Capture the screenshot
    screenshot = ImageGrab.grab()
    draw = ImageDraw.Draw(screenshot)
    width, height = screenshot.size

    # Calculate the size of icons and spacing based on your screenshot
    icon_width = width // grid_columns
    icon_height = height // grid_rows

    # Right and bottom offsets
    right_offset = width // 100 # Adjust as needed
    bottom_offset = height // 12  # Adjust as needed

    # Draw the grid lines, taking into account the right and bottom offsets
    for col in range(grid_columns):
        x = col * icon_width
        draw.line([(x, 0), (x, height - bottom_offset)], fill=line_color, width=line_width)

    for row in range(grid_rows-1):
        y = row * icon_height
        draw.line([(0, y), (width - right_offset, y)], fill=line_color, width=line_width)

    # Draw the numbers at each grid intersection
    number = 1
    for row in range(grid_rows):
        for col in range(grid_columns):
            # Calculate the center of each cell
            cell_center_x = (col * icon_width) + (icon_width // 2)
            cell_center_y = (row * icon_height) + (icon_height // 2)

            # Text to be drawn
            text = str(number)

            # Get the size of the text to be drawn
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            # Calculate the position for the text to be centered
            text_x = cell_center_x - (text_width // 2)
            text_y = cell_center_y - (text_height // 2)

            # Draw the number centered in the cell
            draw.text((text_x, text_y), text, font=font, fill=line_color)

            number += 1

    # Save the modified screenshot with the grid in the current directory
    screenshot.save(filename)

    # Save the image to a buffer to return the base64 encoded string
    buffer = io.BytesIO()
    screenshot.save(buffer, format="PNG")
    buffer.seek(0)
    base64_image = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    return base64_image
    
def analyze_image_with_instructions(base64_image, instructions, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4-vision-preview",  
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": instructions
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "temperature": 0.5,
        "max_tokens": 100
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)  # Replace "API_ENDPOINT_HERE" with the correct endpoint
    return response.json()
    
def process_icon_detection(key_word, api_key = API_KEY):
    base64_screenshot = capture_screenshot_with_grid()
    
    recorded_instructions_1 = "Find the cell number of the cell that contains " + key_word + " , the majority of the subjject must be in the same red square with the cell number to be true. Cell number is in top left part of the cell. output only cell number, If icon can't be detecter output 0. Don't assume or guess, its ok to return 0!"
    result_1 = analyze_image_with_instructions(base64_screenshot, recorded_instructions_1, api_key)
    
    recorded_instructions_2 = "Is " + key_word +" closest to the number" + result_1['choices'][0]['message']['content'] + " ? if false output only 0. if true output only cell number."
    result_2 = analyze_image_with_instructions(base64_screenshot, recorded_instructions_2, api_key)

    
    final_result = result_2['choices'][0]['message']['content']
    
    print(final_result)
    return int(final_result)


