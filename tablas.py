import pandas as pd
import plotly.graph_objects as go

class Tabla:
    def __init__(self, file_path):
        self.df = self.leer_datos(file_path)

    def leer_datos(self, file_path):
        df = pd.read_excel(file_path, engine='openpyxl')
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        return df

    def crear_tabla(self, df_filtrado):
        """Crea una tabla usando Plotly a partir de un DataFrame dado."""
        fig = go.Figure(data=[go.Table(
            header=dict(values=['Proyecto', 'Empleado', 'Tarea', 'Fecha', 'Horas'],
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[df_filtrado['Proyecto'],
                               df_filtrado['Empleado'],
                               df_filtrado['Tarea'],
                               df_filtrado['Fecha'],
                               round(df_filtrado['Horas'], 2)],
                       fill_color='lavender',
                       align='left'))
        ])
        fig.update_layout(title='Tabla Dinámica', titlefont_size=16)
        return fig

    def tabla_suma_horas_proyecto(self):
        """Crea una tabla que muestra la suma de horas por proyecto."""
        df_agrupado = self.df.groupby('Proyecto', as_index=False)['Horas'].sum()
        fig = go.Figure(data=[go.Table(
            header=dict(values=['Proyecto', 'Suma de Horas'],
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[df_agrupado['Proyecto'], round(df_agrupado['Horas'], 2)],
                       fill_color='lavender',
                       align='left'))
        ])
        fig.update_layout(
            title='Suma de Horas por Proyecto',
            titlefont_size=16
        )
        return fig
    
    def tabla_suma_horas_empleado(self):
        """Crea una tabla que muestra la suma de horas por empleado."""
        df_agrupado = self.df.groupby('Empleado', as_index=False)['Horas'].sum()
        fig = go.Figure(data=[go.Table(
            header=dict(values=['Empleado', 'Suma de Horas'],
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[df_agrupado['Empleado'], round(df_agrupado['Horas'], 2)],
                       fill_color='lavender',
                       align='left'))
        ])
        fig.update_layout(
            title='Suma de Horas por Empleado',
            titlefont_size=16
        )
        return fig

    def tabla_desviacion_horas(self, df_estimadas):
        """Crea una tabla que muestra la desviación entre horas estimadas y horas registradas."""
        # Agrupar por 'Nombre' y sumar las 'Horas'
        df_registradas = self.df.groupby('Proyecto')['Horas'].sum().reset_index()
        
        # Renombrar la columna para evitar conflictos
        df_registradas.rename(columns={'Proyecto': 'Nombre', 'Horas': 'Horas Registradas'}, inplace=True)
        
        # Unir los dataframes en base al nombre del proyecto
        df_merged = pd.merge(df_estimadas[['Nombre', 'Horas Estimadas del Proyecto']], df_registradas, on='Nombre')
        
        # Calcular la desviación
        df_merged['Desviación'] = df_merged['Horas Estimadas del Proyecto'] - df_merged['Horas Registradas']
        
        # Calcular la suma total de la desviación
        total_desviacion = df_merged['Desviación'].sum()
        
        # Añadir una fila para la suma total de la desviación
        total_row = pd.DataFrame([['Total', '', '', total_desviacion]], columns=['Nombre', 'Horas Estimadas del Proyecto', 'Horas Registradas', 'Desviación'])
        df_merged = pd.concat([df_merged, total_row], ignore_index=True)
        
        # Crear la tabla de desviación
        fig = go.Figure(data=[go.Table(
            header=dict(values=['Nombre', 'Horas Estimadas del Proyecto', 'Horas Registradas', 'Desviación'],
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[df_merged['Nombre'],
                               round(df_merged['Horas Estimadas del Proyecto'], 2),
                               round(df_merged['Horas Registradas'], 2),
                               round(df_merged['Desviación'], 2)],
                       fill_color='lavender',
                       align='left'))
        ])
        
        fig.update_layout(title='Desviación entre Horas Estimadas y Horas Registradas', titlefont_size=16)
        
        return fig