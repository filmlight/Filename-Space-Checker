
# HuBing DITChina © 2020 Beijing
# Space Checker GUI
# Scan & Replace Space Character in Filename.
# V20200525ORG

# OS: Windows10 Pro x64
# Running Test Passed on Python 3.8.3 x64 Win10 Pro



import platform
import socket
import getpass
import shutil
import os
import time
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import *



# [自定义函数段]
# 仅供菜单项测试
def test_doNothing_fun():
	tmpCheck_lb = Label(winRoot1, text = newChar_Chosen.get()*3)
	tmpCheck_lb.pack()


# 关于菜单 - 显示软件版本
def softVersion_fun():
	messagebox.showinfo('软件版本', '当前软件版本：V0.66 \n 作者：胡冰')


# 关于菜单 - 打开DITChina官网
def openDITWebsite_fun():
	os.system ('start https://git.ditchina.com')


# 1. 选择目标扫描路径函数
def selectRoot_fun():

	global pathSelected

	pathSelected = askdirectory(title = '选择目标扫描路径')
	if pathSelected != "":

		# 将当前工作目录切换至目标路径
		os.chdir(pathSelected)
		selectRootShow_lb.configure(relief = 'sunken', background = 'lightblue', text = '  即将扫描目录： \n' + '  ' + os.getcwd() + '  ')
		nameScan_btn2['state'] = 'normal'

		# 刷新窗口底部状态栏信息，此时定义的磁盘状态信息为局部变量
		dskTotal2, dskUsed2, dskFree2 = shutil.disk_usage ('/')
		sysInfoText.set (' 操作系统：' + platform.system() + ' ' + platform.version() + 
			'  |  主机名：' + socket.gethostname() + '  |  用户名：' + getpass.getuser() + 
			'  |  当前磁盘总容量：%dGB   剩余可用空间：%dGB' % ((dskTotal2 // (2**30)), (dskFree2 // (2**30))))


# 2. 文件名扫描函数
def nameScan_fun():
	nameScan_btn2['state'] = 'disabled'
	listShowArea.configure(state='normal')  # 开启程序文本框区域写入模式
	listShowArea.delete(1.0, END)  # 清除文本框中任何已有内容
	listShowArea.insert(INSERT, '\n')  # 为文本框区域首行插入空行
	print (os.getcwd())

	global filesCount_Total  # 初始化扫描文件计数器
	global badNameFiles_Total  # 初始化不良命名文件计数器

	# 确保每次扫描前清零
	filesCount_Total = 0
	badNameFiles_Total = 0

	# 调用[os.walk]方法遍历指定目录
	for root, dirs, files in os.walk(pathSelected, topdown = False):
		for filename in files:
			filesCount_Total = filesCount_Total + 1
			fileFullPath = os.path.abspath(os.path.join(root, filename))  # 创建文件完整路径变量，并处理Windows系统下斜杠方向
			print (fileFullPath)

			# 判断文件名称是否包含空格字符（不含目录名）
			if (' ') in filename:
				badNameFiles_Total += 1

				listShowArea.insert(INSERT, fileFullPath + '\n')  # 将不良命名文件列出至文本框区域


	scanResult_lb.configure(relief = 'sunken', background = 'lightblue', text = '  扫描目录文件总数：' + str(filesCount_Total) + 
                            '  \n' + '  发现不良命名文件个数：' + str(badNameFiles_Total) + '  ')
	
	# 恢复各功能控件状态
	nameScan_btn2['state'] = 'normal'
	replaceNewChar_btn4['state'] = 'normal'
	listShowArea.configure(state='disabled')  # 禁用文本框区域写入


# 3. 用户选择替换字符回调函数  仅供程序调试用途
def newCharSelected_callback(var, index, mode):
	tmp_test3_lb = Label (winRoot1, text = newChar_Chosen.get())
	tmp_test3_lb.place (x = 170, y = 325)


# 4. 文件名字符替换及日志文件生成函数
def replaceNewChar_fun():
	replaceNewChar_btn4['state'] = 'disabled'

	# 初始化不良命名文件路径列表
	global badFilename_list
	badFilename_list = []

	# 定义被修改名称文件计数器变量
	renamedFiles_Total = 0

	# 再次遍历指定目录
	for root, dirs, files in os.walk(pathSelected, topdown = False):
		for filename in files:
			fileFullPath = os.path.join(root, filename)  # 创建文件完整路径变量，此时不应用abspath方法
			print (fileFullPath)

			# 判断文件名称是否包含空格字符（不含目录名）
			if (' ') in filename:

			    badFilename_list.append(os.path.abspath(fileFullPath))  # 将改名前的文件路径追加至列表中

				# 执行文件名替换
			    newFilename = filename.replace(' ', newChar_Chosen.get())
			    newFileFullPath = os.path.join(root, newFilename)
			    os.replace(fileFullPath, newFileFullPath)
			    badFilename_list.append(os.path.abspath(newFileFullPath))  # 将改名后的文件路径追加至列表中
			    print (newFileFullPath)

			    renamedFiles_Total += 1

	messagebox.showinfo('替换结果', ' ' + str(renamedFiles_Total) + '个文件已被重命名。 ')

	# 创建操作日志文件对象
	renamedLog_File = open ('File_Renamed_Log.txt', mode='a', encoding='utf-8')  # 'a'模式避免清空过往日志记录
	
	# 写入当前日期与时间
	renamedLog_File.write (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
	renamedLog_File.write ('\n\n')
	
	# 写入被检测目录路径
	renamedLog_File.write ('目标检测路径：' + os.getcwd() + '\n')
	renamedLog_File.write ('\n')

	# 写入扫描基本信息
	renamedLog_File.write ('替换空格字符：' + newChar_Chosen.get() + '\n')
	renamedLog_File.write ('\n')

	renamedLog_File.write ('扫描文件总数：' + str(filesCount_Total) + '\n' + '不良命名文件个数：' + str(badNameFiles_Total) + '\n')
	renamedLog_File.write ('\n')

	# 将列表内容逐行写入文件
	for row in badFilename_list:
		renamedLog_File.write('%s\n' % row)

	renamedLog_File.write('\n')
	renamedLog_File.write('-END-')
	renamedLog_File.write('\n\n\n')
	renamedLog_File.close()  # 关闭文件

	# 显示报告文件保存位置
	exportSuccess_lb.configure(relief = 'sunken', background = 'pink', text = ' 日志文件已生成： \n' + ' File_Renamed_Log.txt ')



# [主窗口初始化段]
# 初始化程序主窗口
winRoot1 = Tk()

# 检测程序图标文件是否存在
if  os.path.isfile('DITChina_Icon.ico'):
	winRoot1.iconbitmap ('DITChina_Icon.ico')
else:
	print ('App Icon File Not Found\n')

winRoot1.title (' 文件名空格替换工具 by DITChina ')
winRoot1.geometry('1020x570')
winRoot1.resizable(False, False)


# 全局禁用菜单栏'tearOff'功能
winRoot1.option_add('*tearOff', FALSE)



# [主窗口菜单栏段]
# 创建程序主菜单
menuBar = Menu(winRoot1)
winRoot1.configure (menu = menuBar)

file_Menu = Menu(menuBar)

menuBar.add_cascade (label = ' 文件(F) ', menu = file_Menu)
file_Menu.add_command (label = ' 打开 ', command = selectRoot_fun)
file_Menu.add_command (label = ' 保存 ', command = test_doNothing_fun)
file_Menu.add_separator()
file_Menu.add_command (label = ' 退出 ', command = winRoot1.quit)


about_Menu = Menu(menuBar)

menuBar.add_cascade (label = ' 关于(A) ', menu = about_Menu)
about_Menu.add_command (label = ' 关于软件 ', command = softVersion_fun)
about_Menu.add_command (label = ' DITChina官网 ', command = openDITWebsite_fun)



# [主窗口状态栏段]
# 创建系统信息状态栏
sysInfoText = StringVar()  # 初始化系统状态信息字符串跟踪变量
statusBar = Label (textvariable = sysInfoText, bd = 1, relief = SUNKEN, anchor = W)
statusBar.pack (side = BOTTOM, fill = X)


# 获取程序当前运行所在磁盘容量信息
dskTotal1, dskUsed1, dskFree1 = shutil.disk_usage ('/')

sysInfoText.set (' 操作系统：' + platform.system() + ' ' + platform.version() + 
	'  |  主机名：' + socket.gethostname() + '  |  用户名：' + getpass.getuser() + 
	'  |  当前磁盘总容量：%dGB   剩余可用空间：%dGB' % ((dskTotal1 // (2**30)), (dskFree1 // (2**30))))



# [窗口组件段]
# 步骤1：选择目标检测路径按钮
selectRoot_btn1 = Button (winRoot1, text = ' 1. 请选择目标扫描位置 ', command = selectRoot_fun)
selectRoot_btn1.place (x = 50, y = 30)

# 显示用户选择路径
selectRootShow_lb = Label (winRoot1)
selectRootShow_lb.place (x = 50, y = 75)


# 步骤2：执行文件名扫描按钮，仅扫描不替换
nameScan_btn2 = Button (winRoot1, text = ' 2. 开始执行文件名扫描 ', command = nameScan_fun)
nameScan_btn2.place (x = 50, y = 150)
nameScan_btn2['state'] = 'disabled'

# 扫描完成后显示基本情况
scanResult_lb = Label (winRoot1)
scanResult_lb.place (x = 50, y = 195)


# 步骤3：选择文件名空格替换字符
chooseNewChar_lb = Label (winRoot1, text = ' 3. 选择文件名替换字符： ')
chooseNewChar_lb.place (x = 50, y = 270)

newChar_Chosen = StringVar()  # 初始化文件名替换字符之字符串跟踪变量
newChar_Chosen.set('_')  # 设置替换字符默认值

# 设置用户选择替换字符单选按钮
chooseNewChar_rdbtn1 = Radiobutton (winRoot1, text = '替换为 “_”', variable = newChar_Chosen, value = '_')
chooseNewChar_rdbtn1.place (x = 70, y = 300)
chooseNewChar_rdbtn2 = Radiobutton (winRoot1, text = '替换为 “-”', variable = newChar_Chosen, value = '-')
chooseNewChar_rdbtn2.place (x = 70, y = 325)
chooseNewChar_rdbtn3 = Radiobutton (winRoot1, text = '替换为 “+” （仅供调试）', variable = newChar_Chosen, value = '+')
chooseNewChar_rdbtn3.place (x = 70, y = 350)

newChar_Chosen.trace_add('write', newCharSelected_callback)  # 激活用户选择替换字符跟踪回调


# 步骤4：执行文件名字符替换并生成报告文件
replaceNewChar_btn4 = Button (winRoot1, text = ' 4. 执行文件名字符替换 ', foreground = 'purple', command = replaceNewChar_fun)
replaceNewChar_btn4.place (x = 50, y = 395)
replaceNewChar_btn4['state'] = 'disabled'

# 提示用户勿将文件设置为只读属性
noReadOnly_lb = Label (winRoot1, foreground = 'maroon', text = '*请确认文件为非只读属性')
noReadOnly_lb.place (x = 50, y = 430)

# 提示报告文件输出成功
exportSuccess_lb = Label (winRoot1)
exportSuccess_lb.place (x = 50, y = 465)


# 步骤10：定义不良命名文件列表显示区域标题框架
badListShow_frame = LabelFrame(width = 702, height = 495, bd = 2, text = ' 不良命名文件列表 ')
badListShow_frame.place (x = 280, y = 15)

# 创建列表显示文本框
listShowArea = Text(badListShow_frame, width = 99, height = 36, foreground='blue')  # 文本框长宽以字符长度计算
listShowArea.pack(side = LEFT, expand = YES, fill = BOTH)  # 以填充模式进行显示
listShowArea.configure(state='disabled')  # 默认禁用列表文本框写入

# 创建文本框垂直滚动条
text_scrollBar = Scrollbar(badListShow_frame, orient = VERTICAL, command = listShowArea.yview)
text_scrollBar.pack(side=RIGHT, fill=Y)
listShowArea.configure(yscrollcommand = text_scrollBar.set)  # 设定滚动条滑块与文本框内容联动



winRoot1.mainloop()

