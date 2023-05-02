""" Main view for Vesta
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
    def __init__(self, parent, rows, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.rows = rows
        

        # Populate frame with widgets
        self.draw_widgets()


    def draw_widgets(self):
        """ Populate the main view with all widgets
        """
        ##########
        # Styles #
        ##########
        style = ttk.Style()


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
        columns = ('irb_ref', 'study_name', 'full_name', 'date_created')

        self.tree = ttk.Treeview(self.frm_main, columns=columns, show='headings')
        self.tree.heading('irb_ref', text="IRB Ref.")
        self.tree.heading('study_name', text="Study Name")
        self.tree.heading('full_name', text='Lead')
        self.tree.heading('date_created', text="Created")

        self.tree.column("irb_ref", width=80, stretch=False)
        self.tree.column("study_name", width=350, stretch=False)
        self.tree.column("full_name", width=100, stretch=False)
        self.tree.column("date_created", width=100, stretch=False)

        # Create fake data
        samples = []
        for n in range(1,100):
            samples.append((
                f'irb {n}',
                f'lead {n}',
                f'created {n}',
                f'closed {n}'
            ))

        # Insert data into tree
        #for sample in samples:
        #    self.tree.insert('', tk.END, values=sample)

        for row in self.rows:
            self.tree.insert('', tk.END, values=row)


        # Bind function to tree
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)

        self.tree.grid(row=0, column=0, sticky='nsew')

        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(self.frm_main, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

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
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item['values']
            messagebox.showinfo(
                title="Information",
                message=','.join(record))
