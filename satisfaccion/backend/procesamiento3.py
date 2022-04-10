import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def editcols(col_value):
    try:
        if np.isnan(col_value):
            return None
    except:
        pass
    
    try:
        return int(col_value)
    except:
        pass
    
    try:
        if col_value in ['Muy insatisfecho','1 Muy insatisfecho/a','1 - Pésimo', '1 Muy Insatisfecho']:
            return 1
        if col_value in ['Muy satisfecho','7 Muy satisfecho/a', '7 - Excelente','7 Muy Satisfecho']:
            return 7

        if col_value in ['No sabe', 'Prefiero no responder', 'No responde']:
            return None
    except:
        pass
    
    try:
        splitted_col_value = col_value.split('.')
        return int(splitted_col_value[0])
    except:
        return int(col_value)


def rango_uno_a_siete(col_value):
    if col_value > 7:
        return None
    return col_value


def rango_ponderador(col_value):
    try:
        return float(col_value.replace(",","."))
    except:
        return col_value


def rango_edad(col_value):
    try:
        col_value = int(col_value)
    except:
        return None
        
    if col_value>=18 and col_value<35:
        return '18 a 34'
    if col_value>=35 and col_value<45:
        return '35 a 44'
    if col_value>=45 and col_value<55:
        return '45 a 44'
    if col_value>=55:
        return '55 y mas'
    return 'No informa'

def add_labels(ax):
    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy() 
        ax.text(x+width/2, 
                y+height/2, 
                '{:.1f} %'.format(height), 
                horizontalalignment='center', 
                verticalalignment='center')


def rango_habbase_escala_capredena(col_value):
    try:
        if col_value <4.5:
            return "No habilitado"
        if col_value >=5.5 and col_value<=7:
            return "Habilitado"
        if col_value >=4.5 and col_value<5.5:
            return "Medianamente"
    except:
        return col_value

def rango_habbase_escala_capredenda(col_value):
    try:
        if col_value <4.5:
            return "No habilitado"
        if col_value >=5.5 and col_value<=7:
            return "Habilitado"
        if col_value >=4.5 and col_value<5.5:
            return "Medianamente"
    except:
        return col_value



def categoria_number_to_string_habbase(col_value):
    try:
        if int(col_value) ==1:
            return "No habilitado"
        if int(col_value) ==2:
            return "Habilitado"
        if int(col_value) ==3:
            return "Medianamente"
        return None
    except:
        return col_value




instituciones = [
    # {'codigo': 'Capredena', 'nombre_archivo':'2020_ESU_CAPREDENA'},
    # {'codigo': 'SII', 'nombre_archivo':'2020_ESU_SII'},
    {'codigo': 'Aduana', 'nombre_archivo':'2020_ESU_ADUANAS'},
     # {'codigo': ''},
    # {'codigo': 'SERNAC', 'nombre_archivo':'2020_ESU_SERNAC'},
    # {'codigo': 'Tesoreria', 'nombre_archivo':'2020_ESU_TESORERIA'},
    # {'codigo': 'AN', 'nombre_archivo':'2020_ESU_AN'},
    # {'codigo': 'Chilecompra', 'nombre_archivo':'2020_ESU_CHILECOMPRA'},
    # {'codigo': 'Compin', 'nombre_archivo':'2020_ESU_COMPIN'},
    # {'codigo': 'DICREP', 'nombre_archivo':'2020_ESU_DICREP'},
    # {'codigo': 'DIPRECA', 'nombre_archivo':'2020_ESU_DIPRECA'},
    # {'codigo': 'DT', 'nombre_archivo':'2020_ESU_DT'},
    # {'codigo': 'FONASA', 'nombre_archivo':'2020_ESU_FONASA'},
    # {'codigo': 'Fosis', 'nombre_archivo':'2020_ESU_FOSIS'},
    # {'codigo': 'INE', 'nombre_archivo':'2020_ESU_INE'},
    # {'codigo': 'ISL', 'nombre_archivo':'2020_ESU_ISL'},
    # {'codigo': 'ISP', 'nombre_archivo':'2020_ESU_ISP'},
    # {'codigo': 'Junaeb', 'nombre_archivo':'2020_ESU_JUNAEB'},
    # {'codigo': '', 'nombre_archivo':'2020_ESU_JUNJI'},
    # {'codigo': 'SubseVivienda', 'nombre_archivo':'2020_ESU_MINVU'},
    # {'codigo': 'SENAMA', 'nombre_archivo':'2020_ESU_SENAMA'},
    # {'codigo': 'SEC', 'nombre_archivo':'2020_ESU_SEC'},
    # {'codigo': 'SENCE', 'nombre_archivo':'2020_ESU_SENCE'},
    # {'codigo': 'Sernapesca', 'nombre_archivo':'2020_ESU_SERNAPESCA'},
    # {'codigo': 'SRC', 'nombre_archivo':'2020_ESU_SRCEI'},
    # {'codigo': 'SuseEco', 'nombre_archivo':'2020_ESU_SUBS_ECON'},
    # {'codigo': 'SubseServiciosSociales', 'nombre_archivo':'2020_ESU_SUBS_SERV_SOCIALES'},
    # {'codigo': 'SuperPensiones', 'nombre_archivo':'2020_ESU_SUPER_PENSIONES'},
    # {'codigo': 'SuperSalud', 'nombre_archivo':'2020_ESU_SUPER_SALUD'},
    # {'codigo': 'SUSESO', 'nombre_archivo':'2020_ESU_SUSESO'},
    
    ]

