from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello Flask'

@app.route('/info/<name>') # 타입을 명시하지 않는 경우 str
def get_name(name):
    return "hello {}".format(name)

@app.route('/user/<int:id>') # id는 정수형 타입
def get_user(id):
    return "user id is {}".format(id)

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