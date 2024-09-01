import customtkinter as ctk

def create_text_label(text: str, type: str, master: object) -> ctk.CTkLabel:
    """
    This function creates a custom text label using the customtkinter library.
    The label's font, size, and height are determined by the provided type.

    Parameters:
    - text (str): The text to be displayed in the label.
    - type (str): The type of label to be created. It can be one of the following:
        "large_title", "title_1", "title_2", "title_3", "headline", "body", "callout",
        "subheadline", "footnote", "caption_1", "caption_2"
    - master (object): The parent widget for the label.

    Returns:
    - ctk.CTkLabel: The created custom text label.
    """

    # Create a new CTkLabel with the provided master and text
    label: ctk.CTkLabel = ctk.CTkLabel(
        master=master,
        text=text
    )

    # Set the font and height based on the provided type
    match type:
        case "large_title":
            label.configure(font=("Arial", 26, "normal"), height=32)
        case "title_1":
            label.configure(font=("Arial", 22, "normal"), height=26)
        case "title_2":
            label.configure(font=("Arial", 17, "normal"), height=22)
        case "title_3":
            label.configure(font=("Arial", 15, "normal"), height=20)
        case "headline":
            label.configure(font=("Arial", 13, "bold"), height=16)
        case "body":
            label.configure(font=("Arial", 13, "normal"), height=16)
        case "callout":
            label.configure(font=("Arial", 12, "normal"), height=15)
        case "subheadline":
            label.configure(font=("Arial", 11, "normal"), height=14)
        case "footnote":
            label.configure(font=("Arial", 10, "normal"), height=13)
        case "caption_1":
            label.configure(font=("Arial", 10, "normal"), height=13)
        case "caption_2":
            label.configure(font=("Arial", 10, "normal"), height=13)

    # Return the created label
    return label


def create_segmented_button(master, values) -> ctk.CTkSegmentedButton:
    button = ctk.CTkSegmentedButton(
        master=master,
        font=ctk.CTkFont(size=13, weight="normal"),
        text_color="#ffffff",
        fg_color="#545454",
        selected_color="#4DB848",
        corner_radius=8,
        border_width=None,
        selected_hover_color="#299a2c",
        values=values
    )
    return button


def create_button(master, text, function, color_schema = "normal") -> ctk.CTkButton:
    button = ctk.CTkButton(
        master=master,
        command=function,
        font=ctk.CTkFont(size=13, weight="normal"),
        anchor=ctk.CENTER,
        fg_color="#4DB848",
        text_color="#FFFFFF",
        hover_color="#299a2c",
        corner_radius=8,
        border_width=None,
        text=text
    )

    if color_schema == "red":
        button.configure(fg_color="#FF5722")
        button.configure(hover_color="#FF5722")

    return button


def create_space(master, height) -> ctk.CTkFrame:
    space = ctk.CTkFrame(
        master=master,
        height=height,
        fg_color="transparent",
        bg_color="transparent"
    )
    return space


class ProgressBar(ctk.CTkProgressBar):
    def __init__(self, master: object):
        super().__init__(
            master=master,
            corner_radius=8,
            border_width=None
        )

        self.max_progress: int = 100
        self.progress: int = 0

        # Set the progress bar to  the current progress
        self.set(self.progress)


class SidebarButton():
    def __init__(self, master: object, text: str, command: object):
        self.button: ctk.CTkButton = ctk.CTkButton(
            master=master,
            text=text,
            font=ctk.CTkFont(size=13, weight="normal"),
            anchor=ctk.CENTER,
            fg_color="#4DB848",
            text_color="#FFFFFF",
            hover_color="#299a2c",
            corner_radius=8,
            border_width=None,
            width=125,
            height=32,
            command=command
        )
        self.button.pack_propagate(False)

    def highlight(self):
        self.button.configure(
            fg_color="#4DB848"
        )

    def unhighlight(self):
        self.button.configure(
            fg_color="transparent"
        )


class EntryInput():
    def __init__(self, master: object):
        self.entry: ctk.CTkEntry = ctk.CTkEntry(
            master=master,
            font=ctk.CTkFont(size=13, weight="normal"),
            fg_color="#545454",
            text_color="#FFFFFF",
            corner_radius=8,
            border_width=None,
            border_color="#545454"
        )

    def error(self):
        self.entry.configure(
            border_width=2,
            border_color="red"

        )

    def normal(self):
        self.entry.configure(
            border_width=1,
            border_color="#545454"
        )
