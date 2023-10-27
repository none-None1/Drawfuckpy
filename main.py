from tkinter import *
from time import *
from tkinter.filedialog import *
from PIL import Image, ImageTk
running=False
update=False
insts=0
curtime=0
mat={}
wnd=Tk()
wnd.geometry('512x284')
wnd.title('Drawfuckpy')
code_editor=Text(wnd)
code_editor.insert(END,"code")
code_editor.place(x=0,y=0,height=128,width=256)
input_editor=Text(wnd)
input_editor.insert(END,"input")
input_editor.place(x=0,y=128,height=100,width=256)
run_btn=Button(wnd)
stat=StringVar()
stat.set("Not Running")
stat_label=Label(wnd)
stat_label.config(textvariable=stat)
stat_label.place(x=0,y=256,height=28,width=512)
def click():
    global running,curtime,insts,ip,p,tape,code,inp,img,itk,mat,xy
    xy=(0,0)
    code, inp = code_editor.get('0.0', END), input_editor.get('0.0', END)
    ip,p,tape=0,0,[0]*1000000
    running=True
    code_editor.config(background='gray')
    input_editor.config(background='gray')
    code_editor.config(state='disabled')
    input_editor.config(state='disabled')
    img = Image.new('RGB', (256, 256), (255, 255, 255))
    itk = ImageTk.PhotoImage(img)
    image_label.config(image=itk)
    insts=0
    curtime=perf_counter()
    stat.set("Running - 0 instructions executed, - instructions/s")
    stk=[]
    mat={}
    for j,i in enumerate(code):
        if i=='[':
            stk.append(j)
        if i==']':
            a=stk.pop()
            mat[a]=j
            mat[j]=a
def saveimg():
    im=asksaveasfilename(title='Save image')
    if im:
        img.save(im)
run_btn.config(text='Run',command=click)
run_btn.place(x=0,y=228,height=28,width=128)
save_btn=Button(text='Save Image',command=saveimg)
save_btn.place(x=128,y=228,height=28,width=128)
tape,p,ip=[0]*1000000,0,0
code,inp=code_editor.get('0.0',END),input_editor.get('0.0',END)
rgb,xy=(0,0,0),(0,0)
img=Image.new('RGB',(256,256),(255,255,255))
itk=ImageTk.PhotoImage(img)
image_label=Label(wnd)
image_label.config(image=itk)
image_label.place(x=256,y=0,width=256,height=256)
def runonce():
    global code,ip,p,insts,inp,rgb,xy,img,itk,update
    if insts % 1000 == 0 and update:
        update=False
        itk = ImageTk.PhotoImage(img)
        image_label.config(image=itk)
    insts+=1
    if code[ip]=='+':
        tape[p]=(tape[p]+1)%256
    if code[ip]=='-':
        tape[p]=(tape[p]-1)%256
    if code[ip]==',':
        tape[p]=(ord(inp[0]) if inp else 0)
        inp=inp[1:]
    if code[ip]=='.':
        update=True
        img.load()[xy]=rgb
    if code[ip]=='r':
        rgb=tape[p],rgb[1],rgb[2]
    if code[ip]=='g':
        rgb=rgb[0],tape[p],rgb[2]
    if code[ip]=='b':
        rgb=rgb[0],rgb[1],tape[p]
    if code[ip]=='>':
        p+=1
    if code[ip]=='<':
        p-=1
    if code[ip]=='x':
        xy=tape[p],xy[1]
    if code[ip]=='y':
        xy=xy[0],tape[p]
    if code[ip]=='w':
        xy=xy[0]-1,xy[1]
    if code[ip]=='e':
        xy=xy[0]+1,xy[1]
    if code[ip]=='s':
        xy=xy[0],xy[1]+1
    if code[ip]=='n':
        xy=xy[0],xy[1]-1
    if code[ip]=='[':
        if not tape[p]:
            ip=mat[ip]
            return
    if code[ip]==']':
        if tape[p]:
            ip=mat[ip]
            return
    ip+=1
while 1:
    try:
        if running:
            runonce()
            if ip>=len(code):
                itk = ImageTk.PhotoImage(img)
                image_label.config(image=itk)
                running=False
                stat.set("Not Running")
                code_editor.config(state='normal',background='white')
                input_editor.config(state='normal',background='white')
            else:
                stat.set("Running - {} instructions executed, {} instructions/s".format(insts,insts/(perf_counter()-curtime) if perf_counter()-curtime else '-'))
        wnd.update()
    except:
        break