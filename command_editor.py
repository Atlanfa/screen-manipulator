import tkinter as tk
import json
import pyperclip

class ActionBlock:
    def __init__(self, delay_before_action, action, delay_after_action):
        self.delay_before_action = delay_before_action
        self.action = action
        self.delay_after_action = delay_after_action
    
    def __str__(self):
        return f"{self.action} block"
    
    def update_properties(self, *args):
        pass # I do not know seters and getters in python

# Define other action block classes...
    


#1. **Боковая панель**: Это место, где пользователи могут выбирать различные "блоки действий". Каждый блок действий может быть представлен в виде иконки или названия действия.

#2. **Рабочая область**: Здесь пользователи могут перетаскивать и упорядочивать "блоки действий" для создания последовательности действий. Блоки могут быть связаны стрелками, указывающими порядок действий.

#3. **Панель свойств**: При выборе блока действий на рабочей области, пользователи могут видеть и редактировать свойства этого блока на панели свойств. Свойства могут включать "delay_before_action", "action", и "delay_after_action".

#4. **Текстовый редактор JSON**: Пользователи могут переключаться между графическим интерфейсом и текстовым редактором JSON для просмотра и редактирования последовательности действий в формате JSON.




class MouseMoveBlock(ActionBlock):
    def __init__(self, x, y, delay_before_action, delay_after_action):
        super().__init__(delay_before_action, "mouse_move", delay_after_action)
        self.x = x
        self.y = y

    def update_properties(self, *args):
        self.x,self.y,self.delay_before_action,self.delay_after_action = args[0], args[1], args[2], args[3]
    
    def __str__(self):
        return "{\"delay_befor\": "+f'{self.delay_before_action}'+", \"action\": {\"move\": {\"x\": "+f"{self.x}"+", \"y\": "+f"{self.y}"+"} }, \"delay_after\":"+f"{self.delay_before_action}"+"}"


class MouseClickBlock(ActionBlock):
    def __init__(self,click_type, hold, click_amount, delay_before_action, delay_after_action):
        super().__init__(delay_before_action, "mouse_click", delay_after_action)
        self.click_type = click_type
        self.click_hold = hold
        self.click_amount = click_amount

    def update_properties(self, *args):
        self.click_type,self.click_hold,self.click_amount,self.delay_before_action,self.delay_after_action = args[0], args[1], args[2], args[3], args[4]
    

    def __str__(self):
        return "{\"delay_befor\": "+f"{self.delay_before_action}"+", \"action\": {\"click\": "+f"\"{self.click_type}\""+", \"amount\": "+f'{self.click_amount}'+", \"hold\": "+f'{str(self.click_hold).lower()}'+" }, \"delay_after\":"+f"{self.delay_before_action}"+"}"
        


class MouseScrollBlock(ActionBlock):
    def __init__(self, amount,direction, delay_before_action, delay_after_action):
        super().__init__(delay_before_action, "mouse_scroll", delay_after_action)
        self.amount = amount
        self.direction = direction # True for up, False for down

    def update_properties(self, *args):
        self.amount,self.direction,self.delay_before_action,self.delay_after_action = args[0], args[1], args[2], args[3]

    def __str__(self):
        return "{\"delay_befor\": "+f"{self.delay_before_action}"+", \"action\": {\"scroll\": "+f"{self.amount}"+", \"direction\": "+f"{str(self.direction).lower()}"+" }, \"delay_after\":"+f"{self.delay_before_action}"+"}"

class KeyboardTypeBlock(ActionBlock):
    def __init__(self, text, delay_before_action, delay_after_action):
        super().__init__(delay_before_action, "keyboard_type", delay_after_action)
        self.text = text

    def update_properties(self, *args):
        self.text,self.delay_before_action,self.delay_after_action = args[0], args[1], args[2]

    def __str__(self):
        return "{\"delay_befor\": "+f"{self.delay_before_action}"+", \"action\": {\"type\": "+f'"{self.text}"'+" }, \"delay_after\":"+f"{self.delay_before_action}"+"}"

class CopyClipboardBlock(ActionBlock):
    def __init__(self, delay_before_action, delay_after_action):
        super().__init__(delay_before_action, "copy_clipboard", delay_after_action)

    def update_properties(self, *args):
        self.delay_before_action,self.delay_after_action = args[0], args[1]

    def __str__(self):
        return "{\"delay_befor\": "+f"{self.delay_before_action}"+", \"action\": {\"copy\": true }, \"delay_after\":"+f"{self.delay_before_action}"+"}"
    

class PasteClipboardBlock(ActionBlock):
    def __init__(self, delay_before_action, delay_after_action):
        super().__init__(delay_before_action, "paste_clipboard", delay_after_action)

    def update_properties(self, *args): 
        self.delay_before_action,self.delay_after_action = args[0], args[1]

    def __str__(self):
        return "{\"delay_befor\": "+f"{self.delay_before_action}"+", \"action\": {\"paste\": true }, \"delay_after\":"+f"{self.delay_before_action}"+"}"


