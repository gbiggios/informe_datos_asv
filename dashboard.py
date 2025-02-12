import dash
from dash import dcc, html, Input, Output
import graficos  # Asegúrate de que este archivo contiene la clase Graficos
import tablas

# Leer los datos
file_path = 'tabla-normalizada.xlsx'
graficos_instance = graficos.Graficos(file_path)  # Crear una instancia de la clase Graficos
tablas_instante = tablas.Tabla(file_path)

# Crear la aplicación Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard de Gráficos Interactivos"),
    dcc.Tabs([
        dcc.Tab(label='Porcentaje de proyectos con horas',
                children=[
                    dcc.Graph(
                        id='pocentaje-de-proyectos',
                        figure=graficos_instance.proyectos_conhoras_sinhoras()  # Usar la instancia
                    )
                ]
                ),        
        dcc.Tab(label='Tabla Dinámica',
                children=[
                    html.Div([
                        html.Label('Selecciona un Empleado:'),
                        dcc.Dropdown(
                            id='empleado-dropdown',
                            options=[{'label': emp, 'value': emp} for emp in tablas_instante.df['Empleado'].unique()],
                            value=None,
                            multi=True
                        ),
                        html.Label('Selecciona un Proyecto:'),
                        dcc.Dropdown(
                            id='proyecto-dropdown',
                            options=[{'label': proj, 'value': proj} for proj in tablas_instante.df['Proyecto'].unique()],
                            value=None,
                            multi=True
                        ),
                        dcc.Graph(id='tabla-dinamica')
                    ])
                ]
                ),
        dcc.Tab(label='Suma de Horas por Proyecto', children=[
            dcc.Graph(
                id='suma-horas-proyecto',
                figure=graficos_instance.grafico_suma_horas_proyecto()  # Usar la instancia
            ),
            dcc.Graph(
                id='tabla-suma-horas-proyecto',
                figure=tablas_instante.tabla_suma_horas_proyecto()
            )
        ]),
        dcc.Tab(label='Suma de Horas por Empleado', children=[
            dcc.Graph(
                id='suma-horas-empleado',
                figure=graficos_instance.grafico_suma_horas_empleado()  # Usar la instancia
            ),
            dcc.Graph(
                id='tabla-suma-horas-empleado',
                figure=tablas_instante.tabla_suma_horas_empleado()
            )
        ]),
        dcc.Tab(label='Eficiencia por Proyecto', children=[
            dcc.Graph(
                id='eficiencia-proyecto',
                figure=graficos_instance.grafico_eficiencia_proyecto()  # Usar la instancia
            )
        ]),
        dcc.Tab(label='Horas por Fecha', children=[
            dcc.Graph(
                id='horas-fecha',
                figure=graficos_instance.grafico_horas_fecha()  # Usar la instancia
            )
        ]),
        dcc.Tab(label='Dispersión Empleados', children=[
            dcc.Graph(
                id='dispersion-empleados',
                figure=graficos_instance.grafico_dispersion_eficiencia_empleado()
            )
        ]),
                dcc.Tab(label='Dispersión Tarea-Horas', children=[
            dcc.Graph(
                id='dispersion-Tarea-Horas',
                figure=graficos_instance.grafico_dispersion_horas_tareas_proyecto()
            )
        ]),
        dcc.Tab(label='Horas y Frecuencia por Tarea', children=[
            dcc.Graph(
                id='horas-tareas',
                figure=graficos_instance.grafico_horas_tareas_frecuencia()[0]  # Gráfico de horas
            ),
            dcc.Graph(
                id='frecuencia-tareas',
                figure=graficos_instance.grafico_horas_tareas_frecuencia()[1]  # Gráfico de frecuencia
            )
        ])
    ])
])

@app.callback(
    Output('tabla-dinamica', 'figure'),
    [Input('empleado-dropdown', 'value'),
     Input('proyecto-dropdown', 'value')]
)
def actualizar_tabla(empleado_seleccionado, proyecto_seleccionado):
    df_filtrado = tablas_instante.df

    if empleado_seleccionado:
        df_filtrado = df_filtrado[df_filtrado['Empleado'].isin(empleado_seleccionado)]
    if proyecto_seleccionado:
        df_filtrado = df_filtrado[df_filtrado['Proyecto'].isin(proyecto_seleccionado)]

    return tablas_instante.crear_tabla(df_filtrado)

if __name__ == '__main__':
    app.run_server(debug=True)