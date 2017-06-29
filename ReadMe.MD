

[主机监控部分]
ipMonitor.py  主机存活监控主程序
fping.sh 主机存活监控脚本
serverIp.cfg  主机存活监控配置文件
out.log 主机存活监控日志

[服务监控部分]
serviceMonitor.py  服务监控主程序
service.cfg  服务监控配置文件
nc.sh 服务监控脚本
out1.log 服务监控脚本

[邮件发送部分]
sendmail.py 邮件发送主程序


运行或添加开机启动到rc.local
/usr/bin/nohup /usr/local/bin/python -u /root/python/ipMonitor.py >> /root/python/out.log 2>&1 &
/usr/bin/nohup /usr/local/bin/python -u /root/python/serviceMonitor.py >> /root/python/out1.log 2>&1 &
