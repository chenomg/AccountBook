import os
cmd = "pyinstaller -F -w --icon=icon.ico AccountBook.py"
os.system(cmd)
print('Converted Processing done...')
