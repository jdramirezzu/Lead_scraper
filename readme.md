# 📊 Lead Intelligence Maps - MVP

Este proyecto es un MVP de un producto SaaS para generar y analizar leads extraídos desde Google Maps, enriquecidos con contactos, reputación y puntuación inteligente.

---

## 🚀 Funcionalidades actuales

### 🔍 Scraping de negocios

* Busca negocios desde Google Maps por categoría y ciudad
* Extrae:

  * Nombre, categoría, dirección
  * Teléfono, sitio web
  * Calificación promedio y cantidad de reseñas
  * Hasta 3 reseñas individuales

### 📬 Scraping de contacto

* Ingresa a la web del negocio y extrae todos los correos públicos encontrados

### 🧠 Enriquecimiento

* Lead score ponderado (email, web, rating, reseñas)
* Clasificación por reputación (Excelente, Buena, Regular, Pobre)
* Segmentación automática:

  * Listo para contactar
  * Reputación débil
  * Oportunidad digital

---

## 🧩 Stack tecnológico

### Backend (API)

* Python 3.11+
* FastAPI
* Playwright
* BeautifulSoup
* Ejecuta scraping en proceso aislado

### Frontend (UI)

* React con Vite
* Tailwind CSS + shadcn/ui
* Conecta al endpoint de backend

---

## 🛠 Instalación paso a paso

### 1. Backend

```bash
pip install fastapi uvicorn playwright beautifulsoup4 requests
playwright install
```

#### Archivos importantes:

* `google_scraper.py`: scraping de Google Maps
* `email_scraper.py`: enriquecimiento con correos, score y reputación
* `lead_api.py`: API que expone el endpoint `/scrape`
* `run_scraper.py`: script auxiliar que ejecuta Playwright aisladamente

#### Ejecutar API

```bash
uvicorn lead_api:app --reload
```

### 2. Frontend

#### Crear app React

```bash
npm create vite@latest
cd nombre-del-proyecto
npm install
```

#### Instalar Tailwind CSS

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

#### Configurar Tailwind:

* `tailwind.config.js`

```js
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

* `src/index.css`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

* Asegúrate de importar `./index.css` en `main.jsx`

#### Agrega componente:

* `lead_dashboard.jsx` debe estar en `src/`
* Conecta al endpoint local `http://localhost:8000/scrape`

#### Ejecutar frontend

```bash
npm run dev
```

---

## 📈 Siguiente paso sugerido

* Agregar exportación a CSV o integración con CRM
* Agregar autenticación y límites por plan
* Desplegar API en Fly.io y frontend en Vercel

---

## 🧪 Test rápido

1. Backend corriendo → `http://localhost:8000/scrape?query=panaderia&location=Medellin`
2. Frontend en `http://localhost:5173`
3. Resultado: leads en tiempo real con reputación y contacto.

---

## 📬 Contacto

Cualquier duda técnica o funcional, contactar a Juan R. (owner del proyecto MVP).
