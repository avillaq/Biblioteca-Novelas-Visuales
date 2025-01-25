# Biblioteca de Novelas Visuales

Una biblioteca digital de novelas visuales construida con Django que permite a los usuarios explorar y descargar novelas visuales tanto para PC como para Android. El sitio ofrece una experiencia de usuario fluida con características como búsqueda, filtrado y una sección especial para emulación con Kirikiroid2.

![Inicio](screenshots/home.png)
![Directorio](screenshots/imageViewer.png)
![Android](screenshots/favorites.png)

## ✨ Características

- 🎮 Exploración de novelas visuales para PC y Android
- 🔍 Sistema de búsqueda avanzado
- 🗂️ Filtrado por categorías y fechas
- 📱 Sección dedicada para Android (APK y Kirikiroid2)
- 📖 Vista detallada de cada novela visual
- 💫 Interfaz moderna y responsive
- 🔄 Actualizaciones desde la fuente original

## 🛠️ Tecnologías

- **Backend**: Django 5.0.2
- **Frontend**: HTML5, CSS3, JavaScript
- **Base de datos**: SQLite3
- **APIs**: Blogger API
- **Otros**: BeautifulSoup4, Whitenoise

## 🚀 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/avillaq/Biblioteca-Novelas-Visuales.git
cd Biblioteca-Novelas-Visuales
```

2. Crea y activa un entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Configura las variables de entorno:
```bash
cp .env.example .env
# Edita .env con tus configuraciones
```

5. Realiza las migraciones:
```bash
python manage.py migrate
```

6. Inicia el servidor:
```bash
python manage.py runserver
```

## 🎮 Uso
- Exploración: Navega por la biblioteca usando los filtros de categoría y año
- Búsqueda: Utiliza la barra de búsqueda para encontrar novelas específicas
- Sección Android: Accede a las versiones móviles y guías de instalación
- Detalles: Visualiza screenshots, sinopsis y especificaciones de cada novela

## 📄 License
Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👤 Author
Alexander VQ - [@avillaq](https://github.com/avillaq)