import tkinter as tk
from ui.draft_setup_frame import DraftSetupFrame
from ui.team_setup_frame import TeamSetupFrame
from ui.draft_board_frame import DraftBoardFrame

class DraftApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Fantasy Football Draft Assistant')
        self.geometry('1200x600')

        # Create container frame
        self.container = tk.Frame(self)
        self.container.grid(row = 0, column = 0, sticky = 'nsew')

        # Configure the container grid to fill the entire window
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        # Create dictionary to hold the child frames
        self.frames = {}

        # Initialize and show the first frame
        self.show_frame(DraftSetupFrame)

    def show_frame(self, frame_class, *args):
        # Create the frame if it doesn't exist
        if frame_class not in self.frames:
            if frame_class == DraftSetupFrame:
                frame = frame_class(parent = self.container, controller = self)
            elif frame_class == TeamSetupFrame:
                frame = frame_class(parent = self.container, controller = self,
                                    my_draft = args[0], my_db_table = args[1], my_csv_file = args[2])
            elif frame_class == DraftBoardFrame:
                frame = frame_class(parent = self.container, controller = self, my_draft = args[0],
                                    my_db_table = args[1], my_csv_file = args[2], my_teams = args[3])

            # Store the frame and configure grid
            self.frames[frame_class] = frame
            frame.grid(row = 0, column = 0, sticky = 'nsew')

            # Make sure the frame takes up all space in the container
            self.container.grid_rowconfigure(0, weight = 1)
            self.container.grid_columnconfigure(0, weight = 1)

        # Bring the frame to the front
        frame = self.frames[frame_class]
        frame.tkraise()

# Entry point for the application
if __name__ == '__main__':
    app = DraftApp()
    app.mainloop()
