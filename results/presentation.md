---
theme: gaia
_class: lead
paginate: true
headingDivider: 2
backgroundColor: rgba(255, 255, 255, 1)
backgroundImage: linear-gradient(rgba(255, 255, 255, 0.85),rgba(255, 255, 255, 0.95)), url('https://miro.medium.com/v2/resize:fit:1400/1*mPAa2d5RGUoOB_iamW02LA.png')
marp: true
---

<style>
img {
    display: block;
    margin: auto;
    width: 75vw;
}

h2 {
    margin-bottom: 15px;
    color: #54428E
}

section blockquote {
  /* Base style for all callouts */
  background-color: #f0f0f0;
  border-left: 5px solid #ccc;
  padding: 1rem;
  border-radius: 5px;
  margin-inline-start: 0;
  margin-inline-end: 0;
}

.container-flex {
  display: flex;
  justify-content: center; /* For horizontal centering */
  align-items: center; /* For vertical centering */
  height: 100vh; /* Example: full viewport height */
}

section blockquote p {
  margin: 0; /* Remove default paragraph margin */
}
</style>

# **WikiRacer**
*Programación avanzada*
José Ocampo

# **Ideas fallidas**
<!-- _class: lead -->
## Word embeddings
<img src="https://www.nlplanet.org/course-practical-nlp/_images/word_embeddings.png">

## Word embeddings
- Rendimiento terrible
- No terminó el test `test_wikiracer_1` en menos de 5 minutos
- Similaridad semántica < String similarity (hipótesis)

## Substrings y superstrings
<img src="https://www.programiz.com/sites/tutorial2program/files/string-find-rfind_0.png">


## Substrings y superstrings

- Las coincidencias exactas son muy difíciles de encontrar
- Las que son fáciles de encontrar quitan en lugar de añadir (Ej. `/wiki/A`)

## Levenshtein Distance
> The minimum number of single-character edits (insertions, deletions or substitutions) required to change one word into the other.

## Levenshtein Distance
<img src="https://devopedia.org/images/article/213/5510.1567535069.svg">

## Levenshtein Distance
- Falla en todos los tests complejos
- Al principio pensé que esta era la clave del éxito, pero mientras hacía la presentación me di cuenta que no.

# **Función de costo**
<!-- _class: lead -->

## Implementación
- Dar prioridad máxima a una página si está presente en los links del objetivo
- Eso es todo! (para estos tests)

```python
def costFn(current_link, neighbor_link, goal_links, goal):
        if neighbor_link in goal_links:
            return 0

        # Esta métrica por si misma falla los tests
        # En general, return a, con a > 0, da el mismo resultado
        return Levenshtein.distance(neighbor_link, goal)
```

## Ejemplo: Jesus -> Kobe_Bryant

```python
current_distance=0, current_link='/wiki/Jesus'
current_distance=0, current_link='/wiki/Eucharist'
current_distance=0, current_link='/wiki/ISBN_(identifier)'
current_distance=0, current_link='/wiki/ISSN_(identifier)'
current_distance=0, current_link='/wiki/Main_Page'
current_distance=0, current_link='/wiki/United_States'
current_distance=0, current_link='/wiki/Academy_Awards'
current_distance=0, current_link='/wiki/90th_Academy_Awards'

# Path 
['/wiki/Jesus', '/wiki/ISBN_(identifier)',  '/wiki/United_States',
 '/wiki/Academy_Awards',  '/wiki/90th_Academy_Awards', '/wiki/Kobe_Bryant']
```

# **Resultados**
<!-- _class: lead -->

## Métricas generales 
- 56.56s para correr todos los tests (sin caché)
- Entre 1 y 9 requests para  llegar al objetivo
- Longitud del camino: entre 2 y 6

## Resultados delglosados
| Inicio         | Objetivo       | Requests | Longitud del camino |
|----------------|----------------|----------|---------------------|
| United_Nations | Brazil         | 1        | 2                   |
| Michael_Jordan | Kobe_Bryant    | 1        | 2                   |
| Michael_Jordan | Brazil         | 2        | 3                   |
| Adolf_Hitler   | United_Nations | 2        | 3                   |
| Jesus          | Adolf_Hitler   | 3        | 4                   |
| Michael_Jordan | United_Nations | 3        | 4                   |
| Adolf_Hitler   | Michael_Jordan | 3        | 4                   |

---

| Inicio         | Objetivo       | Requests | Longitud del camino |
|----------------|----------------|----------|---------------------
| Adolf_Hitler   | Brazil         | 3        | 4                   |
| Jesus          | United_Nations | 3        | 3                   |
| Adolf_Hitler   | Kobe_Bryant    | 4        | 4                   |
| United_Nations | Kobe_Bryant    | 4        | 4                   |
| Jesus          | Brazil         | 7        | 5                   |
| Jesus          | Kobe_Bryant    | 8        | 6                   |
| Jesus          | Michael_Jordan | 9        | 6                   |
| Kobe_Bryant    | Brazil         | 9        | 4                   |
