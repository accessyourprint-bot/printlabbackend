p=r'C:\Users\Shiva\Downloads\altprint-backend (6)\altprint\static\full_control.html'
c=open(p,encoding='utf-8').read()
old='function showAddOutlet(){alert(' + chr(39) + 'Add Outlet ' + chr(8212) + ' connect to POST /api/v1/shops' + chr(39) + ');}'
new='function showAddOutlet(){document.getElementById(' + chr(39) + 'addOutletForm' + chr(39) + ').style.display=' + chr(39) + 'block' + chr(39) + ';}'
c=c.replace(old,new)
open(p,'w',encoding='utf-8').write(c)
print('Done, size:',len(c))
