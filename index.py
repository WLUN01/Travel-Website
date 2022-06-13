# pipreqs . --encoding=utf8 --force

import module as module

import flask
# Init flask
App=flask.Flask(__name__)
App.config['JSON_AS_ASCII'] = False

# Init Firebase
FireBase=module.database.DB()
Admin=module.admin.Admin(FireBase)

@App.route('/',methods=['GET','POST'])
def Home():
    return '這是臨時首頁'

@App.route('/api/TravelInfo')
def TravelInfo():
    return flask.jsonify(FireBase.Search('TravelInfo'))

@App.route('/op')
def OP():
    if Admin.LoginAuth():
        return 'Hi '+flask.request.cookies.get('LoginAccount')+'<br><a href="/op/logout">登出</a>'
    else:
        return flask.redirect('/op/login')


@App.route('/op/login',methods=['GET','POST'])
def AdminLogin():
    if flask.request.method=='POST':
        Flag,Cookie=Admin.HandleAdminLogin()
        if not Flag:
            return flask.render_template('Adminlogin.html',ERROR='管理員帳號或密碼錯誤')
        else:
            return Cookie
    return flask.render_template('Adminlogin.html')

@App.route('/op/Info',methods=['GET','POST'])
def Info():
    if Admin.LoginAuth():
        if flask.request.method=='POST':
            if flask.request.values.get('ActionType')=='CU':
                FireBase.HandleUpdateDatabase('CU','TravelInfo')
            elif flask.request.values.get('ActionType')=='D':
                FireBase.HandleUpdateDatabase('D','TravelInfo')
        return flask.render_template('Info.html')
    else:
        return flask.redirect('/op/login')
@App.route('/op/logout')
def AdminLogout():
    Flag,Cookie=Admin.HandleAdminLogout()
    if Flag:
        return Cookie
    else:
        return flask.redirect('/op/login')


App.secret_key=module.tool.GetConfigData('Flask','SecretKey')
if __name__ == '__main__':
    App.run(host='127.0.0.1',port=8000,debug=True)