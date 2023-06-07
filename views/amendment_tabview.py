""" Amendment notebook view
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
class AmendmentFrame(ttk.Frame):
    def __init__(self, parent, studies, _amendvars, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
 
        # Assign variables
        self.studies = studies
        self.studynames = sorted([x[2] for x in self.studies])
        self._amendvars = _amendvars

        # center widgets
        self.grid_columnconfigure(5, weight=1)

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


        ##################
        # Create Widgets #
        ##################
        # Studies combobox
        self.cmbo_study = ttk.Combobox(self.frm_main, 
            textvariable=self._amendvars['study_name'],
            values=self.studynames, state='readonly', width=60)
        self.cmbo_study.grid(column=5, row=5, pady=(0,10))
        
        # Bind function to combobox selection
        self.cmbo_study.bind('<<ComboboxSelected>>', self._get_amendments)


        #############
        # Tree view #
        #############
        columns = ('amend_id', 'submit_date', 'approval_date', 'rationale')
        self.tree = ttk.Treeview(self.frm_main, columns=columns, 
            show='headings')
        # Headings
        self.tree.heading('amend_id', text="ID")
        self.tree.heading('submit_date', text="Submitted")
        self.tree.heading('approval_date', text="Approved")
        self.tree.heading('rationale', text="Rationale")
        # Columns
        self.tree.column('amend_id', width=30, stretch=False)
        self.tree.column('submit_date', width=70, stretch=False)
        self.tree.column('approval_date', width=70, stretch=False)
        self.tree.column('rationale', width=500, stretch=False)

        # Bind function to tree
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)

        # Display tree
        self.tree.grid(row=10, column=5)

        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(self.frm_main, orient=tk.VERTICAL, 
            command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=10, column=6, sticky='ns')


    #############
    # Functions #
    #############
    def _get_amendments(self, event):
        self._amendvars['study_name'].set(self.cmbo_study.get())
        self.event_generate('<<AmendmentStudySelected>>')


    def _populate_tree(self, amendments):
        # Delete any data from amendment tree
        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in amendments:
           self.tree.insert('', tk.END, values=row)


    def item_selected(self, event):
        """ Bound function to Amendments treeview that retrieves
            amendment details and sends event to controller to 
            display amendment editing window.
        """
        # Retrieve study details
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item['values']

            # Insert selected study name to list of values
            record.insert(0, self._amendvars['study_name'].get())

        # Load study details into _amendvars
        for ii, key in enumerate(self._amendvars):
            self._amendvars[key].set(record[ii])

        # Send item select event to controller
        self.event_generate('<<AmendmentTreeSelection>>')
