from datetime import datetime
import pyautogui as pg
import pyperclip
import openpyxl as xl
import tkinter as tk
from excel_screenshot import screen_shot_of_excel
import json


def excel_start_command(path: str, root_window, excel_window) -> None:
    root_window.iconify()
    excel_window.iconify()
    # print(path)
    pg.moveTo((177, 57))
    move_bottom_right()
    pg.hotkey('ctrl', 'c')
    serial = pyperclip.paste()
    pg.moveTo((738, 61))
    move_bottom_right()
    pg.hotkey('ctrl', 'c')
    client = pyperclip.paste()
    pg.moveTo((181, 144))
    move_bottom_right()
    pg.hotkey('ctrl', 'c')
    description = pyperclip.paste()
    xlsx = xl.load_workbook(path)
    sheet = xlsx.active
    # get the last row
    row = sheet.max_row + 1
    # check if there already a row with serial
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    row_data = [None, serial, client, description, None, None, timestamp]
    
    for i in range(1, row):
        if sheet.cell(row=i, column=2).value == serial:
            notify  = tk.Toplevel(excel_window)
            notify.attributes('-topmost', True)
            notify.title('Excel')
            notify_label = tk.Label(notify, text='Serial already exists')
            notify_label.pack()
            notify_button = tk.Button(notify, text='OK', command=lambda: notify.destroy())
            notify_button.pack()
            notify.mainloop()
            break
    else:
        for i, data in enumerate(row_data):
            sheet.cell(row=row, column=i+1, value=data)
    root_window.deiconify()
    excel_window.deiconify()
    xlsx.save(path)
    xlsx.close()
    
def assign_class_excel_command(path: str, root_window) -> None:
    pg.moveTo((181, 144))
    move_bottom_right()
    pg.hotkey('ctrl', 'c')
    description = pyperclip.paste()
    pg.moveTo((177, 57))
    move_bottom_right()
    pg.hotkey('ctrl', 'c')
    serial = pyperclip.paste()
    xlsx = xl.load_workbook(path)
    sheet = xlsx.active
    # get the last row
    
    check = True
    for i in range(1, sheet.max_row+1):
        # print(sheet.cell(row=i, column=2).value)
        if sheet.cell(row=i, column=2).value == serial:
            print('Serial exists')

            check = False
            break
    if not check:
        
        for i in range(1, sheet.max_row+1):
            if sheet.cell(row=i, column=2).value == serial:
                row = i
                break
        
        old_description = sheet.cell(row=row, column=4).value       
        diference = description.replace(old_description, '')
        sheet.cell(row=row, column=5, value=diference)
        xlsx.save(path)
        xlsx.close()
        premade_description_command(path, root_window, row)
    else:
        notify = tk.Toplevel(root_window)
        # bring window to the front
        notify.attributes('-topmost', True)
        notify.title('Excel')
        notify_label = tk.Label(notify, text='Serial does not exist')
        notify_label.pack()
        notify_button = tk.Button(notify, text='OK', command=lambda: notify.destroy())
        notify_button.pack()
        notify.mainloop()


def excel_finish_command(path: str, root_window, excel_window) -> None:
    # iconify the root window
    root_window.iconify()
    excel_window.iconify()
    pg.moveTo((181, 144))
    move_bottom_right()
    pg.hotkey('ctrl', 'c')
    description = pyperclip.paste()
    xlsx = xl.load_workbook(path)
    sheet = xlsx.active
    # get the last row
    row = sheet.max_row
    pg.moveTo((177, 57))
    move_bottom_right()
    pg.hotkey('ctrl', 'c')
    serial = pyperclip.paste()
    # check if there is no serial in excel
    # print(serial)
    check = True
    for i in range(1, sheet.max_row+1):
        # print(sheet.cell(row=i, column=2).value)
        if sheet.cell(row=i, column=2).value == serial:
            print('Serial exists')
            row = i
            check = False
            break
    if not check:
        old_description = sheet.cell(row=row, column=4).value
        diference = description.replace(old_description, '')
        sheet.cell(row=row, column=5, value=diference)
        xlsx.save(path)
        xlsx.close()
        additional_window_with_4_radio_buttons(path, root_window, excel_window, serial)
        # show_amount_of_rows(path, root_window)  
    else:
        notify  = tk.Toplevel(excel_window)
        # bring window to the front
        notify.attributes('-topmost', True)
        notify.title('Excel')
        notify_label = tk.Label(notify, text='Serial does not exist')
        notify_label.pack()
        notify_button = tk.Button(notify, text='OK', command=lambda: notify.destroy())
        notify_button.pack()
        notify.mainloop()
        
    


