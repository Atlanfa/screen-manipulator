import pyautogui
import win32api
from time import sleep
import pyperclip
import json

# monitor = pyautogui.size()

# print(monitor)

# mouse = pyautogui.position()

# print(mouse)
    


# for xy in positions:
    # pyautogui.moveTo(xy)
    # sleep(1)

# return list of range amount_of_moves
def register_mouse_moves(amount_of_moves: int) -> list:
    # move mouse and register amount of left click pressed. amount of left clicks must be equal to amount_of_moves. register position of mouse pointer when mouse was pressed.
    # register only when mouse is pressed down 
    positions = []
    while amount_of_moves > 0:
        if win32api.GetKeyState(0x01) < 0:
            positions.append(pyautogui.position())
            amount_of_moves -= 1
            sleep(1)
    return positions

def move_mouse_to_positions(position) -> None:
    pyautogui.moveTo(position)
    sleep(1)

def send_left_mouse_click() -> None:
    # click left mouse button
    pyautogui.click()

def send_right_mouse_click() -> None:
    # click right mouse button
    pyautogui.click(button='right')

def send_middle_mouse_click() -> None:
    # click middle mouse button
    pyautogui.click(button='middle')

def send_mouse_scroll_up(amount: int) -> None:
    pyautogui.scroll(amount)

def send_mouse_scroll_down(amount: int) -> None:
    pyautogui.scroll(-amount)

def repeat_string_on_keyboard(text: str) -> None:
    pyautogui.write(text, interval=0.05)
    
def execute_commands(command_file) -> None:
    print(command_file)
    clipboard = None
    with open(command_file, 'r') as file:
        command_data = json.load(file)
    for i in command_data:
        # print(i)
        # print(command_data[i]['action'])
        if 'move' in command_data[i]['action'] :
            move_mouse_to_positions((command_data[i]['action']['move']['x'], command_data[i]['action']['move']['y']))
        elif 'click' in command_data[i]['action']:
            if command_data[i]['action']['click'] == 'left':

                for _ in range(command_data[i]['action']['amount']):
                    send_left_mouse_click()
                if command_data[i]['action']['hold'] :
                    pyautogui.mouseDown()
                else:
                    pyautogui.mouseUp()
            elif command_data[i]['action']['click'] == 'right':
                for _ in range(command_data[i]['action']['amount']):
                    send_right_mouse_click()
                if command_data[i]['action']['hold'] :
                    pyautogui.mouseDown(button='right')
                else:
                    pyautogui.mouseUp(button='right')
                    
            elif command_data[i]['action']['click'] == 'middle':
                for _ in range(command_data[i]['action']['amount']):
                    send_middle_mouse_click()
                if command_data[i]['action']['hold'] :
                    pyautogui.mouseDown(button='middle')
                else:
                    pyautogui.mouseUp(button='middle')  
        elif 'scroll' in command_data[i]['action']:
            if command_data[i]['action']['scroll']['direction']:
                send_mouse_scroll_up(command_data[i]['action']['scroll'])
            else:
                send_mouse_scroll_down(command_data[i]['action']['scroll'])
        elif 'type' in  command_data[i]['action'] :
            # print(command_data[i]['action']['type'])
            repeat_string_on_keyboard(command_data[i]['action']['type'])
        elif 'copy' in command_data[i]['action']:
            clipboard = copy_clipboard()
        elif 'paste' in command_data[i]['action'] :
            paste_clipboard(clipboard)
        elif 'select_all' in command_data[i]['action']:
            select_all()
# move_mouse_to_positions(register_mouse_moves(5))

def select_all():
    pyautogui.hotkey('ctrl', 'a')
    
def copy_clipboard():
    pyautogui.hotkey('ctrl', 'c')
    sleep(.01)  # ctrl-c is usually very fast but your program may execute faster
    return pyperclip.paste()


def paste_clipboard(text):
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')

# list_of_text = ['1', '2', '3']

# moves = register_mouse_moves(len(list_of_text))
# for i in moves:
#     print(i)
#     move_mouse_to_positions(i)
#     send_left_mouse_click()
#     repeat_string_on_keyboard(list_of_text.pop(0))
    
# execute_commands('./commands/test.com')
