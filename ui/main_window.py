import tkinter as tk
from ui.draft_setup_frame import DraftSetupFrame
from ui.team_setup_frame import TeamSetupFrame
from ui.draft_board_frame import DraftBoardFrame

class DraftApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Fantasy Football Draft Assistant')
        self.geometry('600x400')

        # Initialize container for frames
        self.container = tk.Frame(self)
        self.container.pack(fill = 'both', expand = True)

        # Dictionary to hold the frames
        self.frames = {}

        # Initialize and show the first frame
        self.show_frame(DraftSetupFrame)

    def show_frame(self, frame_class, *args):
        # Check what type of fram it is
        if frame_class not in self.frames:
            if frame_class == TeamSetupFrame:
                frame = frame_class(parent = self.container, controller = self, my_draft = args[0], my_db_table = args[1])
            elif frame_class == DraftBoardFrame:
                frame = frame_class(parent = self.container, controller = self, my_draft = args[0], my_db_table = args[1], my_teams = args[2])
            else:
                frame = frame_class(parent = self.container, controller = self)

            # Create the frame if it doesn't exist
            self.frames[frame_class] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        # Bring the frame to the front
        frame = self.frames[frame_class]
        frame.tkraise()

if __name__ == '__main__':
    app = DraftApp()
    app.mainloop()
