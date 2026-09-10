import os
import streamlit as st
import plotly.express as px
from contexto.exploracion import frecuencia_ngramas
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

DEBUG = False
st.set_page_config(layout="wide")

# Carpeta donde vive este script (streamlit/). Usar rutas absolutas basadas
# en __file__ para que la app encuentre datos_limpios.xlsx y logoNuevo.jpg
# sin importar desde qué directorio se lance "streamlit run".
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_DATOS = os.path.join(BASE_DIR, "datos_limpios.xlsx")
RUTA_LOGO = os.path.join(BASE_DIR, "logoNuevo.jpg")

def nube_palabras(textos, n_grama):
    dictu = frecuencia_ngramas(texto=textos, n_grama=n_grama)
    nube = WordCloud(background_color='white', prefer_horizontal=0.8, mask=None, random_state=1234, max_words=100, collocations=False)
    figura = nube.generate_from_frequencies(dictu)
    fig = plt.figure(figsize=(20, 20))
    plt.imshow(figura, interpolation='bilinear')
    plt.axis("off")
    return fig

def ajustar_lista(lista):
    nueva_lista = []
    for i in lista:
        nueva_lista.append(i.split(" (")[0])
    return nueva_lista

st.image(RUTA_LOGO, width=400)
st.title('Análisis diálogos regionales - PND 2022 - 2026')
st.markdown(""" ###### Desarrollado por la Unidad de Científicos de Datos (UCD)""")
st.markdown(""" `Contacto:` ucd@dnp.gov.co  -  `Fecha de actualización:` 26/09/2022 9:45 p.m.""")

df = pd.read_excel(RUTA_DATOS)
new_df = df.copy()

# -----------------------------------------------------------------------
st.markdown("""***""")
st.markdown(""" ## Filtros """)

# -----------------------------------------------------------------------
# Filtro - Día
# dia = new_df['Día en el que se desarrolla la mesa de trabajo.'].value_counts().index.tolist()
# freq_dia = new_df['Día en el que se desarrolla la mesa de trabajo.'].value_counts().values.tolist()
# opciones_dia = [f'{subregion} ({str(freq)})' for subregion, freq in zip(dia, freq_dia)]

# dia_selected = st.multiselect( label='Día de trabajo', options=opciones_dia)

# if (dia_selected != []):
#     new_df = new_df[new_df['Día en el que se desarrolla la mesa de trabajo.'].isin(ajustar_lista(dia_selected))]

# -----------------------------------------------------------------------
# Filtro - Subregión
subregiones = new_df['Subregión del Dialogo Regional Vinculante.'].value_counts().index.tolist()
freq_subregiones = new_df['Subregión del Dialogo Regional Vinculante.'].value_counts().values.tolist()
opciones_subregiones = [f'{subregion} ({str(freq)})' for subregion, freq in zip(subregiones, freq_subregiones)]

subregiones_selected = st.multiselect( label='Subregión', options=opciones_subregiones)

if (subregiones_selected != []):
    new_df = new_df[new_df['Subregión del Dialogo Regional Vinculante.'].isin(ajustar_lista(subregiones_selected))]

# -----------------------------------------------------------------------
# Filtro - Transformación
transformaciones = new_df['transformación'].value_counts().index.tolist()
freq_transformaciones = new_df['transformación'].value_counts().values.tolist()
opciones_transformaciones = [f'{transformacion} ({str(freq)})' for transformacion, freq in zip(transformaciones, freq_transformaciones)]

transformaciones_selected = st.multiselect( label='Transformación que se aborda', options=opciones_transformaciones)

if (transformaciones_selected != []):
    new_df = new_df[new_df['transformación'].isin(ajustar_lista(transformaciones_selected))]

# -----------------------------------------------------------------------
# Filtro - Grupos poblacionales
def get_poblaciones(poblaciones):
    pob = []
    for r in poblaciones:
        r_temp = str(r).split(";")
        for rt in r_temp:
            if len(rt) > 0:
                pob.append(rt)
    results = pd.Series(pob)
    return results.value_counts().index.tolist(), results.value_counts().values.tolist()

