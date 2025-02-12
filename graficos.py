import pandas as pd
import plotly.express as px
import networkx as nx
import plotly.graph_objects as go

class Graficos:
    def __init__(self, file_path):
        self.df = self.leer_datos(file_path)

    def leer_datos(self, file_path):
        df = pd.read_excel(file_path, engine='openpyxl')
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        return df

    def calcular_eficiencia(self, group_by='Proyecto'):
        """
        Calcula la eficiencia por proyecto o empleado.

        Args:
            group_by (str): La columna por la que se agrupará el DataFrame (por defecto 'Proyecto').
            Puede ser 'Proyecto' o 'Empleado'.

        Returns:
            pd.DataFrame: Un DataFrame con la eficiencia calculada.
        """
        df_grouped = self.df.groupby(group_by).agg({'Tarea': 'count', 'Horas': 'sum'}).reset_index()
        df_grouped['Eficiencia'] = df_grouped['Tarea'] / df_grouped['Horas']
        return df_grouped

    def grafico_suma_horas_proyecto(self):
        df_grouped = self.df.groupby('Proyecto',as_index=False)['Horas'].sum()
        fig = px.bar(df_grouped,
                     x='Proyecto',
                     y='Horas',
                     color='Proyecto',
                     title='Suma de Horas por Proyecto',
                     height=800
                     )
        return fig

    def grafico_suma_horas_empleado(self):
        df_grouped = self.df.groupby('Empleado',as_index=False)['Horas'].sum()
        fig = px.bar(df_grouped,
                     x='Empleado',
                     y='Horas', 
                     color='Empleado',
                     title='Suma de Horas por Empleado', 
                     height=800)
        return fig

    def grafico_eficiencia_proyecto(self):
        df_grouped = self.calcular_eficiencia(group_by='Proyecto')
        fig = px.bar(df_grouped,
                     x='Proyecto',
                     y='Eficiencia', 
                     color='Proyecto',
                     title='Eficiencia por Proyecto',
                     height=800)
        return fig

    def grafico_horas_fecha(self):
        # Agrupar por fecha y sumar las horas
        df_grouped = self.df.groupby('Fecha').sum().reset_index()
        
        # Crear el gráfico de líneas
        fig = px.line(df_grouped, x='Fecha', y='Horas', title='Suma de Horas por Fecha', height=800)
        fig.update_xaxes(dtick="D", tickformat="%d-%m-%Y")
        return fig

    def proyectos_conhoras_sinhoras(self):
        horas_true = 21
        horas_false = 26
        data = {
            'Estado': ['Con Horas','Sin Horas'],
            'Cantidad':[horas_true,horas_false]
        }

        fig = px.pie(data, names='Estado', values= 'Cantidad', title='Porcentaje proyectos con horas y sin horas')
        return fig 
    
    def grafico_dispersion_eficiencia_empleado(self):
        df_grouped = self.calcular_eficiencia(group_by='Empleado')
        df_grouped = df_grouped.sort_values(by='Eficiencia')  # Ordenar por Eficiencia
        fig = px.scatter(df_grouped,
                         x='Empleado',
                         y='Eficiencia',
                         color='Empleado',
                         title='Dispersión Eficiencia de Empleados')
        return fig
    
    def grafico_dispersion_horas_tareas_proyecto(self):
        df_grouped = self.df.groupby('Proyecto', as_index=False).agg({'Tarea': 'count', 'Horas': 'sum'})

        fig= px.scatter(df_grouped,
                        x='Tarea',
                        y='Horas',
                        color='Proyecto',
                        title='Dispersión Horas - Tareas entre proyectos',
                        height=600)
        
        return fig

    def grafico_horas_tareas_frecuencia(self):
        # Agrupar por tarea y sumar las horas
        df_grouped_horas = self.df.groupby('Tarea')['Horas'].sum().reset_index()
        df_grouped_horas = df_grouped_horas.sort_values(by='Horas', ascending=False)  # Ordenar por horas

        # Agrupar por tarea y contar la frecuencia usando size()
        df_grouped_frecuencia = self.df.groupby('Tarea').size().reset_index(name='Frecuencia')
        df_grouped_frecuencia = df_grouped_frecuencia.sort_values(by='Frecuencia', ascending=False)  # Ordenar por frecuencia

        # Crear el gráfico de barras para las horas
        fig_horas = px.bar(df_grouped_horas, x='Tarea', y='Horas', title='Horas por Tarea (Mayor a Menor)', height=800)

        # Crear el gráfico de barras para la frecuencia
        fig_frecuencia = px.bar(df_grouped_frecuencia, x='Tarea', y='Frecuencia', title='Frecuencia de Tareas (Mayor a Menor)', height=800)

        return fig_horas, fig_frecuencia