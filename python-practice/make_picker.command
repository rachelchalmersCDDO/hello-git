#!/usr/bin/env python
import os  

os.rename('name picker.py', 'name_picker.command') 
os.chmod("name_picker.command", stat.S_IEXEC)

print("Created executable!")
exit()