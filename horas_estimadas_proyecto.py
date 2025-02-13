import pandas as pd

class Proyecto:
    def __init__(self, file_path_inicial, file_path_normalizada):
        self.file_path_inicial = file_path_inicial
        self.file_path_normalizada = file_path_normalizada
        self.df_inicial = None
        self.df_normalizada = None
        self.filtered_projects_df = None

    def cargar_datos(self):
        # Cargar los datos desde los archivos Excel
        self.df_inicial = pd.read_excel(self.file_path_inicial, engine='openpyxl')
        self.df_normalizada = pd.read_excel(self.file_path_normalizada, engine='openpyxl')

    def filtrar_proyectos(self):
        # Extraer los proyectos y las horas estimadas
        project_hours_df = self.df_inicial[['Nombre', 'Horas Estimadas del Proyecto']]

        # Filtrar los proyectos basados en la planilla normalizada
        self.filtered_projects_df = project_hours_df[project_hours_df['Nombre'].isin(self.df_normalizada['Proyecto'])]

    def obtener_proyectos_filtrados(self):
        # Devolver los proyectos filtrados
        return self.filtered_projects_df
