#! /usr/bin/env python  
# -*- coding: UTF-8 -*-  
import os
import time
import threading
from sendmail import *
ser_dic={} #主机字典
sta_dic={} #状态字典

def readfile():	 
	global ser_dic
	print('配置刷新线程启动！')
	while 1:
		file=open('service.cfg','r')
		for i in file:
			ipaddr=i.replace('\n','')
			list = ipaddr.split() #获取主机和主机名列表
			#if not(ser_dic.has_key(list[0])):
			ser_dic[list[0]]=list[1] #写入主机字典
			if not(sta_dic.has_key(list[0])):
				sta_dic[list[0]]=0 #初始化状态字典
		file.close()
		#print(ser_dic) #打印主机字典
		#print(sta_dic) #打印状态字典
		print('被监控主机['+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+']:')
		for i in ser_dic:
			print('主机ip:'+'{:<25}'.format(i)+'服务名:'+'{:<17}'.format(ser_dic[i])+'服务状态:'+str(sta_dic[i]))
		time.sleep(60*2)  #每2分钟加载一次配置文件
		ser_dic={}  #刷新字典
def getStatus(ipaddr,port,protocol=''):
	if(protocol=='udp'):
		protocol='-u'
	else:
		protocol=''
	val=os.popen('sh nc.sh '+ ipaddr + ' '+port+' '+protocol).read().replace('\n','')
	if(val):
		return 0
	else:
		return 1
	
def run():
	print('检测线程启动！')
	while 1:
		for i in ser_dic: 
			target = i.split(':')
			status = getStatus(target[0],target[1],target[2]) #获取主机状态
			#print(status)
			if(status!=0 and sta_dic[i]!=status): #主机状态不正常且和状态字典状态不一致才发送告警邮件
				time_down=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))  #宕机时间
				if send_mail(mailto_list,ser_dic[i]+" 服务未开启","服务名称: "+ser_dic[i]+'\n'+'服务地址：'+i+'\n'+'宕机时间: '+time_down):
					print('发送宕机告警，告警主机: '+i)
			if(status==0 and sta_dic[i]!=status): #主机状态恢复正常，并且和存贮状态不一致发送恢复告警
				time_up=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) 
				if send_mail(mailto_list,ser_dic[i]+" 服务已恢复","服务名称: "+ser_dic[i]+'\n'+'服务地址：'+i+'\n'+'恢复时间: '+time_up):
					print('发送恢复告警，告警主机: '+i)
			sta_dic[i]=status #更新状态
		time.sleep(10) #休息10秒钟
def firstStart():
	time_start=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	if send_mail(mailto_list,"服务监控已经启动","如果这不是你的操作可能监控服务被重启！\n启动时间: "+time_start):  #邮件主题和邮件内容 
		print "发送首次启动通知邮件!"  
	else:  
		print "邮件发送失败!" 
threads = []
t1 = threading.Thread(target=readfile)
threads.append(t1)
t2 = threading.Thread(target=run)
threads.append(t2)
if __name__=="__main__":
	for t in threads:
		t.setDaemon(True)
		t.start()
	firstStart()
	hour = 0
	while 1:  #主线程保持，防止子进程退出
		time.sleep(60*60)
		hour = hour + 1 
		print('检测程序已经运行 '+str(hour)+' 小时！')