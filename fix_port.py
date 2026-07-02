path = r'static\full_control.html'
html = open(path, encoding='utf-8').read()
html = html.replace('window.location.origin', '"http://127.0.0.1:8001"')
open(path,'w',encoding='utf-8').write(html)
print('Done')
