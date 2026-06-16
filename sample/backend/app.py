"""
喔壳 Skills Demo - 后端 API
订单管理 + Todo 待办清单
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)  # 允许跨域

# 数据存储文件
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

ORDERS_FILE = os.path.join(DATA_DIR, 'orders.json')
TODOS_FILE = os.path.join(DATA_DIR, 'todos.json')

# 初始化数据
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ============== 订单管理 API ==============

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """获取订单列表"""
    orders = load_data(ORDERS_FILE)

    # 支持搜索和筛选
    search = request.args.get('search', '')
    status = request.args.get('status', '')

    filtered_orders = orders
    if search:
        filtered_orders = [o for o in filtered_orders
                          if search.lower() in o.get('orderNo', '').lower()
                          or search.lower() in o.get('customerName', '').lower()
                          or search.lower() in o.get('productName', '').lower()]

    if status:
        filtered_orders = [o for o in filtered_orders if o.get('status') == status]

    return jsonify({
        'code': 200,
        'data': filtered_orders,
        'total': len(filtered_orders)
    })

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """获取单个订单"""
    orders = load_data(ORDERS_FILE)
    order = next((o for o in orders if o['id'] == order_id), None)

    if not order:
        return jsonify({'code': 404, 'msg': '订单不存在'}), 404

    return jsonify({'code': 200, 'data': order})

@app.route('/api/orders', methods=['POST'])
def create_order():
    """创建订单"""
    orders = load_data(ORDERS_FILE)
    data = request.json

    # 生成订单 ID
    new_id = max([o['id'] for o in orders], default=0) + 1

    new_order = {
        'id': new_id,
        'orderNo': data.get('orderNo', f'ORD{datetime.now().strftime("%Y%m%d%H%M%S")}'),
        'customerName': data.get('customerName', ''),
        'customerPhone': data.get('customerPhone', ''),
        'productName': data.get('productName', ''),
        'quantity': data.get('quantity', 1),
        'unitPrice': data.get('unitPrice', 0),
        'totalPrice': data.get('totalPrice', 0),
        'status': data.get('status', 'pending'),
        'paymentMethod': data.get('paymentMethod', ''),
        'deliveryAddress': data.get('deliveryAddress', ''),
        'deliveryDate': data.get('deliveryDate', ''),
        'remarks': data.get('remarks', ''),
        'createTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'updateTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    orders.append(new_order)
    save_data(ORDERS_FILE, orders)

    return jsonify({'code': 200, 'msg': '创建成功', 'data': new_order})

@app.route('/api/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """更新订单"""
    orders = load_data(ORDERS_FILE)
    data = request.json

    order_idx = next((i for i, o in enumerate(orders) if o['id'] == order_id), None)
    if order_idx is None:
        return jsonify({'code': 404, 'msg': '订单不存在'}), 404

    # 更新字段
    order = orders[order_idx]
    for key in ['customerName', 'customerPhone', 'productName', 'quantity',
                'unitPrice', 'totalPrice', 'status', 'paymentMethod',
                'deliveryAddress', 'deliveryDate', 'remarks']:
        if key in data:
            order[key] = data[key]

    order['updateTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    orders[order_idx] = order
    save_data(ORDERS_FILE, orders)

    return jsonify({'code': 200, 'msg': '更新成功', 'data': order})

@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """删除订单"""
    orders = load_data(ORDERS_FILE)

    orders = [o for o in orders if o['id'] != order_id]
    save_data(ORDERS_FILE, orders)

    return jsonify({'code': 200, 'msg': '删除成功'})

@app.route('/api/orders/stats', methods=['GET'])
def get_order_stats():
    """获取订单统计"""
    orders = load_data(ORDERS_FILE)

    stats = {
        'total': len(orders),
        'pending': len([o for o in orders if o['status'] == 'pending']),
        'processing': len([o for o in orders if o['status'] == 'processing']),
        'completed': len([o for o in orders if o['status'] == 'completed']),
        'cancelled': len([o for o in orders if o['status'] == 'cancelled']),
        'totalAmount': sum([o.get('totalPrice', 0) for o in orders]),
    }

    return jsonify({'code': 200, 'data': stats})

# ============== Todo 待办清单 API ==============

@app.route('/api/todos', methods=['GET'])
def get_todos():
    """获取待办列表"""
    todos = load_data(TODOS_FILE)

    # 支持筛选
    status = request.args.get('status', '')  # all, active, completed
    priority = request.args.get('priority', '')

    filtered_todos = todos

    if status == 'active':
        filtered_todos = [t for t in filtered_todos if not t.get('completed')]
    elif status == 'completed':
        filtered_todos = [t for t in filtered_todos if t.get('completed')]

    if priority:
        filtered_todos = [t for t in filtered_todos if t.get('priority') == priority]

    return jsonify({
        'code': 200,
        'data': filtered_todos,
        'total': len(filtered_todos)
    })

@app.route('/api/todos', methods=['POST'])
def create_todo():
    """创建待办"""
    todos = load_data(TODOS_FILE)
    data = request.json

    new_id = max([t['id'] for t in todos], default=0) + 1

    new_todo = {
        'id': new_id,
        'title': data.get('title', ''),
        'description': data.get('description', ''),
        'priority': data.get('priority', 'medium'),  # low, medium, high, urgent
        'completed': False,
        'dueDate': data.get('dueDate', ''),
        'tags': data.get('tags', []),
        'createTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'updateTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'completedTime': None
    }

    todos.append(new_todo)
    save_data(TODOS_FILE, todos)

    return jsonify({'code': 200, 'msg': '创建成功', 'data': new_todo})

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """更新待办"""
    todos = load_data(TODOS_FILE)
    data = request.json

    todo_idx = next((i for i, t in enumerate(todos) if t['id'] == todo_id), None)
    if todo_idx is None:
        return jsonify({'code': 404, 'msg': '待办不存在'}), 404

    todo = todos[todo_idx]
    for key in ['title', 'description', 'priority', 'completed', 'dueDate', 'tags']:
        if key in data:
            todo[key] = data[key]

    # 如果标记为完成，记录完成时间
    if data.get('completed') and not todo.get('completedTime'):
        todo['completedTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    elif not data.get('completed'):
        todo['completedTime'] = None

    todo['updateTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    todos[todo_idx] = todo
    save_data(TODOS_FILE, todos)

    return jsonify({'code': 200, 'msg': '更新成功', 'data': todo})

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """删除待办"""
    todos = load_data(TODOS_FILE)

    todos = [t for t in todos if t['id'] != todo_id]
    save_data(TODOS_FILE, todos)

    return jsonify({'code': 200, 'msg': '删除成功'})

@app.route('/api/todos/<int:todo_id>/toggle', methods=['POST'])
def toggle_todo(todo_id):
    """切换待办完成状态"""
    todos = load_data(TODOS_FILE)

    todo_idx = next((i for i, t in enumerate(todos) if t['id'] == todo_id), None)
    if todo_idx is None:
        return jsonify({'code': 404, 'msg': '待办不存在'}), 404

    todo = todos[todo_idx]
    todo['completed'] = not todo.get('completed', False)

    if todo['completed']:
        todo['completedTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        todo['completedTime'] = None

    todo['updateTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    todos[todo_idx] = todo
    save_data(TODOS_FILE, todos)

    return jsonify({'code': 200, 'msg': '更新成功', 'data': todo})

@app.route('/api/todos/stats', methods=['GET'])
def get_todo_stats():
    """获取待办统计"""
    todos = load_data(TODOS_FILE)

    stats = {
        'total': len(todos),
        'active': len([t for t in todos if not t.get('completed')]),
        'completed': len([t for t in todos if t.get('completed')]),
        'urgent': len([t for t in todos if t.get('priority') == 'urgent' and not t.get('completed')]),
        'high': len([t for t in todos if t.get('priority') == 'high' and not t.get('completed')]),
        'overdue': len([t for t in todos
                       if t.get('dueDate')
                       and t.get('dueDate') < datetime.now().strftime('%Y-%m-%d')
                       and not t.get('completed')])
    }

    return jsonify({'code': 200, 'data': stats})

# ============== 健康检查 ==============

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'code': 200,
        'msg': 'OK',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    print("="*60)
    print("WoKe Skills Demo - Backend Service Started")
    print("="*60)
    print("API Address: http://localhost:5000")
    print("Orders API: /api/orders")
    print("Todos API: /api/todos")
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5000)
