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
    def __init__(self, parent, _task, _amendvars, all_studies, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Assign arguments to variables
        self.parent = parent
        self._task = _task
        self._amendvars = _amendvars
        self.studynames = sorted([x[2] for x in all_studies])

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
        small_padding = {'padx':5, 'pady':5}

        # Main container
        self.frm_container = ttk.Frame(self)
        self.frm_container.grid(column=5, row=5, **options)

        # Heading
        self.frm_heading = ttk.Frame(self.frm_container)
        self.frm_heading.grid(column=5, row=5)

        # Inputs
        self.frm_main = ttk.Frame(self.frm_container)
        self.frm_main.grid(column=5, row=10)

        # Separator
        ttk.Separator(self.frm_container, orient='horizontal').grid(
            column=5, columnspan=20, row=15, pady=(10,0), sticky='we')
        
        # Submit button
        self.frm_button = ttk.Frame(self.frm_container)
        self.frm_button.grid(column=5, row=20, pady=(10,0))


        ##################
        # Create Widgets #
        ##################
        # Studies combobox
        ttk.Label(self.frm_main, text="Study:").grid(column=5,
            row=5, **small_padding, sticky='e')
        self.cmbo_study = ttk.Combobox(self.frm_main, 
            textvariable=self._amendvars['study_name'],
            values=self.studynames, state='readonly', width=60)
        self.cmbo_study.grid(column=10, columnspan=20, row=5, sticky='w')

        # Rationale
        ttk.Label(self.frm_main, text="Rationale:").grid(
            column=5, row=10, **small_padding, sticky='e')
        ttk.Entry(self.frm_main, 
            textvariable=self._amendvars['rationale'], width=63).grid(
            column=10, columnspan=20, row=10, sticky='w')

        # Date submitted
        ttk.Label(self.frm_main, text="Date Submitted:").grid(
            column=5, row=15, **small_padding, sticky='e')
        date_entry.DateEntry(self.frm_main,
            textvariable=self._amendvars['submit_date']).grid(
            column=10, row=15, sticky='w')
        ttk.Label(self.frm_main, text="(YYYY-MM-DD)").grid(
            column=11, row=15, sticky='w')       

        # Date closed
        ttk.Label(self.frm_main, text="Date Approved:").grid(
            column=5, row=20, **small_padding)
        date_entry.DateEntry(self.frm_main, 
            textvariable=self._amendvars['approval_date']).grid(
            column=10, row=20, sticky='w')
        ttk.Label(self.frm_main, text="(YYYY-MM-DD)").grid(
            column=11, row=20, sticky='w')

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
            print("\namendment_recordview: Sending submit amendments edits event...")
            self.parent.event_generate('<<AmendmentSubmitEdit>>')
        elif self._task == 'new':
            print("\namendment_recordview: Sending submit new amendment event...")
            self.parent.event_generate('<<AmendmentSubmitNew>>')
        self.destroy()
