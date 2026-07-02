path = r'C:\Users\Shiva\Downloads\altprint-backend (6)\altprint\static\specific_control.html'

# Just restore from backup
import shutil
shutil.copy(path + '.backup', path)
print('Restored from backup!')