grupos_poblacionales, freq_grupos_poblacionales = get_poblaciones(new_df['Presencia de grupos poblacionales en la mesa de trabajo.'].tolist())
opciones_grupos_poblacionales = [f'{grupo_pob} ({str(freq)})' for grupo_pob, freq in zip(grupos_poblacionales, freq_grupos_poblacionales)]

grupos_poblacionales_selected = st.multiselect( label='Contiene grupo poblacional', options=opciones_grupos_poblacionales)

if (len(grupos_poblacionales_selected) > 0):
    new_df = new_df[new_df['Presencia de grupos poblacionales en la mesa de trabajo.'].str.contains('|'.join(ajustar_lista(grupos_poblacionales_selected)))]

# -----------------------------------------------------------------------
# Filtro - Alcance territorial
alcance_territorial = new_df['Alcance territorial del reto (problemática).'].value_counts().index.tolist()
freq_alcance_territorial = new_df['Alcance territorial del reto (problemática).'].value_counts().values.tolist()
opciones_alcance_territorial = [f'{transformacion} ({str(freq)})' for transformacion, freq in zip(alcance_territorial, freq_alcance_territorial)]

alcance_territorial_selected = st.multiselect( label='Alcance territorial del reto (problemática)', options=opciones_alcance_territorial)

if (alcance_territorial_selected != []):
    new_df = new_df[new_df['Alcance territorial del reto (problemática).'].isin(ajustar_lista(alcance_territorial_selected))]

# -----------------------------------------------------------------------
# Filtro - Sectores en los que se inscribe el reto acordado
def get_sectores(poblaciones):
    pob = []
    for r in poblaciones:
        r_temp = str(r).split(";")
        for rt in r_temp:
            if len(rt) > 0 and rt != 'nan':
                pob.append(rt)
    results = pd.Series(pob)
    return results.value_counts().index.tolist(), results.value_counts().values.tolist()

sectores_inscribe_reto, freq_sectores_inscribe_reto = get_sectores(new_df['Sectores en los que se inscribe el reto acordado.'].tolist())
opciones_sectores_inscribe_reto = [f'{grupo_pob} ({str(freq)})' for grupo_pob, freq in zip(sectores_inscribe_reto, freq_sectores_inscribe_reto)]

sectores_inscribe_reto_selected = st.multiselect( label='Contiene grupo poblacional', options=opciones_sectores_inscribe_reto)

if (len(sectores_inscribe_reto_selected) > 0):
    new_df = new_df[new_df['Sectores en los que se inscribe el reto acordado.'].str.contains('|'.join(ajustar_lista(sectores_inscribe_reto_selected)))]

# -----------------------------------------------------------------------
# mensaje - número de registros
# st.markdown(f""" #### Número de registros: {new_df.shape[0]} de {df.shape[0]} """)

# -----------------------------------------------------------------------
st.markdown("""***""")
tab1, tab2 = st.tabs(["Día 1: Mesa de trabajo de identificación", "Día 2: Mesa de trabajo de selección"])

