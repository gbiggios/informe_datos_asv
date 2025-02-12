import pandas as pd
import plotly.express as px
import networkx as nx
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
            header=dict(values=['Proyecto', 'Empleado', 'Tarea','Fecha', 'Horas'],
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
            cells=dict(values=[df_agrupado['Proyecto'], round(df_agrupado['Horas'],2)],
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
            cells=dict(values=[df_agrupado['Empleado'], round(df_agrupado['Horas'],2)],
                    fill_color='lavender',
                    align='left'))
        ])
        fig.update_layout(
            title='Suma de Horas por Empleado',
            titlefont_size=16
        )
        return fig
