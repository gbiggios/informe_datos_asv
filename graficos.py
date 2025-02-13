import pandas as pd
import plotly.express as px
import networkx as nx
import plotly.graph_objects as go

class Graficos:
    def __init__(self, file_path, file_path_estimadas):
        self.df = self.leer_datos(file_path)
        self.df_estimadas = self.leer_datos(file_path_estimadas, fecha=False)

    def leer_datos(self, file_path, fecha=True):
        df = pd.read_excel(file_path, engine='openpyxl')
        if fecha and 'Fecha' in df.columns:
            df['Fecha'] = pd.to_datetime(df['Fecha'])
        return df

    def calcular_eficiencia(self, group_by='Proyecto'):
        df_grouped = self.df.groupby(group_by).agg({'Tarea': 'count', 'Horas': 'sum'}).reset_index()
        df_grouped['Eficiencia'] = df_grouped['Tarea'] / df_grouped['Horas']
        return df_grouped

    def grafico_suma_horas_proyecto(self):
        df_grouped = self.df.groupby('Proyecto', as_index=False)['Horas'].sum()
        df_grouped = df_grouped.sort_values(by='Horas', ascending=False)
        fig = px.bar(df_grouped, x='Proyecto', y='Horas', color='Proyecto', title='Suma de Horas por Proyecto', height=800)
        return fig

    def grafico_suma_horas_empleado(self):
        df_grouped = self.df.groupby('Empleado', as_index=False)['Horas'].sum()
        fig = px.bar(df_grouped, x='Empleado', y='Horas', color='Empleado', title='Suma de Horas por Empleado', height=800)
        return fig

    def grafico_eficiencia_proyecto(self):
        df_grouped = self.calcular_eficiencia(group_by='Proyecto')
        fig = px.bar(df_grouped, x='Proyecto', y='Eficiencia', color='Proyecto', title='Eficiencia por Proyecto', height=800)
        return fig

    def grafico_horas_fecha(self):
        df_grouped = self.df.groupby('Fecha').sum().reset_index()
        fig = px.line(df_grouped, x='Fecha', y='Horas', title='Suma de Horas por Fecha', height=800)
        fig.update_xaxes(dtick="D", tickformat="%d-%m-%Y")
        return fig

    def proyectos_conhoras_sinhoras(self):
        horas_true = 21
        horas_false = 26
        data = {'Estado': ['Con Horas', 'Sin Horas'], 'Cantidad': [horas_true, horas_false]}
        fig = px.pie(data, names='Estado', values='Cantidad', title='Porcentaje proyectos con horas y sin horas')
        return fig

    def grafico_dispersion_eficiencia_empleado(self):
        df_grouped = self.calcular_eficiencia(group_by='Empleado')
        df_grouped = df_grouped.sort_values(by='Eficiencia')
        fig = px.scatter(df_grouped, x='Empleado', y='Eficiencia', color='Empleado', title='Dispersión Eficiencia de Empleados')
        return fig

    def grafico_dispersion_horas_tareas_proyecto(self):
        df_grouped = self.df.groupby('Proyecto', as_index=False).agg({'Tarea': 'count', 'Horas': 'sum'})
        fig = px.scatter(df_grouped, x='Tarea', y='Horas', color='Proyecto', title='Dispersión Horas - Tareas entre proyectos', height=600)
        return fig

    def grafico_horas_tareas_frecuencia(self):
        df_grouped_horas = self.df.groupby('Tarea')['Horas'].sum().reset_index()
        df_grouped_horas = df_grouped_horas.sort_values(by='Horas', ascending=False)
        df_grouped_frecuencia = self.df.groupby('Tarea').size().reset_index(name='Frecuencia')
        df_grouped_frecuencia = df_grouped_frecuencia.sort_values(by='Frecuencia', ascending=False)
        fig_horas = px.bar(df_grouped_horas, x='Tarea', y='Horas', title='Horas por Tarea (Mayor a Menor)', height=800)
        fig_frecuencia = px.bar(df_grouped_frecuencia, x='Tarea', y='Frecuencia', title='Frecuencia de Tareas (Mayor a Menor)', height=800)
        return fig_horas, fig_frecuencia

    def tendencia_horas_por_proyecto(self):
        df_grouped = self.df.groupby(['Proyecto', 'Fecha'])['Horas'].sum().reset_index()
        projects = df_grouped['Proyecto'].unique()
        return df_grouped, projects

    def grafico_desviacion_horas(self):
        # Agrupar por 'Nombre' y sumar las 'Horas'
        df_registradas = self.df.groupby('Proyecto')['Horas'].sum().reset_index()
        
        # Renombrar la columna para evitar conflictos
        df_registradas.rename(columns={'Proyecto': 'Nombre', 'Horas': 'Horas Registradas'}, inplace=True)
        
        # Unir los dataframes en base al nombre del proyecto
        df_merged = pd.merge(self.df_estimadas[['Nombre', 'Horas Estimadas del Proyecto']], df_registradas, on='Nombre')
        
        # Calcular la desviación
        df_merged['Desviación'] = df_merged['Horas Estimadas del Proyecto'] - df_merged['Horas Registradas']
        
        # Crear el gráfico de área
        fig = px.area(df_merged, x='Nombre', y='Desviación', title='Diferencia entre Horas Estimadas y Horas Registradas', color='Nombre',height=800)
        
        return fig