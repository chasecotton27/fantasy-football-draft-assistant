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
        self.container.grid(row=0, column=0, sticky='nsew')

        # Configure the container grid to fill the entire window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create dictionary to hold the child frames
        self.frames = {}

        # Cache last frame arguments to avoid unnecessary recreation
        self.last_args = {}

        # Initialize and show the first frame
        self.show_frame(DraftSetupFrame)

    def show_frame(self, frame_class, *args):
        # Only create the frame if it doesn't exist or args have changed
        args_tuple = tuple(args)
        if (frame_class not in self.frames) or (self.last_args.get(frame_class) != args_tuple):
            # Remove old frame if args have changed
            if frame_class in self.frames:
                self.frames[frame_class].destroy()
                del self.frames[frame_class]

            # Delay expensive frame initialization by passing minimal data
            if frame_class == DraftSetupFrame:
                frame = frame_class(parent=self.container, controller=self)
            elif frame_class == TeamSetupFrame:
                frame = frame_class(parent=self.container, controller=self,
                                    my_draft=args[0], my_db_table=args[1], my_csv_file=args[2])
            elif frame_class == DraftBoardFrame:
                frame = frame_class(parent=self.container, controller=self, my_draft=args[0],
                                    my_db_table=args[1], my_csv_file=args[2], my_teams=args[3])

            # Store the frame and configure grid
            self.frames[frame_class] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            self.last_args[frame_class] = args_tuple

        # Instead of recreating frames, update their data if needed
        frame = self.frames[frame_class]
        if hasattr(frame, "refresh") and args:
            frame.refresh(*args)  # Call a refresh method if it exists

        frame.tkraise()

# Entry point for the application
if __name__ == '__main__':
    app = DraftApp()
    app.mainloop()
