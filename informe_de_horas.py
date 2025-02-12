import pandas as pd
import plotly.express as px

# Leer el archivo Excel
file_path = 'tabla-normalizada.xlsx'
df = pd.read_excel(file_path, engine='openpyxl')


# Gráfico interactivo de suma de horas por proyecto
fig1 = px.bar(df, x='Proyecto', y='Horas', color='Proyecto', title='Suma de Horas por Proyecto')
fig1.update_layout(barmode='stack')
fig1.show()

# Gráfico interactivo de suma de horas por empleado con filtro de proyecto
fig2 = px.bar(df, x='Empleado', y='Horas', color='Empleado', title='Suma de Horas por Empleado')
fig2.update_layout(barmode='stack')
fig2.show()

# Calcular la eficiencia por proyecto
df['Eficiencia'] = df.groupby('Proyecto')['Horas'].transform('sum') / df['Horas']

# Gráfico interactivo de dispersión de eficiencia por proyecto con filtro de empleado
fig3 = px.bar(df, x='Proyecto', y='Eficiencia', title='Eficiencia por Proyecto')
fig3.show()

# Convertir la columna 'Fecha' a tipo datetime
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Gráfico interactivo de líneas de fecha y horas por fecha
fig4 = px.line(df, x='Fecha', y='Horas', title='Horas por Fecha')
fig4.show()