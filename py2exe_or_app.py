import os
cmd = 'pyinstaller -F -w --icon=logo.ico AccountBook.py'
os.system(cmd)
print('Converted Processing done...')
