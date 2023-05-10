import tkinter as tk
from tkinter import ttk


class ValidatedMixin:
    """ Adds a validation functionality to an input widget.
    """
    def __init__(self, *args, error_var=None, **kwargs):
        self.error = error_var or tk.StringVar()
        super().__init__(*args, **kwargs)

        vcmd = self.register(self._validate)
        invcmd = self.register(self._invalid)
        self.configure(
            validate='all',
            validatecommand=(vcmd, '%P', '%s', '%S', '%V', '%i', '%d'),
            invalidcommand=(invcmd, '%P', '%s', '%S', '%V', '%i', '%d')
        )

    
    def _toggle_error(self, on=False):
        self.configure(foreground=('red' if on else 'black'))


    def _validate(self, proposed, current, char, event, index, action):
        self.error.set('')
        self._toggle_error()
        valid=True
        # If the widget is disabled, don't validate
        state = str(self.configure('state')[-1])
        if state == tk.DISABLED:
            return valid
        if event == 'focusout':
            valid = self._focusout_validate(event=event)
        elif event == 'key':
            valid = self._key_validate(
                proposed=proposed,
                current=current,
                char=char,
                event=event,
                index=index,
                action=action
            )
        return valid
    

    def _focusout_validate(self, **kwargs):
        return True
    

    def _key_validate(self, **kwargs):
        return True


    def _invalid(self, proposed, current, char, event, index, action):
        if event == 'focusout':
            self._focusout_invalid(event=event)
        elif event == 'key':
            self._key_invalid(
                proposed=proposed,
                current=current,
                char=char,
                event=event,
                index=index,
                action=action
            )


    def _focusout_invalid(self, **kwargs):
        """ Handle invalid data on a focus event.
        """
        self._toggle_error(True)


    def _key_invalid(self, **kwargs):
        """ Handle invalid data on a key event. 
            By default, do nothing.
        """
        pass


    def trigger_focusout_validation(self):
        valid = self._validate('', '', '', 'focusout', '', '')
        if not valid:
            self._focusout_invalid(event='focusout')
        return valid