def additional_window_with_4_radio_buttons(path, root_window, excel_window, serial) -> None:
    # new window with 4 radio buttons
    window = tk.Toplevel(excel_window)
    window.title('Excel')
    window.attributes('-topmost', True)  # Make the window appear on top
    # create the radio buttons with values [RFR, C, B, A, Scrap]
    radio_var = tk.StringVar()
    radio_var.set('RFR')
    radio_buttons = [
        ('RFR', 'RFR'),
        ('C', 'C'),
        ('B', 'B'),
        ('A', 'A'),
        ('Scrap', 'Scrap'),
        ('SALVAGED','SALVAGED'),
        ('Repaired', 'Repaired')
    ]
    for text, value in radio_buttons:
        radio = tk.Radiobutton(window, text=text, value=value, variable=radio_var)
        radio.pack()
    # create the button that will save the data
    save_button = tk.Button(window, text='Save', command=lambda: [save_data(path, radio_var, window, serial)])
    save_button.pack()
    ask_to_change_description = tk.Label(window, text='Do you want to change the description?')
    ask_to_change_description.pack()
   # yes or no buttons
    yes_button = tk.Button(window, text='Yes', command=lambda: [change_description(path, root_window, window, serial)])
    yes_button.pack()
    no_button = tk.Button(window, text='No', command=lambda: [window.master.deiconify(), window.destroy(), screen_shot_of_excel(path, root_window)])
    no_button.pack()
    window.mainloop()

def change_description(path, root_window, window, serial) -> None:
    xlsx = xl.load_workbook(path)
    sheet = xlsx.active
    for i in range(1, sheet.max_row+1):
        if sheet.cell(row=i, column=2).value == serial:
            row = i
            break
    xlsx.close()
    window.master.deiconify()
    window.destroy()
    custom_description_precommand(path, root_window, row)

def custom_description_command(path, root_window, row) -> None:
    # create a new window for the custom description
    custom_description_window = tk.Toplevel(root_window)
    custom_description_window.title('Excel')
    custom_description_window.attributes('-topmost', True)
    custom_description_label = tk.Label(custom_description_window, text='Enter the custom description')
    custom_description_label.pack()
    custom_description_entry = tk.Entry(custom_description_window)
    custom_description_entry.pack()
    save_description_button = tk.Button(custom_description_window, text='Save', command=lambda: [save_custom_description(path, custom_description_entry.get(), root_window, row), custom_description_window.destroy()])
    save_description_button.pack()
    custom_description_window.mainloop()

def save_custom_description(path, description, root_window, row) -> None:
    xlsx = xl.load_workbook(path)
    sheet = xlsx.active
    for i in range(1, sheet.max_row+1):
        if sheet.cell(row=i, column=2).value == row:
            row = i
            break
    sheet.cell(row=row, column=5, value=description)
    xlsx.save(path)
    xlsx.close()
    screen_shot_of_excel(path, root_window)
    root_window.deiconify()

def show_amount_of_rows(path: str, window) -> None:
    xlsx = xl.load_workbook(path)
    sheet = xlsx.active
    row = sheet.max_row
    show_done_amount = tk.Toplevel()
    counter = 0
    for i in range(1, row+1):
        if sheet.cell(row=i, column=6).value:
            counter += 1
    amount_done = 0
    for i in range(1, row+1):
        if sheet.cell(row=i, column=2).value:
            amount_done += 1
        else:
            break
    amount_salvalged = 0
    for i in range(1, row+1):
        if 'SALVAGED' in f'{sheet.cell(row=i, column=6).value}':
            amount_salvalged += 1

    show_done_amount.attributes('-topmost', True)
    show_done_amount.title('Excel amount done')
    show_done_amount_label = tk.Label(show_done_amount, text=f'Amount done {amount_done-1}\nAmount full {counter - 1}\nAmount salvaged {amount_salvalged}')
    show_done_amount_label.pack()
    show_done_amount_button = tk.Button(show_done_amount, text='OK', command=lambda: show_done_amount.destroy())
    show_done_amount_button.pack()
    xlsx.close()
    window.mainloop()

def custom_description_precommand(path, root_window, row) -> None:
    window_new = tk.Toplevel(root_window)
    window_new.attributes('-topmost', True)
    premade_description = tk.Button(window_new, text='Premade description', command=lambda: [premade_description_command(path, root_window, row), window_new.destroy()])
    premade_description.pack()
    custom_description = tk.Button(window_new, text='Custom description', command=lambda: [custom_description_command(path, root_window, row), window_new.destroy()])
    custom_description.pack()
    window_new.mainloop()
    


