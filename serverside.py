from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLACHEMY_DATABASE_URI']='sqlite:///oshi.db'
db=SQLAlchemy(app)

class Evaluate(db.Model):
    # ここに評価項目を挿入する
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return '<Item {}>'.format(self.name)
    

@app.route('/')
def welcome_webpage():
    return render_template('webpage.html')


# @app.route('/submit', methods=['GET'])
# def submit_survey():
#     # フォームデータの受け取り
#     q1 = request.form.get('q1')
#     q2 = request.form.get('q2')
#     q3 = request.form.get('q3')

#     # データベースへの保存や処理など、必要な処理を実行する

#     # レスポンスの生成
#     response = {'message': 'アンケートが送信されました'}
#     return jsonify(response)


@app.route('/items', methods=['POST'])
def get_items():
    user_rating = float(request.form['rating'])  # ユーザーからの評価を取得します
    items = Item.query.filter(Item.rating >= user_rating).all()  # 評価がユーザーの評価以上の項目のみを取得します
    result = []
    for item in items:
        result.append({'name': item.name, 'rating': item.rating})
    return {'items': result}

if __name__ == '__main__':
    app.run()