class SelectAllBlock(ActionBlock):
    def __init__(self, delay_before_action, delay_after_action):
        super().__init__(delay_before_action, "select_all", delay_after_action)

    def update_properties(self, *args): 
        self.delay_before_action,self.delay_after_action = args[0], args[1]

    def __str__(self):
        return "{\"delay_befor\": "+f"{self.delay_before_action}"+", \"action\": {\"select_all\": true }, \"delay_after\":"+f"{self.delay_before_action}"+"}"


class BlockSequence:
    def __init__(self):
        self.blocks = []
    
    def add_block(self, block):
        self.blocks.append(block)
    
    def remove_block(self, block):
        self.blocks.remove(block)
    
    def __str__(self):
        text = "{\n"
        for i in range(len(self.blocks)):
            text += "\""+str(i)+"\": "+str(self.blocks[i])+",\n"
        text = text[:-2] + "\n}"
        return text

# class LoadFromJSON():
#     def __init__(self, json_file):
#         self.json_file = json_file
#         self.blocks = []
#         self.load_sequence()
    
#     def load_sequence(self):
#         with open(self.json_file, "r") as file:
#             data = json.load(file)
#             for key in data:
#                 if data[key]["action_name"] == "mouse_move":
#                     self.blocks.append(MouseMoveBlock(data[key]['action']["x"], data[key]['action']["y"], data[key]["delay_befor"], data[key]["delay_after"]))
#                 elif data[key]["action_name"] == "mouse_click":
#                     self.blocks.append(MouseClickBlock(data[key]["delay_befor"], data[key]["delay_after"], ))
#                 elif data[key]["action_name"] == "mouse_scroll":
#                     self.blocks.append(MouseScrollBlock(data[key]['action']["amount"], data[key]["delay_befor"], data[key]["delay_after"]))
#                 elif data[key]["action_name"] == "keyboard_type":
#                     self.blocks.append(KeyboardTypeBlock(data[key]['action']["type"], data[key]["delay_befor"], data[key]["delay_after"]))
#                 elif data[key]["action_name"] == "copy_clipboard":
#                     self.blocks.append(CopyClipboardBlock(data[key]["delay_befor"], data[key]["delay_after"]))
#                 elif data[key]["action_name"] == "paste_clipboard":
#                     self.blocks.append(PasteClipboardBlock(data[key]["delay_befor"], data[key]["delay_after"]))

#     def get_blocks(self):
#         return self.blocks

