import tkinter as tk
from tkinter import ttk

from datetime import datetime

from mixins import validatedmixin


class DateEntry(validatedmixin.ValidatedMixin, ttk.Entry):
    """ Entry widget that only accepts ISO date strings.
    """
    def _key_validate(self, action, index, char, **kwargs):
        valid = True
        if action == '0': # Delete action
            valid = True
        elif index in ('0', '1', '2', '3', '5', '6', '8', '9'):
            valid = char.isdigit()
        elif index in ('4', '7'):
            valid = char == '-'
        else: 
            valid = False
        return valid


    def _focusout_validate(self, event):
        valid = True
        # if not self.get():
        #     self.error.set('A value is required')
        #     valid = False
        try:
            datetime.strptime(self.get(), '%Y-%m-%d')
        except ValueError:
            self.error.set('Invalid date')
            valid = False
        return valid
