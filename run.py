# -*- coding: utf-8 -*-
# @Author   : Weizhou
# @Email    : 491315091@qq.com
import os
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS, cross_origin  # 导入包

app = Flask(__name__)
CORS(app, resources=r'/*')


@app.route('/build', methods=['GET'])
def build():
    # filename = request.args.get('filename')
    # path = '/'.join(filename.split('/')[3:])
    # path = '../'+path
    # print(path)
    path = 'api.yml'
    cmd="swagger_py_codegen -s %s  example-app-ui -p demo-ui --ui --spec"%path
    os.system(cmd)
    print('python api打包成功')
    d = {'status':'Flask Api生成成功'}
    response = make_response(jsonify(d))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


app.run(port=5000, debug=True)