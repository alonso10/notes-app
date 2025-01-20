# Notes # Proyecto Notes App

Este proyecto consiste en una **aplicación web** que permite a los usuarios:

1. **Registrar** y **autenticarse** (mediante JWT).
2. **Crear**, **leer**, **actualizar** y **eliminar** (CRUD) notas privadas.
3. Utilizar una **estrategia de bloqueo pesimista** para manejar la concurrencia y prevenir condiciones de carrera al actualizar notas.

## Tecnologías

- **Python** (FastAPI)
- **SQLAlchemy**
- **PostgreSQL**
- **Docker** y **Docker Compose** (opcional para despliegue)
- **React** (Se usa en el frontend, se encuentrar en el siguiente repositorio: [notes-app-frontend](https://github.com/tu-usuario/notes-app-frontend))

---

## Requisitos previos

- Python 3.10+ (recomendado)
- PostgreSQL (instalado localmente o accesible en tu máquina)
- [Opcional] Docker y Docker Compose, si deseas ejecutar todo en contenedores

---

## 1. Ejecución local con virtualenv

A continuación se describe el proceso para ejecutar la aplicación **localmente** usando un entorno virtual de Python:

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/notes-app.git
   cd notes-app

2. **Crear un entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: .\venv\Scripts\activate
   ```
3. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configurar las variables de entorno**:
   ```bash
    cp .env.example .env
    ```
5. **Inicia la aplicación**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
   ```bash
    fastapi dev app/main.py  
    ```
   
## 2. Ejecución con Docker y Docker Compose

El proyecto incluye un Dockerfile (con multi-stage build) y un archivo docker-compose.yml para ejecutar la aplicación junto con PostgreSQL.

### 2.1 Inciar con Docker Compose

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/notes-app.git
   cd notes-app
   ```
2. **Construir e iniciar**:
    ```bash
    docker-compose up --build
    ```
    - Esto levanta los servicios de la aplicación y PostgreSQL.

3. **Acceder a la aplicación**:
    - La aplicación estará disponible en [http://localhost:8000](http://localhost:8000)

4. **Detener y eliminar los contenedores**:
    ```bash
    docker-compose down
    ```
   
### 2.2. Explicación de la configuración

*   **Dockerfile** (multi-stage):
    
    *   En la primera etapa (builder) instala dependencias y crea un entorno limpio.
        
    *   En la segunda etapa (final) copia solo las dependencias ya compiladas, haciendo la imagen más ligera.
        
*   **docker-compose.yml**:
    
    *   Orquesta el contenedor de la aplicación (backend) y el de la base de datos (db) con un volumen para los datos de PostgreSQL.


3\. ¿Por qué se usa bloqueo pesimista en lugar de optimista?
------------------------------------------------------------

La aplicación implementa **bloqueo pesimista** al momento de actualizar notas mediante SELECT ... FOR UPDATE. De esta forma, cuando un proceso accede a modificar una nota, la fila queda bloqueada para otras transacciones hasta que finaliza la operación.

**Ventajas de usar bloqueo pesimista** en este proyecto:

*   **Mayor seguridad en colisiones de escritura**: si varios usuarios intentan modificar la misma nota al mismo tiempo, el primero en adquirir el lock bloquea la fila y evita escrituras simultáneas.
    
*   **Entornos con alta contención**: en escenarios donde es frecuente que varios usuarios editen la misma nota, el bloqueo pesimista reduce la complejidad de manejar versiones o conflictos.
    
*   **Menor riesgo de inconsistencias**: el lock impide que otros cambien la nota mientras se está procesando, evitando la sobrescritura de cambios durante la transacción.
    

El **bloqueo optimista** resulta útil si las colisiones son poco frecuentes y deseas maximizar la concurrencia de lectura, pero requiere el manejo explícito de campos de versión y la detección de conflictos (debes avisar al usuario si algo cambió mientras editaba). En cambio, con el **bloqueo pesimista**, no es necesario reintentar o combinar cambios: el lock impone un orden estricto de escritura
