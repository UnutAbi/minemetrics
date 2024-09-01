import customtkinter as ctk
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk

class WelcomeScreen(ctk.CTkFrame):
    def __init__(self, master, height, version, auto_resource_search_screen, first_label_point, second_label_point, **kwargs):
        super().__init__(master, **kwargs, bg_color="transparent", fg_color="transparent", height=height)

        self.auto_resource_search_screen = auto_resource_search_screen
        self.first_label_point = first_label_point
        self.second_label_point = second_label_point

        self.propagate(True)
        from ui.typography import create_text_label
        self.welcome_label: ctk.CTkLabel = create_text_label(
            "Welcome to MineMetrics",
            "large_title",
            self
        )

        self.software_version: ctk.CTkLabel = create_text_label(
            f"Version: {version}",
            "footnote",
            self
        )

        self.welcome_label.pack(side=ctk.TOP, fill=ctk.X, pady=20)
        self.software_version.configure(text_color="#545454")
        self.software_version.pack(side=ctk.TOP, fill=ctk.X, pady=10)

        self.setup_icon()
        self.setup_start_setup()

    def setup_icon(self):
        """
        Sets up and centers the application icon within the main window.
        """
        # Define the path to the icon image
        image_path = Path("app", "image", "MineMetrics.png")
        
        try:
            # Open the image using PIL
            original_image = Image.open(image_path)
        except Exception as e:
            print(f"Error loading image: {e}")
            # Provide an alternative action, e.g., use a default image
            original_image = Image.new('RGB', (100, 100), color='gray')
        
        # Define the desired size for the icon (width, height)
        icon_size = (100, 100)  # Adjust the size as needed
        
        # Create a CTkImage for both light and dark modes with the specified size
        icon_ctk_image = ctk.CTkImage(
            light_image=original_image,
            dark_image=original_image,
            size=icon_size
        )
        
        # Create a CTkLabel to display the icon
        icon_label = ctk.CTkLabel(
            master=self,   # Set the main window as the parent
            image=icon_ctk_image,      # Assign the CTkImage to the label
            bg_color="transparent",    # Use the transparent background
            text=""                    # No accompanying text
        )
        
        # Center the label within the main window using padding
        icon_label.pack(
            padx=20,  # Horizontal padding
            pady=50   # Vertical padding
        )

    def setup_start_setup(self):
        """
        Sets up the Start Setup button and its functionality.
        """
        from ui.typography import create_button

        def button_function():
            self.forget()
            self.auto_resource_search_screen.pack(fill=ctk.BOTH, expand=1)

            self.first_label_point.configure(text="○ Welcome Screen")
            self.second_label_point.configure(text="● Auto Resource Search")



        start_setup_button: ctk.CTkButton = create_button(
            master=self,
            text="Start Setup",
            function= button_function)
        start_setup_button.pack(pady=20)

class AutoResourceSearchScreen(ctk.CTkFrame):
    def __init__(self, master, have_fun_screen, second_label_point, third_label_point, **kwargs):
        super().__init__(master, **kwargs, bg_color="transparent", fg_color="transparent")

        self.have_fun_screen = have_fun_screen
        self.second_label_point = second_label_point
        self.third_label_point = third_label_point

        from ui.typography import create_text_label
        self.title: ctk.CTkLabel = create_text_label(
            "Auto Resource Search",
            "large_title",
            self
        )
        self.title.pack(pady=20)

        self.description_setup()
        self.launchers_setup()
        self.next_button_setup()

    def description_setup(self):
        from ui.typography import create_text_label

        self.description_label: ctk.CTkLabel = create_text_label(
            "Some Minecraft launchers will be detected automatically\nif they are installed regularly.\nIf not, and the launcher isn't in the list, you can add it manually.",
            "body",
            self
        )
        self.description_label.pack(pady=20)

    def launchers_setup(self):
        """
        Sets up the launchers with their names, icons, and status indicators.
        """
        from ui.typography import create_text_label

        # Configuration variables
        icon_size = (50, 50)  # Size of the launcher icons
        horizontal_spacing = 0.2  # Horizontal spacing between launchers
        vertical_spacing = 0.1  # Vertical spacing between launcher elements

        # Retrieve launcher installation statuses
        from managers.file import is_list_launcher_installed
        launcher_statuses = is_list_launcher_installed()

        # List of launchers and their corresponding icons
        launchers = [
            {"name": "Minecraft", "icon": "minecraft_icon.png", "found": launcher_statuses["Minecraft"]},
            {"name": "CurseForge", "icon": "curseforge_icon.ico", "found": launcher_statuses["CurseForge"]},
            {"name": "Modrinth", "icon": "modrinth_icon.ico", "found": launcher_statuses["Modrinth"]},
            {"name": "Badlion", "icon": "badlion_icon.webp", "found": launcher_statuses["Badlion"]}
        ]

        # Default icon if specific launcher icon is not found
        default_icon_path = Path("app", "image", "404.png")
        
        try:
            default_icon_image = Image.open(default_icon_path).resize(icon_size)
        except Exception as e:
            print(f"Error loading image: {e}")
            # Provide an alternative action, e.g., use a default image
            default_icon_image = Image.new('RGB', icon_size, color='gray')

        default_ctk_image = ctk.CTkImage(light_image=default_icon_image, dark_image=default_icon_image, size=icon_size)

        # Calculate the total number of launchers
        total_launchers = len(launchers)

        for idx, launcher in enumerate(launchers):
            # Create the launcher name label
            name_label: ctk.CTkLabel = create_text_label(
                launcher["name"],
                "body",
                self
            )

            # Load and resize the launcher icon, or use default if not found
            try:
                icon_path = Path("app", "image", "launchers", launcher["icon"])
                icon_image = Image.open(icon_path).resize(icon_size)
                icon_ctk_image = ctk.CTkImage(light_image=icon_image, dark_image=icon_image, size=icon_size)
            except FileNotFoundError:
                icon_ctk_image = default_ctk_image

            # Create the launcher icon label
            icon_label: ctk.CTkLabel = ctk.CTkLabel(
                master=self,
                image=icon_ctk_image,
                bg_color="transparent",
                text=""
            )

            # Determine status based on whether the launcher is found or not
            status_text = "Found" if launcher["found"] else "Not found"
            status_color = "#00FF00" if launcher["found"] else "#FF0000"

            # Create the launcher found status label
            status_label: ctk.CTkLabel = create_text_label(
                status_text,
                "footnote",
                self
            )
            status_label.configure(text_color=status_color)

            # Calculate position for the current launcher
            relx_position = (0.5 - (total_launchers - 1) * horizontal_spacing / 2) + (idx * horizontal_spacing)
            rely_position = 0.5

            # Place the launcher name, icon, and status label vertically aligned with custom spacing
            name_label.place(relx=relx_position, rely=rely_position - vertical_spacing, anchor=tk.CENTER)
            icon_label.place(relx=relx_position, rely=rely_position, anchor=tk.CENTER)
            status_label.place(relx=relx_position, rely=rely_position + vertical_spacing, anchor=tk.CENTER)

        ###

    def next_button_setup(self):
        """
        Sets up the Next button and its functionality.
        """
        from ui.typography import create_button

        def button_function():
            self.forget()
            self.have_fun_screen.pack(fill=ctk.BOTH, expand=1)

            self.second_label_point.configure(text="○ Auto Resource Search")
            self.third_label_point.configure(text="● Have fun!")

            # 
            from managers.classes import ExampleLauncherManager
            example_launcher_manager: ExampleLauncherManager = ExampleLauncherManager()
            example_launcher_manager.save_launchers_to_json()

        next_button: ctk.CTkButton = create_button(
            master=self,
            text="Next",
            function=button_function
        )
        next_button.pack(side=ctk.BOTTOM, pady=60)

