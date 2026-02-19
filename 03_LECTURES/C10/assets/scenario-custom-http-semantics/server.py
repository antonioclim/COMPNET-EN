from __future__ import annotations

import threading
import time
import uuid
from typing import Dict, Any

from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

jobs: Dict[str, Dict[str, Any]] = {}

def worker(job_id: str, payload: Dict[str, Any]):
    jobs[job_id]["status"] = "running"
    jobs[job_id]["progress"] = 0

    try:
        # Simulated long task: "process" N items
        n = int(payload.get("n", 10))
        total = max(n, 1)

        acc = 0
        for i in range(total):
            time.sleep(0.2)
            acc += (i + 1)
            jobs[job_id]["progress"] = int(((i + 1) / total) * 100)

        jobs[job_id]["result"] = {
            "operation": "sum_1_to_n",
            "n": total,
            "value": acc,
        }
        jobs[job_id]["status"] = "done"
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)

@app.post("/jobs")
def create_job():
    payload = request.get_json(silent=True) or {}
    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "id": job_id,
        "status": "pending",
        "progress": 0,
        "created_at": time.time(),
    }

    t = threading.Thread(target=worker, args=(job_id, payload), daemon=True)
    t.start()

    resp = make_response(jsonify({
        "id": job_id,
        "status": "accepted",
    }), 202)
    resp.headers["Location"] = f"/jobs/{job_id}"
    return resp

@app.get("/jobs/<job_id>")
def get_job(job_id: str):
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "job not found"}), 404

    return jsonify({
        "id": job["id"],
        "status": job["status"],
        "progress": job.get("progress", 0),
        "links": {
            "self": f"/jobs/{job_id}",
            "result": f"/jobs/{job_id}/result",
        }
    }), 200

@app.get("/jobs/<job_id>/result")
def get_result(job_id: str):
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "job not found"}), 404

    if job["status"] != "done":
        return jsonify({
            "error": "result not ready",
            "status": job["status"],
        }), 409

    return jsonify(job["result"]), 200

if __name__ == "__main__":
    app.run(port=7000, debug=True)
