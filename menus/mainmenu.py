""" Main menu class for Vesta 
"""

# Import GUI packages
import tkinter as tk
from tkinter import messagebox

class MainMenu(tk.Menu):
    """ Main Menu
    """
    # Find parent window and tell it to 
    # generate a callback sequence
    def _event(self, sequence):
        def callback(*_):
            root = self.master.winfo_toplevel()
            root.event_generate(sequence)
        return callback
    
    
    def _bind_accelerators(self):
        #self.bind_all('<space>', self._event('<<PlaybackStart>>'))
        #self.bind_all('<Control-c>', self._event('<<PlaybackStop>>'))
        self.bind_all('<Control-q>', self._event('<<FileQuit>>'))
        self.bind_all('<Control-n>', self._event('<<FileNewStudy>>'))


    def __init__(self, parent, settings, **kwargs):
        super().__init__(parent, **kwargs)

        # Instantiate
        self._settings = settings

        #############
        # File Menu #
        #############
        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(
            label="New Record...",
            command=self._event('<<FileNewStudy>>'),
            accelerator='Ctrl+N'
        )
        # file_menu.add_command(
        #     label="Session Info...",
        #     command=self._event('<<FileSession>>')
        # )
        file_menu.add_separator()
        file_menu.add_command(
            label="Quit",
            command=self._event('<<FileQuit>>'),
            accelerator='Ctrl+Q'
        )
        self.add_cascade(label='File', menu=file_menu)


        ############## 
        # Tools menu #
        ##############
        tools_menu = tk.Menu(self, tearoff=False)
        tools_menu.add_command(
            label='Audio Settings...',
            command=self._event('<<ToolsAudioSettings>>')
        )
        tools_menu.add_separator()
        tools_menu.add_command(
            label='Calibration...',
            command=self._event('<<ToolsCalibration>>')
        )
        # Add Tools menu to the menubar
        self.add_cascade(label="Tools", menu=tools_menu)


        #############
        # Help Menu #
        #############
        help_menu = tk.Menu(self, tearoff=False)
        help_menu.add_command(
            label='About...',
            command=self.show_about
        )
        help_menu.add_command(
            label='Help...',
            command=self._event('<<Help>>')
        )
        # Add help menu to the menubar
        self.add_cascade(label="Help", menu=help_menu)


        #####################
        # Bind accelerators #
        #####################
        self._bind_accelerators()


    ##################
    # Menu Functions #
    ##################
    # HELP menu
    def show_about(self):
        """ Show the about dialog """
        about_message = self._settings['name']
        about_detail = (
            'Written by: Travis M. Moore\n' +
            'Version {}\n'.format(self._settings['version']) +
            'Created: May 2, 2023\n'
            'Last edited: {}'.format(self._settings['last_edited'])
        )
        messagebox.showinfo(
            title='About',
            message=about_message,
            detail=about_detail
        )
