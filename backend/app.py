from flask import Flask, jsonify, request, g
from flask_cors import CORS
from threading import Lock, local
from db_config import get_db_connection
import functools

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 初始化数据存储
preset_projects = ["项目A", "项目B", "项目C"]
results_lock = Lock()

# 线程本地存储
thread_local = local()

def get_thread_db():
    if not hasattr(thread_local, 'conn'):
        thread_local.conn = get_db_connection()
    return thread_local.conn

def close_thread_db(e=None):
    conn = getattr(thread_local, 'conn', None)
    if conn is not None:
        conn.close()

app.teardown_appcontext(close_thread_db)

def create_test_configs_table():
    conn = get_thread_db()
    try:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS test_configs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_path TEXT NOT NULL,
                dataset_path TEXT NOT NULL,
                project TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
    finally:
        cur.close()

# 创建表
create_test_configs_table()

@app.route('/api/projects', methods=['GET'])
def get_projects():
    return jsonify({"projects": preset_projects})

@app.route('/api/submit', methods=['POST'])
def submit_test():
    data = request.json
    required_fields = ['model_path', 'dataset_path', 'project']
    
    # 检查字段是否存在且不为空
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"error": "所有字段不能为空"}), 400
    
    conn = get_thread_db()
    cur = conn.cursor()
    try:
        cur.execute('''
            INSERT INTO test_configs (model_path, dataset_path, project)
            VALUES (?, ?, ?)
        ''', (data['model_path'], data['dataset_path'], data['project']))
        config_id = cur.lastrowid
        conn.commit()
        return jsonify({"status": "提交成功", "config_id": config_id}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()

@app.route('/api/configs', methods=['GET'])
def get_configs():
    conn = get_thread_db()
    cur = conn.cursor()
    try:
        cur.execute('SELECT id, model_path, dataset_path, project, created_at FROM test_configs ORDER BY created_at DESC')
        configs = cur.fetchall()
        return jsonify({
            "configs": [{
                "id": row[0],
                "model_path": row[1],
                "dataset_path": row[2],
                "project": row[3],
                "created_at": row[4]
            } for row in configs]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()

@app.route('/api/configs/<int:config_id>', methods=['DELETE'])
def delete_config(config_id):
    conn = get_thread_db()
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM test_configs WHERE id = ?', (config_id,))
        conn.commit()
        if cur.rowcount == 0:
            return jsonify({"error": "配置不存在"}), 404
        return jsonify({"status": "删除成功"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()

@app.route('/api/configs/<int:config_id>/run', methods=['POST'])
def run_config(config_id):
    # 这里只返回配置信息，具体执行逻辑由用户实现
    conn = get_thread_db()
    cur = conn.cursor()
    try:
        cur.execute('SELECT model_path, dataset_path, project FROM test_configs WHERE id = ?', (config_id,))
        config = cur.fetchone()
        if not config:
            return jsonify({"error": "配置不存在"}), 404
        
        
        return jsonify({
            "status": "执行请求已接收",
            "config": {
                "model_path": config[0],
                "dataset_path": config[1],
                "project": config[2]
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
