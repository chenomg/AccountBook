import os
cmd = 'pyuic5 -x mainwindow.ui -o mainwindow.py'
try:
    os.system(cmd)
    print('Processing done...')
except Exception as e:
    print(e)
