path = r'C:\Users\Shiva\Downloads\altprint-backend (6)\altprint\static\specific_control.html'
html = open(path, encoding='utf-8').read()

# Remove Sales History button
html = html.replace('<button class="btn" onclick="openSalesHistory()">&#8599; Sales History</button>', '')

print('Sales History button removed:', 'openSalesHistory' not in html or html.count('openSalesHistory') <= 2)
open(path,'w',encoding='utf-8').write(html)
print('Done!')
