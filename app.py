import json

from flask import Flask, request, jsonify

from epubw.auto_machine import *

app = Flask(__name__)


@app.route('/')
def hello_world(name=None):
    return "hello"


@app.route('/search')
def search():
    name = request.args.get('name')
    rs = read_books_url_and_code(name)
    column_list = ['书名', '作者', '出版日期', '出版社', '网盘地址', '提取码']
    l = []
    if len(rs) > 0:
        for ri in rs:
            l.append({column_list[0]: ri[3], column_list[1]: ri[4], column_list[2]: ri[5],
                      column_list[3]: ri[6], column_list[4]: ri[1], column_list[5]: ri[2]})
    # rst = make_response(str(l))
    # rst.headers['Content-Type'] = 'application/json'
    # return Response(json.dumps(str(l)), mimetype='application/json')
    return jsonify(l)


@app.route('/save', methods=['POST'])
def save():
    data = json.loads(request.get_data())
    auto_extract_file(data['url'], data['code'])
    return "ok"


if __name__ == '__main__':
    app.run()
