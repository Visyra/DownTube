import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pytube import YouTube
import customtkinter
import sys
import urllib
import threading

shouldRefresh = False
need_remove = False
url = ""

def combobox_callback(choice):
    global selected_quality_b
    selected_quality_b = str(choice)


class App(customtkinter.CTk):
    
    WIDTH = 600
    HEIGHT = 475

    def refresh(self):
        global shouldRefresh
        while shouldRefresh == True:
            self.update()
            time.wait(0.5)
        return

    def on_closing(self):
        self.destroy()
        sys.exit(0)

    def __init__(self):
        super().__init__()
        self.title("Visyra DownTube")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        #self.iconbitmap("VisyraNetwork.ico")

        global x
        x = threading.Thread(target=self.refresh)
        threading.daemon=True
        x.daemon = True
        x.start()

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)#

        self.label_6 = customtkinter.CTkLabel(master=self.frame_right,
                                        text="Visyra DownTube", font=("Roboto Medium", 20))
        
        self.label_6.place(x=15, y=10)

        # ============ frame_left ============
        self.url_label = customtkinter.CTkLabel(master=self.frame_right, text="YouTube URL: ", font=("Roboto Medium", 14))
        self.url_label.place(x=15, y = 65)
        self.url_entry = customtkinter.CTkEntry(master=self.frame_right, width = 425)
        self.url_entry.place(x=110, y = 65)
        self.url_button = customtkinter.CTkButton(master=self.frame_right, text="Get Information", command = self.get_info)
        self.url_button.place(x=15, y= 100)

        # Create a StringVar to store the selected video quality and file format
        self.selected_quality = ""

    def truncate_title(self, title, max_length=80):
        if len(title) > max_length:
            return title[:max_length-3] + "..."
        return title

    def choose_download_folder(self):
        global folder_path
        folder_path = filedialog.askdirectory()

    def get_info(self):
        global url
        url = self.url_entry.get()
        if url == "":
            messagebox.showerror("Visyra DownTube", "There is no link found in the input box!")
            return
        try:
            yt = YouTube(url)
            self.quality_label = customtkinter.CTkLabel(master=self.frame_right, text="Select Quality:", font=("Roboto Medium", 14))
            self.quality_label.place(x=15, y=250)

            self.selected_quality = ""  # Clear any previous selection
            streams = yt.streams.filter(file_extension='mp4')
            quality_options = [stream.resolution for stream in streams if stream.resolution is not None]

            self.quality_combobox = customtkinter.CTkComboBox(master=self.frame_right, values=quality_options, state="readonly", command=combobox_callback)
            self.quality_combobox.place(x=165, y=250)

            self.info2 = customtkinter.CTkLabel(master=self.frame_right, text = "Video Download Options:", font=("Roboto Medium", 16))
            self.info2.place(x=15, y= 220)
            
            self.info1 = customtkinter.CTkLabel(master=self.frame_right, text = "Video Information:", font=("Roboto Medium", 16))
            self.info1.place(x=15, y= 130)
            self.info_title1 = customtkinter.CTkLabel(master=self.frame_right, text = "Title: ", font=("Roboto Medium", 14))
            self.info_title1.place(x=15, y= 155)
            self.info_title2 = customtkinter.CTkLabel(master=self.frame_right, text=self.truncate_title(yt.title), font=("Roboto Medium", 14))
            self.info_title2.place(x=100, y= 155)
            self.info_author1 = customtkinter.CTkLabel(master=self.frame_right, text = f"Author:", font=("Roboto Medium", 14))
            self.info_author1.place(x=15, y= 175)
            self.info_author2 = customtkinter.CTkLabel(master=self.frame_right, text = f"{yt.author}", font=("Roboto Medium", 14))
            self.info_author2.place(x=100, y= 175)
            self.info_duration1 = customtkinter.CTkLabel(master=self.frame_right, text = f"Duration:", font=("Roboto Medium", 14))
            self.info_duration1.place(x=15, y= 195)
            self.info_duration2 = customtkinter.CTkLabel(master=self.frame_right, text = f"{yt.length} seconds", font=("Roboto Medium", 14))
            self.info_duration2.place(x=100, y= 195)
            self.info_download1 = customtkinter.CTkLabel(master=self.frame_right, text = "Download Folder:", font=("Roboto Medium", 14))
            self.info_download1.place(x=15, y= 290)
            self.info_download_dir_button = customtkinter.CTkButton(master=self.frame_right, text = "Select", font=("Roboto Medium", 14), command = self.choose_download_folder)
            self.info_download_dir_button.place(x=165, y= 290)
            self.info_download_name1 = customtkinter.CTkLabel(master=self.frame_right, text = "File Name:", font=("Roboto Medium", 14))
            self.info_download_name1.place(x=15, y= 325)
            self.info_download_name2 = customtkinter.CTkEntry(master=self.frame_right, width = 425)
            self.info_download_name2.place(x=110, y = 325)
            self.info_download_name2.insert(0, str(yt.title))
            #video_thumbnail.set(f"Thumbnail: {yt.thumbnail_url}")

            self.info3 = customtkinter.CTkLabel(master=self.frame_right, text = "Download Options:", font=("Roboto Medium", 16))
            self.info3.place(x=15, y= 360)

            self.download_video = customtkinter.CTkButton(master = self.frame_right, text = "Download Video", command = self.start_download, font=("Roboto Medium", 14))
            self.download_video.place(x=15, y= 400)
            self.download_thumbnail = customtkinter.CTkButton(master = self.frame_right, text = "Download Thumbnail", command = self.download_thumbnail, font=("Roboto Medium", 14))
            self.download_thumbnail.place(x=185, y= 400)
            
        except Exception as e:
            messagebox.showerror("Visyra DownTube", f"An error occurred while trying to get the video informaiton: {str(e)}")

    def download_thumbnail(self):
        global url
        global folder_path
        selected_file_name = self.info_download_name2.get()
        if url == "":
            messagebox.showerror("Visyra DownTube", "There is no link found in the input box!")
            return
        if selected_file_name == "":
            messagebox.showerror("Visyra DownTube", "There is no selected file name!")
            return
        try:
            yt = YouTube(url)
            thumbnail_url = yt.thumbnail_url
            bs = r"\adsf"
            # Download the thumbnail
            shouldRefresh = True
            messagebox.showinfo("Visyra DownTube", "Please wait while your file is downloading!")
            urllib.request.urlretrieve(thumbnail_url, folder_path + bs[0] + selected_file_name + ".jpg")
            shouldRefresh = False

            messagebox.showinfo("Visyra DownTube", f"Thumbnail for '{yt.title}' downloaded successfully!")
        except Exception as e:
            messagebox.showerror("Visyra DownTube", f"An error occurred while downloading the video thumbnail: {str(e)}")

    
    def start_download(self):
        global url
        global selected_quality_b
        global need_remove
        if url == "":
            messagebox.showerror("Visyra DownTube", "There is no link found in the input box!")
            return
        selected_quality = selected_quality_b
        selected_file_name = self.info_download_name2.get() # Get the selected video quality
        if selected_file_name == "":
            messagebox.showerror("Visyra DownTube", "There is no selected file name!")
            return
        if selected_quality == "":
            messagebox.showerror("Visyra DownTube", "There is no download quality selected!")
            return
        if "" == "":
        #try:
            yt = YouTube(url)

            # Find the stream with the selected quality and format
            video_stream = None
            for stream in yt.streams.filter(file_extension="mp4"):
                if stream.resolution == selected_quality:
                    video_stream = stream
                    break

            video_size_mb = round(video_stream.filesize / (1024 * 1024), 2)
            if not messagebox.askyesno("Visyra DownTube", "The file you are downloading will be " + str(video_size_mb) + " MB. Do you want to continue?"):
                return

            if video_stream:
                video_filename = f"{selected_file_name}.mp4"
                video_filepath = folder_path + video_filename

                # Check if the file already exists
                if os.path.isfile(video_filepath):
                    confirm_overwrite = messagebox.askyesno(
                        "Visyra DownTube",
                        f"'{video_filename}' already exists. Do you want to overwrite it?",
                    )
                    if not confirm_overwrite:
                        return
                    else:
                        need_remove = True

                shouldRefresh = True
                messagebox.showinfo("Visyra DownTube", "Please wait while your file is downloading!")

                if need_remove == True:
                    os.remove(video_filepath)
                
                video_stream.download(folder_path, filename=selected_file_name + ".mp4")
                messagebox.showinfo("Visyra DownTube", f"Video '{yt.title}' downloaded successfully!")
                shouldRefresh = False
            else:
                messagebox.showerror("Visyra DownTube", "No suitable video stream found.")
        #except Exception as e:
            #messagebox.showerror("Visyra DownTube", f"An error occurred while downloading the video: {str(e)}")


app = App()
app.mainloop()