class CommandEditorGUI:
    def __init__(self, root):
        self.root = root
        self.sequence = BlockSequence()
        
        # Create GUI elements
        self.side_panel = tk.Frame(root)
        self.work_area = tk.Frame(root)
        self.property_panel = tk.Frame(root)
        self.json_editor = tk.Text(root)
        


        # Add GUI elements to the root window
        self.side_panel.pack(side=tk.LEFT)
       
        self.property_panel.pack(side=tk.LEFT)
        self.json_editor.pack(side=tk.LEFT)
        self.work_area.pack(side=tk.LEFT)


        # add label for work area
        work_area_label = tk.Label(self.work_area, text="Work Area")
        work_area_label.pack()
        # in work area there will be a list of blocks with numeration and buttons with up and down arrows to make changes in sequence order. for each block there will be a label with block number and block type
    





        # add text to json editor
    
        # mouse_move_icon = tk.PhotoImage(file="mouse_move_icon.png", width=50, height=50)
        # mouse_click_icon = tk.PhotoImage(file="mouse_click_icon.png", width=50, height=50)
        # mouse_scroll_icon = tk.PhotoImage(file="mouse_scroll_icon.png", width=50, height=50)
        # keyboard_type_icon = tk.PhotoImage(file="keyboard_type_icon.png", width=50, height=50)
        # copy_clipboard_icon = tk.PhotoImage(file="copy_clipboard_icon.png", width=50, height=50)
        # paste_clipboard_icon = tk.PhotoImage(file="paste_clipboard_icon.png", width=50, height=50)
        

        self.mouse_move_button = tk.Button(self.side_panel, text="Mouse Move", command=self.add_mouse_move_block)
        self.mouse_click_button = tk.Button(self.side_panel, text="Mouse Click", command=self.add_mouse_click_block)
        self.mouse_scroll_button = tk.Button(self.side_panel, text="Mouse Scroll", command=self.add_mouse_scroll_block)
        self.keyboard_type_button = tk.Button(self.side_panel, text="Keyboard Type", command=self.add_keyboard_type_block)
        self.copy_clipboard_button = tk.Button(self.side_panel, text="Copy Clipboard", command=self.add_copy_clipboard_block)
        self.paste_clipboard_button = tk.Button(self.side_panel, text="Paste Clipboard", command=self.add_paste_clipboard_block)
        self.select_all_button = tk.Button(self.side_panel, text="Select All", command=self.add_select_all_block)
        self.delete_sequence_button = tk.Button(self.side_panel, text="Delete Sequence", command=self.delete_sequance)
        self.copy_sequence_button = tk.Button(self.side_panel, text="Copy Sequence", command=self.copy_sequence_to_clipboard)

        # Add action buttons to the side panel
        
        self.mouse_move_button.pack()
        self.mouse_click_button.pack()
        self.mouse_scroll_button.pack()
        self.keyboard_type_button.pack()
        self.copy_clipboard_button.pack()
        self.paste_clipboard_button.pack()
        self.select_all_button.pack()
        self.br = tk.Label(self.side_panel, text=" ")
        self.br.pack()
        self.delete_sequence_button.pack()
        self.copy_sequence_button.pack()
        # Bind events to the work area canvas

    def copy_sequence_to_clipboard(self):
        pyperclip.copy(self.sequence.__str__())
    
    def delete_sequance(self):
        self.sequence = BlockSequence()
        self.update_work_area()
        self.display_json_editor()
        pass

    def update_work_area(self):
        for widget in self.work_area.winfo_children():
            widget.destroy()
        for i, block in enumerate(self.sequence.blocks):
            # remove all widgets from work area
            
            # add widgets to work area
            work_area_label = tk.Label(self.work_area, text="Work Area")
            work_area_label.pack(side=tk.TOP)
            block_frame = tk.Frame(self.work_area)
            block_frame.pack(side=tk.TOP)
            block_label = tk.Label(block_frame, text=f"Block {i+1}: {type(block).__name__}")
            block_label.pack(side=tk.LEFT)
            up_button = tk.Button(block_frame, text="▲", command=lambda i=i: self.move_block_up(i))
            up_button.pack(side=tk.LEFT)
            down_button = tk.Button(block_frame, text="▼", command=lambda i=i: self.move_block_down(i))
            down_button.pack(side=tk.LEFT)
            delete_button = tk.Button(block_frame, text="Delete", command=lambda i=i: self.delete_block(i))
            delete_button.pack(side=tk.LEFT)
            properties_button = tk.Button(block_frame, text="Properties", command=lambda block=block: self.display_block_properties(block))
            properties_button.pack(side=tk.LEFT)
        
    def move_block_up(self, index):
        if index > 0:
            self.sequence.blocks[index], self.sequence.blocks[index-1] = self.sequence.blocks[index-1], self.sequence.blocks[index]
            self.update_work_area()
            self.display_json_editor()

    def move_block_down(self, index):
        if index < len(self.sequence.blocks)-1:
            self.sequence.blocks[index], self.sequence.blocks[index+1] = self.sequence.blocks[index+1], self.sequence.blocks[index]
            self.update_work_area()
            self.display_json_editor()

    def delete_block(self, index):
        self.sequence.blocks.pop(index)
        self.update_work_area()
        self.display_json_editor()

    def display_block_properties(self, block):
        for widget in self.property_panel.winfo_children():
            widget.destroy()
        
        if isinstance(block, MouseMoveBlock):
            x_label = tk.Label(self.property_panel, text="X:")
            x_label.pack()
            x_entry = tk.Entry(self.property_panel)
            x_entry.insert(0, block.x)
            x_entry.pack()
            y_label = tk.Label(self.property_panel, text="Y:")
            y_label.pack()
            y_entry = tk.Entry(self.property_panel)
            y_entry.insert(0, block.y)
            y_entry.pack()
            delay_before_label = tk.Label(self.property_panel, text="Delay Before:")
            delay_before_label.pack()
            delay_before_entry = tk.Entry(self.property_panel)
            delay_before_entry.insert(0, block.delay_before_action)
            delay_before_entry.pack()
            delay_after_label = tk.Label(self.property_panel, text="Delay After:")
            delay_after_label.pack()
            delay_after_entry = tk.Entry(self.property_panel)
            delay_after_entry.insert(0, block.delay_after_action)
            delay_after_entry.pack()
            submit_button = tk.Button(self.property_panel, text="Submit", command=lambda: [block.update_properties(x_entry.get(), y_entry.get(), delay_before_entry.get(), delay_after_entry.get()), self.display_block_properties(block), self.update_work_area(),self.display_json_editor()])
            submit_button.pack()
        elif isinstance(block, MouseClickBlock):
            click_type = tk.StringVar()
            click_type.set("left")
            click_left = tk.Radiobutton(self.property_panel, text="Left", variable=click_type, value="left")
            click_left.pack()
            click_right = tk.Radiobutton(self.property_panel, text="Right", variable=click_type, value="right")
            click_right.pack()
            click_middle = tk.Radiobutton(self.property_panel, text="Middle", variable=click_type, value="middle")
            click_middle.pack()
            click_hold = tk.BooleanVar()
            click_hold.set(False)
            click_hold_checkbox = tk.Checkbutton(self.property_panel, text="Hold", variable=click_hold)
            click_hold_checkbox.pack()
            click_amount_label = tk.Label(self.property_panel, text="Amount:")
            click_amount_label.pack()
            click_amount_entry = tk.Entry(self.property_panel)
            click_amount_entry.pack()
            delay_before_label = tk.Label(self.property_panel, text="Delay Before:")
            delay_before_label.pack()
            delay_before_entry = tk.Entry(self.property_panel)
            delay_before_entry.pack()
            delay_after_label = tk.Label(self.property_panel, text="Delay After:")
            delay_after_label.pack()
            delay_after_entry = tk.Entry(self.property_panel)
            delay_after_entry.pack()
            submit_button = tk.Button(self.property_panel, text="Submit", command=lambda: [block.update_properties(click_type.get(), click_hold.get(), click_amount_entry.get(), delay_before_entry.get(), delay_after_entry.get()), self.display_block_properties(block), self.update_work_area(),self.display_json_editor()])
            submit_button.pack()
        elif isinstance(block, MouseScrollBlock):
            amount_label = tk.Label(self.property_panel, text="Amount:")
            amount_label.pack()
            amount_entry = tk.Entry(self.property_panel)
            amount_entry.pack()
            direction = tk.BooleanVar()
            direction.set(True)
            direction_up = tk.Radiobutton(self.property_panel, text="Up", variable=direction, value=True)
            direction_up.pack()
            direction_down = tk.Radiobutton(self.property_panel, text="Down", variable=direction, value=False)
            direction_down.pack()
            delay_before_label = tk.Label(self.property_panel, text="Delay Before:")
            delay_before_label.pack()
            delay_before_entry = tk.Entry(self.property_panel)
            delay_before_entry.pack()
            delay_after_label = tk.Label(self.property_panel, text="Delay After:")
            delay_after_label.pack()
            delay_after_entry = tk.Entry(self.property_panel)
            delay_after_entry.pack()
            submit_button = tk.Button(self.property_panel, text="Submit", command=lambda: [block.update_properties(amount_entry.get(), direction.get(), delay_before_entry.get(), delay_after_entry.get()), self.display_block_properties(block), self.update_work_area(),self.display_json_editor()])
            submit_button.pack()
        elif isinstance(block, KeyboardTypeBlock):
            text_label = tk.Label(self.property_panel, text="Text:")
            text_label.pack()
            text_entry = tk.Entry(self.property_panel)
            text_entry.pack()
            delay_before_label = tk.Label(self.property_panel, text="Delay Before:")
            delay_before_label.pack()
            delay_before_entry = tk.Entry(self.property_panel)
            delay_before_entry.pack()
            delay_after_label = tk.Label(self.property_panel, text="Delay After:")
            delay_after_label.pack()
            delay_after_entry = tk.Entry(self.property_panel)
            delay_after_entry.pack()
            submit_button = tk.Button(self.property_panel, text="Submit", command=lambda: [block.update_properties(text_entry.get(), delay_before_entry.get(), delay_after_entry.get()), self.display_block_properties(block), self.update_work_area(),self.display_json_editor()])
            submit_button.pack()
        elif isinstance(block, CopyClipboardBlock):
            delay_before_label = tk.Label(self.property_panel, text="Delay Before:")
            delay_before_label.pack()
            delay_before_entry = tk.Entry(self.property_panel)
            delay_before_entry.pack()
            delay_after_label = tk.Label(self.property_panel, text="Delay After:")
            delay_after_label.pack()
            delay_after_entry = tk.Entry(self.property_panel)
            delay_after_entry.pack()
            submit_button = tk.Button(self.property_panel, text="Submit", command=lambda: [block.update_properties(delay_before_entry.get(), delay_after_entry.get()), self.display_block_properties(block), self.update_work_area(),self.display_json_editor()])
            submit_button.pack()
        elif isinstance(block, PasteClipboardBlock):
            delay_before_label = tk.Label(self.property_panel, text="Delay Before:")
            delay_before_label.pack()
            delay_before_entry = tk.Entry(self.property_panel)
            delay_before_entry.pack()
            delay_after_label = tk.Label(self.property_panel, text="Delay After:")
            delay_after_label.pack()
            delay_after_entry = tk.Entry(self.property_panel)
            delay_after_entry.pack()
            submit_button = tk.Button(self.property_panel, text="Submit", command=lambda: [block.update_properties(delay_before_entry.get(), delay_after_entry.get()), self.display_block_properties(block), self.update_work_area(),self.display_json_editor()])
            submit_button.pack()
        elif isinstance(block, SelectAllBlock):
            delay_before_label = tk.Label(self.property_panel, text="Delay Before:")
            delay_before_label.pack()
            delay_before_entry = tk.Entry(self.property_panel)
            delay_before_entry.pack()
            delay_after_label = tk.Label(self.property_panel, text="Delay After:")
            delay_after_label.pack()
            delay_after_entry = tk.Entry(self.property_panel)
            delay_after_entry.pack()
            submit_button = tk.Button(self.property_panel, text="Submit", command=lambda: [block.update_properties(delay_before_entry.get(), delay_after_entry.get()), self.display_block_properties(block), self.update_work_area(),self.display_json_editor()])
            submit_button.pack()
        pass

    def add_to_json_editor(self, block):
        #before adding block to json editor, remove last 3 characters from json editor and add block to json editor
        json_text = self.json_editor.get("1.0", tk.END)
        json_text = json_text[:-3]
        json_text += str(block)+",\n}"
        self.json_editor.delete("1.0", tk.END)
        self.json_editor.insert(tk.END, json_text)
        pass

    def add_sequence_to_json_editor(self, sequence):
        json_text = self.json_editor.get("1.0", tk.END)
        self.json_editor.delete("1.0", tk.END)
        self.json_editor.insert(tk.END, str(sequence))
    

    def add_mouse_move_block(self):
        # Implement logic to add a MouseMoveBlock to the sequence
        # Open window asking for x and y
        
        # Create a new MouseMoveBlock
        # create new window
        window = tk.Toplevel(self.root)
        window.title("Add Mouse Move Block")
        # create x and y entry
        x_label = tk.Label(window, text="X:")
        x_label.pack()
        x_entry = tk.Entry(window)
        x_entry.pack()
        y_label = tk.Label(window, text="Y:")
        y_label.pack()
        y_entry = tk.Entry(window)
        y_entry.pack()
        # create delay before and after entry
        delay_before_label = tk.Label(window, text="Delay Before:")
        delay_before_label.pack()
        delay_before_entry = tk.Entry(window, textvariable=tk.StringVar(value="0"))
        delay_before_entry.pack()
        delay_after_label = tk.Label(window, text="Delay After:")
        delay_after_label.pack()
        delay_after_entry = tk.Entry(window, textvariable=tk.StringVar(value="0"))
        delay_after_entry.pack()
        # create submit button
        # create validation for x and y and for delay before and after entry. check if they are positive int 
        def validate_input(input):
            try:
                return int(input) > 0
            except:
                return False
        submit_button = tk.Button(window, text="Submit", command=lambda: [self.sequence.add_block(MouseMoveBlock(int(x_entry.get()), int(y_entry.get()), int(delay_before_entry.get()), int(delay_after_entry.get()))), self.display_json_editor(), window.destroy(), self.update_work_area()])
        submit_button.pack()


    def add_select_all_block(self):
        # Implement logic to add a SelectAllBlock to the sequence
        window = tk.Toplevel(self.root)
        window.title("Add Select All Block")
        # create delay before and after entry
        delay_before_label = tk.Label(window, text="Delay Before:")
        delay_before_label.pack()
        delay_before_entry = tk.Entry(window, textvariable=tk.StringVar(value="0"))
        delay_before_entry.pack()
        delay_after_label = tk.Label(window, text="Delay After:")
        delay_after_label.pack()
        delay_after_entry = tk.Entry(window, textvariable=tk.StringVar(value="0"))
        delay_after_entry.pack()
        # create submit button
        submit_button = tk.Button(window, text="Submit", command=lambda: [self.sequence.add_block(SelectAllBlock(int(delay_before_entry.get()), int(delay_after_entry.get()))), self.display_json_editor(), window.destroy(), self.update_work_area()])
        submit_button.pack()
        pass
    
    def add_mouse_click_block(self):
        # Implement logic to add a MouseClickBlock to the sequence
        # open window asking for click type, hold, amount, delay before and after
        window = tk.Toplevel(self.root)
        window.title("Add Mouse Click Block")
        # create click type radio buttons
        click_type = tk.StringVar()
        click_type.set("left")
        click_left = tk.Radiobutton(window, text="Left", variable=click_type, value="left")
        click_left.pack()
        click_right = tk.Radiobutton(window, text="Right", variable=click_type, value="right")
        click_right.pack()
        click_middle = tk.Radiobutton(window, text="Middle", variable=click_type, value="middle")
        click_middle.pack()
        # create click hold checkbutton
        click_hold = tk.BooleanVar()
        click_hold.set(False)
        click_hold_checkbox = tk.Checkbutton(window, text="Hold", variable=click_hold)
        click_hold_checkbox.pack()
        # create click amount entry
        click_amount_label = tk.Label(window, text="Amount:")
        click_amount_label.pack()
        click_amount_entry = tk.Entry(window, textvariable=tk.StringVar(value="1"))
        click_amount_entry.pack()
        # create delay before and after entry
        delay_before_label = tk.Label(window, text="Delay Before:")
        delay_before_label.pack()
        delay_before_entry = tk.Entry(window, textvariable=tk.StringVar(value="0"))
        delay_before_entry.pack()
        delay_after_label = tk.Label(window, text="Delay After:")
        delay_after_label.pack()
        delay_after_entry = tk.Entry(window, textvariable=tk.StringVar(value="0"))
        delay_after_entry.pack()
        # create submit button
        submit_button = tk.Button(window, text="Submit", command=lambda: [self.sequence.add_block(MouseClickBlock(click_type=click_type.get(), hold=click_hold.get(), click_amount=click_amount_entry.get(), delay_before_action=int(delay_before_entry.get()), delay_after_action=int(delay_after_entry.get()))), self.display_json_editor(), window.destroy(), self.update_work_area()])
        submit_button.pack()
        
    
    def add_mouse_scroll_block(self):
        window = tk.Toplevel(self.root)
        window.title("Add Mouse Scroll Block")
        # create amount entry
        amount_label = tk.Label(window, text="Amount:")
        amount_label.pack()
        amount_entry = tk.Entry(window)
        amount_entry.pack()
        # create direction radio buttons
        direction = tk.BooleanVar()
        direction.set(True)
        direction_up = tk.Radiobutton(window, text="Up", variable=direction, value=True)
        direction_up.pack()
        direction_down = tk.Radiobutton(window, text="Down", variable=direction, value=False)
        direction_down.pack()
        # create delay before and after entry
        delay_before_label = tk.Label(window, text="Delay Before:")
        delay_before_label.pack()
        delay_before_entry = tk.Entry(window, textvariable=tk.StringVar(value="0"))
        delay_before_entry.pack()
        delay_after_label = tk.Label(window, text="Delay After:")

        delay_after_label.pack()
        delay_after_entry = tk.Entry(window, textvariable=tk.StringVar(value="0"))
        delay_after_entry.pack()
        # create submit button
        submit_button = tk.Button(window, text="Submit", command=lambda: [self.sequence.add_block(MouseScrollBlock(int(amount_entry.get()), direction.get(), int(delay_before_entry.get()), int(delay_after_entry.get()))), self.display_json_editor(), window.destroy(), self.update_work_area()])
        submit_button.pack()

        pass
    
    def add_keyboard_type_block(self):
        # Implement logic to add a KeyboardTypeBlock to the sequence
        window = tk.Toplevel(self.root)
        window.title("Add Keyboard Type Block")
        # create text entry
        text_label = tk.Label(window, text="Text:")
        text_label.pack()
        text_entry = tk.Entry(window)
        text_entry.pack()
        # create delay before and after entry
        delay_before_label = tk.Label(window, text="Delay Before:")
        delay_before_label.pack()
        delay_before_entry = tk.Entry(window, textvariable=tk.StringVar(value="0"))
        delay_before_entry.pack()
        delay_after_label = tk.Label(window, text="Delay After:")
        delay_after_label.pack()
        delay_after_entry = tk.Entry(window, textvariable=tk.StringVar(value="0"))
        delay_after_entry.pack()
        # create submit button
        submit_button = tk.Button(window, text="Submit", command=lambda: [self.sequence.add_block(KeyboardTypeBlock(text_entry.get(), int(delay_before_entry.get()), int(delay_after_entry.get()))), self.display_json_editor(), window.destroy(), self.update_work_area()])
        submit_button.pack()

        pass
    
    def add_copy_clipboard_block(self):
        # Implement logic to add a CopyClipboardBlock to the sequence
        window = tk.Toplevel(self.root)
        window.title("Add Copy Clipboard Block")
        # create delay before and after entry
        delay_before_label = tk.Label(window, text="Delay Before:")
        delay_before_label.pack()
        delay_before_entry = tk.Entry(window, textvariable=tk.StringVar(value="0"))
        delay_before_entry.pack()
        delay_after_label = tk.Label(window, text="Delay After:")
        delay_after_label.pack()
        delay_after_entry = tk.Entry(window, textvariable=tk.StringVar(value="0"))
        delay_after_entry.pack()
        # create submit button
        submit_button = tk.Button(window, text="Submit", command=lambda: [self.sequence.add_block(CopyClipboardBlock(int(delay_before_entry.get()), int(delay_after_entry.get()))), self.display_json_editor(), window.destroy(), self.update_work_area()])
        submit_button.pack()
        
        pass
    
    def add_paste_clipboard_block(self):
        # Implement logic to add a PasteClipboardBlock to the sequence
        window = tk.Toplevel(self.root)
        window.title("Add Paste Clipboard Block")
        # create delay before and after entry
        delay_before_label = tk.Label(window, text="Delay Before:")
        delay_before_label.pack()
        delay_before_entry = tk.Entry(window, textvariable=tk.StringVar(value="0"))
        delay_before_entry.pack()
        delay_after_label = tk.Label(window, text="Delay After:")
        delay_after_label.pack()
        delay_after_entry = tk.Entry(window, textvariable=tk.StringVar(value="0"))
        delay_after_entry.pack()
        # create submit button
        submit_button = tk.Button(window, text="Submit", command=lambda: [self.sequence.add_block(PasteClipboardBlock(int(delay_before_entry.get()), int(delay_after_entry.get()))), self.display_json_editor(), window.destroy(), self.update_work_area()])
        submit_button.pack()
        
        pass

        

    def display_sequence(self):
        # Implement logic to display the sequence of blocks on the work area canvas
        # Clear the work area canvas
        self.work_area.delete("all")
        
        # Display the blocks on the work area canvas
        # Create graphical representations of the blocks and connect them with arrows

        self.work_area.block_positions = {}
        for i in range(len(self.sequence.blocks)):
            block = self.sequence.blocks[i]
            if isinstance(block, MouseMoveBlock):
                block_id = self.work_area.create_rectangle(10, 10, 50, 50, fill="blue")
            elif isinstance(block, MouseClickBlock):
                block_id = self.work_area.create_rectangle(10, 10, 50, 50, fill="red")
            elif isinstance(block, MouseScrollBlock):
                block_id = self.work_area.create_rectangle(10, 10, 50, 50, fill="green")
            elif isinstance(block, KeyboardTypeBlock):
                block_id = self.work_area.create_rectangle(10, 10, 50, 50, fill="yellow")
            elif isinstance(block, CopyClipboardBlock):
                block_id = self.work_area.create_rectangle(10, 10, 50, 50, fill="orange")
            elif isinstance(block, PasteClipboardBlock):
                block_id = self.work_area.create_rectangle(10, 10, 50, 50, fill="purple")
            
            self.work_area.block_positions[block_id] = (50*i, 50*i)
            self.work_area.create_text(30, 30, text=str(i))
            
            if i > 0:
                self.work_area.create_line(self.work_area.block_positions[block_id-1][0], self.work_area.block_positions[block_id-1][1], self.work_area.block_positions[block_id][0], self.work_area.block_positions[block_id][1])
            
    def save_sequence_to_json(self, file_path):
        # Implement logic to save the sequence of blocks to a JSON file
        # Convert the sequence to a JSON string
        json_string = str(self.sequence)
        data = json.loads(json_string)
        with open(file_path, "w") as file:
            json.dump(data, file)

        pass

    def load_sequence_from_json(self, file_path):
        # Implement logic to load a sequence of blocks from a JSON file
        # Load the JSON file and convert it to a sequence of blocks
        load_from_json = LoadFromJSON(file_path)
        self.sequence = load_from_json.get_blocks()
        pass
    
    def display_json_editor(self):
        # Implement logic to display the JSON editor with the sequence of blocks as JSON text
        # Clear the JSON editor
        self.json_editor.delete("1.0", tk.END)
        
        # Display the sequence of blocks as JSON text
        json_string = str(self.sequence)
        self.json_editor.insert(tk.END, json_string)
        pass

    def save_json_editor_to_sequence(self):
        # Implement logic to save the JSON text in the editor to the sequence of blocks
        # Convert the JSON text to a sequence of blocks
        json_string = self.json_editor.get("1.0", tk.END)
        data = json.loads(json_string)
        self.sequence = BlockSequence()
        

        pass

    def display_block_properties(self, block):
        # Implement logic to display the properties of a block on the property panel
        # Clear the property panel
        for widget in self.property_panel.winfo_children():
            widget.destroy()
        
        # Display the properties of the block
        # Create labels and entry fields for each property
        # Add a submit button to update the block's properties
        self.property_panel.block = block
        if isinstance(block, MouseMoveBlock):
            x_label = tk.Label(self.property_panel, text="X:")
            x_label.pack()
            x_entry = tk.Entry(self.property_panel)
            x_entry.insert(0, block.x)
            x_entry.pack()
            y_label = tk.Label(self.property_panel, text="Y:")
            y_label.pack()
            y_entry = tk.Entry(self.property_panel)
            y_entry.insert(0, block.y)
            y_entry.pack()
            delay_before_label = tk.Label(self.property_panel, text="Delay Before:")
            delay_before_label.pack()
            delay_before_entry = tk.Entry(self.property_panel)
            delay_before_entry.insert(0, block.delay_before_action)
            delay_before_entry.pack()
            delay_after_label = tk.Label(self.property_panel, text="Delay After:")
            delay_after_label.pack()
            delay_after_entry = tk.Entry(self.property_panel)
            delay_after_entry.insert(0, block.delay_after_action)
            delay_after_entry.pack()
            submit_button = tk.Button(self.property_panel, text="Submit", command=lambda: [block.update_properties(x_entry.get(), y_entry.get(), delay_before_entry.get(), delay_after_entry.get()), self.display_block_properties(block), self.update_work_area(),self.display_json_editor()])
            submit_button.pack()
        elif isinstance(block, MouseClickBlock):
            click_type = tk.StringVar()
            click_type.set("left")
            click_left = tk.Radiobutton(self.property_panel, text="Left", variable=click_type, value="left")
            click_left.pack()
            click_right = tk.Radiobutton(self.property_panel, text="Right", variable=click_type, value="right")
            click_right.pack()
            click_middle = tk.Radiobutton(self.property_panel, text="Middle", variable=click_type, value="middle")
            click_middle.pack()
            click_hold = tk.BooleanVar()
            click_hold.set(False)
            click_hold_checkbox = tk.Checkbutton(self.property_panel, text="Hold", variable=click_hold)
            click_hold_checkbox.pack()
            click_amount_label = tk.Label(self.property_panel, text="Amount:")
            click_amount_label.pack()
            click_amount_entry = tk.Entry(self.property_panel)
            click_amount_entry.pack()
            delay_before_label = tk.Label(self.property_panel, text="Delay Before:")
            delay_before_label.pack()
            delay_before_entry = tk.Entry(self.property_panel)
            delay_before_entry.pack()
            delay_after_label = tk.Label(self.property_panel, text="Delay After:")
            delay_after_label.pack()
            delay_after_entry = tk.Entry(self.property_panel)
            delay_after_entry.pack()
            submit_button = tk.Button(self.property_panel, text="Submit", command=lambda: [block.update_properties(click_type.get(), click_hold.get(), click_amount_entry.get(), delay_before_entry.get(), delay_after_entry.get()), self.display_block_properties(block), self.update_work_area(),self.display_json_editor()])
            submit_button.pack()
        elif isinstance(block, MouseScrollBlock):
            amount_label = tk.Label(self.property_panel, text="Amount:")
            amount_label.pack()
            amount_entry = tk.Entry(self.property_panel)
            amount_entry.pack()
            direction = tk.BooleanVar()
            direction.set(True)
            direction_up = tk.Radiobutton(self.property_panel, text="Up", variable=direction, value=True)
            direction_up.pack()
            direction_down = tk.Radiobutton(self.property_panel, text="Down", variable=direction, value=False)
            direction_down.pack()
            delay_before_label = tk.Label(self.property_panel, text="Delay Before:")
            delay_before_label.pack()
            delay_before_entry = tk.Entry(self.property_panel)
            delay_before_entry.pack()
            delay_after_label = tk.Label(self.property_panel, text="Delay After:")
            delay_after_label.pack()
            delay_after_entry = tk.Entry(self.property_panel)
            delay_after_entry.pack()
            submit_button = tk.Button(self.property_panel, text="Submit", command=lambda: [block.update_properties(amount_entry.get(), direction.get(), delay_before_entry.get(), delay_after_entry.get()), self.display_block_properties(block), self.update_work_area(),self.display_json_editor()])
            submit_button.pack()
        elif isinstance(block, KeyboardTypeBlock):
            text_label = tk.Label(self.property_panel, text="Text:")
            text_label.pack()
            text_entry = tk.Entry(self.property_panel)
            text_entry.pack()
            delay_before_label = tk.Label(self.property_panel, text="Delay Before:")
            delay_before_label.pack()
            delay_before_entry = tk.Entry(self.property_panel)
            delay_before_entry.pack()
            delay_after_label = tk.Label(self.property_panel, text="Delay After:")
            delay_after_label.pack()
            delay_after_entry = tk.Entry(self.property_panel)
            delay_after_entry.pack()
            submit_button = tk.Button(self.property_panel, text="Submit", command=lambda: [block.update_properties(text_entry.get(), delay_before_entry.get(), delay_after_entry.get()), self.display_block_properties(block), self.update_work_area(),self.display_json_editor()])
            submit_button.pack()
        elif isinstance(block, CopyClipboardBlock):
            delay_before_label = tk.Label(self.property_panel, text="Delay Before:")
            delay_before_label.pack()
            delay_before_entry = tk.Entry(self.property_panel)
            delay_before_entry.pack()
            delay_after_label = tk.Label(self.property_panel, text="Delay After:")
            delay_after_label.pack()
            delay_after_entry = tk.Entry(self.property_panel)
            delay_after_entry.pack()
            submit_button = tk.Button(self.property_panel, text="Submit", command=lambda: [block.update_properties(delay_before_entry.get(), delay_after_entry.get()), self.display_block_properties(block), self.update_work_area(),self.display_json_editor()])
            submit_button.pack()
        elif isinstance(block, PasteClipboardBlock):
            delay_before_label = tk.Label(self.property_panel, text="Delay Before:")
            delay_before_label.pack()
            delay_before_entry = tk.Entry(self.property_panel)
            delay_before_entry.pack()
            delay_after_label = tk.Label(self.property_panel, text="Delay After:")
            delay_after_label.pack()
            delay_after_entry = tk.Entry(self.property_panel)
            delay_after_entry.pack()
            submit_button = tk.Button(self.property_panel, text="Submit", command=lambda: [block.update_properties(delay_before_entry.get(), delay_after_entry.get()), self.display_block_properties(block), self.update_work_area(),self.display_json_editor()])
            submit_button.pack()
        elif isinstance(block, SelectAllBlock):
            delay_before_label = tk.Label(self.property_panel, text="Delay Before:")
            delay_before_label.pack()
            delay_before_entry = tk.Entry(self.property_panel)
            delay_before_entry.pack()
            delay_after_label = tk.Label(self.property_panel, text="Delay After:")
            delay_after_label.pack()
            delay_after_entry = tk.Entry(self.property_panel)
            delay_after_entry.pack()
            submit_button = tk.Button(self.property_panel, text="Submit", command=lambda: [block.update_properties(delay_before_entry.get(), delay_after_entry.get()), self.display_block_properties(block), self.update_work_area(),self.display_json_editor()])
            submit_button.pack()

# Implement the update_properties method for each block class
# Implement the is_clicked method for each block class
        

# Create the root window
root = tk.Tk()

# Create an instance of the CommandEditorGUI class
command_editor = CommandEditorGUI(root)

# Start the Tkinter event loop
root.mainloop()
