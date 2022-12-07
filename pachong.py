import requests, time, threading, os, webbrowser, sys, json
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import messagebox


flag = 1

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55 "
}




def check(temp, flag):
    
    if temp.find(ct) != -1:
        flag = 1
    if not (ne == ''):
        if temp.find(ne) != -1:
            flag = 0
    return flag

def pc():
    global progress_bar, info

    progress_bar = StringVar()
    label_progress=Label(window, textvariable= progress_bar, font=('微软雅黑', 10))
    label_progress.place(y=610, x=30)

    info = StringVar()
    label_info = Label(window, textvariable= info, font=('微软雅黑', 10))
    label_info.place(y=640, x=30)

    gene = threading.Thread(target=pc_main)
    gene.setDaemon(True)
    gene.start()
    
    progress = threading.Thread(target=prog_bar)
    progress.setDaemon(True)
    progress.start()

def pc_main():

    global ct, ne, rd_ch, flag, start, number, file, url, errorid
    choose_type = ['title','p']

    errorid = 0
    file = open("result.txt", "w", encoding='utf-8')
    file.write('---------------START------------------\n')
    #print('---------------START------------------')

    flag = 1
    start = time.perf_counter()

    webIdStart = entry_range1.get()
    webIdEnd = entry_range2.get()
    if entry_website.get() == '':
        messagebox.showerror('参数有误','您还未输入网址，请输入网址后重试')
        errorid = 1
        return

    if not rd_type.get():
        try:
            st = int(webIdStart)
            en = int(webIdEnd)
        except:
            messagebox.showerror('参数出错','您输入的参数有误，请检查后重新输入')
            errorid = 1
            return
    else:
        st = 0
        en = 1
    ct = entry_ct.get()
    ne = entry_ne.get()
    if entry_end.get() == '无':
        webEnd = ''
    else:
        webEnd = entry_end.get()
    
    number = 1
    f = 0
    while st < en:
        if not rd_type.get():
            url = entry_website.get() + str(st) + webEnd
        else :
            url = entry_website.get() + webIdStart + webEnd
        f = 0
        try:
            resp = requests.get(url, headers=headers)
        except:
            messagebox.showerror('参数错误', '您输入的参数有误，请检查后重试')
            errorid = 1
            return
        soup = BeautifulSoup(resp.text, 'lxml')
        res = str(resp)
        if res == '<Response [200]>':
            try:
                info.set('网站标题：' + soup.head.title.text)
            except:
                NONE
            for i in soup.find_all(choose_type[int(rd_ch.get())]):
                a = str(i.text)
                f = check(a, f)
        #else:
            #print('Something wrong, please check the response code for help' + res)
        #try:
            #print(f'{number}.{soup.head.title.text}  {webIdStart}')
        #except:
            #NONE

        if f == 1:
            if not rd_ch.get():
                    file.write(str(number) + '.' + str(soup.head.title.text) + '\n')
            else :
                    file.write(str(number) + '.' + str(soup.body.p.text) + '\n')
            if not rd_type.get():
                file.write('\t网址: %s%d\n' % (entry_website.get(), st))
            else:
                file.write('\t网址: %s%s\n' % (entry_website.get(), webIdStart))
            number += 1

        st += 1

    file.write('------------------FINISH--------------------\n')
    file.write('公告爬虫完毕')
    file.close()

    #print('------------------FINISH--------------------')

    flag = 0

def pc_gui():
    global window, entry_ct, entry_ne, entry_end, entry_range1, entry_range2, entry_website, rd_type, rd_ch, sample1, sample2,\
        website, lrange, lct, lne, lend
    window = Tk()
    window.geometry('1080x960+50+14')
    window.title('爬虫')
    window.resizable(width=True, height=True)

    label_type = Label(window, text='请选择爬虫类型', font=('微软雅黑', 10))
    label_type.place(y=30, x=30)

    rd_type = IntVar()
    rd_type1 = Radiobutton(window, text='多篇公告爬虫', font=('微软雅黑', 10), variable = rd_type, value = 0, command=bulletin)
    rd_type1.place(y=60, x=30)
    rd_type2 = Radiobutton(window, text='检索爬虫', font=('微软雅黑', 10), variable= rd_type, value= 1, command=search)
    rd_type2.place(y=90, x=30)

    label_choose = Label(window, text='请选择爬虫内容位置', font=('微软雅黑', 10))
    label_choose.place(y=120, x=30)
    
    rd_ch = IntVar()
    rd_choose1 = Radiobutton(window, text='标题', font=('微软雅黑', 10), variable= rd_ch, value= 0)
    rd_choose1.place(y=150, x=30)

    rd_choose2 = Radiobutton(window, text='正文', font=('微软雅黑', 10), variable= rd_ch, value= 1)
    rd_choose2.place(y=180, x=30)
    
