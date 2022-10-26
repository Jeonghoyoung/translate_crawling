import util.file_util as ft


a = ft.get_all_lines('../data/trans/papago_enko.txt')
b = ft.get_all_lines('../data/enko.txt')
print(len(a))
print(a[:10])

print(len(b))
print(b[:10])

c = ''
for s in b[:10]:
    c = c + '\n' +s
print(c)

b_1 = '\n'.join(b[10:20])
