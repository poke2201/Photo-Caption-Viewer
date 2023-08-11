import PySimpleGUI as sg
import os


class EmptyFindText(Exception):
    "Find Text in Add Mode is empty"
    pass

class FileMissing(Exception):
    "File went missing before image updated"
    pass

def initialize_files(folder_path):

    image_list = [file for file in os.listdir(folder_path) if file.endswith(".png")]

    return image_list

def caption_match(filepath):
    
    # Matches Image to Caption, assumes same name
    
    match_name = os.path.splitext(filepath)[0] + ".txt"
    if os.path.isfile(match_name) is True:
        return match_name
    else:
        return ""

def update_folders():
    if values["-FOLDER-"] == "":
        # Needed for copy paste functionality, event loop will update values["-FOLDER-"] next iteration
        pass
    else:
        image_list = initialize_files(values["-FOLDER-"])
        window["-FILE LIST-"].update(image_list, set_to_index=0)
        window["-FILE LIST-"].set_focus()
        get_data(values["-FOLDER-"], image_list[0], window)

        return image_list

def get_data(folder_value, file_value, window, deletion_check_bool=False):

    #DOES NOT WORK WITH SPACES IN IMAGE NAME
    
    try:
        filename = os.path.join(folder_value, file_value)
        caption_file = caption_match(filename)
        window["-IMAGE OUT-"].update(filename)
        if os.path.isfile(filename) == True:
            window["-IMAGE-"].update(filename=filename)
        else:
            raise FileMissing("File went missing before image updated.")
        if caption_file != "":
            window["-CAPTION_FILE-"].update(value=caption_file)
            with open(caption_file) as caption:
                lines = caption.read()
                window["-CAPTION_DATA-"].update(value = lines)
        else:
            window["-CAPTION_DATA-"].update(value = '')
            window["-LOG CAPTION-"].update(value='No caption found in folder')

    except Exception as e:
        # Handles error only when GUI event deletes items. Default boolean value is false to prevent accidental deletions.
        if deletion_check_bool == False:
            sg.popup_error(f'An error happened.  Here is the info: {e} Refreshing window and removing missing reference.')
            update_folders()
        else:
            pass

def find_replace_caption(txt_file, replace_text, find_text='', mode='Add'):
    with open(txt_file, 'r') as caption_file:
        caption = caption_file.read()

        if mode == 'Add':

            #ONLY WORKS ON THE FIRST INSTANCE CURRENTLY
            
            if find_text == '':
                raise EmptyFindText("Find Text in Add Mode is empty.")
            else:
                split_caption = caption.split(' ')
                insert_index = [index for index, caption_part in enumerate(split_caption) if find_text in caption_part][0] + 1
                split_caption.insert(insert_index, replace_text)
                caption = ' '.join(split_caption)

        elif mode == 'Prefix':
            caption = f"{replace_text} {caption}"

        elif mode == 'Suffix':
            caption = f"{caption} {replace_text}"
        
        else:
            if find_text == '':
                raise EmptyFindText("Find Text in Add Mode is empty.")
            else:
                caption = caption.replace(find_text, replace_text)

    with open(txt_file, 'w') as caption_file:
        caption_file.write(caption)
    

