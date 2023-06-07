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
class StudyView(tk.Toplevel):
    def __init__(self, parent, _task, _vars, researchers, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Assign arguments to variables
        self.parent = parent
        self._task = _task
        self._vars = _vars
        self.researchers = researchers
        self.study_types = ['Main Study', 'Sub-Study']

        # Window setup
        self.withdraw()
        self.focus()
        if self._task == 'edit':
            self.title(f"Edit Study")
        elif self._task == 'new':
            self.title("New Study")
        self.grab_set() # Disable root window (toplevel as modal window)

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

        # Submit button
        self.frm_button = ttk.Frame(self.frm_container)
        self.frm_button.grid(column=5, row=15, pady=(10,0))


        ##################
        # Create Widgets #
        ##################
        # Study title/heading
        ttk.Entry(self.frm_heading, font=('', 11, 'bold'), justify='center',
            width=50, textvariable=self._vars['study_name']).grid(
            column=5, columnspan=15, row=0, sticky='we', pady=(0,5))

        # Separator
        ttk.Separator(self.frm_container, orient='horizontal').grid(
            column=5, columnspan=20, row=12, pady=(10,0), sticky='we')

        # IRB Reference
        ttk.Label(self.frm_main, text="IRB Ref:").grid(
            column=5, row=5, **small_padding)
        ttk.Entry(self.frm_main, 
            textvariable=self._vars['irb_ref']).grid(column=10, row=5)

        # Study type
        ttk.Label(self.frm_main, text="Study Type:").grid(
            column=5, row=15, **small_padding)
        ttk.Combobox(self.frm_main, values=self.study_types, 
            state='readonly', width=17,
            textvariable=self._vars['study_type']).grid(column=10, row=15)

        # Researchers
        ttk.Label(self.frm_main, text="Researcher:").grid(
            column=5, row=20, **small_padding)
        ttk.Combobox(self.frm_main, textvariable=self._vars['researcher_id'],
            values=list(self.researchers.keys()), state='readonly',
            width=17).grid(column=10, row=20)

        # Date created
        ttk.Label(self.frm_main, text="Date Created:").grid(
            column=5, row=25, **small_padding)
        #ttk.Entry(self.frm_main,
        #    textvariable=self._vars['date_created']).grid(column=10, row=25)
        date_entry.DateEntry(self.frm_main,
            textvariable=self._vars['date_created']).grid(column=10, row=25)
        ttk.Label(self.frm_main, text="(YYYY-MM-DD)").grid(
            column=15, row=25, **small_padding)       

        # Date closed
        ttk.Label(self.frm_main, text="Date Closed:").grid(
            column=5, row=30, **small_padding)
        # ttk.Entry(self.frm_main, 
        #     textvariable=self._vars['date_closed']).grid(column=10, row=30)
        date_entry.DateEntry(self.frm_main, 
            textvariable=self._vars['date_closed']).grid(column=10, row=30)
        ttk.Label(self.frm_main, text="(YYYY-MM-DD)").grid(
            column=15, row=30, **small_padding)  

        # Submit button
        ttk.Button(self.frm_button, text="Submit", 
            command=self._on_submit).grid(column=5, row=5)


    #################
    # General Funcs #
    #################
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
            self.parent.event_generate('<<StudyViewSubmitEdit>>')
        elif self._task == 'new':
            print("\nstudyview: Sending submit new record event...")
            self.parent.event_generate('<<StudyViewSubmitNew>>')
        self.destroy()
