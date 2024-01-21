from flask import Flask, request, jsonify
from transformers import pipeline
import mysql.connector
import logging

app = Flask(__name__)
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-de")

DB_HOST = 'mysql'
DB_USER = 'chandan'
DB_PASSWORD = 'password'
DB_DATABASE = 'InternAssignment'

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )

def execute_query(query, params=None):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return result

create_table_query = '''
CREATE TABLE IF NOT EXISTS translation_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id TEXT NOT NULL,
    original_text TEXT NOT NULL,
    translated_text TEXT NOT NULL
);
'''
drop_table_query = '''
DROP TABLE IF EXISTS translation_history;
'''
# execute_query(drop_table_query)
execute_query(create_table_query)

@app.route('/translate', methods=['POST'])
def translate_text():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        text_to_translate = data.get('text')

        if username == 'example' and password == 'password':
            translated_text = translator(text_to_translate)[0]['translation_text']

            insert_query = '''
            INSERT INTO translation_history (user_id, original_text, translated_text)
            VALUES (%s, %s, %s);
            '''
            execute_query(insert_query, (username, text_to_translate, translated_text))

            return jsonify({'translated_text': translated_text})
        else:
            return jsonify({'error': 'Invalid credentials'})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/history/<username>', methods=['GET'])
def get_history(username):
    try:
        password = request.args.get('password')
        logging.info(f"Received history request for user: {username}, password: {password}")


        if username == 'example' and password == 'password':
            user_id_query = '''
            SELECT id FROM translation_history
            WHERE user_id = %s;
            '''
            history_query = '''
            SELECT original_text, translated_text FROM translation_history
            WHERE user_id = %s;
            '''
            user_history = execute_query(history_query, (username,))

            return jsonify({'translation_history': user_history})
        else:
            return jsonify({'error': 'Invalid credentials'})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
