from flask import Flask, request, jsonify, render_template,redirect
from flask_sqlalchemy import SQLAlchemy
import sqlite3

#flaskを使うためのおまじないです
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////Users/ikenoshuri/システム主専攻実習_推し/example.db'
db=SQLAlchemy(app)

#SQLite３を使うためのおまじないです
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

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
#     instagram = db.Column(db.String(80), nullable=False)
#     youtube = db.Column(db.String(80), nullable=False)



    def __repr__(self):
        return '<Sns {}>'.format(self.name)
    
#ここはルートでHTMLを表示するだけです
@app.route('/')
def welcome_webpage():
    return render_template('webpage.html')

@app.route('/survey.html')
def welcome_survey():
    return render_template('survey.html')

@app.route('/webpage.html')
def again_webpage():
    return render_template('webpage.html')

@app.route('/survey.html',methods= ["POST"])
def survey_process():
    # user_rate = [int(rate) for rate in request.form.getlist('rate')]
    
    # ここで値をHTMLから受け取りたいです
    # 引数はHTMLサイドと同じ名前にしないといけないので揃えてください（どちらに揃えても大丈夫です）
    
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
    params.append(member)

    if age == '多い':
        conditions.append("age >= ?")
    elif age == '少ない':
        conditions.append("age < ?")
    params.append(age)

    if sing == '多い':
        conditions.append("sing >= ?")
    elif sing == '少ない':
        conditions.append("sing < ?")
    params.append(sing)

    if fan == '多い':
        conditions.append("fan >= ?")
    elif fan == '少ない':
        conditions.append("fan < ?")
    params.append(fan)

    if music_1 == '多い':
        conditions.append("music_1 >= ?")
    elif music_1 == '少ない':
        conditions.append("music_1 < ?")
    params.append(music_1)

    if music_2 == '多い':
        conditions.append("music_2 >= ?")
    elif music_2 == '少ない':
        conditions.append("music_2 < ?")
    params.append(music_2)

    #ここはエラーチェックです
    #質問が６つあるので長さが6でないとリダイレクトしてもう一度記入して絵もらうことになります
    if len(conditions)==6 and len(params)==6:
        return render_template('/result.html',conditions=conditions,params=params)
    else:
        #もう一度やり直してくださいという表記が欲しい
        return redirect('/survey.html')
    

@app.route('/result.html',methods=["GET","POST"])
def get_items():
    #surveyから送られたリストを受け取る
    rates=tuple(request.args.get('conditions'))
    #HTMLに送るための結果のリスト
    results=[]
    if rates:
        #データベースにアクセスして、取得する
        query="SELECT * FROM evaluate WHERE " + " AND ".join(rates) 
        cursor.execute(query, (rates))
        results = cursor.fetchall()

        return render_template('result.html', results=results)
    else:
        return redirect('/survey.html')
if __name__ == '__main__':
    # db.create_all()
    app.run()

