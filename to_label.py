import json

file = open('D://cs//python//project//sentiment-malaya.json', 'r', encoding='utf-8')
content = json.load(file)
file.close()
f = open('D://cs//python//project//label-malaya.txt', 'w', encoding='utf-8')
label_list = ['negative', 'positive']
for label in label_list:
    f.write('__label__'+str(label)+' '+' '.join(content[label])+'\n')
    print('写入'+str(label)+'标签成功')
f.close()