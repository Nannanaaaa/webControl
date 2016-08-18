# -*- coding: utf-8 -*-

# from flask.ext.bootstrap import Bootstrap
from flask import Flask, render_template, redirect, request, flash
# from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, validators

from util.DataBaseManager import DataBaseManager
from util.getMsg import getMsg

from flask_bootstrap import Bootstrap
from flask_wtf import Form
import re, time

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'youcouldneverknowhis-name'
app.config.from_object(__name__)


class contentForm(Form):
    # ip = StringField('', [validators.Length(min=7, max=15)])
    ip = StringField('')
    iplan = StringField('')
    commandInConfig = StringField(u'')
    commandInWrite = TextAreaField(u'', default="")
    sendCommand = SubmitField(u'发送命令')
    clearCommand = SubmitField(u'清空命令')


@app.route('/', methods=['GET', 'POST'])
def index():
    # msg = getMsg()
    ip = request.remote_addr
    # iplan = request.remote_addr
    form = contentForm()
    dataBaseManager = DataBaseManager()
    if form.validate_on_submit():
        ip = form.ip.data
        iplan = form.iplan.data
        flag_ip = re.match(r'^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$', ip)
        flag_iplan = re.match(r'^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$', iplan)
        ip_temp = request.remote_addr
        # iplan_temp = msg.getLanip()
        flag = (flag_ip and flag_iplan)
        if not (flag and flag_ip):
            return render_template('index.html', form=form, ip=ip_temp, othererrorinfo=u'IP地址格式不对或者漏写IP，请重新输入!')
        else:
            innerCommand = form.commandInConfig.data
            writeCommand = form.commandInWrite.data
            if not (innerCommand or writeCommand):
                errorinfo = u'内置命令和自定义代码至少要写一个！'
                return render_template('index.html', form=form, errorinfo=errorinfo)
            else:
                flash(u'命令发送成功！')
                info = {'iplan': iplan, 'ip': ip, 'innerCommand': innerCommand, 'writeCommand': writeCommand, 'run': False, 'time':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
                dataBaseManager.insert(info)
            return redirect('/')

    return render_template('index.html', form=form, errorinfo='', othererrorinfo='', ip=ip)


@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/other')
def other():
    return render_template('other.html')
if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=80, threaded=True)
    # app.run(processes=10)
    app.run()