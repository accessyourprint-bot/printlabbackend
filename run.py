
import base64
data = base64.b64decode(open('b64.txt').read().strip())
open(r'staticull_control.html','wb').write(data)
print('Done! Written', len(data), 'bytes')