with tab1:
    st.header("Día 1: Mesa de trabajo de identificación")
    new_df_1 = new_df[new_df['Día en el que se desarrolla la mesa de trabajo.'].isin(['Día 1: Mesa de trabajo de identificación'])]
    st.markdown(f""" #### Número de registros: {new_df_1.shape[0]} de {df.shape[0]} """)
    # -----------------------------------------------------------------------
    # Primera sección
    st.markdown("""***""")

    value = new_df_1['Seleccione la transformación que se aborda en la mesa de trabajo.'].value_counts().index.tolist()
    count = new_df_1['Seleccione la transformación que se aborda en la mesa de trabajo.'].value_counts().values.tolist()

    df_pie_1 = pd.DataFrame(list(zip(value, count)), columns =['value', 'count'])
    fig_1 = px.pie(df_pie_1, values='count', names='value',)

    grupos_poblacionales_2, freq_grupos_poblacionales_2 = get_poblaciones(new_df_1['Presencia de grupos poblacionales en la mesa de trabajo.'].tolist())
    df_pie_2 = pd.DataFrame(list(zip(grupos_poblacionales_2, freq_grupos_poblacionales_2)), columns =['value', 'count'])
    fig_2 = px.pie(df_pie_2, values='count', names='value')

    pie_col1, pie_col2 = st.columns(2)
    with pie_col1:
        st.markdown("### Distribución de registros por transformación abordada")
        # st.markdown(f""" ### Unigramas """)
        st.plotly_chart(fig_1, use_container_width=True, config=dict(displayModeBar=False))

    with pie_col2:
        st.markdown("### Distribución de registros por grupos poblacionales")
        # st.markdown(f""" ### Bigramas """)
        st.plotly_chart(fig_2, use_container_width=True, config=dict(displayModeBar=False))

    # -----------------------------------------------------------------------
    # Limpieza datos para las nubes de palabras

    lista_terminos_1 = []
    for my_list in new_df_1.reto_kws_clean.tolist():
        if str(my_list) != 'nan':
            lista_terminos_1.extend(my_list.split(","))
    terminos_1 = ' '.join(lista_terminos_1)


    lista_terminos_2 = []
    for my_list in new_df_1.antecendentes_clean.tolist():
        if str(my_list) != 'nan':
            lista_terminos_2.extend(my_list.split(","))
    terminos_2 = ' '.join(lista_terminos_2)


    lista_terminos_3 = []
    for my_list in new_df_1.alternativas_clean.tolist():
        if str(my_list) != 'nan':
            lista_terminos_3.extend(my_list.split(","))
    terminos_3 = ' '.join(lista_terminos_3)


    lista_terminos_4 = []
    for my_list in new_df_1.propuestas_clean.tolist():
        if str(my_list) != 'nan':
            lista_terminos_4.extend(my_list.split(","))
    terminos_4 = ' '.join(lista_terminos_4)


    lista_terminos_5 = []
    for my_list in new_df_1.observaciones_clean.tolist():
        if str(my_list) != 'nan':
            lista_terminos_5.extend(my_list.split(","))
    terminos_5 = ' '.join(lista_terminos_5)

    if not DEBUG:
        # '--------------------------------------------------------------------------------------'
        # Nubes de palabras - Retos identificados

        st.markdown("""***""")
        st.markdown(""" ## Retos identificados """)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f""" ### Unigramas """)
            if len(terminos_1) == 0:
                st.markdown(""" Sin información""")
            else:
                st.pyplot(nube_palabras(terminos_1, 1), clear_figure=True)

        with col2:
            st.markdown(f""" ### Bigramas """)
            if len(terminos_1) == 0:
                st.markdown(""" Sin información""")
            else:
                st.pyplot(nube_palabras(terminos_1, 2), clear_figure=True)

        # '--------------------------------------------------------------------------------------'
        # Nubes de palabras - Antecedentes

        st.markdown("""***""")
        st.markdown(""" ## Antecedentes """)
        col3, col4 = st.columns(2)
        with col3:
            st.markdown(f""" ### Unigramas """)
            if len(terminos_2) == 0:
                st.markdown(""" Sin información""")
            else:
                st.pyplot(nube_palabras(terminos_2, 1), clear_figure=True)

        with col4:
            st.markdown(f""" ### Bigramas """)
            if len(terminos_2) == 0:
                st.markdown(""" Sin información""")
            else:
                st.pyplot(nube_palabras(terminos_2, 2), clear_figure=True)

        # -----------------------------------------------------------------------
        # Nubes de palabras - Alternativas identificadas

        st.markdown("""***""")
        st.markdown(""" ## Alternativas identificadas """)
        col5, col6 = st.columns(2)
        with col5:
            st.markdown(f""" ### Unigramas """)
            if len(terminos_3) == 0:
                st.markdown(""" Sin información""")
            else:
                st.pyplot(nube_palabras(terminos_3, 1), clear_figure=True)

        with col6:
            st.markdown(f""" ### Bigramas """)
            if len(terminos_3) == 0:
                st.markdown(""" Sin información""")
            else:
                st.pyplot(nube_palabras(terminos_3, 2), clear_figure=True)

        # -----------------------------------------------------------------------
        # Nubes de palabras - Propuestas

        st.markdown("""***""")
        st.markdown(""" ## Propuestas """)

        col7, col8 = st.columns(2)
        with col7:
            st.markdown(f""" ### Unigramas """)
            if len(terminos_4) == 0:
                st.markdown(""" Sin información""")
            else:
                st.pyplot(nube_palabras(terminos_4, 1), clear_figure=True)

        with col8:
            st.markdown(f""" ### Bigramas """)
            if len(terminos_4) == 0:
                st.markdown(""" Sin información""")
            else:
                st.pyplot(nube_palabras(terminos_4, 2), clear_figure=True)

        # -----------------------------------------------------------------------
        # Nubes de palabras - Observaciones

        st.markdown("""***""")
        st.markdown(""" ## Observaciones """)
        col9, col10 = st.columns(2)
        with col9:
            st.markdown(f""" ### Unigramas """)
            if len(terminos_5) == 0:
                st.markdown(""" Sin información""")
            else:
                st.pyplot(nube_palabras(terminos_5, 1), clear_figure=True)

        with col10:
            st.markdown(f""" ### Bigramas """)
            if len(terminos_5) == 0:
                st.markdown(""" Sin información""")
            else:
                st.pyplot(nube_palabras(terminos_5, 2), clear_figure=True)

        # -----------------------------------------------------------------------

