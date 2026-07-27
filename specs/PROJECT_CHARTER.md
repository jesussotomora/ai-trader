# AI-Trader: Documento de Visión y Carta del Proyecto (Project Charter)

**Nombre del Proyecto:** `ai-trader`  
**Autor / Owner:** Jesús Soto Mora (`jesussotomora`)  
**Fecha de Creación:** 2026-07-27  
**Estado:** Fase 0 — Investigación Completada & Carta del Proyecto Establecida  
**Repositorio GitHub:** [https://github.com/jesussotomora/ai-trader](https://github.com/jesussotomora/ai-trader)

---

## 1. Visión del Proyecto y Objetivo Principal

### 🎯 Visión
Crear una plataforma modular, automatizada e inteligente de trading e inversión (`ai-trader`) que combine **Modelos de Lenguaje de Gran Escala (LLMs)**, **Análisis de Sentimiento de Noticias**, **Indicadores Técnicos** y **Búsqueda Semántica Vectorial (RAG)** para ejecutar operaciones bursátiles y de criptomonedas con una gestión de riesgo profesional.

### 🚩 Objetivo Principal
Construir un motor de trading capaz de:
1. **Poner a competir a múltiples modelos de IA (Modo Arena)** o **consolidar sus recomendaciones en un consejo asesor (Modo Consejo)**.
2. Operar sin infringir los Términos de Servicio (ToS) de las suscripciones de los proveedores de IA (ChatGPT Plus, Claude Pro, Gemini Advanced, OpenCode Go).
3. Estar optimizado para usuarios que residen en **México**, facilitando el fondeo en pesos (MXN vía SPEI) e integrando brokers modernos (Interactive Brokers, Alpaca y Bitso).
4. Proteger estrictamente el capital del usuario mediante controles automatizados de riesgo (Stop-Loss, Take-Profit, límites por posición y disyuntores de drawdown).

---

## 2. Objetivos Específicos & Criterios de Éxito

* **Soporte de Suscripciones Web Existentes:** Permitir al usuario usar sus suscripciones actuales (ej. Gemini Advanced activo, Claude Pro, ChatGPT Plus, OpenCode Go) a través de asistentes interactivos formateados en JSON y herramientas CLI oficiales, evitando gastos de API por token.
* **Dualidad de Modos de Operación:**
  * **Modo A (Arena de Competencia):** Varios LLMs administran portafolios virtuales independientes compitiendo por rendimiento (Sharpe Ratio, Win Rate).
  * **Modo B (Consejo Asesor / Consenso):** IAs especializadas (Analista Técnico, Auditor Fundamental con Gemini 2M contexto, Analista de Sentimiento) que alimentan a un Sintetizador de Consenso para emitir órdenes unificadas.
* **Operativa Eficiente en México:**
  * *Entorno de Pruebas (Sandbox):* Integración con la API gratuita de **Alpaca Paper Trading**.
  * *Entorno de Producción en Acciones/ETFs:* Integración con **Interactive Brokers (IBKR)** permitiendo depósitos en MXN por SPEI y cambio a USD a tasa institucional.
  * *Entorno Cripto:* Integración con la API de **Bitso Alpha** para pares MXN/Cripto con fondeo inmediato SPEI 24/7.
* **Extracción Completa de Contexto en Noticias:** Utilizar scraping de cuerpo entero (`newspaper3k`) en lugar de snippets de titular para no perder información crítica.
* **Sustitución de Gimmicks por RAG Financiero:** Reemplazar experimentos cómicos (como las letras de Taylor Swift del Video #1) por una base de conocimiento vectorial que compare noticias contra reportes SEC 10-K y datos macroeconómicos.

---

## 3. Fuentes de Inspiración y Referencias

1. **Video #1 (Lewis Menelaws - Trading Bot $10k Experiment):**
   * *Referencia:* Demostración de bots de trading en Python (Momentum, Sentimiento de Noticias y Búsqueda Vectorial) usando Interactive Brokers.
   * *Enlace:* [https://www.youtube.com/watch?v=zh008MNMOlo](https://www.youtube.com/watch?v=zh008MNMOlo)
2. **Video #2 (The Koerner Office Podcast - 5 IAs con $5,000 USD de Dinero Real):**
   * *Referencia:* Competencia real de 6 meses entre Claude, ChatGPT, Gemini, Grok y Perplexity. Claude obtuvo **+140% de rendimiento** y el grupo superó al S&P 500 por 11x-12x (+56% vs +5%). Demuestra el valor de forzar tesis de inversión y reglas de salida.
   * *Enlace:* [https://www.youtube.com/watch?v=DKM94g3Hr_M](https://www.youtube.com/watch?v=DKM94g3Hr_M)
3. **Repositorio GitHub (`SomeRandomGuy009/news-bot`):**
   * *Referencia:* Extracción de texto completo de noticias y resúmenes NLP usando `newspaper3k` + `nltk` + `NewsAPI`.
   * *Enlace:* [https://github.com/SomeRandomGuy009/news-bot](https://github.com/SomeRandomGuy009/news-bot)

---

## 4. Metodología y Plan de Implementación (Cómo lo Haremos)

El desarrollo del proyecto se dividirá en 5 capas arquitectónicas:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           CAPA DE USUARIO & UI                          │
│        (Dashboard Web / CLI / Asistente de Prompts Formateados)         │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
┌────────────────────────────────────▼────────────────────────────────────┐
│                    CAPA DE INTELIGENCIA Y MODELOS (LLM)                 │
│    - Capa de Cumplimiento ToS (Prompt Helper, OpenCode Go, Claude Code) │
│    - Motor Modo A (Arena de Competencia con Portafolios Simulados)      │
│    - Motor Modo B (Consejo Asesor: Técnico, Fundamental, Sentimiento)   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
┌────────────────────────────────────▼────────────────────────────────────┐
│                    CAPA DE DATOS Y CONOCIMIENTO (RAG)                   │
│    - NewsScraperService (newspaper3k + NewsAPI + Caching SQLite)        │
│    - Financial RAG Engine (Vector DB + SEC 10-K + Indicadores Macro)     │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
┌────────────────────────────────────▼────────────────────────────────────┐
│                       CAPA DE GESTIÓN DE RIESGO                         │
│    - RiskManager (Stop-Loss, Take-Profit, Max Position Size, Drawdown)  │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
┌────────────────────────────────────▼────────────────────────────────────┐
│                        CAPA DE CONECTORES (BROKERS)                     │
│    - AlpacaAdapter (Paper Trading / Sandbox gratis)                     │
│    - IBKRAdapter (Producción Acciones/ETFs vía SPEI MXN)                │
│    - BitsoAdapter (Cripto MXN 24/7)                                     │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Índice de Investigación y Archivos Recolectados (`specs/misc/`)

Todos los documentos de investigación previa generados se encuentran organizados y sincronizados en Git dentro de `specs/misc/`:

* 📁 **[specs/misc/SUMMARY.md](file:///Users/jesussoto/development/projects/ai-trader/ai-trader/specs/misc/SUMMARY.md):** Índice maestro y mapeo de toda la investigación preliminar.
* 📄 **[specs/misc/youtube-zh008MNMOlo-analysis.md](file:///Users/jesussoto/development/projects/ai-trader/ai-trader/specs/misc/youtube-zh008MNMOlo-analysis.md):** Análisis del video #1 (Lewis Menelaws - Trading Bot $10k).
  * 📜 *Transcripción:* [specs/misc/youtube-zh008MNMOlo-transcript.txt](file:///Users/jesussoto/development/projects/ai-trader/ai-trader/specs/misc/youtube-zh008MNMOlo-transcript.txt)
* 📄 **[specs/misc/github-news-bot-analysis.md](file:///Users/jesussoto/development/projects/ai-trader/ai-trader/specs/misc/github-news-bot-analysis.md):** Análisis del repositorio de scraping de noticias con `newspaper3k`.
* 📄 **[specs/misc/youtube-DKM94g3Hr_M-analysis.md](file:///Users/jesussoto/development/projects/ai-trader/ai-trader/specs/misc/youtube-DKM94g3Hr_M-analysis.md):** Análisis del video #2 (Competencia de 5 IAs con $5k real money).
  * 📜 *Transcripción:* [specs/misc/youtube-DKM94g3Hr_M-transcript.txt](file:///Users/jesussoto/development/projects/ai-trader/ai-trader/specs/misc/youtube-DKM94g3Hr_M-transcript.txt)
* 📄 **[specs/misc/ai-subscriptions-cost-benefit.md](file:///Users/jesussoto/development/projects/ai-trader/ai-trader/specs/misc/ai-subscriptions-cost-benefit.md):** Matriz costo/beneficio de suscripciones web de IA (ChatGPT Plus, Claude Pro, Gemini, OpenCode Go, Kimi K3, Perplexity, DeepSeek, Qwen).
* 📄 **[specs/misc/mexico-automated-trading-platforms.md](file:///Users/jesussoto/development/projects/ai-trader/ai-trader/specs/misc/mexico-automated-trading-platforms.md):** Análisis de brokers, costos y automatización en México (IBKR, Alpaca, Bitso, fondeo SPEI).
* 📄 **[specs/misc/llm-architecture-and-compliance.md](file:///Users/jesussoto/development/projects/ai-trader/ai-trader/specs/misc/llm-architecture-and-compliance.md):** Especificación de cumplimiento ToS, taxonomía de modelos, rol de Gemini Advanced (infraestructura y contexto 2M), modos duales (Arena vs Consejo) y RAG financiero.
