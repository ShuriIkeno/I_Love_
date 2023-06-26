from flask import Flask, request, render_template, redirect, send_file
import threading
from flask_httpauth import HTTPBasicAuth
import sqlite3

#flaskを使うためのおまじないです
app = Flask(__name__)
auth = HTTPBasicAuth()
# スレッドローカルストレージを使用してSQLite接続を保存する
thread_local = threading.local()

users = {
    "kisl2023": "7g2023",
}
@auth.get_password
def get_pw(username):
    return users.get(username) if username in users else None


def get_db():
    # スレッドローカルストレージから接続を取得する
    if not hasattr(thread_local, 'connection'):
        thread_local.connection = sqlite3.connect('example.db')
    return thread_local.connection

def get_cursor():
    # スレッドローカルストレージからカーソルを取得する
    db = get_db()
    if not hasattr(thread_local, 'cursor'):
        thread_local.cursor = db.cursor()
    return thread_local.cursor

def get_image_data(image_id):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    search_image='image/'+image_id
    c.execute('SELECT image FROM sns WHERE image = ?', (search_image,))
    result = c.fetchall()
    image_data=''
    if result:
        image = result[0]
        for i in image:
            image_data+=i
        conn.close()
        return image_data
    else:
        conn.close()
        return None

#ここはルートでHTMLを表示するだけです
@app.route('/')
@auth.login_required
def welcome():
    return render_template('webpage.html')

@app.route('/survey')
@auth.login_required
def survey():
    return render_template('survey1.html')

@app.route('/webpage')
@auth.login_required
def webpage():
    return render_template('webpage.html')

@app.route('/result',methods=["GET","POST"])
@auth.login_required
def result():
    member = request.form.get('member')
    age = request.form.get('age')
    sing = request.form.get('sing')
    fan = request.form.get('fan')
    music_1 = request.form.get('music_1')
    
    conditions = []
    params = []
   
    #ここでは受け取った値の値によってデータベースの条件式が変化します
    #多いなら>=を選択する、少ないなら<にする
    if member == '多い':
        conditions.append("member >= ?")
    elif member == '少ない':
        conditions.append("member < ?")
    member=10
    params.append(member)

    if age == '多い':
        conditions.append("age >=?")
    elif age == '少ない':
        conditions.append("age < ?")
    age=19
    params.append(age)

    if sing == '多い':
        conditions.append("sing >=?")
    elif sing == '少ない':
        conditions.append("sing <?")
    sing=6
    params.append(sing)

    if fan == '多い':
        conditions.append("fan >= ?")
    elif fan == '少ない':
        conditions.append("fan < ?")
    fan=6
    params.append(fan)

    if music_1 == '1':
        conditions.append("music_1 =?")
    elif music_1 == '2':
        conditions.append("music_1 = ?")
    params.append(music_1)

    #ここはエラーチェックです
    #質問が６つあるので長さが5でないとリダイレクトしてもう一度記入してもらうことになります
    if len(conditions)!=5:
        return redirect('survey')
    
    #HTMLに送るための結果のリスト
    results=[]
    sns=[]
    if conditions:
        #データベースにアクセスして、取得する
        query = "SELECT name FROM evaluate WHERE "
        for i, condition in enumerate(conditions):
            if i !=0:
                query += " AND "
                query += condition
            else:
                query+=condition
        
        params = tuple(params)

        cursor = get_cursor()
        results=cursor.execute(query,params)
        results = cursor.fetchall()
        

        
        for i in results:
            querySns = "SELECT name, image, twitter, youtube, instagram FROM sns WHERE name=?"
            cursorSns = get_cursor()
            cursorSns.execute(querySns,i)
       
            for row in cursorSns.fetchall():
                image_name = row[0]
                image_url = row[1]  # 画像データへのURL
                snsTwitter = row[2]  # SNS
                snsYoutube = row[3]
                snsInstagram=row[4]
                sns.append({"name": image_name, "url": image_url, "Twitter": snsTwitter, "Youtube": snsYoutube, "Instagram": snsInstagram})
            
        if result is not None:
            return render_template('result.html', results=results,sns=sns)#rate=params,string=query値チェック用
        else:
            return redirect('survey')
    else:
        return redirect('survey')

@app.route('/image/<image_up>',methods=["GET","POST"])
@auth.login_required
def image(image_up):
    
    image_data = get_image_data(image_up)
    # 画像データをクライアントに送信
    return send_file(image_data, mimetype='image/jpeg')

@app.route('/icon/<icon_up>',methods=["GET","POST"])
@auth.login_required
def icon(icon_up):
    image_data = 'icon/'+icon_up
    # 画像データをクライアントに送信
    return send_file(image_data, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run()
