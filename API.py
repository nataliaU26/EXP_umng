from flask import Flask, jsonify, request
import pymysql
from flask_cors import CORS
import logging
from asgiref.wsgi import WsgiToAsgi

app = Flask(__name__)
#CORS(app, resources={r"/login": {"origins": "http://localhost:3000"}}, supports_credentials=True)
CORS(app, supports_credentials=True)
asgi_app = WsgiToAsgi(app)
db_config = {
    'host': 'mentordb.mysql.database.azure.com',
    'user': 'mentordbuser',
    'password': 'm3nt0r2024%',
    'db': 'mentordb1',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
    'ssl': {'ca': 'DigiCertGlobalRootCA.crt.pem'}
}


@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"Error interno,por favor intente más tarde: {str(e)}") 
    return jsonify(error="Ocurrió un error interno, por favor intente más tarde."), 500


                            #---Dashboard components

#Home display        
@app.route('/')
def home():
    return 'MentorIA statistics DEPLOY'

#Primary filter Usertype and companyId
def get_user_company_id_if_admin(id):
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            query = """
                SELECT company_id, type_id 
                FROM users 
                WHERE id = %s;
            """
            cursor.execute(query, (id,))
            user_info = cursor.fetchone()
            
            if user_info and user_info['type_id'] == 3:
                return user_info['company_id']
            else:
                return None
            
    except Exception as e:
        print(f"Error al obtener la información del usuario: {e}")
        return None
    finally:
        connection.close()

def get_messages_by_company_id(company_id):
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            query = """
                SELECT 
                u.id AS user_id,
                u.name AS username,
                DATE(m.timestamp) AS date,
                COUNT(m.id) AS message_count
                FROM messages m
                INNER JOIN users u ON m.user_id = u.id
                WHERE u.company_id = %s
                GROUP BY user_id, date
                ORDER BY date ASC, username ASC;
            """
            cursor.execute(query, (company_id,))
            result = cursor.fetchall() 
            
            if result:
                return jsonify(result), 200
            else:
                return jsonify({"message": "No messages found for this company"}), 404
        
    except Exception as e:
        print(f"Error al obtener los mensajes: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        connection.close()
        
#Endpoint-messages by day per company
@app.route('/messagesuserbyday/<int:id>', methods=['GET'])
def messagesuserbyday(id):
    company_id = get_user_company_id_if_admin(id)
    if company_id is None:
        return jsonify({"message": "User not found or not admin"}), 404
    return get_messages_by_company_id(company_id)



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(asgi_app, host='0.0.0.0', port=8000)

"""if __name__ == '__main__':
    app.run(debug=True)"""

""""""