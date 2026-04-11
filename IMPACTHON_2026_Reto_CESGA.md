# IMPACTHON 2026
**GDG Santiago de Compostela · ETSE / USC**
**10 – 12 de abril de 2026**

---

## Plantilla de Definición de Reto

**Empresa / Sponsor:** Cátedra Camelia Medicina Personalizada - Plexus
**Nombre del reto:** LocalFold: Interfaz web intuitiva para predicción de proteínas
**Tipo de reto:** Problema concreto + Tecnología específica
**Elaborado por:** Biotecnología / Bioinformática / Salud

---

## 1. INFORMACIÓN DEL SPONSOR / ORGANIZACIÓN

| Campo | Contenido |
|---|---|
| **Empresa** | Cátedra Camelia Medicina Personalizada - Plexus |
| **Sector** | Salud · Bioinformática · Computación científica |
| **Web / Contacto** | catedra-camelia.usc.es |
| **Representante** | Responsable técnico de la Cátedra Camelia |
| **Premio para el ganador** | Mentoring con el equipo técnico de la Cátedra + posibilidad de continuar el desarrollo en el entorno CESGA real |
| **¿Traéis hardware?** | No — el hardware es el supercomputador CESGA Finis Terrae III, accesible vía API |

**Por qué patrocinamos Impacthón:**
El reto que proponemos necesita talento frontend y de producto. Tenemos la infraestructura (el clúster CESGA con nodos GPU A100 y AlphaFold2 instalado), tenemos el backend simulado listo, y necesitamos el componente que falta: una interfaz web que haga ese sistema accesible a investigadores sin formación técnica. El hackathon es la forma más directa de obtener prototipos reales, feedback de usabilidad y potencialmente encontrar el equipo que continúe el desarrollo. El resultado del hackathon sería la base de un portal que se desplegaría en producción conectado al CESGA real.

---

## 2. DEFINICIÓN ESTRATÉGICA DEL RETO

### 2.1 Problema real de base

**¿Cuál es el problema?**

La ejecución de sistemas modernos de predicción de estructuras proteicas (como AlphaFold2) presenta una barrera tecnológica significativa para investigadores del ámbito biológico debido a los requisitos de infraestructura: sistemas Linux, GPUs NVIDIA, hasta ~3 TB de bases de datos genéticas y sistemas de colas HPC (Slurm). El cuello de botella no es la calidad del modelo de IA — es la "última milla" operativa: enviar una secuencia, monitorizar su ejecución en el clúster y visualizar los resultados de forma comprensible para un biólogo.

El CESGA (Centro de Supercomputación de Galicia) ya tiene AlphaFold2 instalado y operativo en Finis Terrae III. La infraestructura existe. Lo que falta es la interfaz web que la haga accesible.

**¿Es un problema real?**

Sí. Es el problema central del reto. Los equipos no entrenarán modelos de IA ni accederán al supercomputador real — para eso se les proporciona una API mock que simula exactamente el comportamiento del sistema real. La misión es diseñar y construir la interfaz a través de la cual los investigadores interactuarán con ese sistema en producción.

### 2.2 Tipo de reto

| Marcado | Tipo | Descripción |
|---|---|---|
| ✅ | **Problema concreto** | Parte de una necesidad real. Los hackers proponen cómo resolverla. |
| ☐ | Reto abierto / genérico | — |
| ✅ | **Tecnología específica** | Se requiere consumir la API REST proporcionada. La tecnología es el medio, no el fin. |
| ☐ | Hardware | — |

### 2.3 Uso de inteligencia artificial

**¿Integra IA?**
El núcleo del reto es construir la interfaz para un sistema de IA (AlphaFold2), pero los equipos no necesitan implementar IA. Se valora positivamente el uso de herramientas de IA como apoyo al desarrollo (copilots de código, generación de explicaciones de métricas biológicas, asistentes de UX).

**Uso de IA:** Opcional — se valora positivamente como herramienta de apoyo al desarrollo.

---

## 3. ENUNCIADO PARA LOS PARTICIPANTES

### 3.1 Título del reto

**Título:** BioHack: Democratizando el plegamiento de proteínas

**Subtítulo:** Crea un portal "AlphaFold-like" que conecte a cualquier biólogo con la potencia de un clúster de IA

### 3.2 Descripción del problema

Los modelos de IA para predicción de estructuras proteicas han revolucionado la biología, pero usarlos requiere ser experto en terminales, GPUs y clústeres computacionales. El CESGA (Centro de Supercomputación de Galicia) tiene AlphaFold2 instalado y operativo — el problema es que ningún investigador sin formación técnica puede usarlo directamente.

En este reto construirás la "última milla": un portal web intuitivo que permita a cualquier investigador pegar una secuencia de aminoácidos, ver de forma realista el progreso de su cálculo en la cola del supercomputador, y terminar interactuando con la proteína 3D resultante y sus métricas de confianza — exactamente como lo hace la AlphaFold Database pública, pero conectado a infraestructura propia.

Se os proporciona una API REST desplegada que simula fielmente el comportamiento del sistema real: cola de jobs (PENDING → RUNNING → COMPLETED), ficheros PDB/mmCIF de estructura, métricas de confianza pLDDT y PAE, datos biológicos y contabilidad de recursos HPC. Vuestro trabajo es el frontend.

### 3.3 Objetivo del reto

Construir una interfaz web atractiva y "novice-friendly" que consuma la API REST proporcionada. El proyecto debe:

1. **Formulario de entrada** — ingesta de secuencias FASTA con validación básica (el header `>` es obligatorio), selector de recursos (GPUs, memoria) y feedback claro de errores.

