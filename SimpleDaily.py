#!/usr/bin/env python
#coding:UTF-8
#author liupeixin
#version 0.1 单人邮箱发送功能，仅支持纯文本
#version 0.2 增加周五周报提醒

import email
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import smtplib
from datetime import date

VERSION = str(0.2)

def sendEmail(authInfo, fromAdd, toAdd, subject, plainText, htmlText):
    '''发送邮件'''
    strFrom = fromAdd
    strTo = ', '.join(toAdd)

    server = authInfo.get('server')
    user = authInfo.get('user')
    passwd = authInfo.get('password')

    if not (server and user and passwd) :
        print 'incomplete login info, exit now'
        return

    # 设定root信息
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    #msgRoot['Cc'] = strFrom
    msgRoot['Disposition-Notification-To'] = strFrom
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    #print msgRoot

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    #设定纯文本信息
    msgText = MIMEText(plainText, 'plain', 'UTF-8')
    msgAlternative.attach(msgText)

    #设定HTML信息
    msgText = MIMEText(htmlText, 'html', 'UTF-8')
    msgAlternative.attach(msgText)
    
##    #设定内置图片信息
##    fp = open('test.jpg', 'rb')
##    msgImage = MIMEImage(fp.read())
##    fp.close()
##    msgImage.add_header('Content-ID', '')
##    msgRoot.attach(msgImage)

    #发送邮件
    smtp = smtplib.SMTP()
    #设定调试级别，依情况而定
    smtp.set_debuglevel(1)
    smtp.connect(server)
    smtp.login(user, passwd)
    smtp.sendmail(strFrom, strTo, msgRoot.as_string())
    smtp.quit()
    return

def doMail(describe):
    '''初始化邮件参数'''
    html = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<HTML><HEAD>
<META content="text/html; charset=UTF-8" http-equiv=Content-Type>
<META name=GENERATOR content="MSHTML 8.00.7600.16625"><LINK rel=stylesheet 
href="BLOCKQUOTE{margin-Top: 0px; margin-Bottom: 0px; margin-Left: 2em}"></HEAD>
<BODY style="MARGIN: 10px; FONT-FAMILY: verdana; FONT-SIZE: 10pt">
<DIV><FONT size=2 face=Verdana>
%s
</FONT></DIV>

<DIV><FONT size=2 face=Verdana></FONT>&nbsp;</DIV>
<DIV align=left><FONT color=#c0c0c0 size=2 face=Verdana>
%s
</FONT></DIV><FONT size=2 face=Verdana>
<HR style="WIDTH: 122px; HEIGHT: 1px" align=left SIZE=1>

<DIV><FONT color=#c0c0c0 size=2 face=Verdana><SPAN>%s</SPAN> 
</FONT></DIV></FONT>%s</BODY></HTML>
'''
    info = '\n' + '-'*5 + 'This mail send by Daily Mail Program V ' + VERSION + '-'*5 + '\n'
    
    day = date.today().strftime('%Y-%m-%d')
    name = '测试用户名'
    endname = '测试落款用户名'
    
    authInfo = {}
    authInfo['server'] = 'smtp.163.com'
    authInfo['user'] = 'fengyi_test@163.com'
    authInfo['password'] = 'fengyitest'
    
    fromAdd = authInfo['user']
    toAdd = ['fengyi_temp@163.com']
    subject = '%s %s' % (name, day)
    plainText = '%s\n\n%s\n%s\n%s%s' % (describe,day, '-'*10, endname, info)

    describe = describe.replace('\n','<br />')
    info = info.replace('\n','<br />')
    htmlText = html % (describe,day,endname,info)
    
    sendEmail(authInfo, fromAdd, toAdd, subject, plainText, htmlText)

def getWorkDescribe():
    '''获得工作日志输入'''
    yes = 'n'
    line = ''
    while(True):
        if(yes.lower() == 'y'):
            break
        text = ''
        print 'Daily Mail Program V ' + VERSION + '\nInput what do you do today,ok to exit!:'
        if date.today().isoweekday() >= 5:
            print 'Today is weekend, week report need to write.'
        while(True):
            line = raw_input()
            if line.lower() == 'ok':
                break
            elif line.lower() == 'exit':
                text = 'exit\n'
                break
            text += line + '\n'
        if(text == 'exit\n'):
            break
        yes = raw_input('The work describe:\n' + text + '\nDo you sure to send? y or n: ')
    return text[:-1].decode('gbk').encode('UTF-8')

def saveDialy():
    '''保存日志'''
    day = date.today()
    
if __name__ == '__main__' :
    describe = getWorkDescribe()
    #print describe
    if describe != 'exit':
            doMail(describe)

    raw_input('\nanykey to close......')
    
    

    
