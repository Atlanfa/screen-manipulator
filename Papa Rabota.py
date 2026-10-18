import tkinter as tk
import os
from tm import execute_commands
from random import randint

#python gui from 
# - <window size='fullscreen', transparacy='0.5'>
# - <top_part>
# - <text_label text='current mouse location'>shows current mouse location</text_label>
# - </top_part>
# - <middle_rigth_part>
# - <frame padding='20px'>
# - <list_of_buttons>buttons loaded from amount of files in folder. and each button is with action made from commands in files</list_of_buttons>
# - </frame>
# - </middle_rigth_part>
# - </window>
# Create the main window
window = tk.Tk()
window.attributes('-alpha', 0.5)

# Create the top part
top_part = tk.Frame(window)
top_part.pack()

# Create the text label
text_label = tk.Label(top_part, text='current mouse location')
text_label.pack()

# Create the middle right part
middle_right_part = tk.Frame(window)
middle_right_part.pack()

# Create the frame
frame = tk.Frame(middle_right_part, padx=20, pady=20)
frame.pack()

# Create the list of buttons
list_of_buttons = tk.Label(frame, text='buttons loaded from amount of files in folder. and each button is with action made from commands in files')
list_of_buttons.pack()

# create a function that will update the label with the current mouse position
def update_label():
    x, y = window.winfo_pointerxy()
    text_label.config(text=f'Mouse Position: x: {x}, y: {y}')
    text_label.after(100, update_label)

# call the function
update_label()

# read ammount of files ending on .com in folder commands and place as many buttons as there are files
# Get the path to the "commands" folder

# Create a button for each file
def do_magic(file):
    return magic(file)

def magic(file):
    try:
        # Minimize window
        window.iconify()
        execute_commands(f'{file}')
        print(f'{file}')
        # Maximize window
        window.deiconify()
        return file
    except Exception as e:
        # Save error logs
        with open('error_logs.txt', 'a') as f:
            f.write(f'Error executing command for file {file}: {str(e)}\n')
        # Do nothing
        pass

def create_and_pack_by_folder(folder_path, color):
    # Convert color to hex
    hex_color = '#%02x%02x%02x' % color
    # Create a frame for the column
    frame = tk.Frame(middle_right_part, bg=hex_color)
    frame.pack(side=tk.LEFT, padx=50)
    # Create a label for the column
    label = tk.Label(frame, text=folder_path.split('\\')[-1], font=('Helvetica', 20, 'bold'), fg=hex_color)
    label.pack()
    # Get the list of files in the folder
    files = [file for file in os.listdir(folder_path) if file.endswith(".json")]
    # Create and pack buttons for each file in the folder
    print(f'{folder_path}')
    print(f'{files}')
    [tk.Button(frame, text=f'{file}'.split('.')[0], command=lambda t=f'{folder_path}\{file}': do_magic(t)).pack() for file in files]

    def on_enter(event):
        event.widget.config(bg='yellow')

    def on_leave(event):
        event.widget.config(bg='SystemButtonFace')

    for button in frame.winfo_children():
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)

def create_and_pack():
    
     # Increase the font size
    window.option_add("*Font", "Helvetica 20")
    
    # get path to all folders in commands
    folders = [folder for folder in os.listdir(os.path.join(os.path.dirname(__file__), "commands"))]
    for folder in folders:
        # print(folder)
        folder_path = os.path.join(os.path.dirname(__file__), f"commands\{folder}")
        create_and_pack_by_folder(folder_path, (randint(0, 255), randint(0, 255), randint(0, 255)))
        # print(folder_path)
    
    # [tk.Button(frame, text=f'{file}'.split('.')[0], command=lambda t=f'{file}': do_magic(t)).pack() for file in files_fail]
    # [tk.Button(frame, text=f'{file}'.split('.')[0], command=lambda t=f'{file}': do_magic(t)).pack() for file in files_pass]
    # Create three separate frames for each column
    # frame_fail = tk.Frame(frame, bg='red')
    # frame_pass = tk.Frame(frame, bg='green')
    # frame_na = tk.Frame(frame, bg='blue')
    # frame_bat = tk.Frame(frame, bg='black')

    # # Set padding between columns
    # frame_fail.pack(side=tk.LEFT, padx=50)
    # frame_na.pack(side=tk.LEFT, padx=50)
    # frame_pass.pack(side=tk.LEFT, padx=50)
    # frame_bat.pack(side=tk.TOP, padx=50)
    
    # # adapt the font size
    # font_size = int(window.winfo_screenheight() / 80)


    # # Create labels for each column
    # label_fail = tk.Label(frame_fail, text='Fail', font=('Helvetica', font_size, 'bold'), fg='red')
    # label_pass = tk.Label(frame_pass, text='Pass', font=('Helvetica', font_size, 'bold'), fg='green')
    # label_na = tk.Label(frame_na, text='NA', font=('Helvetica', font_size, 'bold'), fg='blue')
    # label_bat = tk.Label(frame_bat, text='Remove', font=('Helvetica', font_size, 'bold'), fg='black')
    # # Pack the labels above each column
    # label_fail.pack()
    # label_pass.pack()
    # label_na.pack()
    # label_bat.pack()
    

    # # Create and pack buttons for each file in the corresponding frame
    # [tk.Button(frame_fail, text=f'{file}'.split('.')[0], command=lambda t=f'Fail/{file}': do_magic(t), fg='red', font=('Helvetica', font_size, 'bold')).pack() for file in files_fail]
    # [tk.Button(frame_pass, text=f'{file}'.split('.')[0], command=lambda t=f'Pass/{file}': do_magic(t), fg='green', font=('Helvetica', font_size, 'bold')).pack() for file in files_pass]
    # [tk.Button(frame_na, text=f'{file}'.split('.')[0], command=lambda t=f'NA/{file}': do_magic(t), fg='blue', font=('Helvetica', font_size, 'bold')).pack() for file in files_na]
    # [tk.Button(frame_bat, text=f'{file}'.split('.')[0], command=lambda t=f'Battery/{file}': do_magic(t), fg='black', font=('Helvetica', font_size, 'bold')).pack() for file in files_na]
    
    # # Bind events to buttons for hover effect
    # for button in frame_fail.winfo_children():
    #     button.bind('<Enter>', on_enter)
    #     button.bind('<Leave>', on_leave)

    # for button in frame_pass.winfo_children():
    #     button.bind('<Enter>', on_enter)
    #     button.bind('<Leave>', on_leave)

    # for button in frame_na.winfo_children():
    #     button.bind('<Enter>', on_enter)
    #     button.bind('<Leave>', on_leave)
    
    

create_and_pack()    


# Start the main loop
window.mainloop()