#/////

    sample1 = StringVar()
    label_sample1 = Label(window, font=('微软雅黑', 10), textvariable= sample1)
    label_sample1.place(y=210, x=30)

    sample2 = StringVar()
    label_sample2 = Label(window, font=('微软雅黑', 10), textvariable= sample2)
    label_sample2.place(y=240, x=30)

    label_website = Label(window, text= '请输入需要爬虫的网址主体)', font= ('微软雅黑', 10))
    label_website.place(y=270, x=30)

    entry_website = Entry(window, font=('微软雅黑', 10), width=100)
    entry_website.place(y=300, x=30)

    lrange = StringVar()
    label_range = Label(window, textvariable=lrange, font=('微软雅黑', 10))
    label_range.place(y=330, x=30)

    entry_range1 = Entry(window, font=('微软雅黑', 10), width= 10)
    entry_range1.place(y=360, x=30)

    entry_range2 = Entry(window, font=('微软雅黑', 10), width=10)
    entry_range2.place(y=360, x=130)

    label_end = Label(window, text='请输入爬虫网站的尾缀', font=('微软雅黑', 10))
    label_end.place(y=390, x=30)

    entry_end = Entry(window, font=('微软雅黑', 10), width= 30)
    entry_end.place(y=420, x=30)

    label_ct = Label(window, text='请输入关键词', font=('微软雅黑', 10))
    label_ct.place(y=450, x=30)

    entry_ct = Entry(window, font=('微软雅黑', 10))
    entry_ct.place(y=480,x=30)

    label_ne = Label(window, text='请输入忽略内容', font=('微软雅黑', 10))
    label_ne.place(y=510, x=30)
    
    entry_ne = Entry(window, font=('微软雅黑', 10))
    entry_ne.place(y=540, x=30)

    entry_ne = Entry(window, font=('微软雅黑', 10))
    entry_ne.place(y=540, x=30)

    bt_generate = Button(window, text='运行', font=('微软雅黑', 10), command= pc)
    bt_generate.place(y=570, x=30)
    bulletin()

def bulletin():
    sample1.set('输入网址格式: 网址主体+范围编号起始+范围编号结束+尾缀, 如网址: https://www.caanet.org.cn/newsdetail.mx?id=7980')
    sample2.set('主体: https://www.caanet.org.cn/newsdetail.mx?id=  范围编号起始: 7980   范围编号结束: 8125   尾缀: (没有可不填写)')
    lrange.set('请输入需要爬虫网站的范围')
    entry_range2.config(state= NORMAL)

def search():
    sample1.set('输入网址格式: 网址主体+搜索内容+尾缀, 如网址: https://www.baidu.com/s?ie=UTF-8&wd=hello')
    sample2.set('主体: https://www.baidu.com/s?ie=UTF-8&wd=   搜索内容: hello   尾缀: (没有可不填写)')
    lrange.set('请输入需要爬虫获取的搜索内容')
    entry_range2.config(state= DISABLED)


def prog_bar():
    errorid = 0
    global flag
    dot = '.'
    count = 0
    progress_bar.set('')
    info.set('')
    time.sleep(0.1)
    while flag:
        try:
            progress_bar.set(f'正在获取网站 {url} 内容，请稍后{dot}')
#           time.sleep(0.1)
        except:
            return
        count += 1
        dot += '.'
        if count == 3:
            count = 0
            dot = '.'
        if errorid == 1:
            return
    end = time.perf_counter()
    time.sleep(0.1)
    flag = 1

    pic_time = round(end-start)
    progress_bar.set(f'---爬虫结束，本次任务得到有效信息{number-1}条，共耗时{pic_time}秒---')

    info.set(f'详细信息请点击查看按钮')

    bt_open = Button(window, text='打开文件', font=('微软雅黑', 10), command= openfile)
    bt_open.place(y=680, x=30)


def of():
    os.system('result.txt')

def openfile():
    openf = threading.Thread(target= of)
    openf.setDaemon(True)
    openf.start()
    

pc_gui()
window.mainloop()
