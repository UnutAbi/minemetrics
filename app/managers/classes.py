class Resource():
    def __init__(self, name: str, type: str, path: str):
        self.name: str = name
        self.type: str = type
        self.path: str = path
        
        # If the resource has only one instance:
        self.instance: Instance = None
        
        # If the resource has multiple instances:
        self.instances: set[Instance] = set()

class Instance():
    def __init__(self, name: str, path: str, logs: set):
        self.name: str = name
        self.path: str = path
        self.logs: set = logs
        self.gui: dict = {}
    
    def add_gui(self, gui_name: str, gui_obj: object):
        self.gui[gui_name] = gui_obj

class TimeBlock:
    def __init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def add_time(self, hours: int = 0, minutes: int = 0, seconds: int = 0):
        """
        Adds the specified amount of time to the current TimeBlock.
        """
        self.hours += hours
        self.minutes += minutes
        self.seconds += seconds
        self.normalize()

    def normalize(self):
        """
        Normalizes the time so that 60 seconds become 1 minute,
        and 60 minutes become 1 hour.
        """
        if self.seconds >= 60:
            self.minutes += self.seconds // 60
            self.seconds = self.seconds % 60

        if self.minutes >= 60:
            self.hours += self.minutes // 60
            self.minutes = self.minutes % 60

    def reset(self):
        """
        Resets the TimeBlock to 0 hours, 0 minutes, and 0 seconds.
        """
        self.hours = 0
        self.minutes = 0
        self.seconds = 0

    def __str__(self):
        """
        Returns a string representation of the TimeBlock in the format HH:MM:SS.
        """
        return f"{self.hours:02}:{self.minutes:02}:{self.seconds:02}"
    

    @classmethod
    def from_seconds(cls, total_seconds: int):
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return cls(hours, minutes, seconds)

class ExampleLauncherManager:
    def __init__(self):
        from pathlib import Path
        import platform
        import json

        self.launchers = {}

        # Initialize common paths
        if platform.system() == 'Windows':
            self.app_data_path = Path.home() / "AppData" / "Roaming"
        else:
            self.app_data_path = Path.home() / "Library" / "Application Support"
        self.doc_path = Path.home() / "Documents"

        # Define example launchers
        self.add_launcher("CurseForge", "Container", Path(self.doc_path, "curseforge", "minecraft", "Instances"))
        self.add_launcher("Modrinth", "Container", Path(self.app_data_path, "ModrinthApp", "profiles"))

        if platform.system() == 'Windows':
            minecraft_log_path = Path(self.app_data_path, ".minecraft", "logs")
        else:
            minecraft_log_path = Path(self.app_data_path, "minecraft", "logs")

        self.add_launcher("Minecraft Vanilla", "Instance", minecraft_log_path)
        self.add_launcher("Badlion", "Instance", minecraft_log_path / "blclient")

    def add_launcher(self, name: str, launcher_type: str, path) -> None:
        """
        Add an example launcher to the manager.
        """
        self.launchers[name] = {
            "type": launcher_type,
            "path": path
        }

    def find_installed_launchers(self) -> dict[str, bool]:
        """
        Check which example launchers are installed.
        """
        installed_launchers = {}
        for name, info in self.launchers.items():
            installed_launchers[name] = info["path"].exists()

        return installed_launchers

    def save_launchers_to_json(self, filename: str = "resources.json") -> None:
        """
        Save the example launchers to a JSON file, ensuring no duplicate names.
        If a name already exists but the path differs, a numeric suffix is added to the name.
        """
        from pathlib import Path
        from json import dump, load
        import os

        app_data_path = self.get_app_data_path()
        self.create_folder(app_data_path)
        json_file_path = Path(app_data_path, filename)

        def load_existing_launchers() -> dict:
            """Load existing launchers from the JSON file."""
            if json_file_path.exists() and os.path.getsize(json_file_path) > 0:
                try:
                    with open(json_file_path, 'r') as json_file:
                        return load(json_file)
                except Exception as e:
                    print(f"Error loading JSON: {e}")
            return {}

        def make_name_unique(name: str, existing_launchers: dict, path: str) -> str:
            """Ensure the launcher name is unique by adding a numeric suffix if necessary."""
            base_name = name
            counter = 1

            while name in existing_launchers:
                if existing_launchers[name]["path"] == path:
                    return name  # Same name and path, no need to change
                else:
                    counter += 1
                    name = f"{base_name} {counter}"

            return name

        def convert_paths_to_strings() -> dict:
            """Convert Path objects to strings and ensure unique launcher names."""
            converted = {}
            for name, info in self.launchers.items():
                unique_name = make_name_unique(name, existing_launchers, str(info["path"]))
                converted[unique_name] = {"type": info["type"], "path": str(info["path"])}
            return converted

        def save_to_json(data: dict) -> None:
            """Save the final launcher data to a JSON file."""
            with open(json_file_path, 'w') as json_file:
                dump(data, json_file, indent=4)
            print(f"Launchers saved to {json_file_path}")

        # Main function flow
        existing_launchers = load_existing_launchers()
        launchers_serializable = convert_paths_to_strings()
        existing_launchers.update(launchers_serializable)
        save_to_json(existing_launchers)


    @staticmethod
    def get_app_data_path():
        """
        Get the application data path.
        """
        from pathlib import Path
        import platform

        if platform.system() == 'Windows':
            return Path.home() / "AppData" / "Roaming" / "com.umutac" / "MineMetrics"
        else:
            return Path.home() / "Library" / "Application Support" / "com.umutac" / "MineMetrics"

    @staticmethod
    def create_folder(path: str) -> None:
        """
        Create a folder if it doesn't exist.
        """
        from pathlib import Path
        path = Path(path)

        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"Created folder: {str(path)}")
        else:
            print(f"Folder already exists: {str(path)}")
