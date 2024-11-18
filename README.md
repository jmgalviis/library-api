# Library API

Library API es una aplicación basada en FastAPI para gestionar una biblioteca. Permite realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) sobre libros, incluyendo funcionalidades como búsqueda y filtrado.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalados los siguientes componentes:

- **Python** (versión 3.9 o superior)
- **PostgreSQL** (base de datos)
- **Poetry** (gestor de dependencias, opcional)
- **Docker** (para ejecutar la aplicación en un contenedor, opcional)

---

## Configuración del Proyecto

### 1. Clonar el Repositorio

```bash
git clone https://github.com/jmgalviis/library-api
cd library-api
```
### 2. Configurar el Entorno Virtual

Crea y activa un entorno virtual para el proyecto en local:

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Configurar Variables de Entorno

Crea un archivo .env en la raíz del proyecto con la configuración de la base de datos:
```text
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/library
```

### 4 Instalar Dependencias

Instala las dependencias del proyecto utilizando pip:
```bash
pip install -r requirements.txt
```
Si usas Poetry, instala las dependencias con:
```bash
poetry install
```

### 5 Ejecutar el Servidor de Desarrollo

Inicia el servidor local:
```bash
uvicorn app.main:app --reload
```

## Documentación de la API

Puedes acceder a la documentación generada automáticamente por Swagger:
- Swagger UI: http://127.0.0.1:8000/docs

## Ejecución de Pruebas

Ejecuta las pruebas unitarias para verificar la funcionalidad del proyecto:
```bash
pytest
```

# Uso con Docker
## 1. Construir la Imagen de Docker
```bash
docker build -t library-api .
```

## 2. Ejecutar el Contenedor
```bash
docker run -d -p 8000:8000 --env-file .env library-api
```

# Contacto

- Nombre: JuanMa Galvis
- Email: jmgalviis@gmail.com







