import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- CLASE OBLIGATORIA (POO) ---
class DataAnalyzer:
    def __init__(self, data):
        self.df = data

    def obtener_info_general(self):
        # Retorna tipos de datos y suma de nulos
        return self.df.dtypes, self.df.isnull().sum()

    def clasificar_variables(self):
        # Identifica automáticamente variables numéricas y categóricas
        num = self.df.select_dtypes(include=['number']).columns.tolist()
        cat = self.df.select_dtypes(include=['object']).columns.tolist()
        return num, cat

# --- CONFIGURACIÓN E INTERFAZ ---
st.set_page_config(page_title="Bank Marketing Analysis", layout="wide")

# Sidebar con menú obligatorio
st.sidebar.title("Menú Principal")
menu = st.sidebar.radio("Navegación", ["Módulo 1: Home", "Módulo 2: Carga de Datos", "Módulo 3: EDA", "Conclusiones"])

# MÓDULO 1: HOME (Presentación)
if menu == "Módulo 1: Home":
    st.title("Proyecto: Análisis Exploratorio Bank Marketing")
    st.write("Análisis integral para entender la caída de la efectividad del 12% al 8% en las campañas comerciales.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Datos del Autor")
        st.write("- **Nombre:** Kristel Palacios")
        st.write("- **Curso:** Especialización Python for Analytics")
        st.write("- **Año:** 2026")
    
    with col2:
        st.subheader("Tecnologías utilizadas")
        st.write("Python, Pandas, Streamlit, Matplotlib, Seaborn")

# MÓDULO 2: CARGA DEL DATASET
elif menu == "Módulo 2: Carga de Datos":
    st.header("📂 Carga del Dataset")
    archivo = st.file_uploader("Carga el archivo BankMarketing.csv", type=["csv"])
    
    if archivo:
        # Cargamos el archivo (sep=None para detectar comas o puntos y coma)
        df = pd.read_csv(archivo, sep=None, engine='python')
        st.session_state['df'] = df # Guardamos los datos para usarlos en el EDA
        st.success("¡Archivo cargado correctamente!")
        
        st.write("### Vista previa (head)")
        st.dataframe(df.head())
        
        st.write(f"**Dimensiones del dataset:** {df.shape[0]} filas y {df.shape[1]} columnas")
    else:
        st.info("Por favor, sube el archivo .csv para comenzar el análisis.")

# --- MÓDULO 3: EDA (Núcleo del proyecto) ---
elif menu == "Módulo 3: EDA":
    if 'df' in st.session_state:
        df = st.session_state['df']
        analyzer = DataAnalyzer(df)
        st.title("📊 Análisis Exploratorio de Datos (EDA)")

        # Pestañas para organizar los 10 ítems
        tab_gen, tab_dist, tab_bi = st.tabs(["Estadística y Tipos", "Distribuciones", "Análisis de Campaña"])

        with tab_gen:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Ítem 1: Información General")
                st.write(df.dtypes)
                st.write(f"Nulos totales: {df.isnull().sum().sum()}")
            
            with col2:
                st.subheader("Ítem 2: Clasificación de Variables")
                # Aquí llamamos a la función que corregimos en la clase
                num_vars, cat_vars = analyzer.clasificar_variables()
                st.write(f"**Numéricas:** {len(num_vars)}")
                st.write(f"**Categóricas:** {len(cat_vars)}")

            st.subheader("Ítem 3: Estadísticas Descriptivas")
            st.write(df.describe())

            st.subheader("Ítem 4: Análisis de Faltantes")
            st.write(df.isna().sum())

        with tab_dist:
            st.subheader("Ítem 5: Distribución de Variables Numéricas")
            var_num = st.selectbox("Selecciona una variable numérica:", df.select_dtypes(include=['number']).columns)
            fig, ax = plt.subplots()
            sns.histplot(df[var_num], kde=True, ax=ax, color="skyblue")
            st.pyplot(fig)

            st.subheader("Ítem 6: Análisis de Variables Categóricas")
            var_cat = st.selectbox("Selecciona una variable categórica:", df.select_dtypes(include=['object']).columns)
            fig2, ax2 = plt.subplots()
            df[var_cat].value_counts().plot(kind='bar', ax=ax2, color="orange")
            st.pyplot(fig2)

        with tab_bi:
            st.subheader("Ítem 7: Edad vs Aceptación (y)")
            # Usamos una visualización de caja para ver la distribución por grupo
            fig3, ax3 = plt.subplots()
            sns.boxplot(x='y', y='age', data=df, ax=ax3)
            st.pyplot(fig3)

            st.subheader("Ítem 8: Educación vs Aceptación")
            ct = pd.crosstab(df['education'], df['y'])
            st.bar_chart(ct)

            st.subheader("Ítem 9: Análisis Dinámico de Parámetros")
            filtro_edad = st.slider("Filtrar por rango de edad:", int(df['age'].min()), int(df['age'].max()), (20, 50))
            df_filtrado = df[(df['age'] >= filtro_edad[0]) & (df['age'] <= filtro_edad[1])]
            st.write(f"Clientes en este rango: {len(df_filtrado)}")

            st.subheader("Ítem 10: Hallazgos Clave")
            st.info("Se observa una mayor concentración de aceptación en clientes con mayor duración de contacto.")

# --- CONCLUSIONES ---
elif menu == "Conclusiones":
    st.title("✅ Conclusiones del Análisis")
    st.write("1. La duración de la llamada es el factor más influyente en la conversión.")
    st.write("2. Clientes con educación universitaria tienden a aceptar más la campaña.")
    st.write("3. El canal 'celular' es más efectivo que el 'teléfono fijo'.")
    st.write("4. Existe una alta concentración de clientes jóvenes que no han sido contactados previamente.")
    st.write("5. Se recomienda priorizar contactos de más de 200 segundos para mejorar el ratio del 8%.")

# Firma al final de la aplicación
st.write("---")
st.caption("Elaborado por Kristel Palacios")