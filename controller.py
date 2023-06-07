""" SQLite study tracking database proof of concept.

    Written by: Travis M. Moore
    Created: May 2, 2022
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Import system packages
import os

# Import misc packages
import webbrowser
import markdown

# Import custom modules
# Menu imports
from menus import mainmenu
# Function imports
from functions import resource_path
# Model imports
from models import sessionmodel
from models import calmodel
from models import csvmodel
from models import updatermodel
from models import dbmodel
# View imports
from views import study_tabview
from views import amendment_tabview
from views import sessionview
from views import audioview
from views import calibrationview
from views import study_recordview


#########
# BEGIN #
#########
class Application(tk.Tk):
    """ Application root window
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #############
        # Constants #
        #############
        self.NAME = 'Clinical Study Database'
        self.VERSION = '0.0.0'
        self.EDITED = 'June 07, 2023'

        # Create menu settings dictionary
        self._menu_settings = {
            'name': self.NAME,
            'version': self.VERSION,
            'last_edited': self.EDITED
        }


        ###################
        # Variables Dicts #
        ###################
        self._studyvars = {
            'study_id': tk.IntVar(),
            'irb_ref': tk.StringVar(),
            'study_name': tk.StringVar(),
            'study_type': tk.StringVar(),
            'researcher_id': tk.StringVar(),
            'date_created': tk.StringVar(),
            'date_closed': tk.StringVar(),
        }

        self._amendvars = {
            'study_name': tk.StringVar(),
            'amend_id': tk.IntVar(),
            'submit_date': tk.StringVar(),
            'approval_date': tk.StringVar(),
            'rationale': tk.StringVar(),
        }


        ######################################
        # Initialize Models, Menus and Views #
        ######################################
        # Setup main window
        self.withdraw() # Hide window during setup
        self.resizable(False, False)
        self.title(self.NAME)

        self.grid_columnconfigure(0, weight=1) # center widget
        #self.grid_rowconfigure(0, weight=1) # center widget

        # Assign special quit function on window close
        # Used to close Vulcan session cleanly even if 
        # user closes window via "X"
        self.protocol('WM_DELETE_WINDOW', self._quit)

        # Load current session parameters from file
        # Or load defaults if file does not exist yet
        self.sessionpars_model = sessionmodel.SessionParsModel()
        self._load_sessionpars()

        # Load CSV writer model
        self.csvmodel = csvmodel.CSVModel(self.sessionpars)

        # Load calibration model
        self.calmodel = calmodel.CalModel(self.sessionpars)

        # Load database model
        database = r"C:\Users\MooTra\OneDrive - Starkey\Desktop\IRB_Tracking.db"
        self.db = dbmodel.DBModel()
        self.conn = self.db.create_connection(database)

        self._get_record_values()

        # Title label
        ttk.Label(self, style='Heading.TLabel',
                  text="Clinical Study Database").grid(
            column=5, row=2, pady=(5,0))

        # Create notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=5, column=5, padx=10)

        # Load main view
        self.mainview = study_tabview.MainFrame(self.notebook, self.all_studies, self._studyvars)
        self.mainview.grid(row=0, column=0)

        # Load amendment view
        self.amendmentview = amendment_tabview.AmendmentFrame(self.notebook, self.all_studies, self._amendvars)
        self.amendmentview.grid(row=0, column=0)

        # Populate notebook tabs
        self.notebook.add(self.mainview, text="Studies")
        self.notebook.add(self.amendmentview, text="Amendments")

        # Display open study count
        self.open_study_count = tk.StringVar(value=f"Open Studies: {len(self.open_studies)}")
        ttk.Label(
            self, textvariable=self.open_study_count).grid(
            column=5, row=15, sticky='w', padx=10
        )

        # Display total study count
        self.total_study_count = tk.StringVar(value=f"Total Studies: {len(self.all_studies)}")
        ttk.Label(self, 
                  textvariable=self.total_study_count).grid(
            column=5, row=20, sticky='w', padx=10, pady=(0,10))

        # Load menus
        menu = mainmenu.MainMenu(self, self._menu_settings)
        self.config(menu=menu)

        # Create callback dictionary
        event_callbacks = {
            # File menu
            '<<FileNewStudy>>': lambda _: self.show_new_study_view(),
            '<<FileSession>>': lambda _: self._show_session_dialog(),
            '<<FileQuit>>': lambda _: self._quit(),

            # Tools menu
            '<<ToolsAudioSettings>>': lambda _: self._show_audio_dialog(),
            '<<ToolsCalibration>>': lambda _: self._show_calibration_dialog(),

            # Help menu
            '<<Help>>': lambda _: self._show_help(),

            # Main view commands
            '<<MainTreeSelection>>': lambda _: self.show_edit_study_view(),

            # Amendment view commands
            '<<AmendmentStudySelected>>': lambda _: self._populate_amendments(),
            '<<AmendmentTreeSelection>>': lambda _: self.show_edit_amendment_view(),

            # Study view commands
            '<<StudyViewSubmitEdit>>': lambda _: self.save_study_edits(),
            '<<StudyViewSubmitNew>>': lambda _: self.create_new_study(),

            # Session dialog commands
            '<<SessionSubmit>>': lambda _: self._save_sessionpars(),

            # Calibration dialog commands
            '<<CalPlay>>': lambda _: self.play_calibration_file(),
            '<<CalStop>>': lambda _: self.stop_calibration_file(),
            '<<CalibrationSubmit>>': lambda _: self._calc_level(),

            # Audio dialog commands
            '<<AudioDialogSubmit>>': lambda _: self._save_sessionpars(),
        }

        # Bind callbacks to sequences
        for sequence, callback in event_callbacks.items():
            self.bind(sequence, callback)

        # Center main window
        self.center_window()

        # Check for updates
        _filepath = r'\\starfile\Public\Temp\MooreT\Custom Software\version_library.csv'
        u = updatermodel.VersionChecker(_filepath, self.NAME, self.VERSION)
        if not u.current:
            self.destroy()


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


    def _get_record_values(self):
        # Select all open studies
        with self.conn:
            self.open_studies = self.db.select_open_studies(self.conn)
            self.all_studies = self.db.select_all_studies(self.conn)
            self.researchers = dict(self.db.select_active_researchers(self.conn))


    def _quit(self):
        """ Disconnect device(s), if possible.
            Exit the application.
        """
        # Quit app
        self.destroy()


    #######################
    # File Menu Functions #
    #######################
    def show_new_study_view(self):
        """ Show record view
        """
        # Reset self._studyvars
        for var in self._studyvars:
            self._studyvars[var].set('')

        self._studyvars['study_id'].set(0)
        
        # Create and display window
        print('\ncontroller: Calling new study view')
        study_recordview.StudyView(self, 'new', self._studyvars, self.researchers)


    #######################
    # Main View Functions #
    #######################
    def _on_save(self):
        """ Format values and send to csv model.
        """
        # Get tk variable values
        data = dict()
        for key in self.sessionpars:
            data[key] = self.sessionpars[key].get()

        # Save data
        print('controller: Calling save record function')
        self.csvmodel.save_record(data)


    def show_edit_study_view(self):
        """ Show record view
        """
        # Create and display window
        print('\ncontroller: Calling edit study view')
        study_recordview.StudyView(self, 'edit', self._studyvars, self.researchers)


    #############################
    # Amendments View Functions #
    #############################
    def _populate_amendments(self):
        """ Get list of amendments for selected study.
        """
        # Get study id based on name of selected study
        id = self.db.get_studyid_from_name(self.conn, [self._amendvars['study_name'].get()])
        # Extract id from [(int,)]
        id = id[0][0]

        # Call select amendments query
        with self.conn:
            rows = self.db.select_amendments(self.conn, [id])
        # Drop final value from each tuple
        amendments = [x[0:4] for x in rows]
        # Populate tree with amendments
        self.amendmentview._populate_tree(amendments)


    def show_edit_amendment_view(self):
        print("\nShow amendment edit view")


    ########################
    # Study View Functions #
    ########################
    def _prepare_study_vars(self):
        # Convert full name to researcher id
        self._get_researcher_id_from_name()

        # Create list of vars
        vals = self._create_list_from_vars(self._studyvars)

        # Move study_id from first position to last in list
        vals = vals[1:] + [vals[0]]

        return vals


    def _get_researcher_id_from_name(self):
        # Replace researcher full name with id
        try:
            id = int(self.researchers[self._studyvars['researcher_id'].get()])
            self._studyvars['researcher_id'].set(id)
        except KeyError:
            pass


    def _create_list_from_vars(self, vars):
        # Create list of _studyvars values
        vals = []
        for var in vars:
            # Check for NULLs
            x = vars[var].get()
            if (x == "None") or (x == ""):
                x = None
            vals.append(x)

        return vals


    def refresh_view(self):
        # Repull generic values
        self._get_record_values()

        self.open_study_count.set(f"Open Studies: {len(self.open_studies)}")
        self.total_study_count.set(f"Total Studies: {len(self.all_studies)}")

        # Delete data from mainview tree
        for row in self.mainview.tree.get_children():
            self.mainview.tree.delete(row)

        # Load data into tree
        for row in self.all_studies:
            self.mainview.tree.insert('', tk.END, values=row)


    def create_new_study(self):
        # Prepare study vars for database
        vals = self._prepare_study_vars()

        # Drop study_id from list
        vals.pop(6)

        # Update record
        with self.conn:
            self.db.create_study(self.conn, vals)

        # Refresh record tree
        self.refresh_view()


    def save_study_edits(self):
        # Prepare study vars for database
        vals = self._prepare_study_vars()

        # Update record
        with self.conn:
            self.db.update_study(self.conn, vals)

        # Refresh record tree
        self.refresh_view()


    ############################
    # Session Dialog Functions #
    ############################
    def _show_session_dialog(self):
        """ Show session parameter dialog
        """
        print("\ncontroller: Calling session dialog...")
        sessionview.SessionDialog(self, self.sessionpars)


    def _load_sessionpars(self):
        """ Load parameters into self.sessionpars dict 
        """
        vartypes = {
        'bool': tk.BooleanVar,
        'str': tk.StringVar,
        'int': tk.IntVar,
        'float': tk.DoubleVar
        }

        # Create runtime dict from session model fields
        self.sessionpars = dict()
        for key, data in self.sessionpars_model.fields.items():
            vartype = vartypes.get(data['type'], tk.StringVar)
            self.sessionpars[key] = vartype(value=data['value'])
        print("\ncontroller: Loaded sessionpars model fields into " +
            "running sessionpars dict")


    def _save_sessionpars(self, *_):
        """ Save current runtime parameters to file 
        """
        print("\ncontroller: Calling sessionpar model set and save funcs...")
        for key, variable in self.sessionpars.items():
            self.sessionpars_model.set(key, variable.get())
            self.sessionpars_model.save()


    ########################
    # Tools Menu Functions #
    ########################
    def _show_audio_dialog(self):
        """ Show audio settings dialog
        """
        print("\ncontroller: Calling audio dialog...")
        audioview.AudioDialog(self, self.sessionpars)

    def _show_calibration_dialog(self):
        """ Display the calibration dialog window
        """
        print("\ncontroller: Calling calibration dialog...")
        calibrationview.CalibrationDialog(self, self.sessionpars)


    ################################
    # Calibration Dialog Functions #
    ################################
    def play_calibration_file(self):
        """ Load calibration file and present
        """
        # Get calibration file
        self.calmodel._get_cal_file()

        # Play calibration file
        self.calmodel.play_cal()


    def stop_calibration_file(self):
        """ Stop playback of calibration file
        """
        # Stop calibration playback
        self.calmodel.stop_cal()


    def _calc_level(self):
        # Calculate new presentation level
        self.calmodel._calc_level()

        # Save level
        self._save_sessionpars()


    #######################
    # Help Menu Functions #
    #######################
    def _show_help(self):
        """ Create html help file and display in default browser
        """
        print("controller: Looking for help file in compiled " +
            "version temp location...")
        help_file = resource_path.resource_path('README\\README.html')
        #help_file = self.resource_path('README\\README.html')
        file_exists = os.access(help_file, os.F_OK)
        if not file_exists:
            print('controller: Not found!\nChecking for help file in ' +
                'local script version location')
            # Read markdown file and convert to html
            with open('README.md', 'r') as f:
                text = f.read()
                html = markdown.markdown(text)

            # Create html file for display
            with open('.\\assets\\README\\README.html', 'w') as f:
                f.write(html)

            # Open README in default web browser
            webbrowser.open('.\\assets\\README\\README.html')
        else:
            #help_file = self.resource_path('README\\README.html')
            webbrowser.open(help_file)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