with tab2:
    st.header("Día 2: Mesa de trabajo de identificación")
    new_df_2 = new_df[new_df['Día en el que se desarrolla la mesa de trabajo.'].isin(['Dia 2: Mesa de trabajo de selección'])]
    st.markdown(f""" #### Número de registros: {new_df_2.shape[0]} de {df.shape[0]} """)

    # -----------------------------------------------------------------------
    # Primera sección
    st.markdown("""***""")

    value, count = get_sectores(new_df_2['Afectación poblacional del reto acordado.'].tolist())
    df_pie_1_pag2 = pd.DataFrame(list(zip(value, count)), columns =['value', 'count'])
    fig_1_pag2 = px.pie(df_pie_1_pag2, values='count', names='value')

    sectores_inscribe_reto2, freq_sectores_inscribe_reto2 = get_sectores(new_df_2['Sectores en los que se inscribe el reto acordado.'].tolist())
    df_pie_2_pag2 = pd.DataFrame(list(zip(sectores_inscribe_reto2, freq_sectores_inscribe_reto2)), columns =['value', 'count'])
    fig_2_pag2 = px.pie(df_pie_2_pag2, values='count', names='value')

    pie_col1_pag2, pie_col2_pag2 = st.columns(2)
    with pie_col1_pag2:
        st.markdown("### Afectación poblacional del reto acordado")
        st.plotly_chart(fig_1_pag2, use_container_width=True, config=dict(displayModeBar=False))

    with pie_col2_pag2:
        st.markdown("### Sectores en los que se inscribe el reto acordado")
        st.plotly_chart(fig_2_pag2, use_container_width=True, config=dict(displayModeBar=False))
    
    # -----------------------------------
    value, count = get_sectores(new_df_2['sectores_entidades'].tolist())
    df_pie_3_pag2 = pd.DataFrame(list(zip(value, count)), columns =['value', 'count'])
    fig_3_pag2 = px.pie(df_pie_3_pag2, values='count', names='value')

    value, count = get_sectores(new_df_2['alternativas_cat'].tolist())
    df_pie_4_pag2 = pd.DataFrame(list(zip(value, count)), columns =['value', 'count'])
    fig_4_pag2 = px.pie(df_pie_4_pag2, values='count', names='value')

    pie_col3_pag2, pie_col4_pag2 = st.columns(2)
    with pie_col3_pag2:
        st.markdown("### ¿A qué sector o sectores perteneces las entidades que podrían implementar dicha alternativa?")
        st.plotly_chart(fig_3_pag2, use_container_width=True, config=dict(displayModeBar=False))

    with pie_col4_pag2:
        st.markdown("### Categoría de la alternativa propuesta")
        st.plotly_chart(fig_4_pag2, use_container_width=True, config=dict(displayModeBar=False))

    # -----------------------------------
    value, count = get_sectores(new_df_2['departamentos'].tolist())
    df_pie_5_pag2 = pd.DataFrame(list(zip(value, count)), columns =['value', 'count'])
    fig_5_pag2 = px.pie(df_pie_5_pag2, values='count', names='value')

    st.markdown("### ¿En cuál o cuáles departamentos toma lugar la alternativa planteada?")
    st.plotly_chart(fig_5_pag2, use_container_width=True, config=dict(displayModeBar=False))
    # -----------------------------------------------------------------------
    # Limpieza datos para las nubes de palabras

    lista_terminos_1_pag2 = []
    for my_list in new_df_2.reto_acordado_clean.tolist():
        if str(my_list) != 'nan':
            lista_terminos_1_pag2.extend(my_list.split(","))
    terminos_1_pag2 = ' '.join(lista_terminos_1_pag2)


    lista_terminos_2_pag2 = []
    for my_list in new_df_2.alternativas2_clean.tolist():
        if str(my_list) != 'nan':
            lista_terminos_2_pag2.extend(my_list.split(","))
    terminos_2_pag2 = ' '.join(lista_terminos_2_pag2)


    lista_terminos_3_pag2 = []
    for my_list in new_df_2.observaciones2_clean.tolist():
        if str(my_list) != 'nan':
            lista_terminos_3_pag2.extend(my_list.split(","))
    terminos_3_pag2 = ' '.join(lista_terminos_3_pag2)

    # -----------------------------------------------------------------------
    # Nubes de palabras - Retos acordados

    st.markdown("""***""")
    st.markdown(""" ## Retos acordados """)
    col_nube1_pag2, col_nube2_pag2 = st.columns(2)
    with col_nube1_pag2:
        st.markdown(f""" ### Unigramas """)
        if len(terminos_1_pag2) == 0:
            st.markdown(""" Sin información""")
        else:
            st.pyplot(nube_palabras(terminos_1_pag2, 1), clear_figure=True)

    with col_nube2_pag2:
        st.markdown(f""" ### Bigramas """)
        if len(terminos_1_pag2) == 0:
            st.markdown(""" Sin información""")
        else:
            st.pyplot(nube_palabras(terminos_1_pag2, 2), clear_figure=True)

    # -----------------------------------------------------------------------
    # Nubes de palabras -  antecedes + alternativas

    st.markdown("""***""")
    st.markdown(""" ## Antecedes y Alternativas """)
    col_nube3_pag2, col_nube4_pag2 = st.columns(2)
    with col_nube3_pag2:
        st.markdown(f""" ### Unigramas """)
        if len(terminos_2_pag2) == 0:
            st.markdown(""" Sin información""")
        else:
            st.pyplot(nube_palabras(terminos_2_pag2, 1), clear_figure=True)

    with col_nube4_pag2:
        st.markdown(f""" ### Bigramas """)
        if len(terminos_2_pag2) == 0:
            st.markdown(""" Sin información""")
        else:
            st.pyplot(nube_palabras(terminos_2_pag2, 2), clear_figure=True)

    # -----------------------------------------------------------------------
    # Nubes de palabras -  observaciones 2

    st.markdown("""***""")
    st.markdown(""" ## Observaciones """)
    col_nube5_pag2, col_nube6_pag2 = st.columns(2)
    with col_nube5_pag2:
        st.markdown(f""" ### Unigramas """)
        if len(terminos_2_pag2) == 0:
            st.markdown(""" Sin información""")
        else:
            st.pyplot(nube_palabras(terminos_2_pag2, 1), clear_figure=True)

    with col_nube6_pag2:
        st.markdown(f""" ### Bigramas """)
        if len(terminos_2_pag2) == 0:
            st.markdown(""" Sin información""")
        else:
            st.pyplot(nube_palabras(terminos_2_pag2, 2), clear_figure=True)

    # -----------------------------------------------------------------------
    