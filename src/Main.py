import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import imageio_ffmpeg
import imageio
import os
import matplotlib as mpl
from matplotlib.colors import ListedColormap
import re


class GUI:
    def __init__(self, Image_arr, wavenumber_arr, file_location):
        # get the data, it's size, wavenumber range and file location
        self.Image_arr = Image_arr
        self.Image_arr = np.flip(Image_arr, axis=0)
        self.shape = np.shape(self.Image_arr)
        self.current_image_index = 0
        self.wavenumber_arr = wavenumber_arr
        self.file_location = file_location
        
        # create the main window and canvas
        self.root = tk.Tk()
        self.root.title("Hyperspectral imaging analysis") 
        self.root.geometry("1200x500")              # set window size
        self.root.resizable(False, False)           # prevent window resizing       

        # create the figure
        self.fig = Figure(figsize=(14, 5))
        hex_colors = [
            "#000000", "#000005", "#00000a", "#00000f", "#000014", "#00001a", "#00001f", "#000024", 
            "#000029", "#00002e", "#000034", "#000039", "#00003e", "#000043", "#000048", "#00004e", 
            "#000053", "#000058", "#00005d", "#000062", "#000068", "#00006d", "#000072", "#000077", 
            "#00007c", "#000082", "#000087", "#00008c", "#000091", "#000096", "#00009c", "#0000a1", 
            "#0000a6", "#0000ab", "#0000b0", "#0000b6", "#0000bb", "#0000c0", "#0000c5", "#0000ca", 
            "#0000d0", "#0000d5", "#0000da", "#0000df", "#0000e4", "#0000ea", "#0000ef", "#0000f4", 
            "#0400f9", "#0900ff", "#0e00fa", "#1300f5", "#1700ef", "#1c00ea", "#2100e4", "#2600df", 
            "#2a00da", "#2f00d4", "#3400cf", "#3900c9", "#3d00c4", "#4200be", "#4700b9", "#4c00b4", 
            "#5100ae", "#5100a9", "#5100a3", "#51009e", "#510098", "#510093", "#51008e", "#510088", 
            "#500083", "#50007d", "#500078", "#500072", "#50006d", "#500068", "#500062", "#4f005d", 
            "#540057", "#590052", "#5e004c", "#630047", "#680042", "#6d003c", "#720037", "#770031", 
            "#7c002c", "#810026", "#860021", "#8b001c", "#900016", "#950011", "#9a000b", "#9f0006", 
            "#a40000", "#a90000", "#ae0000", "#b40000", "#b90000", "#be0000", "#c40000", "#c90000", 
            "#ce0000", "#d40000", "#d90000", "#de0000", "#e40000", "#e90000", "#ff0000", "#ff0000", 
            "#ff0000", "#ff0000", "#ff0500", "#ff0a00", "#ff1000", "#ff1500", "#ff1b00", "#ff2000", 
            "#ff2500", "#ff2b00", "#ff3000", "#ff3600", "#ff3b00", "#ff4000", "#ff4600", "#ff4b00", 
            "#ff5100", "#ff5504", "#ff5a09", "#ff5f0e", "#ff6413", "#ff6918", "#ff6d1c", "#ff7221", 
            "#ff7726", "#ff7c2b", "#ff8130", "#ff8635", "#ff8a39", "#ff8f3e", "#ff9443", "#ff9948", 
            "#ff9e4d", "#ffa352", "#ffa34d", "#ffa347", "#ffa341", "#ffa33b", "#ffa335", "#ffa32f", 
            "#ffa329", "#ffa324", "#ffa31e", "#ffa318", "#ffa312", "#ffa30c", "#ffa306", "#ffa300", 
            "#ffa300", "#ffa300", "#ffa300", "#f8a300", "#f0a300", "#e8a300", "#e1a300", "#d9a300", 
            "#d1a300", "#caa300", "#c2a300", "#baa300", "#b3a300", "#aba300", "#a3a300", "#a8a300",
            "#ada300", "#b2a903", "#b7af06", "#bcb509", "#c1bb0c", "#c6c110", "#cbc713", "#d1cd16",
            "#d6d419", "#dbda1d", "#e0e020", "#e5e623", "#eaec26", "#eff229", "#f4f82d", "#f9ff30",
            "#ffff33", "#ffff36", "#ffff3a", "#ffff3d", "#ffff40", "#ffff43", "#ffff47", "#ffff4a",
            "#ffff4d", "#ffff50", "#ffff53", "#ffff57", "#ffff5a", "#ffff5d", "#ffff60", "#ffff64", 
            "#ffff67", "#ffff6a", "#ffff6d", "#ffff70", "#ffff74", "#ffff77", "#ffff7a", "#ffff7d", 
            "#ffff81", "#ffff84", "#ffff87", "#ffff8a", "#ffff8e", "#ffff91", "#ffff94", "#ffff97",
            "#ffff9a", "#ffff9e", "#ffffa1", "#ffffa4", "#ffffa7", "#ffffab", "#ffffae", "#ffffb1",
            "#ffffb4", "#ffffb7", "#ffffbb", "#ffffbe", "#ffffc1", "#ffffc4", "#ffffc8", "#ffffcb",
            "#ffffce", "#ffffd1", "#ffffd5", "#ffffd8", "#ffffdb", "#ffffde", "#ffffe1", "#ffffe5",
            "#ffffe8", "#ffffeb", "#ffffee", "#fffff2", "#fffff5", "#fffff8", "#fffffb", "#ffffff"
        ]
        rgb_colors = [mpl.colors.hex2color(color) for color in hex_colors]
        self.cmap = ListedColormap(rgb_colors)

        # create image plot
        self.ax = self.fig.add_subplot(121)
        self.ax.axis('off')                                                                     # turn off axis and ticks
        self.im = self.ax.imshow(self.Image_arr[self.current_image_index], cmap=self.cmap)      # create the image plot
        divider = make_axes_locatable(self.ax)                                                  # create axes for colorbar
        cax = divider.append_axes("right", size="5%", pad=0.05)                                 # position, size and distance form the image of the colorbar
        cbar  = self.fig.colorbar(self.im, cax=cax, label = "wIR-PHI signal (a.u.)")            # create colorbar
        self.im.set_clim(np.min(self.Image_arr), np.max(self.Image_arr))                        # set the limits of the colorbar to the min and max of the data
        # create spectra plot
        self.rectangle = self.ax.add_patch(plt.Rectangle((10,10),3,3,edgecolor='r',facecolor='none')) # select the initial area for the spectra
        self.ax2 = self.fig.add_subplot(122)                                                          # create a 2d graph on the left side of the window. plot of the data x_data and y_data

        # create the tkinter canvas and add the figure to it
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        # add the toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.update()

        # create a button to open a file
        self.open_button = tk.Button(self.root, text="Open File", command=self.open_file)
        self.open_button.place(x=15, y=15)
        #create a button to save image
        self.save_button = tk.Button(self.root, text="Save Image", command=self.save_image)
        self.save_button.place(x=15, y=45)

        # create curent wavenumber lable on a canvas
        self.current_wv = self.wavenumber_arr[self.current_image_index]
        self.label = tk.Label(self.root, text=(f"Wavenumer: {self.current_wv} (cm⁻¹)"))
        self.label.place(x=300, y=15)
        # create a wavenumber slider for scrolling through the images
        self.lambda_slider = tk.Scale(self.root, from_=0, to=self.shape[0]-1, command=self.update_image, orient=tk.HORIZONTAL, length=387, showvalue=False)
        self.lambda_slider.set(0)
        self.lambda_slider.pack(side=tk.BOTTOM, fill=tk.X)
        self.lambda_slider.place(x=154, y=35)

        # create spectra parremeters title
        self.label2 = tk.Label(self.root, text=("Spectra parameters:"))
        self.label2.place(x=15, y=125)
        # create a rectangle position (width and height) sliders 
        self.x_slider = tk.Scale(self.root, from_=0, to=self.shape[2], command=self.update_spectra, label="x-axis", orient=tk.HORIZONTAL)
        self.y_slider = tk.Scale(self.root, from_=0, to=self.shape[1], command=self.update_spectra, label="y-axis", orient=tk.HORIZONTAL)
        self.width_slider = tk.Scale(self.root, from_=0, to=self.shape[2], command=self.update_spectra, label="width", orient=tk.HORIZONTAL)
        self.height_slider = tk.Scale(self.root, from_=0, to=self.shape[1], command=self.update_spectra, label="hight", orient=tk.HORIZONTAL)
        for slider in [self.x_slider, self.y_slider, self.width_slider, self.height_slider]: # set initial rectangle dimensionas and position
            slider.set(3)
        #plase rectangle position sliders on the canvas
        self.x_slider.place(x=15, y=145)
        self.width_slider.place(x=15, y=200)
        self.y_slider.place(x=15, y=280)
        self.height_slider.place(x=15, y=340)

        # create a button to save the spectra with it's coordinates
        self.update_button = tk.Button(self.root, text="Save Spectra", command=self.save_spectra)
        self.update_button.place(x=15, y=410)

        # start the GUI event loop
        self.root.mainloop()

    def open_file(self): # open a file when the button is clicked
        self.file_path = filedialog.askopenfilename(filetypes=[("Numpy files", "*.npy")]) # load the data from the file
        if self.file_path:
            self.Image_arr = np.load(self.file_path)
            self.Image_arr = np.flip(self.Image_arr, axis=0)
            self.shape = np.shape(self.Image_arr)
            self.current_image_index = 0
            
            # Extract wavenumber information from the file path
            match = re.search(r'\[(\d+)-(\d+)-(\d+)\]', self.file_path)
            if match:
                start_wavenumber = int(match.group(2))
                end_wavenumber = int(match.group(1))
                step_wavenumber = int(match.group(3))
                self.wavenumber_arr = np.arange(start_wavenumber, end_wavenumber - step_wavenumber, -step_wavenumber)
            else: #print in red
                print (f"Can't extract wavenumber information from the file path: {self.file_path}")

            # Update the sliders' ranges
            self.lambda_slider.config(to=self.shape[0]-1)
            self.x_slider.config(to=self.shape[2])
            self.y_slider.config(to=self.shape[1])
            self.width_slider.config(to=self.shape[2])
            self.height_slider.config(to=self.shape[1])

            self.update_image(0)
            self.im.set_clim(np.min(self.Image_arr), np.max(self.Image_arr))  # update the colormap limits
            self.update_spectra()                                             # update the spectra plot

    def update_image(self, index):
        self.current_image_index = int(index)
        self.im.set_data(self.Image_arr[self.current_image_index])
        self.current_wv = self.wavenumber_arr[self.current_image_index]
        self.label = tk.Label(self.root, text=(f"Wavenumer: {self.current_wv} (cm⁻¹)"))
        self.label.place(x=300, y=15)
        self.canvas.draw_idle()

    def save_image(self):
        directory_path = os.path.dirname(self.file_path)
        np.savetxt(f"{directory_path}/{self.current_wv}(cm⁻¹).txt", self.Image_arr[self.current_image_index])#, fmt='%1.4e')

    def update_spectra(self, event=None):
        #update rctange position and size
        x = self.x_slider.get()
        y = self.y_slider.get()
        width = self.width_slider.get()
        height = self.height_slider.get()
        self.rectangle.set_bounds(x, y, width, height)

        #calculate the spectra
        self.signal = np.max(self.Image_arr[:,y:y+width+1,x:x+height+1], axis = (1,2))
        # print (self.signal)
        #update the spectra plot
        self.ax2.clear()                                     # clear the current plot
        self.ax2.plot(self.wavenumber_arr, self.signal)      # update the data of the plot
        self.ax2.set_ylabel("wIR-PHI signal (a.u.)")
        self.ax2.set_xlabel("Wavenumber (cm⁻¹)")
        self.ax2.set_title("wIR-PHI spectra")
        self.ax2.yaxis.set_label_position("right")
        self.ax2.tick_params(axis='both', which='both', direction='in', labelleft=False, labelright=True)       
        self.ax2.invert_xaxis()  # This line inverts the x-axis
        self.canvas.draw_idle()

    def save_spectra(self):
        #save the data
        self.spectra = np.array([self.wavenumber_arr, self.signal])
        self.spectra = self.spectra.T
        spectrum_name = f"spectra_x={self.x_slider.get()}_y={self.y_slider.get()}_width={self.width_slider.get()}_height={self.height_slider.get()}.txt"
        directory_path = os.path.dirname(self.file_path)
        spectra_path = f"{directory_path}/{spectrum_name}"
        np.savetxt(spectra_path, self.spectra)
        #save the coordinates
        self.coordinates = np.array([self.x_slider.get(), self.y_slider.get(), self.width_slider.get(), self.height_slider.get()])
        print (f"Spectra saved as {spectrum_name}")

if __name__ == "__main__":
    Image_arr = np.random.rand(201, 100, 100)
    wavenumber_arr = np.arange(1840, 1040-4, -4)
    file_location = '.'
    GUI(Image_arr, wavenumber_arr, file_location)