import os
import cv2
import tkinter as tk
import numpy as np

global point1, point2
global ensure
global point_list

point_list = []

def createWinSure():
    """ 创建一个确认框
    """
    global ensure
    win=tk.Tk()
    label=tk.Label(win,text="确认图像标注正确",bg="white",fg="black")
    label.pack()
    buttony=tk.Button(win,text="正确",command=lambda:confirm(1,win)) #收到消息执行这个函数
    buttony.pack() # 加载到窗体
    buttonn=tk.Button(win,text="错误",command=lambda:confirm(0,win)) #收到消息执行这个函数
    buttonn.pack() # 加载到窗体
    buttonn=tk.Button(win,text="结束",command=lambda:confirm(2,win)) #收到消息执行这个函数
    buttonn.pack() # 加载到窗体
    win.mainloop()

def confirm(flag,win):
    """ 点击确认框后，将结果保存到全局变量 ensure 中
    """
    global ensure
    ensure = flag
    win.destroy()

def on_mouse(event, x, y, flags, param):
    """ 鼠标响应，每次确认完一次都会重新绘制图像
    Notes:
        矩形框颜色(B, G, R)
    """
    global point1,point2
    global point_list
    global ensure
    global pressure
    img = param[0]
    index = param[1]
    box_length = 2 # 矩形框宽度
    img2 = img.copy() # 每次鼠标响应都会重新绘制
    if event == cv2.EVENT_LBUTTONDOWN: #左键点击
        point1 = (x,y)
        cv2.circle(img2, point1, 10, (0,255,0), box_length) # 单击时绘制 绿色圆形框 示意
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON): #按住左键拖曳
        cv2.rectangle(img2, point1, (x,y), (255,0,0), box_length) # 绘制 蓝色矩形框
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_LBUTTONUP: #左键释放
        point2 = (x,y)
        cv2.rectangle(img2, point1, point2, (0,0,255), box_length) # 绘制 红色矩形框
        createWinSure() # 创建一个确认框
        
        if ensure == 0: # 框选错误，重新框选
            print('未标记，请在图片上重新框选!')
            
        elif ensure == 1: # 框选正确，继续
            point_list.append([point1[0], point1[1], point2[0], point2[1]])
            print('已经增加一处标记，请继续框选，标记框数量:', len(point_list))
            img2 = cv2.rectangle(img2, point1, point2, (0,0,255), box_length) # 绘制 蓝色矩形框
            cv2.imshow('image', img2)
            
        else: # 结束
            print("--结束当前图片标记--\n")
            np.savetxt(str(index) + ".csv", point_list, delimiter=",", fmt='%d')
            point_list = [] # 将列表清零
            cv2.imshow('image', img2)
            cv2.destroyAllWindows()

def main():
    for root, dirs, files in os.walk('./data/'): 
        for i in range(0,len(files)):
            print("--当前标记的图片:", i)
            img = cv2.imread('./data/'+files[i])
            cv2.namedWindow('image', 0)
            cv2.setMouseCallback('image', on_mouse, [img,i])
            cv2.imshow('image', img)
            cv2.waitKey(0)

if __name__ == '__main__':
    main()