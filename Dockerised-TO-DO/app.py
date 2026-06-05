"""
Production-grade To-Do API with comprehensive CRUD operations.
"""

from flask import Flask, request, jsonify
from datetime import datetime
from functools import wraps
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# In-memory data store (replace with database for production)
todos = {}
todo_counter = 0

# Health check endpoint
@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint for container orchestration."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "todo-api",
        "version": os.getenv("API_VERSION", "1.0.0")
    }), 200

# GET all todos with pagination
@app.route("/todos", methods=["GET"])
def get_todos():
    """Retrieve all todos with optional pagination."""
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    todos_list = list(todos.values())
    start = (page - 1) * limit
    end = start + limit
    
    logger.info(f"Fetched todos - page: {page}, limit: {limit}, total: {len(todos_list)}")
    
    return jsonify({
        "data": todos_list[start:end],
        "total": len(todos_list),
        "page": page,
        "limit": limit
    }), 200

# GET single todo by ID
@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    """Retrieve a specific todo by ID."""
    if todo_id not in todos:
        logger.warning(f"Todo not found - ID: {todo_id}")
        return jsonify({"error": "Todo not found"}), 404
    
    return jsonify(todos[todo_id]), 200

# CREATE new todo
@app.route("/todos", methods=["POST"])
def create_todo():
    """Create a new todo item."""
    global todo_counter
    
    data = request.get_json()
    
    if not data or "task" not in data:
        logger.warning("Invalid todo creation request - missing task field")
        return jsonify({"error": "Missing 'task' field"}), 400
    
    if not data["task"].strip():
        logger.warning("Invalid todo creation request - empty task")
        return jsonify({"error": "Task cannot be empty"}), 400
    
    todo_counter += 1
    todo = {
        "id": todo_counter,
        "task": data["task"].strip(),
        "completed": data.get("completed", False),
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    
    todos[todo_counter] = todo
    logger.info(f"Todo created - ID: {todo_counter}, task: {todo['task'][:50]}")
    
    return jsonify(todo), 201

# UPDATE todo
@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    """Update an existing todo item."""
    if todo_id not in todos:
        logger.warning(f"Update failed - Todo not found, ID: {todo_id}")
        return jsonify({"error": "Todo not found"}), 404
    
    data = request.get_json()
    
    if "task" in data:
        if not data["task"].strip():
            logger.warning(f"Update failed - Empty task, ID: {todo_id}")
            return jsonify({"error": "Task cannot be empty"}), 400
        todos[todo_id]["task"] = data["task"].strip()
    
    if "completed" in data:
        todos[todo_id]["completed"] = bool(data["completed"])
    
    todos[todo_id]["updated_at"] = datetime.utcnow().isoformat()
    
    logger.info(f"Todo updated - ID: {todo_id}")
    return jsonify(todos[todo_id]), 200

# DELETE todo
@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    """Delete a todo item."""
    if todo_id not in todos:
        logger.warning(f"Delete failed - Todo not found, ID: {todo_id}")
        return jsonify({"error": "Todo not found"}), 404
    
    deleted = todos.pop(todo_id)
    logger.info(f"Todo deleted - ID: {todo_id}, task: {deleted['task'][:50]}")
    
    return jsonify({"message": "Todo deleted successfully", "id": todo_id}), 200

# DELETE all todos
@app.route("/todos", methods=["DELETE"])
def delete_all_todos():
    """Delete all todo items."""
    global todos
    count = len(todos)
    todos.clear()
    logger.info(f"All todos deleted - count: {count}")
    return jsonify({"message": f"Deleted {count} todos"}), 200

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
