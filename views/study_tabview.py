""" Studies (main) notebook view
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


#########
# BEGIN #
#########
class MainFrame(ttk.Frame):
    def __init__(self, parent, studies, _studyvars, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.studies = studies
        self._studyvars = _studyvars

        # Populate frame with widgets
        self.draw_widgets()


    def draw_widgets(self):
        """ Populate the main view with all widgets
        """
        ##########
        # Styles #
        ##########
        self.style = ttk.Style(self)
        self.style.configure('Heading.TLabel', font=('', 16))


        #################
        # Create frames #
        #################
        options = {'padx':10, 'pady':10}

        # Main container
        self.frm_main = ttk.Frame(self)
        self.frm_main.grid(column=5, row=5, **options)


        ###############
        # Tree Widget #
        ###############
        columns = ('study_id', 'irb_ref', 'study_name', 'study_type', 'full_name', 'date_created', 'date_closed')
        self.tree = ttk.Treeview(self.frm_main, columns=columns, show='headings')
        # Headings
        self.tree.heading('study_id', text="ID")
        self.tree.heading('irb_ref', text="IRB Ref.")
        self.tree.heading('study_name', text="Study Name")
        self.tree.heading('study_type', text="Study Type")
        self.tree.heading('full_name', text='Researcher')
        self.tree.heading('date_created', text="Created")
        self.tree.heading('date_closed', text="Closed")
        # Columns
        self.tree.column("study_id", width=30, stretch=False)
        self.tree.column("irb_ref", width=70, stretch=False)
        self.tree.column("study_name", width=300, stretch=False)
        self.tree.column("study_type", width=70, stretch=False)
        self.tree.column("full_name", width=100, stretch=False)
        self.tree.column("date_created", width=70, stretch=False)
        self.tree.column("date_closed", width=70, stretch=False)

        # Load data into tree
        for row in self.studies:
            self.tree.insert('', tk.END, values=row)

        # Bind function to tree
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)

        # Display tree
        self.tree.grid(row=10, column=5)

        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(self.frm_main, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=10, column=6, sticky='ns')

        # KNOWN ISSUE WITH HORIZONTAL SCROLLING WITH TREEVIEW
        # scrollbar_x = ttk.Scrollbar(self.frm_main, orient=tk.HORIZONTAL, command=self.tree.xview)
        # self.tree.configure(xscroll=scrollbar_x.set)
        # scrollbar_x.grid(row=1, column=0, sticky='we')


    #############
    # Functions #
    #############
    def _on_save(self):
        self.event_generate('<<MainSave>>')


    def item_selected(self, event):
        """ Bound function to Studies treeview that retrieves
            study details and send event to controller to 
            display study editing window.
        """
        # Retrieve study details
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item['values']

        # Load study details into _studyvars
        for ii, key in enumerate(self._studyvars):
            self._studyvars[key].set(record[ii])

        # Send item select event to controller
        self.event_generate('<<MainTreeSelection>>')
