from flask import Flask, jsonify, abort, make_response, request
from TsqlParser import Parser


def create_app():
    app = Flask(__name__)
    req = 'SELECT c1,c2 FROM tab1'
    p = Parser(input_data=req, type=2)
    requests = [
        {
            'id': 1,
            'request': req,
            'string': p.to_string(),
            'correct': p.status,
            'json': p.to_json(),
            'time': p.get_time()[5:],
            'tokens': p.tokens()

     }
    ]

    @app.route('/', methods=['GET'])
    def server_is_working():
        return "Server is working", 200

    @app.route('/tasks', methods=['GET'])
    def get_tasks():
        return jsonify({'info request': requests}), 200

    @app.route('/tasks/<int:task_id>', methods=['GET'])
    def get_task(task_id):
        req = filter(lambda t: t['id'] == task_id, requests)
        list_task = list(req)
        if len(list_task) == 0:
            abort(404)
        return jsonify(list_task[0])

    @app.route('/tasks/<int:task_id>/<string:task_param>', methods=['GET'])
    def get_task_param(task_id, task_param):
        req = filter(lambda t: t['id'] == task_id, requests)
        list_task = list(req)
        if len(list_task) == 0:
            abort(404)
        try:
            list_task[0][task_param]
        except KeyError:
            abort(404)
        return jsonify(list_task[0][task_param])

    @app.route('/tasks', methods=['POST'])
    def create_task():
        if not request.json or not 'request' in request.json:
            abort(400)
        p = Parser(input_data=request.json['request'], type=2)
        if p.status is True:
            task = {
                'id': requests[-1]['id'] + 1,
                'request': request.json['request'],
                'string': p.to_string(),
                'correct': p.status,
                'json': p.to_json(),
                'time': p.get_time()[5:],
                'tokens': p.tokens()
            }
        else:
            task = {
                'id': requests[-1]['id'] + 1,
                'request': request.json['request'],
                'string': None,
                'correct': p.status,
                'json': None,
                'time': None,
                'tokens': None
            }
        requests.append(task)
        return jsonify({'task': task}), 201

    @app.route('/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        task = filter(lambda t: t['id'] == task_id, requests)
        list_task = list(task)
        if len(list_task) == 0:
            abort(404)
        requests.remove(list_task[0])
        return jsonify({'result': True})

    @app.route('/tasks/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        task = filter(lambda t: t['id'] == task_id, requests)
        list_task = list(task)
        if len(list_task) == 0:
            abort(404)
        if not request.json or not 'request' in request.json:
            abort(400)
        p = Parser(input_data=request.json['request'], type=2)
        if p.status is True:
            list_task[0]['request'] = request.json['request']
            list_task[0]['string'] = p.to_string()
            list_task[0]['correct'] = p.status
            list_task[0]['json'] = p.to_json()
            list_task[0]['time'] = p.get_time()[5:]
            list_task[0]['tokens'] = p.tokens()
        else:
            list_task[0]['request'] = request.json['request']
            list_task[0]['string'] = None
            list_task[0]['correct'] = False
            list_task[0]['json'] = None
            list_task[0]['time'] = None
            list_task[0]['tokens'] = None
        return jsonify({'task': list_task[0]})

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
