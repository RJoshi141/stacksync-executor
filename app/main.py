from flask import Flask, request, jsonify
from executor import run_script_safely

app = Flask(__name__)

@app.route("/execute", methods=["POST"])
def execute_script():
    data = request.get_json()

    # Validate input
    if not data or "script" not in data:
        return jsonify({"error": "Missing 'script' in request body"}), 400

    script = data["script"]

    try:
        result, stdout = run_script_safely(script)
        return jsonify({
            "result": result,
            "stdout": stdout
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
