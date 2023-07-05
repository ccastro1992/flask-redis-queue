# project/server/main/views.py

import redis
from rq import Queue, Connection
from flask import render_template, Blueprint, jsonify, request, current_app
from project.server.main.tasks import create_task

from redis import Redis
from rq import Queue
from rq.job import Job
from rq import Connection, Worker

main_blueprint = Blueprint("main", __name__,)


@main_blueprint.route("/", methods=["GET"])
def home():
    return render_template("main/home.html")


@main_blueprint.route("/tasks", methods=["POST"])
def run_task():
    task_type = request.form["type"]
    with Connection(redis.from_url(current_app.config["REDIS_URL"])):
        q = Queue()
        task = q.enqueue(create_task, task_type)
    response_object = {
        "status": "success",
        "data": {
            "task_id": task.get_id()
        }
    }
    return jsonify(response_object), 202


@main_blueprint.route("/tasks_failed", methods=["GET"])
def tasks_failed():
    response_object = {}

    redis_url = "redis://localhost:6379/0"
    redis_connection = redis.from_url(redis_url)
    with Connection(redis_connection):
        queue = Queue()
        registry = queue.failed_job_registry

        failed_ids = []
        for job_id in registry.get_job_ids():
            failed_ids.append(job_id)

        response_object = {
            "failed": len(registry),
            "failed_ids": failed_ids,
        }

    return jsonify(response_object)


@main_blueprint.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    with Connection(redis.from_url(current_app.config["REDIS_URL"])):
        q = Queue()
        task = q.fetch_job(task_id)
    if task:
        response_object = {
            "status": "success",
            "data": {
                "task_id": task.get_id(),
                "task_status": task.get_status(),
                "task_result": task.result,
            },
        }
    else:
        response_object = {"status": "error"}
    return jsonify(response_object)