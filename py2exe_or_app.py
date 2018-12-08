import os
cmd1 = "pyinstaller -F -w --icon=icon.ico --hidden-import PyQt5.sip AccountBook_transportation.py"
cmd2 = "pyinstaller -F -w --icon=icon.ico --hidden-import PyQt5.sip AccountBook_communication.py"
os.system(cmd1)
os.system(cmd2)
print('Converted Processing done...')
