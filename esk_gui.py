import tkinter as tk
from os import listdir
from main import target
import threading

class EskGui(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.grid(sticky=tk.N + tk.S + tk.W + tk.E)
        self.grid_propagate(0)

        parent.title("Eskdalemuir Vibrations")

        """
        Labels
        """

        self.label = tk.Label(parent, text="I'm picking up good vibrations...")
        self.label.grid(column=0, row=0, sticky=tk.W, columnspan=2)

        """
        Buttons
        """

        self.button_container = tk.Frame(parent)
        self.button_container.grid(column=1, row=2)

        # Run Button
        self.run_button = tk.Button(self.button_container, text="Run", command=self.select_options)
        self.run_button.grid(column=0, row=0, sticky=tk.W + tk.E)


        """
        Variables
        """
        self.download_path = (r"Q:\1 Projects\2 Development\381 Eskdalemuir"
                              r"\5 Technical\5.1 Monitoring Campaign\381-190109-4013")

        self.download_options = tk.Variable(value=listdir(self.download_path))
        self.sensor_options = tk.Variable(value=["6v70", "6v71", "6v73", "6w19", "6v24", "6o35", "6t93",
                                                 "Fortis1", "Rad1", "Rad2"])

        """
        List Boxes
        """

        # download folders
        self.download_box = tk.Listbox(listvariable=self.download_options,
                                       selectmode=tk.MULTIPLE, exportselection=0)

        self.download_box.grid(column=0, row=1)

        # sensors
        self.sensor_box = tk.Listbox(listvariable=self.sensor_options, selectmode=tk.MULTIPLE, exportselection=0)
        self.sensor_box.grid(column=2, row=1)

        """
        Entries
        """

        self.out_path = tk.Entry(parent)
        self.out_path.grid(column=2, row=2)

    def select_options(self):
        """
        :return:
        """

        """
        define the variables we want to output
        """
        download_out_list = list()
        accelerometer_out_list = list()
        sensor_out_list = list()

        """
        Assign the data to the lists
        """
        download_selection = self.download_box.curselection()
        for download_folder in download_selection:
            value = self.download_box.get(download_folder)
            download_out_list.append(value)


        sensor_selection = self.sensor_box.curselection()
        for sensor in sensor_selection:
            value = self.sensor_box.get(sensor)
            sensor_out_list.append(value)

        """
        Set these to be class variables so they can be accessed by the controls
        """
        self.download_folders = download_out_list
        self.sensors = sensor_out_list

        """
        Just print to say what has happened
        """
        print("set download folders to: ", download_out_list)
        print("set accelerometers to: ", accelerometer_out_list)
        print("set sensors to: ", sensor_out_list)


        print("Output file: ", self.out_path.get())

        args = [self.download_folders, self.sensors, self.out_path.get()]

        self.thread = threading.Thread(target=target, args=args)
        self.thread.start()




if __name__ == "__main__":
    window = tk.Tk()
    esk_gui = EskGui(window)
    window.mainloop()