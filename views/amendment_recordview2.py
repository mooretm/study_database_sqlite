""" Study view.
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk

# Import custom modules
from widgets import date_entry


#########
# BEGIN #
#########
class AmendmentRecordView(tk.Toplevel):
    def __init__(self, parent, _task, _amendvars, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Assign arguments to variables
        self.parent = parent
        self._task = _task
        self._amendvars = _amendvars

        # Window setup
        self.withdraw()
        self.focus()
        if self._task == 'edit':
            self.title(f"Edit Amendment")
        elif self._task == 'new':
            self.title("New Amendment")

        # Disable root window (toplevel as modal window)
        self.grab_set() 

        # Draw widgets
        self._draw_widgets()

        # Center window
        self.center_window()


    def _draw_widgets(self):
        """ Populate the frame with all widgets.
        """
        #################
        # Create frames #
        #################
        options = {'padx':10, 'pady':10}
        small_padding = {'padx':5, 'pady':5, 'sticky':'e'}

        # Main container
        self.frm_container = ttk.Frame(self)
        self.frm_container.grid(column=5, row=5, **options)

        # Heading
        self.frm_heading = ttk.Frame(self.frm_container)
        self.frm_heading.grid(column=5, row=5)

        # Inputs
        self.frm_main = ttk.Frame(self.frm_container)
        self.frm_main.grid(column=5, row=10)

        # Rationale
        self.frm_rationale = ttk.Frame(self.frm_container)
        self.frm_rationale.grid(column=5, row=12)

        # Separator
        ttk.Separator(self.frm_container, orient='horizontal').grid(
            column=5, columnspan=20, row=15, pady=(10,0), sticky='we')
        
        # Submit button
        self.frm_button = ttk.Frame(self.frm_container)
        self.frm_button.grid(column=5, row=20, pady=(10,0))


        ##################
        # Create Widgets #
        ##################
        # Study title/heading
        ttk.Entry(self.frm_heading, font=('', 11, 'bold'), justify='center',
            width=50, textvariable=self._amendvars['study_name'],
            state='disabled').grid(column=5, columnspan=15, row=5, pady=(0,5))

        # Date submitted
        ttk.Label(self.frm_main, text="Date Submitted:").grid(
            column=5, row=5, **small_padding)
        date_entry.DateEntry(self.frm_main,
            textvariable=self._amendvars['submit_date']).grid(
            column=10, row=5)
        ttk.Label(self.frm_main, text="(YYYY-MM-DD)").grid(
            column=15, row=5, **small_padding)       

        # Date closed
        ttk.Label(self.frm_main, text="Date Approved:").grid(
            column=5, row=10, **small_padding)
        date_entry.DateEntry(self.frm_main, 
            textvariable=self._amendvars['approval_date']).grid(
            column=10, row=10)
        ttk.Label(self.frm_main, text="(YYYY-MM-DD)").grid(
            column=15, row=10, **small_padding)

        # Rationale
        ttk.Label(self.frm_rationale, text="Rationale:").grid(
            column=5, row=15, **small_padding)
        ttk.Entry(self.frm_rationale, 
            textvariable=self._amendvars['rationale'], width=70).grid(
            column=10, row=15)

        # Submit button
        ttk.Button(self.frm_button, text="Submit", 
            command=self._on_submit).grid(column=5, row=5)


    #####################
    # General Functions #
    #####################
    def center_window(self):
        """ Center the root window 
        """
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2
        self.geometry("+%d+%d" % (x, y))
        self.deiconify()


    def _on_submit(self):
        if self._task == 'edit':
            print("\nstudyview: Sending submit edits event...")
            self.parent.event_generate('<<AmendmentSubmitEdit>>')
        elif self._task == 'new':
            print("\nstudyview: Sending submit new record event...")
            self.parent.event_generate('<<AmendmentSubmitNew>>')
        self.destroy()
