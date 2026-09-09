from wsgiref.simple_server import make_server  #importa herramienta para crear el server
import json   #importa herramienta para recibir y mandar respuesta json


tasks = {}
next_id = 1


def response(start_response, status, data=None):
    if data is None:
        body = b""
    else:
        body = json.dumps(data).encode("utf-8")

    headers = [
        ("Content-Type", "application/json"),
        ("Content-Length", str(len(body)))
    ]

    start_response(status, headers)
    return [body]


def application(environ, start_response):
    global next_id

    method = environ["REQUEST_METHOD"]  #puede ser PATCH, POST, GET O DELTE
    path = environ["PATH_INFO"]         #puede ser /tasks, /tasks/n

    # GET /tasks
    if method == "GET" and path == "/tasks":
        return response(start_response, "200 OK", list(tasks.values()))

    # Separar /tasks/{id}
    parts = path.strip("/").split("/")

    # Verificar que sea /tasks/{id}
    if len(parts) == 2 and parts[0] == "tasks":
        try:
            task_id = int(parts[1])
        except ValueError:
            return response(start_response, "404 Not Found",
                            {"error": "Tarea no encontrada"})

        # GET /tasks/{id}
        if method == "GET":
            if task_id not in tasks:
                return response(start_response, "404 Not Found",
                                {"error": "Tarea no encontrada"})

            return response(start_response, "200 OK", tasks[task_id])

        # PATCH /tasks/{id}
        if method == "PATCH":
            if task_id not in tasks:
                return response(start_response, "404 Not Found",
                                {"error": "Tarea no encontrada"})

            content_length = int(environ.get("CONTENT_LENGTH") or 0)
            body = environ["wsgi.input"].read(content_length)

            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                return response(start_response, "400 Bad Request",
                                {"error": "JSON inválido"})

            # Modificación parcial
            tasks[task_id].update(data)

            return response(start_response, "200 OK", tasks[task_id])

        # DELETE /tasks/{id}
        if method == "DELETE":
            if task_id not in tasks:
                return response(start_response, "404 Not Found",
                                {"error": "Tarea no encontrada"})

            deleted_task = tasks.pop(task_id)

            return response(start_response, "200 OK", deleted_task)

        # La ruta existe, pero el método no está permitido
        return response(start_response, "405 Method Not Allowed",
                        {"error": "Método no permitido"})

    # POST /tasks
    if method == "POST" and path == "/tasks":
        content_length = int(environ.get("CONTENT_LENGTH") or 0)
        body = environ["wsgi.input"].read(content_length)

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            return response(start_response, "400 Bad Request",
                            {"error": "JSON inválido"})

        task = {
            "id": next_id,
            **data
        }

        tasks[next_id] = task
        next_id += 1

        return response(start_response, "201 Created", task)

    # Ruta /tasks con otro método
    if path == "/tasks":
        return response(start_response, "405 Method Not Allowed",
                        {"error": "Método no permitido"})

    # Cualquier otra ruta
    return response(start_response, "404 Not Found",
                    {"error": "Ruta no encontrada"})


if __name__ == "__main__":
    server = make_server("localhost", 9292, application)   #crea el srv

    print("Servidor escuchando en http://localhost:9292")

    server.serve_forever()