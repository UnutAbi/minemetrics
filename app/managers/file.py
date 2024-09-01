def get_app_data_path():
    from pathlib import Path
    from os import name as osName

    app_data_path: Path

    if osName == 'nt':
        app_data_path = Path.home() / "AppData" / "Roaming"
    else:
        app_data_path = Path.home() / "Library" / "Application Support"

    app_data_path = app_data_path / "com.umutac" / "MineMetrics"

    return app_data_path


def create_folder(path: str) -> None:
    from pathlib import Path
    path = Path(path)

    if not isinstance(path, Path):
        print("Giving Path is not a Path")
        return None

    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print("Created folder: " + str(path))
    else:
        print("Folder already exists: " + str(path))


def initialize_default_resources() -> None:
    from pathlib import Path
    import json
    appdata: Path = get_app_data_path()

    filename: str = "resources.json"
    file_path: Path = Path(appdata, filename)

    # Create file
    if not file_path.exists():
        with open(file_path, 'w') as file:
            file.write(json.dumps({}))
        print("Created file: " + str(file_path))
    else:
        print("File already exists: " + str(file_path))

def load_json(path: str, filename: str, create_file_if_not_exists: bool = False) -> dict:
    from pathlib import Path
    import json
    path = Path(path)

    # Check: If path exists
    if not path.exists():
        return None, "Path does not exist"

    file_path: Path = Path(path, filename + ".json")

    # Check: If file exists
    if not file_path.exists():
        if create_file_if_not_exists:
            initialize_default_resources()
        else:
            return None, "Could not create"

    # Try to read json and return it
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            return json_data
    except:
        return None, "Could not read"

def save_json(path: str, filename: str, data: dict, create_file_if_not_exists: bool = False) -> dict:
    from pathlib import Path
    import json
    path = Path(path)

    # Check: If path exists
    if not path.exists():
        return None, "Path does not exist"

    file_path: Path = Path(path, filename + ".json")

    # Check: If file exists and create if necessary
    if not file_path.exists() and create_file_if_not_exists:
        initialize_default_resources()

    # Try to write json
    try:
        with open(file_path, 'w') as file:
            file.write(json.dumps(data))
            return True
    except:
        return None, "Could not write"

def create_settings_cfg() -> None:
    import configparser 
    config = configparser.ConfigParser()

    config['DEFAULT'] = {
        'auto_update': 'on',
        'saving_mode': 'persistent'
    }

    from pathlib import Path
    appdata: Path = get_app_data_path()
    config_file = Path(appdata, "settings.cfg")

    with open(config_file, 'w') as configfile:
        config.write(configfile)


def get_setting(setting_name: str) -> str:
    from configparser import ConfigParser
    config = ConfigParser()
    config.read(get_app_data_path() / "settings.cfg")

    return config.get('DEFAULT', setting_name)


def set_setting(setting_name: str, value: str) -> None:
    from configparser import ConfigParser
    config = ConfigParser()
    config.read(get_app_data_path() / "settings.cfg")

    config.set('DEFAULT', setting_name, value)

    with open(get_app_data_path() / "settings.cfg", 'w') as configfile:
        config.write(configfile)

def is_list_launcher_installed() -> dict[str, bool]:
    from pathlib import Path
    import platform

    app_data_path: Path

    if platform.system() == 'Windows':
        app_data_path = Path.home() / "AppData" / "Roaming"
    else:
        app_data_path = Path.home() / "Library" / "Application Support"

    doc_path: Path = Path.home() / "Documents"

    launcher_curseforge: Path = Path(doc_path, "curseforge", "minecraft", "Instances")
    launcher_modrinth: Path = Path(app_data_path, "ModrinthApp", "profiles")
    launcher_minecraft: Path

    # if windows it's .minecraft if mac it's minecraft
    if platform.system() == 'Windows':
        launcher_minecraft = app_data_path, ".minecraft", "logs"
    else:
        launcher_minecraft = Path(app_data_path, "minecraft", "logs")

    print(launcher_minecraft)

    launcher_badlion: Path = Path(launcher_minecraft, "blclient")

    installed_launchers: dict[str, bool] = {
        "CurseForge": launcher_curseforge.exists(),
        "Modrinth": launcher_modrinth.exists(),
        "Minecraft": launcher_minecraft.exists(),
        "Badlion": launcher_badlion.exists()
        # Add more launchers as needed
    }

    return installed_launchers
    

def is_initialized():
    from pathlib import Path
    
    app_data_path: Path = get_app_data_path()
    settings_cfg_file = Path(app_data_path, "settings.cfg")
    resource_file = Path(app_data_path, "resources.json")

    if not app_data_path.exists():
        return False
    
    if not resource_file.exists():
        initialize_default_resources()
        return False
    else:
        from json import load
        with open(resource_file, 'r') as file:
            json_data = load(file)
            if len(json_data) == 0:
                return False

    if not settings_cfg_file.exists():
        create_settings_cfg()

    return True
    
def auto_insert_launchers():
    from managers.classes import ExampleLauncherManager
    example_launcher_manager: ExampleLauncherManager = ExampleLauncherManager()
    example_launcher_manager.find_installed_launchers()
    example_launcher_manager.save_launchers_to_json()