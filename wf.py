import base64,os
path=r'static\full_control.html'
b64=open('b64.txt').read().strip()
data=base64.b64decode(b64)
open(path,'wb').write(data)
print('Done! Written',len(data),'bytes')
