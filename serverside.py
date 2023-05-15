from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit_survey():
    # フォームデータの受け取り
    q1 = request.form.get('q1')
    q2 = request.form.get('q2')
    q3 = request.form.get('q3')

    # データベースへの保存や処理など、必要な処理を実行する

    # レスポンスの生成
    response = {'message': 'アンケートが送信されました'}
    return jsonify(response)

if __name__ == '__main__':
    app.run()