for institucion in instituciones:
    print(institucion)
    file= '/home/christian/repo/hacienda/satisfaccion2021/s3/metodologia/2020_Bases_SPSS/{}.sav'.format(institucion["nombre_archivo"])
    import pyreadstat
    try:
        df = pd.read_spss(file)
    except:
        df, meta = pyreadstat.read_sav(file, encoding='latin1')
    pd.set_option("display.max_columns", None)
    df.head()
    
    rows_cantidad = df.shape[0]

    
    try:
        df['HABBASE'] = df['HabBase']
    except:
        pass

    try:
        df['PEX05'] = df['P2']
    except:
        pass
    
    try:
        df['U3'] = df['D2_EDAD']
        
        df['F_POND'] = df['PONDERADOR'].apply(rango_ponderador)
    except:
        pass
    
    try:
        df['hab'] = df['HABILITACION']
    except:
        df['hab'] = df['HABBASE']
    
    
    df['PEX05'] = df['PEX05'].apply(editcols)
    df['EDAD_AGR'] = df['U3'].apply(rango_edad)
    
    if institucion["nombre_archivo"] == '2020_ESU_SERNAC':
        df['HABBASE'] = df['HABBASE'].apply(categoria_number_to_string_habbase)
        
    if institucion["nombre_archivo"] == '2020_ESU_DT':
        df['PH01']=df['PH01'].apply(editcols)
        df['PH03']=df['PH03'].apply(editcols)
        df['PH04']=df['PH04'].apply(editcols)
        # PARECDE
        # df['HABBASE'] = df[['PH01', 'PH03', 'PH04']].mean(axis=1)
        df['HABBASE'] = df[['PH01', 'PH04']].mean(axis=1)
        df['HABBASE'] = df['HABBASE'].apply(rango_habbase)
    
    if institucion["nombre_archivo"] == '2020_ESU_SII':
        df['PH01']=df['PH01'].apply(editcols).apply(rango_uno_a_siete)
        df['PH02']=df['PH02'].apply(editcols).apply(rango_uno_a_siete)
        df['PH03']=df['PH03'].apply(editcols).apply(rango_uno_a_siete)
        df['PH04']=df['PH04'].apply(editcols).apply(rango_uno_a_siete)
        # PARECDE
        # df['HABBASE'] = df[['PH01', 'PH03', 'PH04']].mean(axis=1)
        df['hab'] = df[['PH01', 'PH02', 'PH03', 'PH04']].mean(axis=1)
        df['hab'] = df['hab'].apply(rango_habbase)
        
    # DT 2020
    if institucion["nombre_archivo"] == '2020_ESU_SUBS_SERV_SOCIALES':
        df['PH01_1']=df['PH01_1'].apply(editcols)
        df['PH01_4']=df['PH01_4'].apply(editcols)
        # PARECDE
        # df['HABBASE'] = df[['PH01', 'PH03', 'PH04']].mean(axis=1)
        df['HABBASE'] = df[['PH01_1', 'PH01_4']].mean(axis=1)
        df['HABBASE'] = df['HABBASE'].apply(rango_habbase)
       

    print(df["hab"])
    if df["hab"].dtype=='float64':
        df['hab'] = df['hab'].apply(rango_habbase)
    

    try:
        df["F_POND"] = pd.to_numeric(df["F_POND"])
    except:
        pass
    
    color_dict = {'insatisfecho':'red', 'neutro': 'orange', 'satisfecho':'green'}
    fig, axs = plt.subplots(2, 2,figsize=(20,20))
    # 7/0
    # df['PH01_1'] = df['PH01_1'].apply(editcols)
    # df['PH01_4'] = df['PH01_4'].apply(editcols)
    # df['HABBASE'] = df['HABBASE'].apply(editcols)
    #  df['promedio_habilitacion'] = df[['PH01_1', 'PH01_4']].mean(axis=1)
    # df[df['HABBASE'].isin(['Habilitado'])]['promedio_habilitacion']
    # df[df['HABBASE'].isin(['Medianamente'])]['promedio_habilitacion'].describe()
    

    # Ultima experiencia
    # df.groupby(['PEX05']).sum()['F_POND']
    # [df['HABBASE'].isin(['No habilitado'])]["HABBASE"]
    
    print("Cantidad de NO habilitdo: {}".format(df[df['hab'].isin(['No habilitado'])]["hab"].count()))
    print("Cantidad de Medianamente: {}".format(df[df['hab'].isin(['Medianamente'])]["hab"].count()))
    print("Cantidad de Habilitdo: {}".format(df[df['hab'].isin(['Habilitado'])]["hab"].count()))
    
    total = df[df['PEX05'].isin([1,2,3,4,5,6,7])]['F_POND'].sum()
    satisfecho = df[df['PEX05'].isin([6,7])]['F_POND'].sum()
    neutro= df[df['PEX05'].isin([5])]['F_POND'].sum()
    insatisfecho = df[df['PEX05'].isin([1,2,3,4])]['F_POND'].sum()
    neto = round((satisfecho-insatisfecho)/total*100,1)
    
    dfp = pd.DataFrame({'insatisfecho': [insatisfecho]/total*100,
                       'neutro': [neutro]/total*100,
                       'satisfecho':[satisfecho]/total*100}, index= [2020])
    
    dfp.plot.bar(ax=axs[0,0], rot=0, stacked=True,color=color_dict)
    axs[0,0].set_title("Neto: {}%".format(neto))
    add_labels(axs[0,0])
    
    # Por Habilitacion
    
    totales = df[df['PEX05'].isin([1,2,3,4,5,6,7])].groupby('hab')['F_POND'].sum()
    insatisfechos= df[df['PEX05'].isin([1,2,3,4])].groupby('hab')['F_POND'].sum()/totales*100
    neutros= df[df['PEX05'].isin([5])].groupby('hab')['F_POND'].sum()/totales*100
    satisfechos= df[df['PEX05'].isin([6,7])].groupby('hab')['F_POND'].sum()/totales*100
    
    print(totales.index)
    dfp = pd.DataFrame({'insatisfecho': insatisfechos,
                       'neutro': neutros,
                       'satisfecho':satisfechos}, index= totales.index)
    
    ax = dfp.plot.bar(ax=axs[0,1], rot=0, stacked=True,color=color_dict)
    axs[0,1].set_title(institucion["codigo"])
    add_labels(axs[0,1])
        
    
    # Por EDAD
    totales = df[df['PEX05'].isin([1,2,3,4,5,6,7])].groupby('EDAD_AGR')['F_POND'].sum()
    insatisfechos= df[df['PEX05'].isin([1,2,3,4])].groupby('EDAD_AGR')['F_POND'].sum()/totales*100
    neutros= df[df['PEX05'].isin([5])].groupby('EDAD_AGR')['F_POND'].sum()/totales*100
    satisfechos= df[df['PEX05'].isin([6,7])].groupby('EDAD_AGR')['F_POND'].sum()/totales*100
    
    
    dfp = pd.DataFrame({'insatisfecho': insatisfechos,
                       'neutro': neutros,
                       'satisfecho':satisfechos}, index= totales.index)
    
    ax = dfp.plot.bar(ax=axs[1,0], rot=0, stacked=True,color=color_dict)
    axs[1,0].set_title(institucion["codigo"])
    add_labels(axs[1,0])
    
    
    df["PEX05"] = pd.to_numeric(df["PEX05"])
    
    boxplot = df[df['PEX05'].isin([1,2,3,4,5,6,7])].boxplot(column=['PEX05'])
    fig.savefig('imagenes/{}.png'.format(institucion["codigo"]))
