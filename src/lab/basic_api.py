from flask import Flask, request, jsonify
app = Flask(__name__)

resource = [] #서버 리소스
@app.route('/')
def hello():
    return 'Hello Flask'

@app.route('/info/<name>') # 타입을 명시하지 않는 경우 str
def get_name(name):
    return "hello {}".format(name)

@app.route('/user/<int:user_id>', methods = ['GET']) # id는 정수형 타입
def get_user(user_id):
    for user in resource :
        if user['user_id'] is user_id :
            return jsonify(user)

    return jsonify(None)

@app.route('/json/<int:dest_id>/<message>')
@app.route('/JSON/<int:dest_id>/<message>')
def send_message(dest_id, message):
    json = {
        "bot_id" : dest_id,
        "message" : message
    }
    return json

if __name__ == '__main__' :
    app.run()