import customtkinter as ctk
import tkinter as tk

version: str = "1.0.0 Beta"
window_width: int = 720
window_height: int = 480
window_title: str = "MineMetrics"

sidebar_width: int = 150

def update_cpu_ram_text(text: ctk.CTkLabel):
    from psutil import Process
    from os import getpid
    from time import sleep

    process: Process = Process(getpid())

    try:
        del getpid

        while True:
            if text == None:
                print("Text not found")
                continue

            sleep(1)
            cpu = process.cpu_percent()
            ram = process.memory_info().rss / 1024 / 1024
            output = f"CPU: {cpu}% - RAM: {ram:.2f} MB"
            text.configure(text=output)
            text.update()
    except Exception as e:
        print(f"An error occurred in the tick function: {e}")


class MainWindow():
    def __init__(self):
        self.initialize_variables()

        self.setup_window_appearance()
        self.setup_sidebar()
        self.setup_sidebar_content()
        self.setup_sidebar_footer()
        self.setup_sidebar_footer_content()

        self.start_seperated_threads()

        self.setup_main_frames()

    def initialize_variables(self):
        # Scnes:
        # 0: home
        # 1: dashboard
        # 2: settings
        # 3: settings
        self.scenes_frames: tuple = ()
        self.sidebar_buttons: tuple = ()

    def forget_all_scenes(self):
        for frame in self.scenes_frames:
            frame.pack_forget()

    def change_scene(self, scene: int):
        self.forget_all_scenes()

        for button in self.sidebar_buttons:
            button.unhighlight()

        self.sidebar_buttons[scene].highlight()
        self.scenes_frames[scene].pack(
            side=ctk.RIGHT, fill=ctk.BOTH, expand=1
        )

    def setup_window_appearance(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.main_window: ctk.CTk = ctk.CTk()
        self.main_window.title(window_title)
        self.main_window.geometry(f"{window_width}x{window_height}")
        self.main_window.resizable(False, False)
        self.main_window.maxsize(window_width, window_height)

        self.menubar: tk.Menu = tk.Menu(self.main_window)
        self.main_window.config(menu=self.menubar)

    def setup_sidebar(self):
        self.sidebar: ctk.CTkFrame = ctk.CTkFrame(
            master=self.main_window,
            width=sidebar_width,
            corner_radius=0,
            border_width=0,
            fg_color="#3b3b3b"
        )
        self.sidebar.pack_propagate(False)
        self.sidebar.pack(side=ctk.LEFT, fill=ctk.BOTH)

    def setup_sidebar_content(self):
        from ui.typography import create_text_label

        self.title: ctk.CTkLabel = create_text_label(
            f"{window_title}", "title_2", self.sidebar)
        self.title.pack(pady=20, padx=20)

        from ui.typography import SidebarButton

        self.home_button: SidebarButton = SidebarButton(
            self.sidebar, "Home", lambda: self.change_scene(0))
        self.dashboard_button: SidebarButton = SidebarButton(
            self.sidebar, "Dashboard", lambda: self.change_scene(1))
        self.settings_button: SidebarButton = SidebarButton(
            self.sidebar, "Settings", lambda: self.change_scene(2))

        self.home_button.button.pack(
            pady=5, padx=20, side=ctk.TOP, anchor=ctk.NW)
        self.dashboard_button.button.pack(
            pady=5, padx=20, side=ctk.TOP, anchor=ctk.NW)
        self.settings_button.button.pack(
            pady=5, padx=20, side=ctk.TOP, anchor=ctk.NW)

        self.sidebar_buttons = (
            self.home_button,
            self.dashboard_button,
            self.settings_button)

    def setup_sidebar_footer(self):
        self.sidebar_footer = ctk.CTkFrame(
            master=self.sidebar,
            width=sidebar_width,
            corner_radius=0,
            border_width=0,
            fg_color="transparent"
        )
        self.sidebar_footer.pack(side=ctk.BOTTOM, fill=ctk.X)

    def setup_sidebar_footer_content(self):
        from ui.typography import create_text_label

        self.cpu_ram_text: ctk.CTkLabel = create_text_label(
            "CPU: 0% - RAM: 0MB", "footnote", self.sidebar_footer)

        self.software_version_label: ctk.CTkLabel = create_text_label(
            f"Version: {version}", "footnote", self.sidebar_footer)
        
        self.software_version_label.pack(pady=0, padx=5, fill=ctk.X)
        self.cpu_ram_text.pack(pady=20, padx=5, fill=ctk.X)


    def start_seperated_threads(self):
        from threading import Thread

        self.cpu_ram_thread = Thread(
            target=update_cpu_ram_text, args=(self.cpu_ram_text,))
        self.cpu_ram_thread.start()

    def setup_main_frames(self):
        from ui.home import window as home_window
        from ui.dashboard import window as dashboard_window
        from ui.settings import window as settings_window

        self.home_frame: home_window = home_window(master=self.main_window)
        self.dashboard_frame: dashboard_window = dashboard_window(
            master=self.main_window)
        self.settings_frame: settings_window = settings_window(
            master=self.main_window)

        self.scenes_frames = (
            self.home_frame, self.dashboard_frame, self.settings_frame)

        self.change_scene(0)

    def run(self):
        self.main_window.mainloop()


def main():
    from managers.file import is_initialized

    is_initialized_bool: bool = is_initialized()
    if(is_initialized_bool):
        app = MainWindow()
        app.run()
    else:
        from managers.mineMetricsWelcome import MainWindow as mm
        app = mm(window_title, window_width, window_height, version)
        app.run()
        app.main_window.destroy()

        del app
        del mm

        app = MainWindow()
        app.run()  


if __name__ == "__main__":
    main()
