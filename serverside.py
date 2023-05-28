from flask import Flask, request, jsonify, render_template,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////Users/ikenoshuri/システム主専攻実習_推し/example.db'
db=SQLAlchemy(app)

class Evaluate(db.Model):
    # ここに評価項目を挿入する
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return '<Evaluate {}>'.format(self.name)
    

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
    user_rating = int(request.form.get('data-rating'))  # ユーザーからの評価を取得します
    if user_rating is not None:
        return redirect('/result.html?user_rating={}'.format(user_rating))
    else:
        return redirect('/survey.html')

@app.route('/result.html',methods=["GET","POST"])
def get_items():
    user_rating = request.args.get('user_rating')
    if user_rating is not None:
        user_rating = int(user_rating)
        items = Evaluate.query.filter(Evaluate.age >= user_rating).all()
        results = []
        for item in items:
            results.append({'name': item.name, 'age': item.age})
        return render_template('result.html', results=results)
    else:
        return redirect('/survey.html')
if __name__ == '__main__':
    # db.create_all()
    app.run()

