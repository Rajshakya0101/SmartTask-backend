from flask import Flask, request, jsonify
from flask_cors import CORS
import pulp
import logging
import sys
import re
import os

app = Flask(__name__)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins
# Alternatively, restrict to specific origins:
# CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}})

# Configure logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def preprocess_expression(expression):
    """
    Ensure proper formatting of mathematical expressions by adding explicit multiplication.
    Example: Converts '2x + 3y' to '2*x + 3*y'.
    """
    return re.sub(r"(?<=\d)([a-zA-Z])", r"*\1", expression)

@app.route('/solve', methods=['POST'])
def solve_task_scheduler():
    try:
        # Retrieve input data from POST request
        data = request.json
        logger.debug(f"Received data: {data}")

        # Extract problem details
        tasks = data.get('tasks')  # List of task dictionaries
        max_hours = data.get('max_hours')
        labor_capacity = data.get('labor_capacity')
        task_dependencies = data.get('task_dependencies', [])  # List of tuples (i, j)

        # Validate required inputs
        if not tasks or not max_hours or not labor_capacity:
            return jsonify({"error": "Tasks, max_hours, and labor_capacity are required"}), 400

        if not isinstance(tasks, list) or not all(isinstance(task, dict) for task in tasks):
            return jsonify({"error": "Tasks must be a list of task dictionaries"}), 400

        # Validate each task structure
        for task in tasks:
            required_keys = ['name', 'priority', 'time', 'labor']
            if not all(key in task for key in required_keys):
                return jsonify({"error": f"Task {task} is missing required fields: {required_keys}"}), 400
            if not isinstance(task['priority'], (int, float)) or task['priority'] < 0:
                return jsonify({"error": f"Invalid priority for task {task['name']}"}), 400
            if not isinstance(task['time'], (int, float)) or task['time'] <= 0:
                return jsonify({"error": f"Invalid time for task {task['name']}"}), 400
            if not isinstance(task['labor'], (int, float)) or task['labor'] <= 0:
                return jsonify({"error": f"Invalid labor for task {task['name']}"}), 400

        # Create the LP problem
        prob = pulp.LpProblem("Task_Scheduling_Problem", pulp.LpMaximize)

        # Create variables for each task
        task_vars = {}
        for task in tasks:
            task_name = task['name']
            partial_allowed = task.get('partial_allowed', False)

            # Create binary or continuous variable based on partial_allowed
            if partial_allowed:
                task_vars[task_name] = pulp.LpVariable(task_name, 0, 1)  # Continuous variable [0, 1]
            else:
                task_vars[task_name] = pulp.LpVariable(task_name, 0, 1, cat='Binary')  # Binary variable {0, 1}

        # Objective function: Maximize total priority
        prob += pulp.lpSum(task['priority'] * task_vars[task['name']] for task in tasks), "Total_Priority"

        # Time constraint: Total time of selected tasks should not exceed max_hours
        prob += pulp.lpSum(task['time'] * task_vars[task['name']] for task in tasks) <= max_hours, "Total_Time"

        # Labor constraint: Total labor of selected tasks should not exceed labor_capacity
        prob += pulp.lpSum(task['labor'] * task_vars[task['name']] for task in tasks) <= labor_capacity, "Total_Labor"

        # Task dependency constraints: Ensure task dependencies are respected
        for i, j in task_dependencies:
            if i in task_vars and j in task_vars:
                prob += task_vars[i] <= task_vars[j], f"Task_Dependency_{i}to{j}"
            else:
                return jsonify({"error": f"Invalid dependency: {i} or {j} not found in tasks"}), 400

        # Deadline constraints for tasks with deadlines
        for task in tasks:
            if 'deadline' in task and task['deadline'] is not None:
                prob += task['time'] * task_vars[task['name']] <= task['deadline'], f"Deadline_{task['name']}"

        logger.debug("Objective function and constraints added successfully.")

        # Solve the problem
        prob.solve()

        # Check if the problem is solved successfully
        if prob.status == -1:  # Problem not solved or infeasible
            return jsonify({"error": "Optimization problem is infeasible. Check constraints or input data."}), 400

        # Prepare the response
        status = pulp.LpStatus[prob.status]
        results = {var: task_vars[var].varValue for var in task_vars}
        response = {
            "status": status,
            "results": results,
            "objective_value": pulp.value(prob.objective)
        }

        logger.debug(f"Response prepared: {response}")
        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}")
        return jsonify({"error": str(e)}), 400



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