class HaveFunScreen(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, bg_color="transparent", fg_color="transparent")

        from ui.typography import create_text_label, create_button
        self.title: ctk.CTkLabel = create_text_label(
            "Have fun!",
            "large_title",
            self
        )
        self.title.pack(pady=20)

        self.additional_information()
        self.close_button_setup()

    def additional_information(self):
        """
        Additional information about the program state.
        """
        from ui.typography import create_text_label

        additional_info_label: ctk.CTkLabel = create_text_label(
            "Just a heads-up:\n\n"
            "MineMetrics currently tracks only your local playtime.\n"
            "If your Minecraft data is lost, it will only show playtime from the last session.\n\n"
            "In the future, I plan to add a cloud option to save your data more reliably. Stay tuned for updates!",
            "body",
            self
        )
        additional_info_label.pack(pady=20)

    def close_button_setup(self):
        """
        Sets up the button to close the application.
        """
        from ui.typography import create_button

        def close_application():
            self.master.quit()

        close_button: ctk.CTkButton = create_button(
            master=self,
            text="Finish",
            function=close_application
        )
        close_button.pack(pady=20)

class MainWindow():
    def __init__(self, window_title, window_width, window_height, version):
        self.window_height: int = window_height
        self.progress_area_height: int = 64
        self.version: str = version

        self.setup_window_appearance(window_title, window_width, window_height)
        self.progress_area_setup()
        self.initialize_screen_sections()

    def initialize_screen_sections(self):
        self.have_fun_screen = HaveFunScreen(self.main_window)
        self.auto_resource_search_screen = AutoResourceSearchScreen(self.main_window, self.have_fun_screen, self.second_label_point, self.third_label_point)
        self.welcome_screen = WelcomeScreen(self.main_window,(self.window_height - self.progress_area_height), self.version, self.auto_resource_search_screen, self.first_label_point, self.second_label_point)
        self.welcome_screen.pack()


    def setup_window_appearance(self, window_title, window_width, window_height):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.main_window: ctk.CTk = ctk.CTk()
        self.main_window.title(window_title)
        self.main_window.geometry(f"{window_width}x{window_height}")
        self.main_window.resizable(False, False)
        self.main_window.maxsize(window_width, window_height)

        self.menubar: tk.Menu = tk.Menu(self.main_window)
        self.main_window.config(menu=self.menubar)

    def progress_area_setup(self):
        progress_area: ctk.CTkFrame = ctk.CTkFrame(
            master=self.main_window,
            height=self.progress_area_height,
            corner_radius=0,
            border_width=None,
            bg_color="#2B2B2B")
        progress_area.pack(side=ctk.BOTTOM, fill=ctk.X)

        # three labels point
        from ui.typography import create_text_label
        self.first_label_point: ctk.CTkLabel = create_text_label(
            "● Welcome Screen",
            "title",
            progress_area
        )

        self.second_label_point: ctk.CTkLabel = create_text_label(
            "○ Auto Resource Search",
            "title",
            progress_area
        )

        self.third_label_point: ctk.CTkLabel = create_text_label(
            "○ Have fun!",
            "title",
            progress_area
        )

        # Set the positions of the labels within the progress area 
        # And next to eacher other 
        # And place them to the center

        self.first_label_point.place(relx=0.2, rely=0.5, anchor=tk.CENTER)
        self.second_label_point.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.third_label_point.place(relx=0.8, rely=0.5, anchor=tk.CENTER)

    def run(self):
        self.main_window.mainloop()
