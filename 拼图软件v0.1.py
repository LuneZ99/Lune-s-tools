import tkinter as tk
import PIL.Image as im
import tkinter.messagebox
import tkinter.filedialog
import datetime

window = tk.Tk()
window.title('拼图软件v0.1')
window.geometry('300x100')

def choose_pic():
    global filenames
    filenames = tkinter.filedialog.askopenfilenames()
    if len(filenames) != 0:
        print(len(filenames))
        string_filename = ""
        for i in range(0, len(filenames)):
            string_filename += str(filenames[i]) + "\n"
        print("您选择的文件是：" + string_filename)
    else:
        print("您没有选择任何文件")
    key=1
    for i in range(0, len(filenames)):
        dic[key]=im.open(str(filenames[i]))
        key+=1
    print('图片读取完成,读取了%d张\n'%len(filenames))

def run():
    var1 = var.get()
    def wid0(dic, width):
        for j in dic:
            wid1, hig1 = dic[j].size
            if wid1 != width:
                dic[j] = dic[j].resize((width, hig1 * width // wid1))
        print('图像大小调整完成...')


    choose_pic()
    wid = var1

    wid0(dic,wid)  # 调整图片宽度
    hig = 0
    for u in dic:
        w, h = dic[u].size
        hig += h
    oim = im.new('RGB', (wid, hig))
    x, y = 0, 0
    for m in dic:
        oim.paste(dic[m], (x, y))
        dx, dy = dic[m].size
        y += dy
    if(len(filenames)!=0):
        oim.save(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')+".jpg")
        tk.messagebox.showinfo(title='hi',message='成功')
    else:
        pass

dic={}

var=tk.IntVar()
var.set('1000')

e=tk.Entry(window,textvariable=var,width=20)
e.place(x=35, y=50)
tk.Label(window,text='请输入要拼接的图像宽度',font=('微软雅黑',10),width=20,height=1).place(x=25,y=10)
tk.Button(window, text='一键拼图',width=10,height=2,command=run).place(x=200, y=20)

window.mainloop()
