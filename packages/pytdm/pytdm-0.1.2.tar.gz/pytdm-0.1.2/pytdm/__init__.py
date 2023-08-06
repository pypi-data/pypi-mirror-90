"""Pytońska treść do mowy - Python Text to Speech library for Polish"""
from .translacja import repolonizuj, anglicyzuj, francyzuj
from .mowa import mów, zapisz, tłumacz

__version__ = "0.1.2"

# to make it non-polish-keyboard friendly:
mow = mów
tlumacz = tłumacz
