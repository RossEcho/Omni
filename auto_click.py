import pyautogui
from config import SCREEN_RESOLUTION

def click_by_cell_number_with_row_adjustment(cell_number, grid_columns, grid_rows, screen_width, screen_height):
    # Calculate cell dimensions without offsets, assuming full screen usage
    cell_width = screen_width / grid_columns
    cell_height = screen_height / grid_rows

    # Determine the cell's column and row from the cell number
    cell_col = ((cell_number - 1) % grid_columns) + 1
    cell_row = ((cell_number - 1) // grid_columns) + 1

    # Calculate the center of the cell
    center_x = (cell_col - 0.5) * cell_width
    
    # Implement a dynamic vertical adjustment based on the row
    if cell_row <= 1:
        
        vertical_adjustment = ((cell_row - 1) / 8) * 40  
    else:
        
        vertical_adjustment = 0

    center_y = ((cell_row - 0.5) * cell_height) + vertical_adjustment

    # Click at the calculated position
    pyautogui.click(center_x, center_y)
    pyautogui.press('enter')

def icon_click(cell):
    click_by_cell_number_with_row_adjustment(cell, 25, 13, SCREEN_RESOLUTION["width"], screen_height = SCREEN_RESOLUTION["height"])  # Test in row 1

