# -*- coding: utf-8 -*-
# 得到的是外网IP,也可以得到局域网IP
import re, urllib2
import socket


class getMsg(object):
    def __init__(self):
        pass

    def _getHtml(self, url):
        try:
            hdr = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
            req = urllib2.Request(url, headers=hdr)
            page = urllib2.urlopen(req)
            html = page.read()
        except:
            html = ''
        return html

    # 获取外网ip
    def getWebip(self):
        try:
            a = self._getHtml('http://www.whatismyip.com.tw/')
            myip = re.search('\d+\.\d+\.\d+\.\d+', a).group(0)
        except:
            try:
                a = self._getHtml('http://ip.myhostadmin.net/')
                myip = re.search('\d+\.\d+\.\d+\.\d+', a).group(0)
            except:
                myip = '0.0.0.0'
        return myip

    # 获取局域网ip
    def getLanip(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = socket.getservbyname("http", "tcp")
        soc.connect(("www.baidu.com", port))
        myip = soc.getsockname()[0]
        soc.close()
        return myip

    # 获取电脑主机名
    def getHostname(self):
        hostname = socket.gethostname()
        return hostname

if __name__ == '__main__':
    getMsg = getMsg()
    print getMsg.getWebip()
    print getMsg.getLanip()
    print getMsg.getHostname()
