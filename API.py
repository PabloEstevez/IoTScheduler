#!/usr/bin/python3

from DeviceController import gpio_status, on_off, get_devices
from CronScheduler import set_task, remove_task, get_tasks
from flask import Flask,request,jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

## DeviceController API
@app.route("/gpio_status",methods=["GET"])
def gpio_status_API():
    if request.method == "GET":
        #FROM QUERY STRINGS
        id_API = request.args.get('id')
        #EXECUTE PYTHON COMMAND
        status = gpio_status(id_API)
        print("Estado: " + str(status))
        #RETURN THE INPUT
        return jsonify({'gpio_status': status })

@app.route("/on_off",methods=["POST"])
def on_off_API():
    if request.method == "POST":
        print("Recibido: " + str(request.json))
        #FROM QUERY STRINGS
        #id_API = request.args.get('id')
        #status_API = request.args.get('status')
        # FROM BODY
        id_API = request.json['id']
        status_API = request.json['status']
        #EXECUTE PYTHON COMMAND
        return_on_off_API = on_off(id_API,status_API)
        #RETURN THE INPUT
        return jsonify({'on_off': return_on_off_API })

## CronScheduler API
@app.route("/set_task",methods=["POST"])
def set_task_API():
    if request.method == "POST":
        #FROM BODY
        #print(request.form.getlist)
        command_init_API = request.form['command_init']
        command_final_API = request.form['command_final']
        inicio_API = request.form['inicio']
        duracion_API = request.form['duracion']
        comentario_API = request.form['comentario']
        ott_API = bool(request.form['ott'])
        #EXECUTE PYTHON COMMAND
        set_task(command_init_API, command_final_API, inicio_API, duracion_API, comentario_API, ott_API)
        #RETURN THE INPUT
        return jsonify(command_init_API, command_final_API, inicio_API, duracion_API, comentario_API, ott_API)

@app.route("/remove_task",methods=["POST"])
def remove_task_API():
    if request.method == "POST":
        #FROM BODY
        id_API = request.form['id']
        #EXECUTE PYTHON COMMAND
        remove_task(id_API)
        #RETURN THE INPUT
        return jsonify({'remove_task': id_API })

@app.route("/get_tasks",methods=["GET"])
def get_tasks_API():
    if request.method == "GET":
        #EXECUTE PYTHON COMMAND
        tasks = get_tasks()
        #RETURN THE INPUT
        return jsonify({'tasks': tasks })

@app.route("/get_devices",methods=["GET"])
def get_devices_API():
    if request.method == "GET":
        #EXECUTE PYTHON COMMAND
        devices = get_devices()
        #RETURN THE INPUT
        return jsonify({'devices': devices })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
