import PIL.Image as Im
import copy
import time
import sys

sys.setrecursionlimit(3200)             # 设置最大递归次数为3200
sta = time.clock()                      # 记录程序开始时间戳


def cut(im):                            # 切片

    im0 = Im.open(im+'.jpg')
    if im0.mode != 'L':
        im0 = im0.convert('L')
    wid, hig = im0.size
    x = wid // 250
    y = hig // 250
    ri = 0

    for xi in range(x):
        for yi in range(y):
            im = im0.crop([xi * 250, yi * 250, (xi + 1) * 250, (yi + 1) * 250])
            im.save('a' + str(ri) + '.jpg')
            ri += 1

    if (wid % 250) != 0:
        for yi in range(y):
            im1 = im0.crop([x * 250, yi * 250, wid, (yi + 1) * 250])
            im1.save('a' + str(ri) + '.jpg')
            ri += 1

    if (hig % 250) != 0:
        for xi in range(x):
            im2 = im0.crop([xi * 250, y * 250, (xi + 1) * 250, hig])
            im2.save('a' + str(ri) + '.jpg')
            ri += 1

    if (wid % 250) != 0 and (hig % 250) != 0:
        im3 = im0.crop([x * 250, y * 250, wid, hig])
        im3.save('a' + str(ri) + '.jpg')
        ri += 1

    print('\n切片完成，共', ri, '片', '预计运行时间', (ri+1)**2/3.25, 's')

    return ri


def read(lis0, lis1, f):

    fp = 'a'+str(f)+'.jpg'              # 读取
    im0 = Im.open(fp)
    pic = im0.load()
    wid, hig = im0.size

    line = [0]                          # 初始化一维数组（单列）
    line *= hig
    for i1 in range(wid):
        lis0.append(copy.copy(line))    # 初始化二维数组
        lis1 = copy.deepcopy(lis0)      # 初始化遍历状态

    for xw in range(wid):
        for yh in range(hig):
            if pic[xw, yh] <= 200:      # 阈值 ∈ [0, 255]
                lis0[xw][yh] = 1        # 初始化目标像素

    return wid, hig, lis0, lis1


def dfs(lis0, xi, yi, lis1, wid, hig):  # 深度优先搜索

    lis1[xi][yi] = 1                    # 标记为已搜索

    if xi == wid or yi == hig:          # 消除切片分割单块造成的误差
        return 0

    for delta in ([1, 0], [0, 1], [-1, 0], [0, -1]):
        if 0 <= xi+delta[0] < wid and 0 <= yi+delta[1] < hig:                                   # 判断未越界
            if lis1[xi+delta[0]][yi+delta[1]] == 0 and lis0[xi+delta[0]][yi+delta[1]] == 1:     # 判断为目标 & 未标记
                dfs(lis0, xi+delta[0], yi+delta[1], lis1, wid, hig)                             # 进入满足条件的像素

    return 1


def counter(fp):

    cou = 0     # 初始化总数

    piece = cut(fp)

    print('计算中。。。')

    for i in range(piece):

        li0 = []
        li1 = []
        count = 0

        wi, hi, li0, li1 = read(li0, li1, i)        # 读取分块

        for xa in range(wi):
            for ya in range(hi):
                if li0[xa][ya] == 1 and li1[xa][ya] == 0:
                    xb, yb = xa, ya
                    count += dfs(li0, xb, yb, li1, wi, hi)

        print('切片', i+1, '共计', count)
        cou += count

    print('总计', cou, '个图形')


def main(fpp):
    try:
        counter(fpp)
    except RecursionError:
        print('\n单个图形面积太大，即将栈溢出……\n程序将自动缩小后再重新计算……')
        ims = Im.open(fpp + '.jpg')
        w, h = ims.size
        ims = ims.resize((w//2, h//2))
        ims.save(fpp + 's.jpg')
        main(fpp + 's')


fpi = input('\n输入文件名(不包括后缀):')
main(fpi)

end = time.clock()              # 记录运算结束时间戳
print('耗时', end-sta, 's')
print('完成\n按 ENTER 键退出……')
aaa = input()
