from flask import Flask, request, render_template, redirect, send_file
import threading
from flask_sqlalchemy import SQLAlchemy
import sqlite3

#flaskを使うためのおまじないです
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////Users/ikenoshuri/システム主専攻実習_推し/example.db'
# db=SQLAlchemy(app)


# スレッドローカルストレージを使用してSQLite接続を保存する
thread_local = threading.local()

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
    c.execute('SELECT image FROM pre_sns WHERE image = ?', (search_image,))
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
#ここはデータベースのクラスを設定しています
#ですが設定により使わないかもしれません
#使う場合がありますので残しておいてください
# class Evaluate(db.Model):
    # ここに評価項目を挿入する
    # id=db.Column(db.Integer,primary_key=True)
    # name = db.Column(db.String(80), nullable=False)
    # member = db.Column(db.Integer, nullable=False)
    # age = db.Column(db.Integer, nullable=False)
    # sing = db.Column(db.Integer,nullable=False)
    # fan = db.Column(db.Integer,nullable=False)
    # music_1 = db.Column(db.Integer,nullable=False)
    # music_2 = db.Column(db.Integer,nullable=False)

    # def __repr__(self):
    #     return '<Evaluate {}>'.format(self.name)

# class Sns(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     twitter = db.Column(db.String(80), nullable=False)
#     youtube = db.Column(db.String(80), nullable=False)



    # def __repr__(self):
    #     return '<Sns {}>'.format(self.name)
    
#ここはルートでHTMLを表示するだけです
@app.route('/')
def welcome():
    return render_template('webpage.html')

@app.route('/survey')
def survey():
    return render_template('survey1.html')

@app.route('/webpage')
def webpage():
    return render_template('webpage.html')

@app.route('/result',methods=["GET","POST"])
def result():
    member = request.form.get('member')
    age = request.form.get('age')
    sing = request.form.get('sing')
    fan = request.form.get('fan')
    music_1 = request.form.get('music_1')
    music_2 = request.form.get('music_2')
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

    # if music_2 == '3':
    #     conditions.append("music_2 = ?")
    # elif music_2 == '4':
    #     conditions.append("music_2 = ?")
    # params.append(music_2)

    #ここはエラーチェックです
    #質問が６つあるので長さが6でないとリダイレクトしてもう一度記入してもらうことになります
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
            querySns = "SELECT name, image, twitter, youtube FROM pre_sns WHERE name=?"
            cursorSns = get_cursor()
            cursorSns.execute(querySns,i)
            
            for row in cursorSns.fetchall():
                image_name = row[0]
                image_url = row[1]  # 画像データへのURL
                snsTwitter = row[2]  # SNS
                snsYoutube = row[3]

                sns.append({"name": image_name, "url": image_url, "Twitter": snsTwitter, "Youtube": snsYoutube})
            
        if result is not None:
            return render_template('result.html', results=results,sns=sns)#rate=params,string=query値チェック用
        else:
            return redirect('survey')
    else:
        return redirect('survey')

@app.route('/image/<image_up>',methods=["GET","POST"])
def image(image_up):
    image_data = get_image_data(image_up)
    # 画像データをクライアントに送信
    return send_file(image_data, mimetype='image/jpeg')



if __name__ == '__main__':
    # db.create_all()
    app.run()
