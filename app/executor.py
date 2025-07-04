import subprocess
import tempfile
import json
import os

NSJAIL_PATH = "/usr/local/bin/nsjail"
JAIL_CFG_PATH = os.path.join(os.path.dirname(__file__), "jail_config.cfg")

def run_script_safely(script_code):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as temp_file:
        temp_file.write(script_code)
        temp_file_path = temp_file.name

    try:
        result = subprocess.run([
            NSJAIL_PATH,
            "--config", JAIL_CFG_PATH,
            "--",
            "python3",
            temp_file_path
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=5,
        text=True)

        stdout = result.stdout
        stderr = result.stderr

        if result.returncode != 0:
            raise RuntimeError(stderr)

        # The script must output a JSON object from main()
        lines = stdout.strip().splitlines()
        last_line = lines[-1] if lines else ""
        try:
            output = json.loads(last_line)
        except json.JSONDecodeError:
            raise ValueError("main() did not return a valid JSON object")

        return output, stdout
    finally:
        os.remove(temp_file_path)
