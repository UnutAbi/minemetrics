import customtkinter as ctk

class window(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=1)

        self.open_app_setting: OpenAppDataSetting = OpenAppDataSetting(self)
        self.open_app_setting.pack(pady=5, padx=10, side=ctk.TOP, anchor=ctk.NW, fill=ctk.X)

        self.clear_app_setting: ClearAppDataSetting = ClearAppDataSetting(self)
        self.clear_app_setting.pack(pady=5, padx=10, side=ctk.TOP, anchor=ctk.NW, fill=ctk.X)
        
class OpenAppDataSetting(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#3b3b3b")

        from ui.typography import create_text_label, create_button

        self.label = create_text_label(
            "Open AppData:", "body", self
        )
        self.label.configure(width=32)
        self.label.pack(pady=5, padx=10, side=ctk.LEFT)

        def open_folder_app_data() -> None:
            from managers.file import get_app_data_path
            from pathlib import Path

            import subprocess
            import platform

            appdata_path: Path = get_app_data_path()
            system_platform: str = platform.system()

            if system_platform == "Windows":
                subprocess.run(["explorer", str(appdata_path)])
            elif system_platform == "Darwin":  # macOS
                subprocess.run(["open", str(appdata_path)])

        # Btn to open the folder dict
        # self.open_btn = ctk.CTkButton(self, text="Open", command=open_folder_app_data)
        self.open_btn = create_button(
            self,
            text="Open",
            function=open_folder_app_data
        )

        self.open_btn.configure(width=10)  # Set the button width to 10 characters for better readability
        self.open_btn.pack(pady=5, padx=10, side=ctk.RIGHT, fill=ctk.X, expand=True)

class ClearAppDataSetting(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#3b3b3b")

        from ui.typography import create_text_label, create_button

        self.label = create_text_label(
            "Clear AppData:", "body", self
        )

        self.label.configure(width=32)
        self.label.pack(pady=5, padx=10, side=ctk.LEFT)

        def clear_app_data() -> None:
            from managers.file import get_app_data_path
            from pathlib import Path
            import shutil

            appdata_path: Path = get_app_data_path()

            if appdata_path.exists():
                shutil.rmtree(appdata_path)
                print(f"AppData folder '{appdata_path}' deleted successfully.")
            else:
                print(f"AppData folder '{appdata_path}' does not exist.")
        
        # Btn to delete the folder dict
        self.delete_btn = create_button(self, "Delete", clear_app_data, "red")
        self.delete_btn.configure(width=10)  # Set the button width to 10 characters for better readability
        self.delete_btn.pack(pady=5, padx=10, side=ctk.RIGHT, fill=ctk.X, expand=True)