def premade_description_command(path, root_window, row) -> None:
    with open('premade/pmade.json', 'r') as file:
        data = json.load(file)
    if len(data) == 0:
        notify = tk.Toplevel(root_window)
        notify.attributes('-topmost', True)
        notify.title('Excel')
        notify_label = tk.Label(notify, text='No premade descriptions')
        notify_label.pack()
        notify_button = tk.Button(notify, text='OK', command=lambda: notify.destroy())
        notify_button.pack()
        notify.mainloop()
    else:
        notify = tk.Toplevel(root_window)
        checkboxes = []
        notify.attributes('-topmost', True)
        frame_grade = tk.Frame(notify)
        frame_grade.pack(side=tk.RIGHT)
        radio_var = tk.StringVar()
        # radio_var.set('RFR')
        radio_buttons = [
            ('RFR', 'RFR'),
            ('C', 'C'),
            ('B', 'B'),
            ('A', 'A'),
            ('Scrap', 'Scrap'),
            ('SALVAGED','SALVAGED')
        ]
        for text, value in radio_buttons:
            radio = tk.Radiobutton(frame_grade, text=text, value=value, variable=radio_var)
            radio.pack()
        for key, value in data.items():
            fr = tk.Frame(notify)
            
            for j in value:
                frame = tk.Frame(fr)
                frame.pack(side=tk.TOP)
                minus_value_var = tk.StringVar(value="")
                checkbox_minus = tk.Checkbutton(frame, text="-", variable=minus_value_var, onvalue=f"remove {value[j]}", offvalue='')
                # increase the size of the checkbox
                checkbox_minus.config(font=('Helvetica', 20))
                checkbox_minus.pack(side=tk.LEFT)
                button = tk.Button(frame, text=value[j], command=lambda k=value[j]: [save_premade_description(path, k, root_window, row), notify.destroy()])
                button.pack(side=tk.LEFT)
                plus_value_var = tk.StringVar(value='')
                checkbox_plus = tk.Checkbutton(frame, text="+", variable=plus_value_var, onvalue=f'add {value[j]}', offvalue='')
                checkbox_plus.pack(side=tk.LEFT)
                checkboxes.append((minus_value_var, plus_value_var))
            fr.pack(side=tk.RIGHT)
        whiped = tk.StringVar(value='')
        checkbox_whiped = tk.Checkbutton(notify, text='Wiped', variable=whiped, onvalue='Wiped', offvalue='')
        checkbox_whiped.pack()
        tested = tk.StringVar(value='')
        checkbox_tested = tk.Checkbutton(notify, text='Tested', variable=tested, onvalue='Tested', offvalue='')
        checkbox_tested.pack()
        submit_button = tk.Button(notify, text='Submit', command=lambda: [submit_premade_description(path, root_window, row, checkboxes, whiped, tested, radio_var), notify.destroy()])
        submit_button.pack()
        notify.mainloop()

def submit_premade_description(path, root_window, row, checkboxes, whiped, tested, radio_var) -> None:
    result = ''
    for minus, plus in checkboxes:
        if minus.get() or plus.get():
            result +=" " + minus.get() + '/ ' + plus.get() + ' '
    result += '/ ' + whiped.get() + '/ ' + tested.get()
    save_premade_and_final_description(path, result, root_window, row, radio_var.get())

def save_premade_and_final_description(path, description, root_window, row, radio) -> None:
    xlsx = xl.load_workbook(path)
    sheet = xlsx.active
    for i in range(1, sheet.max_row+1):
        if sheet.cell(row=i, column=2).value == row:
            row = i
            break
    sheet.cell(row=row, column=5, value=description)
    sheet.cell(row=row, column=6, value=radio)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sheet.cell(row=row, column=8, value=timestamp)
    before = sheet.cell(row=row, column=7).value
    diference = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S') - datetime.strptime(before, '%Y-%m-%d %H:%M:%S')
    sheet.cell(row=row, column=9, value=diference)
    xlsx.save(path)
    xlsx.close()
    screen_shot_of_excel(path, root_window)

def save_premade_description(path, description, root_window, row) -> None:
    xlsx = xl.load_workbook(path)
    sheet = xlsx.active
    for i in range(1, sheet.max_row+1):
        if sheet.cell(row=i, column=2).value == row:
            row = i
            break
    sheet.cell(row=row, column=5, value=description)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sheet.cell(row=row, column=8, value=timestamp)
    before = sheet.cell(row=row, column=7).value
    diference = timestamp - datetime.strptime(before, '%Y-%m-%d %H:%M:%S')
    sheet.cell(row=row, column=9, value=diference) 
    xlsx.save(path)
    xlsx.close()
    screen_shot_of_excel(path, root_window)

def save_data(path,  radio_var, window, serial) -> None:
    xlsx = xl.load_workbook(path)
    sheet = xlsx.active
    for i in range(1, sheet.max_row+1):
        if sheet.cell(row=i, column=2).value == serial:
            row = i
            break
    sheet.cell(row=row, column=6, value=radio_var.get())
    print(radio_var.get())
    print(row)
    xlsx.save(path)
    xlsx.close()
    screen_shot_of_excel(path, window)
    
    
    
    

def move_bottom_right():
    pg.mouseDown(button='left')
    width, height = pg.size()
    # move mouse to the bottom right corner
    pg.moveTo(width - 50, height - 50)
    pg.mouseUp(button='left')

