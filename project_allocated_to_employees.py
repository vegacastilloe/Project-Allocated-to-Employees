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

print(f'Match expected: 🐍✅ #{df_result.to_dict() == expected.to_dict()}\n')  # True si todo coincide

# 💾 Exportación opcional
# df_result.to_excel("project_allocated_to_employees_output.xlsx", index=False)


---
