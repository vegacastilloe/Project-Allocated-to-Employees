# 🧠 Unpivoted Data Project Allocated to Employees

![License: MIT](https://img.shields.io/badge/License-MIT-cyan.svg)
![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![Last Updated](https://img.shields.io/github/last-commit/vegacastilloe/Project-Allocated-to-Employees)
![Language](https://img.shields.io/badge/language-español-darkred)

#
---
- 🌟 --- CAN YOU SOLVE THIS - EXCEL CHALLENGE 909 --- 🌟
- 🌟 **Author**: Excel (Vijay A. Verma) BI

    - 🔰 Unpivotar y organizar los datos de proyectos de empleados

 🔰 Este script toma un DataFrame de Excel con columnas `EmpID`, `Name`, `Dept`, `Project Data`. La finalidad es detallar el proceso realizado para unpivotar y organizar los datos de proyectos de empleados.

 🔗 Link to Excel file:
 👉 https://lnkd.in/dbxD7MQz

**My code in Python** 🐍 **for this challenge**

 🔗 https://github.com/vegacastilloe/Project-Allocated-to-Employees/blob/main/project_allocated_to_employees.py

---
---

## Unpivoted Data Project Allocated to Employees

Aquí se detalla el proceso realizado para unpivotar y organizar los datos de proyectos de empleados:

1.  **Carga de Datos:**
    *   Primero, se definió la URL del archivo Excel en la variable `xl`.
    *   Se utilizó `pandas` para leer el archivo Excel desde la URL, especificando la hoja `'Sheet1'` y configurando la primera fila como encabezado.
    *   Las columnas del DataFrame `df_raw` se limpiaron de espacios en blanco.

2.  **Preparación Inicial del DataFrame:**
    *   Se creó `df_input` seleccionando las columnas clave: `EmpID`, `Name`, `Dept` y `Project Data`. Se eliminaron las filas completamente vacías en estas columnas.

3.  **Lógica de Unpivotado e Identificación de Proyectos 'Bench':**
    *   Se inicializó una lista vacía, `unpivoted_data`, para almacenar los datos transformados.
    *   Se iteró sobre cada fila de `df_input` usando `itertuples()`.
    *   Para cada empleado, se extrajo 'EmpID', 'Name', 'Dept' y la cadena de 'Project Data'.
    *   **Proyectos con Horas:** Si la columna 'Project Data' contenía información (no nula y no vacía):
        *   Se dividió la cadena por el separador `|` para obtener pares de 'Proyecto:Horas'.
        *   Cada par se dividió por `:` para obtener el nombre del proyecto y las horas.
        *   Se intentó convertir las horas a un número entero. Si las horas eran 10 o más, se creó un diccionario con los datos del empleado y el proyecto, y se añadió a una lista temporal `employee_projects`.
    *   **Proyectos 'Bench':** Si la columna 'Project Data' estaba vacía, o si después de procesar todos los proyectos de un empleado, `employee_projects` quedaba vacía (lo que significa que ningún proyecto cumplió el criterio de 10+ horas):
        *   Se añadió una entrada a `employee_projects` con 'Project' como 'Bench' y 'Hours' como 0.
    *   Finalmente, todas las entradas de `employee_projects` (ya sean proyectos reales o 'Bench') se extendieron a la lista `unpivoted_data`.

4.  **Creación y Ordenación del DataFrame Resultante:**
    *   La lista `unpivoted_data` se convirtió en un nuevo DataFrame llamado `df_result`.
    *   `df_result` se ordenó ascendentemente por la columna 'EmpID' y se reinició el índice para mantenerlo limpio.

5.  **Verificación y Visualización (Opcional):**
    *   Se realizó una comparación con un DataFrame `expected` (derivado de las columnas originales del Excel que representaban el resultado deseado) para verificar la exactitud de la transformación.
    *   Los resultados de esta comparación (y el DataFrame final `df_result`) se imprimieron para mostrar la estructura y los valores.



## 📦 Requisitos

- Python 3.9+
- Paquetes:
- pandas openpyxl (para leer .xlsx)
- Archivo Excel con al menos:
    - Las columnas: `EmpID`, `Name`, `Dept` y `Project Data`.
    - En las columnas `EmpID`, `Name`, `Dept`, `Project` y `Hours` : resultados esperados para comparación

---

## 🚀 Cómo funciona

- Lee un archivo Excel desde una URL o ruta local.
- Limpia columnas vacías y espacios en los encabezados.
- Aplica una transformación regex para invertir el case de palabras completas.
- Compara el resultado con una columna de respuestas.
- Imprime una tabla con el resultado y la validación.

---

## 📤 Salida

El script imprime : # True si al comparar df_result contra expected, ambos convertidos en diccionario, ambos coinciden.
---

## 🧹 Output:


||
|--------|
|Match expected: 🐍✅ #True|

---

## 🛠️ Personalización

Puedes adaptar el script para:

- Aplicar reglas más complejas
- Exportar el resultado a Excel o CSV

---

## 🚀 Ejecución

```python
import pandas as pd

df_raw = pd.read_excel(xl, header=1, sheet_name='Sheet1')
df_raw.columns = df_raw.columns.str.strip()
df_input = df_raw[['EmpID', 'Name', 'Dept', 'Project Data']].dropna(how='all').copy()
df_input

unpivoted_data = []

for row in df_input.itertuples(index=False):
    emp_id = row.EmpID
    name = row.Name
    dept = row.Dept
    project_data = row._3

    employee_projects = []

    if pd.isna(project_data) or (isinstance(project_data, str) and not project_data.strip()):
        employee_projects.append({
            'EmpID': emp_id,
            'Name': name,
            'Dept': dept,
            'Project': 'Bench',
            'Hours': 0
        })
    else:
        project_pairs = project_data.split('|')
        for pair in project_pairs:
            if ':' in pair:
                project_name, hours_str = pair.split(':', 1)
                try:
                    hours_int = int(hours_str)
                    if hours_int >= 10:
                        employee_projects.append({
                            'EmpID': emp_id,
                            'Name': name,
                            'Dept': dept,
                            'Project': project_name,
                            'Hours': hours_int
                        })
                except ValueError:
                    continue

    if not employee_projects:
        unpivoted_data.append({
            'EmpID': emp_id,
            'Name': name,
            'Dept': dept,
            'Project': 'Bench',
            'Hours': 0
        })
    else:
        unpivoted_data.extend(employee_projects)

df_result = pd.DataFrame(unpivoted_data)
expected = df_raw.iloc[:,  [5, 6, 7, 8, 9]].dropna(how='all').rename(columns=lambda x: x.replace('.1', ''))

print(f'Match expected: 🐍✅ #{df_result.to_dict() == expected.to_dict()}\n')  # True si todo coincide```

### 💾 Exportación opcional
```python
# # df_result.to_excel("project_allocated_to_employees_output.xlsx", index=False)
```
---
### 📄 Licencia
---
Este proyecto está bajo ![License: MIT](https://img.shields.io/badge/License-MIT-cyan.svg). Puedes usarlo, modificarlo y distribuirlo libremente.

---
