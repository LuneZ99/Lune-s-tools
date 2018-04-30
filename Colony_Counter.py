import PIL.Image as Im
import copy
import time

# import sys
# sys.setrecursionlimit(3200)           设置最大递归次数为3200（视操作系统可能反而引起溢出，故暂时注释）

sta = time.clock()                      # 记录程序开始时间戳


def cut(im, si=250):                    # 切片函数，大小为 si×si 以内

    im0 = Im.open(im+'.png')
    '''
    if im0.mode != 'L':
        im0 = im0.convert('L')
        '''
    wid, hig = im0.size
    x = wid // si
    y = hig // si
    ri = 0

    for xi in range(x):
        for yi in range(y):
            im = im0.crop([xi * si, yi * si, (xi + 1) * si, (yi + 1) * si])
            im.save('a' + str(ri) + '.bmp')
            ri += 1

    if (wid % si) != 0:
        for yi in range(y):
            im1 = im0.crop([x * si, yi * si, wid, (yi + 1) * si])
            im1.save('a' + str(ri) + '.bmp')
            ri += 1

    if (hig % si) != 0:
        for xi in range(x):
            im2 = im0.crop([xi * si, y * si, (xi + 1) * si, hig])
            im2.save('a' + str(ri) + '.bmp')
            ri += 1

    if (wid % si) != 0 and (hig % si) != 0:
        im3 = im0.crop([x * si, y * si, wid, hig])
        im3.save('a' + str(ri) + '.bmp')
        ri += 1

    print('\n切片完成，共', ri, '片')

    return ri, si


def read(lis0, lis1, f):                # 读取图片并转化为二维数组函数

    fp = 'a'+str(f)+'.bmp'              # 读取
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
            if pic[xw, yh][0] > 250 and pic[xw, yh][1] < 66 and pic[xw, yh][2] < 66:
                lis0[xw][yh] = 1        # 初始化目标像素
            if pic[xw, yh][0] > 250 and 66 < pic[xw, yh][1] < 180 and 80 < pic[xw, yh][2] < 220:
                lis0[xw][yh] = 2

    return wid, hig, lis0, lis1


def dfs(lis0, xi, yi, lis1, wid, hig, si, typ):  # 深度优先搜索

    lis1[xi][yi] = 1                        # 标记为已搜索

    for delta in ([1, 0], [0, 1], [-1, 0], [0, -1]):
        if 0 <= xi+delta[0] < wid and 0 <= yi+delta[1] < hig:                                # 判断未越界
            if (xi % si + 1) == si or (yi % si + 1) == si:                                   # 消除切片分割单块造成的误差
                return 0
            if lis1[xi+delta[0]][yi+delta[1]] == 0 and lis0[xi+delta[0]][yi+delta[1]] == typ:  # 判断为目标 & 未标记
                dfs(lis0, xi+delta[0], yi+delta[1], lis1, wid, hig, si, typ)                      # 进入满足条件的像素

    return 1


def counter(fp, trr):                               # 对文件切片并计数函数

    cou1 = 0     # 初始化总数
    cou2 = 0

    piece, s = cut(fp, trr)                         # 调用切片函数

    print('计算中。。。')

    for i in range(piece):                          # 对于每一个分块
        for j in range(2):
            li0 = []
            li1 = []
            count = 0

            wi, hi, li0, li1 = read(li0, li1, i)        # 读取分块

            for xa in range(wi):                        # 对每个像素进行判断&搜索&计数
                for ya in range(hi):
                    if li0[xa][ya] == j+1 and li1[xa][ya] == 0:
                        xb, yb = xa, ya
                        count += dfs(li0, xb, yb, li1, wi, hi, s, j+1)

            print('切片', i, '共计', count)
            if j == 0:
                cou1 += count
            if j == 1:
                cou2 += count

    print('总计', cou1, cou2, '个图形')


def main(fpp, tr=250):          # 主程序函数，检测并阻止栈溢出
    try:
        counter(fpp, tr)        # 调用切片+计数函数
    except RecursionError:
        print('\n单个图形面积太大，即将栈溢出……\n程序将自动缩小后再重新计算……')    # 对照片的长宽等比减小
        ims = Im.open(fpp + '.png')
        w, h = ims.size                                                            # 缩放至面积为1/2
        ims = ims.resize((int(w/(2**0.5)), int(h/(2**0.5))))   # 被注释部分为抗锯齿选项 会导致个数减小
        ims.save(fpp + 's.png')                                                    # 是否是因为处理了毛边？
        main(fpp + 's', int(tr/(2**0.5)))                                      # 对新图执行main函数


fpi = input('\n输入文件名(不包括后缀):')
tri = input('切片宽（默认250，可不填）：')      # 该变量将进入多层函数，默认250

if tri == '':                                 # 检测tri是否为空而使用默认
    main(fpi)                                 # 执行主函数main
else:
    main(fpi, int(tri))

end = time.clock()                            # 记录运算结束时间戳
print('耗时', end-sta, 's')
print('完成\n按 ENTER 键退出……')               # 是否可做按任意键退出？
aaa = input()