def find_replace_window(folder):
    caption_mode = ['Add', 'Prefix', 'Suffix', 'Replace']
    
    text_input_column = [
        [sg.Text('Original Text', size=(30,1)), sg.InputText(key="-FIND-")],
        [sg.Text('Replacement or Additional Text', size=(30,1)), sg.InputText(key="-REPLACE-")]
    ]
    
    layout = [
        [sg.Column(text_input_column)],
        [sg.Combo(caption_mode, default_value=caption_mode[0], auto_size_text=True, readonly=True, key="-CAPTION MODE-")],
        [sg.Button('Proceed', bind_return_key=True), sg.Button('Close'),]

    ]
    
    window = sg.Window("Find and Replace Caption Tool", layout, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Close" or event == sg.WIN_CLOSED:
            break
        elif event == "Proceed":
            try:
                values_tuple = (values["-REPLACE-"], values["-FIND-"], values["-CAPTION MODE-"])
                
                caption_list = [file for file in os.listdir(folder) if file.endswith(".txt")]
                batch_caption = [os.path.join(folder, caption)for caption in caption_list]

                for caption_file in batch_caption:
                    find_replace_caption(caption_file, values_tuple[0], values_tuple[1], values_tuple[2])

                sg.popup('Operation Completed!')
                
            except EmptyFindText:
                sg.popup_error("Original (Find) Text is empty, this operation requires a find text.")

    window.close()

        
# ----- GUI Elements -----

sg.theme('BluePurple')

file_list_column =[
    [sg.Push(), sg.Text('Training Folder'), sg.Input(size=(50,2), enable_events=True, key="-FOLDER-"), sg.FolderBrowse(key="-FOLDER-")],
    
    [sg.Push(), sg.Listbox(values=[], size=(40,20), enable_events=True, key="-FILE LIST-"), sg.Push()],
]

image_viewer_column = [
    [sg.Text("Image Selected:", size=(40,1))],
    [sg.Text("Select File", key="-IMAGE OUT-", size=(50,3))],
    [sg.Image(key="-IMAGE-")],
]

text_viewer_column = [
    [sg.Text("Caption Selected:", size=(40,1))],
    [sg.Text("Select File", key="-CAPTION_FILE-", size=(50,3))],
    [sg.Multiline(key="-CAPTION_DATA-",
                        size=(50,10),
                        default_text="Select image file to display found caption"),
     sg.Button("Save")],
    [sg.Button("Find and Replace Batch Captions")],
    [sg.Text(key="-LOG CAPTION-")]
        
]

image_control_column = [[
    sg.Button("Previous Image"),
    sg.Button("Next Image"),
    sg.Button("Delete Image"),
    sg.Exit()],
    [sg.Text(key="-LOG IMAGE-")]
]


# ----- Layout -----

layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
        sg.VSeperator(),
        sg.Column(text_viewer_column), 
    ],
        [sg.Column(image_control_column)]
]


# ----- Event Loop -----

window = sg.Window("Image Viewer", layout, return_keyboard_events=True, finalize=True)
window.bind("<Control-d>", "Next Image")
window.bind("<Control-a>", "Previous Image")
window.bind("<Delete>", "Delete Image")
window.bind("<Control-s>", "Save")  # new line to bind Ctrl+s to Save

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    elif event == "-FOLDER-":
        try:
            image_list = update_folders()
            
        except Exception as e:
            print(e)

    if len(values["-FILE LIST-"]) > 0:
        if event == "-FILE LIST-":
            try:
                get_data(values["-FOLDER-"], values["-FILE LIST-"][0], window)
            except Exception as e:
                print(e)

        elif event == "Previous Image":
            # Iterate Up File List
            iter_index = image_list.index(values["-FILE LIST-"][0]) - 1

            if iter_index == -1:
                iter_index = len(image_list) -1
            
            # update values
            window["-FILE LIST-"].update(set_to_index=iter_index)
            get_data(values["-FOLDER-"], image_list[iter_index], window)

        elif event == "Next Image":
            # Iterate Down File List
            iter_index = image_list.index(values["-FILE LIST-"][0]) + 1

            if iter_index is len(image_list):
                iter_index = 0
            
            # update values
            window["-FILE LIST-"].update(set_to_index=iter_index)
            get_data(values["-FOLDER-"], image_list[iter_index], window)

        elif event == "Delete Image":
            # Delete Selected File and caption
            iter_index = image_list.index(values["-FILE LIST-"][0]) - 1
            filename = os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0])
            caption_file = caption_match(filename)
            window["-LOG IMAGE-"].update(f'Deleted {values["-FILE LIST-"][0]}')
            os.remove(filename)
            os.remove(caption_file)

            # Update Values
            try:
                get_data(values["-FOLDER-"], image_list[iter_index], window, deletion_check_bool=True)
                image_list = initialize_files(values["-FOLDER-"])

            except IndexError:
                image_list = []

            window["-FILE LIST-"].update(image_list)

        if event == "Find and Replace Batch Captions":
            find_replace_window(values["-FOLDER-"])

        elif event == "Save":
            filename = os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0])
            caption_file = caption_match(filename)

            if caption_file == "":
                window["-LOG CAPTION-"].update(f'No caption found in folder')

            else:
                with open(caption_file, "w") as caption:
                    caption.write(values["-CAPTION_DATA-"])
                window["-LOG CAPTION-"].update(f'Saved {values["-FILE LIST-"][0]}')

    else:
        if event == "Find and Replace Batch Captions":
            if values["-FOLDER-"] == '':
                window["-LOG CAPTION-"].update('Please select a folder')
            else:
                find_replace_window(values["-FOLDER-"])
        
        #Error Display without selected files
        elif event == "Previous Image":
            window["-LOG IMAGE-"].update("File not selected, select a file")

        elif event == "Next Image":
            window["-LOG IMAGE-"].update("File not selected, select a file")

        elif event == "Delete Image":
            window["-LOG IMAGE-"].update("File not selected, select a file")

        
            
window.close()
