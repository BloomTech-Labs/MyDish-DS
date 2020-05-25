from flask import Flask, jsonify, request

# app
application = Flask(__name__)

# routes
@application.route('/', methods=['GET'])

def ourdummyreturn():
    #dummy_return
    alpha = ['list item1', 'list item2', 'list item3']
    beta = ['list item4', 'list item5', 'list item6']
    dummy_return = {'dummy1': alpha, 'dummy2': beta}

    # return data
    return jsonify(results=dummy_return)

if __name__ == '__main__':
    application.run(port = 5001, debug=True)
