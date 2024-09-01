import customtkinter as ctk
from managers.classes import TimeBlock
import threading

class window(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=1)

        self.viewer: ActionViewBlock = ActionViewBlock(self)
        self.viewer.pack(side=ctk.TOP, fill=ctk.BOTH,
                         expand=1, padx=10, pady=10)
        
        self.resources_viewer: ResourcesViewer = ResourcesViewer(self)
        self.resources_viewer.pack(side=ctk.BOTTOM, fill=ctk.BOTH,
                                   expand=1, padx=10, pady=0)
        
        
        self.viewer.RESOURCESVIEWER = self.resources_viewer


class ResourceBlockView(ctk.CTkFrame):
    def __init__(self, master, name, resource_type, path):
        super().__init__(master, fg_color="#545454")

        self.header_frame: ctk.CTkFrame = ctk.CTkFrame(self)
        self.header_frame.pack(pady=5, padx=10, side=ctk.TOP, fill=ctk.X)

        self.name_label = ctk.CTkLabel(self.header_frame, text=name)
        self.name_label.pack(pady=5, padx=10, side=ctk.LEFT)

        self.type_label = ctk.CTkLabel(self.header_frame, text=resource_type)
        self.type_label.pack(pady=5, padx=10, side=ctk.RIGHT)

        self.path = path
        self.name = name

        self.content_frame: ctk.CTkFrame = ctk.CTkFrame(self, height=4)
        self.content_frame.pack(pady=5, padx=10, side=ctk.BOTTOM, fill=ctk.BOTH, expand=1)

        # Unabhängig von der Art, speichere Instanzen in einer Liste
        self.instances = []

        # Setup je nach Typ
        if resource_type == "Instance":
            self.setup_for_instance()
        else:
            self.setup_for_container()

    def setup_for_instance(self):
        from ui.typography import create_text_label
        from managers.classes import Instance
        from managers.mc import get_logs

        # Erstelle eine Instanz und füge sie zur Liste hinzu
        instance = Instance(self.name, self.path, get_logs(path=self.path))
        self.instances.append(instance)

        # GUI Setup
        self.progress_label: ctk.CTkLabel = create_text_label(f"Logs - 0/{len(instance.logs)}", "body", self.content_frame)
        self.progress_label.pack(pady=5, padx=10)

    def setup_for_container(self):
        from ui.typography import create_text_label
        from managers.mc import get_instances, get_logs
        from managers.classes import Instance
        from pathlib import Path

        # Hole alle Instanzen
        instances_sets = get_instances(path=self.path)
        self.progress_label: ctk.CTkLabel = create_text_label(f"Instances - 0/{len(instances_sets)}", "body", self.content_frame)
        self.progress_label.pack(pady=5, padx=10)

        # Erstelle eine Frame für jede Instanz
        for instance_name in instances_sets:
            instance_path = Path(self.path, instance_name)

            # Erstelle und speichere Instanz
            instance = Instance(instance_name, instance_path, get_logs(instance_path))
            self.instances.append(instance)

            # GUI Setup für jede Instanz
            instance_frame: ctk.CTkFrame = ctk.CTkFrame(master=self, fg_color="#3b3b3b")
            instance_frame.pack(pady=5, padx=10, side=ctk.TOP, anchor=ctk.NW, fill=ctk.X)

            instance_label = ctk.CTkLabel(instance_frame, text=instance_name)
            instance_label.pack(pady=5, padx=10, side=ctk.LEFT)

            instance_status_label = ctk.CTkLabel(instance_frame, text=f"Logs - 0/{len(instance.logs)}")
            instance_status_label.pack(pady=5, padx=10, side=ctk.RIGHT)

            # Füge GUI-Element zu Instanz hinzu
            instance.add_gui("instance_status_label", instance_status_label)



class ResourcesViewer(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#3b3b3b")


class ActionViewBlock(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#3b3b3b")
        self.RESOURCESVIEWER: ResourcesViewer

        from ui.typography import create_button, create_text_label

        # Analyse Button
        self.analyse_btn = create_button(
            self, "Start Analysing", self.start_analysing
        )
        self.analyse_btn.pack(
            pady=20, padx=20, side=ctk.TOP, anchor=ctk.NW, fill=ctk.X
        )

        # Label for total playtime
        self.total_time_label = create_text_label("Total Playtime: 00:00:00", "body", self)
        self.total_time_label.pack(
            pady=10, padx=20, side=ctk.TOP, anchor=ctk.NW, fill=ctk.X
        )

        self.views: tuple = tuple()
        self.resource_blocks = []

    def start_analysing(self):
        # Disable the button during analysis
        self.analyse_btn.configure(text="Analysing ...", state="disabled", fg_color="yellow")
        self.reset_analysis_state()

        # Load and process resource blocks
        from managers.file import load_json, get_app_data_path
        from pathlib import Path

        self.appdata: Path = get_app_data_path()
        self.resources: dict = load_json(self.appdata, "resources", True)

        for key, value in self.resources.items():
            resource_block_view: ResourceBlockView = ResourceBlockView(
                self.RESOURCESVIEWER, key, value["type"], value["path"]
            )
            resource_block_view.pack(
                pady=5, padx=10, side=ctk.TOP, anchor=ctk.NW, fill=ctk.X
            )
            
            self.resource_blocks.append(resource_block_view)

        # Start processing in a separate thread
        thread = threading.Thread(target=self.process_resource_blocks)
        thread.start()

    def process_resource_blocks(self):
        from managers.handler import packages, run, post_essentiel_data

        #total_time_block = TimeBlock(0, 0, 0)  # Initialize total TimeBlock

        for resource_block in self.resource_blocks:
            print(f"Processing {resource_block.name} of type {resource_block.type_label.cget('text')}")
            packages.add(resource_block)

        post_essentiel_data(analyse_btn=self.analyse_btn, analyse_btn_command=self.start_analysing, total_time_label=self.total_time_label)

        run()
        
        # Re-enable the button after analysis is complete
        #self.analyse_btn.configure(text="Start Analysis Again", state="normal", command=self.start_analysing)

    def reset_analysis_state(self):
        # Clear previous resource blocks and reset packages
        from managers.handler import packages
        packages.clear()

        # Destroy existing resource blocks to avoid invalid references
        self.resource_blocks.clear()
        for widget in self.RESOURCESVIEWER.winfo_children():
            widget.destroy()

        # Reset the total playtime label
        self.total_time_label.configure(text="Total Playtime: 00:00:00")