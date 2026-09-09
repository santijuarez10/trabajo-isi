## Verbos HTTP

* **GET:** se utiliza para obtener o consultar información. Por ejemplo, obtener todas las tareas o una tarea específica.

* **POST:** se utiliza para crear un nuevo recurso. Por ejemplo, crear una nueva tarea.

* **PATCH:** se utiliza para modificar parcialmente un recurso existente. Por ejemplo, cambiar solamente el estado `done` de una tarea sin modificar su título.

* **DELETE:** se utiliza para eliminar un recurso. Por ejemplo, eliminar una tarea.

### Por qué POST no es idempotente?

POST no es idempotente porque realizar la misma petición varias veces puede producir diferentes resultados. Por ejemplo, si hacemos dos veces un `POST /tasks` para crear una tarea, se crean dos tareas diferentes, cada una con su propio `id`.
