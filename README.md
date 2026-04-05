# FERMEST API

API REST para simulación y optimización de procesos de fermentación mediante algoritmos genéticos. Construida con FastAPI, SQLAlchemy y arquitectura hexagonal.

---

## Instalación

```bash
pip install -r requirements.txt
```

Configura tu archivo `.env` en la raíz del proyecto:

```env
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=3306
DB_NAME=fermest
```

Inicia el servidor:

```bash
uvicorn main:app --reload
```

Documentación interactiva disponible en `http://localhost:8000/docs`.

---

## Endpoints

### POST `/run-experiment`

Ejecuta el algoritmo genético con las condiciones iniciales dadas. Crea el experimento, evoluciona la población y persiste todos los resultados en la base de datos.

**Body:**
```json
{
  "ph": 5.5,
  "temperature": 30.0,
  "sugar": 10.0,
  "microorganism": "saccharomyces",
  "micro_amount": 1.5
}
```

**Respuesta:**
```json
{
  "experiment_id": "3f2a1b4c-...",
  "best_individual": {
    "rpm": 143.21,
    "temperature": 31.4,
    "flow": 6.82,
    "fitness": 0.8741
  },
  "history": [0.51, 0.63, 0.71, 0.78, 0.84, ...]
}
```

| Campo | Descripción |
|-------|-------------|
| `experiment_id` | ID único del experimento, úsalo en los demás endpoints |
| `best_individual` | Mejor solución encontrada al final de la evolución |
| `history` | Fitness del mejor individuo en cada generación |

---

### GET `/experiment/{experiment_id}`

Devuelve el resumen completo del experimento: todas las generaciones con todos sus individuos y sus métricas. No incluye datos de simulación para mantener la respuesta liviana.

**Ejemplo:**
```
GET /experiment/3f2a1b4c-...
```

**Respuesta:**
```json
{
  "experiment": {
    "id": "3f2a1b4c-...",
    "ph": 5.5,
    "temperature": 30.0,
    "sugar": 10.0
  },
  "generations": [
    {
      "generation": 0,
      "best_fitness": 0.63,
      "individuals": [
        {
          "id": "7c9e2d1a-...",
          "rpm": 120.4,
          "temperature": 28.1,
          "flow": 5.3,
          "fitness": 0.61,
          "ethanol": 3.21,
          "biomass": 5.44,
          "substrate": 1.02,
          "efficiency": 0.82,
          "energy": 210.4
        }
      ]
    }
  ]
}
```

Útil para graficar la distribución de todos los individuos en el espacio de parámetros.

---

### GET `/experiment/{experiment_id}/best-per-generation`

Devuelve únicamente el mejor individuo de cada generación. Más liviano que el endpoint anterior y optimizado para graficar la evolución del algoritmo.

**Ejemplo:**
```
GET /experiment/3f2a1b4c-.../best-per-generation
```

**Respuesta:**
```json
{
  "experiment_id": "3f2a1b4c-...",
  "generations": [
    {
      "generation": 0,
      "best_fitness": 0.63,
      "best_individual": {
        "id": "7c9e2d1a-...",
        "rpm": 120.4,
        "temperature": 28.1,
        "flow": 5.3,
        "fitness": 0.63,
        "ethanol": 3.21,
        "biomass": 5.44,
        "substrate": 1.02,
        "efficiency": 0.82,
        "energy": 210.4
      }
    }
  ]
}
```

---

### GET `/simulation/{individual_id}`

Devuelve los 200 puntos de tiempo de la simulación ODE de un individuo específico. Úsalo solo cuando necesites ver la curva detallada de fermentación de un individuo concreto.

**Ejemplo:**
```
GET /simulation/7c9e2d1a-...
```

**Respuesta:**
```json
{
  "time":      [0.0, 1.005, 2.01, ...],
  "biomass":   [1.5, 1.62, 1.74, ...],
  "substrate": [10.0, 9.81, 9.61, ...],
  "ethanol":   [0.0, 0.09, 0.19, ...]
}
```

---

## Cómo generar las gráficas

Instala las dependencias necesarias:

```bash
pip install matplotlib pandas
```

---

### Gráfica 1 — Evolución del fitness por generación

Muestra cómo mejoró el algoritmo genético a lo largo de las generaciones. Los datos vienen directamente del `POST /run-experiment`.

```python
import matplotlib.pyplot as plt

history = [0.51, 0.63, 0.71, 0.78, 0.84]  # campo "history" de la respuesta

plt.figure(figsize=(10, 5))
plt.plot(range(1, len(history) + 1), history, marker="o", linewidth=2, color="steelblue")
plt.title("Evolución del fitness por generación")
plt.xlabel("Generación")
plt.ylabel("Mejor fitness")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("fitness_evolution.png", dpi=150)
plt.show()
```

---

### Gráfica 2 — Parámetros del mejor individuo por generación

Muestra cómo fueron cambiando RPM, temperatura y flujo del mejor individuo a lo largo de la evolución. Usa el endpoint `/best-per-generation`.

