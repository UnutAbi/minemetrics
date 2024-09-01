import customtkinter as ctk

class window(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=1)

        self.resource_viewer: ResourcesViewer = ResourcesViewer(self)
        self.resource_manager: ResourceManager = ResourceManager(self)

        self.resource_viewer.ResourceManger = self.resource_manager
        self.resource_manager.ResourcesViewer = self.resource_viewer

        self.resource_manager.pack(
            side=ctk.TOP, fill=ctk.BOTH, expand=1, padx=10, pady=10)
        self.resource_viewer.pack(
            side=ctk.TOP, fill=ctk.BOTH, expand=1, padx=10, pady=10)


class ResourceManager(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#3b3b3b")

        self.ResourcesViewer: object

        self.label = ctk.CTkLabel(
            master=self,
            text="ResourceManager",
            font=ctk.CTkFont(size=20, weight="bold")
        )

        self.label.pack(pady=10, padx=20)

        self.setup_input_forms()

    def setup_input_forms(self):
        from ui.typography import create_text_label, EntryInput
        self.name_input_label = create_text_label("Name:", "body", self)
        self.name_input_label.pack(
            side=ctk.TOP, anchor=ctk.NW, padx=10, pady=10)

        self.name_input_entry: EntryInput = EntryInput(self)
        self.name_input_entry.entry.pack(side=ctk.TOP, anchor=ctk.NW,
                                         padx=10, pady=0, fill=ctk.BOTH)

        self.path_input_label = create_text_label("Path:", "body", self)
        self.path_input_label.pack(
            side=ctk.TOP, anchor=ctk.NW, padx=10, pady=10)

        self.path_input_entry: EntryInput = EntryInput(self)
        self.path_input_entry.entry.pack(side=ctk.TOP, anchor=ctk.NW,
                                         padx=10, pady=0, fill=ctk.BOTH)

        self.type_input_label = create_text_label("Type:", "body", self)
        self.type_input_label.pack(
            side=ctk.TOP, anchor=ctk.NW, padx=10, pady=10)

        from ui.typography import create_segmented_button
        self.type_input_CTkSegmentedButton = create_segmented_button(
            self, ("Instance", "Container"))
        self.type_input_CTkSegmentedButton.pack(
            side=ctk.TOP, anchor=ctk.NW, padx=10, fill=ctk.BOTH)

        from ui.typography import create_button

        self.add_resource_button = create_button(
            self, "Add Resource", lambda: self.validate_inputs())
        self.add_resource_button.pack(
            side=ctk.TOP, padx=10, pady=10, fill=ctk.BOTH)

        del create_text_label
        del create_segmented_button
        del create_button

    def validate_inputs(self):
        self.is_valid_type: bool = False
        self.is_valid_name: bool = False
        self.is_valid_path: bool = False

        def validate_type():
            if self.type_input_CTkSegmentedButton.get() != "":
                self.is_valid_type = True
                self.type_input_CTkSegmentedButton.configure(
                    fg_color="#545454")
            else:
                self.type_input_CTkSegmentedButton.configure(fg_color="red")

        def validate_name():
            if self.name_input_entry.entry.get() != "":
                self.is_valid_name = True
                self.name_input_entry.normal()
            else:
                self.name_input_entry.error()

        def validate_path():
            from pathlib import Path
            if Path(self.path_input_entry.entry.get()).exists() and self.path_input_entry.entry.get() != "":
                self.is_valid_path = True
                self.path_input_entry.normal()
            else:
                self.path_input_entry.error()

        validate_type()
        validate_name()
        validate_path()

        # TODO: JSON Save <> After Validating
        # If all validation, save it to the json file ??
        if self.is_valid_type and self.is_valid_name and self.is_valid_path:
            from managers.file import load_json, save_json, get_app_data_path
            from managers.classes import Resource
            from pathlib import Path

            self.appdata: Path = get_app_data_path()
            self.resources: dict = load_json(self.appdata, "resources", True)

            self.resource: Resource = Resource(
                self.name_input_entry.entry.get(),
                self.path_input_entry.entry.get(),
                self.type_input_CTkSegmentedButton.get()
            )

            # Add resource to resources
            self.resources[self.name_input_entry.entry.get()] = {
                "type": self.type_input_CTkSegmentedButton.get(),
                "path": self.path_input_entry.entry.get()
            }

            save_json(self.appdata, "resources", self.resources)

            # After Save remove all unneeded resources to save ram
            del load_json, save_json, get_app_data_path
            del self.appdata, self.resource, self.resources

            self.name_input_entry.entry.delete(0, ctk.END)
            self.path_input_entry.entry.delete(0, ctk.END)
            self.type_input_CTkSegmentedButton.set("")
            self.type_input_CTkSegmentedButton.configure(fg_color="#545454")

            self.name_input_entry.normal()
            self.path_input_entry.normal()
            self.type_input_CTkSegmentedButton.configure(fg_color="#545454")

            self.ResourcesViewer.update_list()


class ResourceView(ctk.CTkFrame):
    def __init__(self, master: object, resource_name: str, resource_type: str, resource_path: str):
        super().__init__(master, fg_color="#545454")

        self.resource_name: str = resource_name
        self.ResourceManger: object

        from ui.typography import create_text_label, create_button

        self.resource_name_label: ctk.CTkLabel = create_text_label(
            resource_name, "body", self)

        self.resource_name_label.pack(
            side=ctk.LEFT, anchor=ctk.CENTER, padx=10, pady=10)

        self.resource_type_label: ctk.CTkLabel = create_text_label(
            resource_type, "body", self)

        self.resource_btn_delete: ctk.CTkButton = create_button(
            self, "Delete", lambda: self.delete_resource())

        self.resource_btn_delete.pack(
            side=ctk.RIGHT, anchor=ctk.NW, padx=10, pady=10)

        self.resource_type_label.pack(
            side=ctk.RIGHT, anchor=ctk.CENTER, padx=10, pady=10)

    def delete_resource(self):
        from managers.file import load_json, get_app_data_path, save_json
        from pathlib import Path

        self.appdata: Path = get_app_data_path()
        self.resources: dict = load_json(self.appdata, "resources", True)

        # Delete the resource from the database and save it

        print(self.resources)
        del self.resources[self.resource_name]
        print(self.resources)

        save_json(self.appdata, "resources", self.resources)
        del load_json, get_app_data_path, save_json

        self.master.update_list()


class ResourcesViewer(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#3b3b3b")

        self.ResourceManger: object

        self.label = ctk.CTkLabel(
            master=self,
            text="Resource Viewer",
            font=ctk.CTkFont(size=20, weight="bold")
        )

        self.label.pack(pady=10, padx=20)

        self.resources_view: tuple = tuple()

        self.update_list()

        from ui.typography import create_space

        self.empty_space = create_space(self, 10)
        self.empty_space.pack(
            side=ctk.BOTTOM, anchor=ctk.CENTER)

    def forget_all_resources(self) -> None:
        for resource_view in self.resources_view:
            try:
                resource_view.forget()
                del resource_view
            except AttributeError:
                pass

        self.resources_view = tuple()

    def update_list(self) -> None:
        self.forget_all_resources()
        from managers.file import load_json, get_app_data_path
        from pathlib import Path

        self.appdata: Path = get_app_data_path()

        self.resources: dict = load_json(self.appdata, "resources", True)

        for key, value in self.resources.items():
            resource_view: ResourceView = ResourceView(
                self, key, value["type"], value["path"]
            )
            resource_view.pack(
                side=ctk.TOP, anchor=ctk.NW, padx=10, pady=5, fill=ctk.BOTH)

            self.resources_view += (resource_view,)
