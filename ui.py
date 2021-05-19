import tkinter as tk
from tkinter import ttk
import sys
import run
import crawler
def main():
    def choose(f2f1,f2,t):
        b1=tk.Button(f2f1,text='1. Search', width=25, height=1,command=lambda:us(f2f1,f2,t))
        b1.pack()
        b4=tk.Button(f2f1,text='2. Start Download Animation', width=25, height=1,command=lambda:t.insert('end','1'))
        b4.pack()
        b5=tk.Button(f2f1,text='3. Start Download User-Video', width=25, height=1,command=uv)
        b5.pack()
        b6=tk.Button(f2f1,text='Quit Program', width=25, height=1,command=lambda:sys.exit())
        b6.pack()
    def uv():
        def close():
            frame.destroy()
        frame=tk.Frame(f1)
        frame.pack(side='top')
        var.set('Enter the Start and Stop id')
        e1 = tk.Entry(frame,  width=5,show = None)
        e1.pack(side='left')
        e2 = tk.Entry(frame,  width=5,show = None)
        e2.pack(side='left')
        b1 = tk.Button(frame, text='Commit', width=10,height=1, command=lambda:run.uv(int(e1.get()),int(e2.get())))
        b1.pack(side='left')
        b4 = tk.Button(frame, text='Close', width=10,height=1, command=close)
        b4.pack(side='left')
    def an():
        def close():
            frame.destroy()
        frame=tk.Frame(f1)
        frame.pack(side='top')
        var.set('Enter the Start and Stop page')
        e1 = tk.Entry(frame,  width=5,show = None)
        e1.pack(side='left')
        e2 = tk.Entry(frame,  width=5,show = None)
        e2.pack(side='left')
        b1 = tk.Button(frame, text='Commit', width=10,height=1, command=lambda:run.ba(int(e1.get()),int(e2.get())))
        b1.pack(side='left')
        b4 = tk.Button(frame, text='Close', width=10,height=1, command=close)
        b4.pack(side='left')
        
    def us(frame,fra,t):
        var='ok1\n'
        t.insert('end', var)
        frame.pack_forget()
        frame1 = tk.Frame(fra)
        frame1.pack()
        b1=tk.Button(frame1,text='1. Search user', width=25, height=1,command=lambda:user())
        b1.pack()
        b2=tk.Button(frame1,text='2. Search video', width=25, height=1,command=video)
        b2.pack()
        b3=tk.Button(frame1,text='3. Search animation', width=25, height=1,command=anim)
        b3.pack()
        b4=tk.Button(frame1,text='Back', width=25, height=1,command=lambda:usback(frame,frame1))
        b4.pack()
    def video():
        def search(frame2,key,add=0):
            nonlocal p
            if add!=0:
                p=(p+add)
                page=p
                if p<1:
                    p=(1)
                    page=1
            else:
                p=(1)
                page=1
            res=crawler.search('video',key,page)
            tree = ttk.Treeview(frame2, show = "headings", selectmode = tk.BROWSE)      # #创建表格对象
            tree["columns"] =(
            "title",
            "description",
            "author",
            "play",
            'video_review',
            "favorites",
            "review",
            "pubdate",
            "duration",
            "arcurl"            )     # #定义列
            tree.column("title", width=100)          # #设置列
            tree.column("description", width=100)
            tree.column("author", width=100)
            tree.column("play", width=100)
            tree.column("video_review", width=100)
            tree.column("favorites", width=100)
            tree.column("review", width=100)
            tree.column("pubdate", width=100)
            tree.column("duration", width=100)
            tree.column("arcurl", width=100)
            tree.heading("title", text='title')          # #设置列
            tree.heading("description", text='description')
            tree.heading("author",text='author')
            tree.heading("play", text='play')
            tree.heading("video_review", text='video_review')
            tree.heading("favorites", text='favorites')
            tree.heading("review", text='review')
            tree.heading("pubdate", text='pubdate')
            tree.heading("duration", text='duration')
            tree.heading("arcurl", text='arcurl')
            for x in res:
                tree.insert("", 0, values=x)
            tree.pack(side='bottom')
        def changepage(f1,key,add):
            nonlocal frame2
            frame2.destroy()
            frame2 = tk.Frame(f1)
            frame2.pack(side='top')
            search(frame2,key,add)
        def close():
            frame1.destroy()
            frame2.destroy()
        frame1 = tk.Frame(f1)
        frame1.pack(side='top')
        frame2 = tk.Frame(f1)
        frame2.pack(side='top')
        e = tk.Entry(frame1,  width=10,show = None)
        e.pack(side='left')
        p=1
        b1 = tk.Button(frame1, text='Search Video', width=10,height=1, command=lambda:changepage(f1,e.get(),0))
        b1.pack(side='left')   
        b2 = tk.Button(frame1, text='Next Page', width=10,height=1, command=lambda:changepage(f1,e.get(),1))
        b3 = tk.Button(frame1, text='Last Page', width=10,height=1, command=lambda:changepage(f1,e.get(),-1))
        b2.pack(side='left')
        b3.pack(side='left')
        b4 = tk.Button(frame1, text='Close', width=10,height=1, command=close)
        b4.pack()
    def anim():
        def search(frame2,key,add=0):
            nonlocal p
            if add!=0:
                p=(p+add)
                page=p
                if p<1:
                    p=(1)
                    page=1
            else:
                p=(1)
                page=1
            res=crawler.search('media_bangumi',key,page)
            tree = ttk.Treeview(frame2, show = "headings", selectmode = tk.BROWSE)      # #创建表格对象
            tree["columns"] =(
            "title",
            "areas",
            "desc",
            "pubtime",
            "scorecount",
            "score",
            "goto_url"
            )     # #定义列
            tree.column("title", width=100)          # #设置列
            tree.column("areas", width=100)
            tree.column("desc", width=100)
            tree.column("pubtime", width=100)
            tree.column("scorecount", width=100)
            tree.column("score", width=100)
            tree.column("goto_url", width=100)
            tree.heading("title", text='title')          # #设置列
            tree.heading("areas", text='areas')
            tree.heading("desc",text='desc')
            tree.heading("pubtime", text='pubtime')
            tree.heading("scorecount", text='scorecount')
            tree.heading("score", text='score')
            tree.heading("goto_url", text='goto_url')
            for x in res:
                tree.insert("", 0, values=x)
            tree.pack(side='bottom')
        def changepage(f1,key,add):
            nonlocal frame2
            frame2.destroy()
            frame2 = tk.Frame(f1)
            frame2.pack(side='top')
            search(frame2,key,add)
        def close():
            frame1.destroy()
            frame2.destroy()
        frame1 = tk.Frame(f1)
        frame1.pack(side='top')
        frame2 = tk.Frame(f1)
        frame2.pack(side='top')
        e = tk.Entry(frame1,  width=10,show = None)
        e.pack(side='left')
        p=1
        b1 = tk.Button(frame1, text='Search Animation', width=15,height=1, command=lambda:changepage(f1,e.get(),0))
        b1.pack(side='left')   
        b2 = tk.Button(frame1, text='Next Page', width=10,height=1, command=lambda:changepage(f1,e.get(),1))
        b3 = tk.Button(frame1, text='Last Page', width=10,height=1, command=lambda:changepage(f1,e.get(),-1))
        b2.pack(side='left')
        b3.pack(side='left')
        b4 = tk.Button(frame1, text='Close', width=10,height=1, command=close)
        b4.pack()        
    def usback(frame,frame1):
        frame1.pack_forget()
        frame.pack()
    def user():
        def search(frame2,key,add=0):
            nonlocal p
            if add!=0:
                p=(p+add)
                page=p
                if p<1:
                    p=(1)
                    page=1
            else:
                p=(1)
                page=1
            res=crawler.search('bili_user',key,page)
            tree = ttk.Treeview(frame2, show = "headings", selectmode = tk.BROWSE)      # #创建表格对象
            tree["columns"] = (
                "uname",
                "mid",
                "usign",
                "fans",
                "videos",
                "level",
                "gender"
            )     # #定义列
            tree.column("uname", width=100)          # #设置列
            tree.column("mid", width=100)
            tree.column("usign", width=100)
            tree.column("fans", width=100)
            tree.column("videos", width=100)
            tree.column("level", width=100)
            tree.column("gender", width=100)
            tree.heading("uname", text='uname')          # #设置列
            tree.heading("mid", text='mid')
            tree.heading("usign",text='usign')
            tree.heading("fans", text='fans')
            tree.heading("videos", text='videos')
            tree.heading("level", text='level')
            tree.heading("gender", text='gender')
            for x in res:
                tree.insert("", 0, values=x)
            tree.pack(side='bottom')
        def changepage(f1,key,add):
            nonlocal frame2
            frame2.destroy()
            frame2 = tk.Frame(f1)
            frame2.pack(side='top')
            search(frame2,key,add)
        def close():
            frame1.destroy()
            frame2.destroy()
        frame1 = tk.Frame(f1)
        frame1.pack(side='top')
        frame2 = tk.Frame(f1)
        frame2.pack(side='top')
        e = tk.Entry(frame1,  width=10,show = None)
        e.pack(side='left')
        p=1
        b1 = tk.Button(frame1, text='Search User', width=10,height=1, command=lambda:search(frame2,e.get()))
        b1.pack(side='left')   
        b2 = tk.Button(frame1, text='Next Page', width=10,height=1, command=lambda:changepage(f1,e.get(),1))
        b3 = tk.Button(frame1, text='Last Page', width=10,height=1, command=lambda:changepage(f1,e.get(),-1))
        b2.pack(side='left')
        b3.pack(side='left')
        b4 = tk.Button(frame1, text='Close', width=10,height=1, command=close)
        b4.pack()
    window = tk.Tk()
    window.title('User Interface')
    window.geometry('1000x800')
    f1 = tk.Frame(window)
    f2 = tk.Frame(window)
    f1.place(x=260, y=50, anchor='nw')
    f2.place(x=40, y=50, anchor='nw')
    f1f1=tk.Frame(f1)
    f1f1.pack(side='top')
    f1f2=tk.Frame(f1)
    f1f2.pack(side='top')
    f1f3=tk.Frame(f1)
    f1f3.pack(side='top')
    f2f1=tk.Frame(f2)
    f2f1.pack()
    var = tk.StringVar() 
    l = tk.Label(f1f1,  textvariable=var, bg='white', fg='black', font=('Arial', 12), width=55, height=2)
    l.pack(side='left')    
    t = tk.Text(f1f2,width=69, height=10)
    t.pack(side='left')
    scroll = tk.Scrollbar(f1f2)
    scroll.pack(side='left',fill='y')
    scroll.config(command=t.yview)
    t.config(yscrollcommand=scroll.set)
    choose(f2f1,f2,t)
    window.mainloop()

if __name__=='__main__':
    main()