```python
import requests
import matplotlib.pyplot as plt

experiment_id = "tu-experiment-id"
data = requests.get(f"http://localhost:8000/experiment/{experiment_id}/best-per-generation").json()

generaciones  = [g["generation"] for g in data["generations"]]
fitness       = [g["best_fitness"] for g in data["generations"]]
rpms          = [g["best_individual"]["rpm"] for g in data["generations"]]
temperaturas  = [g["best_individual"]["temperature"] for g in data["generations"]]
flujos        = [g["best_individual"]["flow"] for g in data["generations"]]

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("Evolución del mejor individuo por generación", fontsize=14)

axes[0, 0].plot(generaciones, fitness, marker="o", color="steelblue")
axes[0, 0].set_title("Fitness")
axes[0, 0].set_xlabel("Generación")
axes[0, 0].grid(True, linestyle="--", alpha=0.5)

axes[0, 1].plot(generaciones, rpms, marker="o", color="tomato")
axes[0, 1].set_title("RPM")
axes[0, 1].set_xlabel("Generación")
axes[0, 1].grid(True, linestyle="--", alpha=0.5)

axes[1, 0].plot(generaciones, temperaturas, marker="o", color="seagreen")
axes[1, 0].set_title("Temperatura (°C)")
axes[1, 0].set_xlabel("Generación")
axes[1, 0].grid(True, linestyle="--", alpha=0.5)

axes[1, 1].plot(generaciones, flujos, marker="o", color="goldenrod")
axes[1, 1].set_title("Flujo")
axes[1, 1].set_xlabel("Generación")
axes[1, 1].grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("best_per_generation.png", dpi=150)
plt.show()
```

---

### Gráfica 3 — Dispersión de individuos (fitness vs parámetros)

Muestra cómo se distribuyen todos los individuos en el espacio de parámetros, coloreados por fitness. Usa el endpoint `/experiment/{id}`.

```python
import requests
import matplotlib.pyplot as plt

experiment_id = "tu-experiment-id"
data = requests.get(f"http://localhost:8000/experiment/{experiment_id}").json()

rpms   = []
temps  = []
flujos = []
fitness = []

for gen in data["generations"]:
    for ind in gen["individuals"]:
        rpms.append(ind["rpm"])
        temps.append(ind["temperature"])
        flujos.append(ind["flow"])
        fitness.append(ind["fitness"])

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle("Distribución de individuos coloreados por fitness", fontsize=14)

sc1 = axes[0].scatter(rpms, fitness, c=fitness, cmap="viridis", alpha=0.6)
axes[0].set_xlabel("RPM")
axes[0].set_ylabel("Fitness")
axes[0].set_title("Fitness vs RPM")
plt.colorbar(sc1, ax=axes[0])

sc2 = axes[1].scatter(temps, fitness, c=fitness, cmap="viridis", alpha=0.6)
axes[1].set_xlabel("Temperatura (°C)")
axes[1].set_ylabel("Fitness")
axes[1].set_title("Fitness vs Temperatura")
plt.colorbar(sc2, ax=axes[1])

sc3 = axes[2].scatter(flujos, fitness, c=fitness, cmap="viridis", alpha=0.6)
axes[2].set_xlabel("Flujo")
axes[2].set_ylabel("Fitness")
axes[2].set_title("Fitness vs Flujo")
plt.colorbar(sc3, ax=axes[2])

plt.tight_layout()
plt.savefig("individuals_scatter.png", dpi=150)
plt.show()
```

---

### Gráfica 4 — Curvas de fermentación de un individuo

Muestra la evolución de biomasa, sustrato y etanol en el tiempo para un individuo específico. Usa el endpoint `/simulation/{individual_id}`.

```python
import requests
import matplotlib.pyplot as plt

individual_id = "tu-individual-id"
data = requests.get(f"http://localhost:8000/simulation/{individual_id}").json()

time      = data["time"]
biomass   = data["biomass"]
substrate = data["substrate"]
ethanol   = data["ethanol"]

fig, ax1 = plt.subplots(figsize=(10, 5))

ax1.plot(time, biomass,   label="Biomasa",   color="seagreen",  linewidth=2)
ax1.plot(time, substrate, label="Sustrato",  color="steelblue", linewidth=2)
ax1.plot(time, ethanol,   label="Etanol",    color="tomato",    linewidth=2)
ax1.set_xlabel("Tiempo (h)")
ax1.set_ylabel("Concentración (g/L)")
ax1.set_title("Curvas de fermentación")
ax1.legend()
ax1.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("fermentation_curves.png", dpi=150)
plt.show()
```

---

## Resumen de endpoints

| Método | Endpoint | Cuándo usarlo |
|--------|----------|---------------|
| `POST` | `/run-experiment` | Ejecutar el AG y obtener resultados |
| `GET`  | `/experiment/{id}` | Ver todos los individuos de todas las generaciones |
| `GET`  | `/experiment/{id}/best-per-generation` | Ver evolución del mejor individuo |
| `GET`  | `/simulation/{individual_id}` | Ver curva de fermentación de un individuo |

## Estructura del proyecto

```
├── application
│   ├── dto
│   │   ├── experiment_input_dto.py
│   │   └── experiment_output_dto.py
│   └── use_cases
│       ├── get_best_per_generation.py
│       ├── get_experiment.py
│       ├── get_results.py
│       ├── get_simulation.py
│       └── run_experiment.py
├── domain
│   ├── entities
│   │   ├── experiment.py
│   │   ├── generation.py
│   │   └── individual.py
│   ├── repositories
│   │   └── experiment_repository.py
│   └── services
│       ├── energy.py
│       ├── fitness.py
│       ├── genetic_algorithm.py
│       └── simulator.py
├── infrastructure
│   ├── database
│   │   ├── connection.py
│   │   └── models.py
│   └── repositories
│       ├── mysql_experiment_repository.py
│       ├── mysql_generation_repository.py
│       ├── mysql_individual_repository.py
│       └── mysql_simulation_repository.py
├── interfaces
│   └── api
│       ├── controllers.py
│       ├── routes.py
│       └── schemas.py
├── main.py
├── requirements.txt
└── .env
```