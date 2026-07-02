path = r'static\full_control.html'
html = open(path, encoding='utf-8').read()
idx = html.find('accountmgmt')
print('Found at:', idx)
print(repr(html[idx-30:idx+60]))
