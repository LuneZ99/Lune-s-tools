import PIL.Image as im


def read(dic):
    k = 1
    while True:
        fp = str(k) + '.jpg'
        key = 'ima' + str(k)
        try:
            dic[key] = im.open(fp)
        except FileNotFoundError:
            print('图片读取完成,共%d张...\n注：输入图片应该按顺序以"1.jpg"开始命名。\n' % (k-1))
            break
        else:
            k += 1


def wid0(dic, width):
    for j in dic:
        wid1, hig1 = dic[j].size
        if wid1 != width:
            dic[j] = dic[j].resize((width, hig1*width//wid1))
    print('图像大小调整完成...')


pict = {}
read(pict)
wid = int(input('输出图片的宽度，单位px\n'))
wid0(pict, wid)     # 调整图片宽度
hig = 0
for u in pict:
    w, h = pict[u].size
    hig += h
oim = im.new('RGB', (wid, hig))
x, y = 0, 0
for m in pict:
    oim.paste(pict[m], (x, y))
    dx, dy = pict[m].size
    y += dy
oim.save('output.jpg')
print('完成！')
