# Photo-Caption-Viewer
Reducing the Pain of Captioning by making a gui.

## Installation

Use package manager [pip](https://pip.pypa.io/en/stable/) to install PySimpleGUI.  This is tested on Python 3.10.8, no idea if this will work on previous versions of Python.

```bash
python.exe -m pip install PySimpleGUI
```
On the GitHub page, click the green Code button, download as zip, then unzip it. Then if you have python configured to run .py files, just double click PhotoViewerScript.py

## Usage
Run the script and let the GUI open.
Select a folder with your training images and captions by clicking on the **Browse** button.  The program will still show images without captions but functionality becomes a photo app. As this program was written using Python's native tkinter package, **.JPG** photos are **not supported**.  Make sure all pictures are in .png.

![image](https://user-images.githubusercontent.com/48573359/211654614-970fd97f-181d-4973-9ebd-7b03032ad594.png)

The GUI will load a list of images in the folder along with paired captions.  The program is assuming the captions are the **same exact name as the picture**. Select any picture and the image and caption will load.

![image](https://user-images.githubusercontent.com/48573359/211935468-fd6fd3bd-ca9f-45ec-9c96-f264fd674ec5.png)

### Find and Replace Bulk Caption Feature
This feature is for bulk changing captions if there is something you really need to add.  

![image](https://user-images.githubusercontent.com/48573359/211656649-1a1ac585-ca66-4312-a81d-299669642687.png)

#### Modes of Bulk Caption Feature
- **Add** - Inserts text after a specific substring in caption. This assumes only one instance of the substring exists in caption, this may break for very large data sets until I find the time to somehow do caption verification.  Make sure your substring is one word to avoid any bugs.

- **Prefix** - Prepends text before caption.  **Original Text** not required.

- **Suffix** - Adds text to the end of caption. **Original Text** not required.

- **Replace** - Finds phrase and replaces with replacement.

### Keyboard Shortcuts (may add more in the future)
- **TAB** - Start editing caption

- **UP/DOWN Arrow Key** - Move up/down in image list

- **DEL** - Deletes image. **DOES NOT HAVE A CONFIRMATION SCREEN**.


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change

## License

[GPL](https://choosealicense.com/licenses/gpl-3.0/)