2. **Gestión asíncrona del ciclo de vida del job** — polling del estado (PENDING → RUNNING → COMPLETED), visualización de logs de progreso simulados, indicadores visuales de cada fase.

3. **Visor molecular 3D interactivo** — renderizado de los ficheros PDB/mmCIF devueltos por la API usando **Mol\*** (recomendado, mismo visor que usa la AlphaFold Database oficial), NGL Viewer o 3Dmol.js. Rotación, zoom, selección de residuos.

4. **Visualización de métricas de confianza** — colorear la estructura por pLDDT (azul = muy confiable, naranja = región desordenada), heatmap 2D de la matriz PAE con interpretación accesible para no especialistas.

5. **Integración creativa de datos adicionales** — la API devuelve solubilidad, índice de inestabilidad, predicción de estructura secundaria (% hélice/lámina/coil), cargos, cisteínas, pesos moleculares, metadata UniProt/PDB. El equipo decide cómo presentarlos para aportar valor al investigador.

**Ejemplos de enfoques posibles** (no son obligatorios, son inspiración):

- **Portal estilo AlphaFold DB:** página de resultados inspirada en alphafold.ebi.ac.uk — visor Mol\* central, panel lateral con métricas, descarga en un click.
- **Dashboard de investigación:** múltiples jobs en paralelo, comparación de estructuras, historial de envíos, filtrado por proteína/estado.
- **Wizard paso a paso:** flujo guiado para usuarios sin experiencia — cada pantalla explica qué significa el paso actual y qué va a ocurrir, con tooltips educativos sobre pLDDT, PAE, FASTA.

### 3.4 Material de apoyo y recursos

| Recurso / Herramienta | URL / Acceso | Notas |
|---|---|---|
| **API Mock desplegada** | `https://api-mock-cesga.onrender.com` | Acceso público, sin token |
| **Swagger UI interactivo** | `https://api-mock-cesga.onrender.com/docs` | Explorar y probar endpoints desde el navegador |
| **Guía de usuario completa** | `GET /` → enlace en la respuesta | Incluye ejemplos en curl, Python y JavaScript |
| **Catálogo de proteínas** | `GET /proteins/` | 22 proteínas con metadata real (UniProt, PDB) |
| **Secuencias FASTA de ejemplo** | `GET /proteins/samples` | 8 secuencias listas para copiar y pegar |
| **Mol\* viewer** | `https://molstar.org/viewer/` | Visor 3D recomendado, mismo que AlphaFold DB |
| **3Dmol.js** | `https://3dmol.csb.pitt.edu` | Alternativa más ligera, fácil de embeber |
| **AlphaFold Database** (referencia visual) | `https://alphafold.ebi.ac.uk` | Ver cómo presenta resultados el sistema real |

**Endpoints principales de la API:**

```
POST /jobs/submit              →  Enviar job (fasta_sequence + fasta_filename obligatorios)
GET  /jobs/{id}/status         →  Estado: PENDING / RUNNING / COMPLETED / FAILED
GET  /jobs/{id}/outputs        →  PDB, mmCIF, pLDDT, PAE, datos biológicos, logs
GET  /jobs/{id}/accounting     →  CPU-hours, GPU-hours, eficiencias
GET  /proteins/                →  Catálogo de proteínas identificables
GET  /proteins/samples         →  FASTA de ejemplo listos para usar
```

> **Nota cold-start:** La API está en el tier gratuito de Render. La primera petición tras 15 minutos de inactividad puede tardar ~30 segundos. Las siguientes son instantáneas.

**¿Cómo obtendrán acceso?**
Acceso público sin registro. La URL se compartirá en el canal de Discord del hackathon y estará disponible desde el inicio del evento. No se necesitan tokens ni credenciales.

### 3.5 Criterios de valoración

| Prioridad | Criterio | Descripción |
|---|---|---|
| **1º** | **Usabilidad y UX orientada al biólogo** | Facilidad de uso para usuarios no bioinformáticos. Mensajes de error claros. Explicaciones de métricas (pLDDT, PAE, solubilidad) comprensibles para alguien sin formación en computación. El "test del biólogo": ¿podría usarlo alguien que nunca ha abierto una terminal? |
| **2º** | **Visualización e interpretabilidad** | Calidad del visor 3D (rotación fluida, coloreado por pLDDT funcional). Heatmap PAE con interpretación. Presentación de métricas biológicas adicionales de forma significativa, no como lista de números crudos. |
| **3º** | **Gestión del ciclo de vida del job** | El flujo PENDING → RUNNING → COMPLETED se comunica claramente. El usuario sabe en todo momento qué está pasando. Los logs son legibles. Los errores se manejan con gracia. |
| **4º** | **Integración creativa de los datos de la API** | La API devuelve más datos de los mínimos (solubilidad, toxicidad, estructura secundaria, metadata de proteínas, accounting HPC). Se valora que el equipo encuentre formas ingeniosas de presentarlos que aporten valor real al investigador. |
| **5º** | **Viabilidad técnica como base para producción** | El código está estructurado de forma que pueda conectarse al backend real (CESGA) con cambios mínimos. El diseño contempla autenticación, manejo de errores de red y estados de carga. |

### 3.6 Qué NO se premia

- **Conectar al CESGA real o implementar AlphaFold2**: el reto es la interfaz, no la infraestructura. La API mock ya proporciona todos los datos necesarios.
- **Perfección del código o completitud total**: un prototipo funcional que demuestre la experiencia de usuario completa en los casos principales vale más que código perfectamente testeado pero con UX descuidada.
- **Originalidad del modelo de IA o la biología**: no se evalúa el conocimiento biológico ni la mejora de los algoritmos de predicción. El reto es de producto y frontend.
