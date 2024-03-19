from flask import Flask, jsonify, request, make_response
import pymysql
from flask_cors import CORS, cross_origin
from asgiref.wsgi import WsgiToAsgi

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
asgi_app = WsgiToAsgi(app)

db_config = {
    'host': 'umng-experiment.database.windows.net',
    'user': 'JuanChurio',
    'password': 'UmngExperimento4$',
    'db': 'datos-experimentos',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    connection = pymysql.connect(**db_config)
    return connection


@app.route('/insertRows', methods=['POST', 'OPTIONS'])

def insertRows():


    try:
        connect = get_db_connection()
        return jsonify({"status": "success", "message": "Row inserted successfully"})
    except:
        return jsonify({"status": "failure", "message": "connexion failed"})
    # if  request.method == 'POST':
    #     data = request.json
        
    #     connection = get_db_connection()
    #     try:
    #         with connection.cursor() as cursor:
    #             sql = '''
    #                 INSERT INTO DatosExperimento (CONDITION_A, CONDITION_B, GRAPH, timeTaken, Error, controlCondition, timePer)
    #                 VALUES (%s, %s, %s, %s, %s, %s, %s)
    #             '''
    #             cursor.execute(sql, (data['CONDITION_A'], data['CONDITION_B'], data['GRAPH'], data['timeTaken'], data['Error'], data['controlCondition'], data['timePer']))
    #         connection.commit()
    #     finally:
    #         connection.close()
    #     return jsonify({"status": "success", "message": "Row inserted successfully"})
    # return jsonify({"status": "success", "message": "wtf"})

@app.route('/testdb')
def test_db():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')  # Simple query to test the connection
            result = cursor.fetchone()
            return jsonify(result), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        connection.close()

@app.route("/")
def helloWorld():
    return "Hello, cross-origin-world!"

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(asgi_app, host='0.0.0.0', port=8000)
