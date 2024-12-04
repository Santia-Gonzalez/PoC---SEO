import advertools as adv
import pandas as pd
import matplotlib.pyplot as plt

log_file = 'advertools/seo_analysis.log'

extra_config = {
    'ROBOTSTXT_OBEY': True,
    'LOG_FILE': log_file,
    'LOG_LEVEL': 'INFO'
}

url = 'https://www.omni.pro/es/'
output_file = 'advertools/seo_report.jl'

adv.crawl(url, output_file=output_file, follow_links=True, custom_settings=extra_config)

seo_df = pd.read_json(output_file, lines=True)

print(seo_df.columns.tolist())  # Mostrar todas las columnas disponibles

# Manejar NaNs y convertir a string
seo_df['title'] = seo_df['title'].fillna('').astype(str)
seo_df['meta_desc'] = seo_df['meta_desc'].fillna('').astype(str)

# Longitud de los títulos
seo_df['title_length'] = seo_df['title'].apply(len)

# Longitud de las meta descripciones
seo_df['meta_desc_length'] = seo_df['meta_desc'].apply(len)

print(seo_df)

print(seo_df[['url', 'title', 'title_length', 'meta_desc', 'meta_desc_length', 'ip_address', 'status']])

# Contar el número de etiquetas H1, H2, etc.
for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
    if tag in seo_df.columns:
        seo_df[f'{tag}_count'] = seo_df[tag].apply(lambda x: len(str(x).split(',')) if pd.notnull(x) else 0)
    else:
        seo_df[f'{tag}_count'] = 0  # Si la columna no existe, asignar valor 0

print(seo_df[['url', 'h1_count', 'h2_count', 'h3_count', 'h4_count', 'h5_count', 'h6_count']])

# Contar enlaces internos y externos
seo_df['internal_links_count'] = seo_df['links_url'].apply(lambda x: len(str(x).split(',')) if pd.notnull(x) else 0)
seo_df['external_links_count'] = seo_df['nav_links_url'].apply(lambda x: len(str(x).split(',')) if pd.notnull(x) else 0)

print(seo_df[['url', 'internal_links_count', 'external_links_count', 'status']])

link_test = seo_df['links_text'].dropna().str.cat(sep=' ')
word_freq_df = adv.word_frequency(link_test, rm_words=adv.stopwords['spanish'])

print(word_freq_df.head())


# Longitud de Títulos
seo_df.plot(kind='bar', x='url', y='title_length', figsize=(10, 5))
plt.title('Longitud de Títulos por URL')
plt.xlabel('URL')
plt.ylabel('Longitud del Título')
plt.show()

# Conteo de Encabezados H1
seo_df.plot(kind='bar', x='url', y='h1_count', figsize=(10, 5))
plt.title('Conteo de Etiquetas H1 por URL')
plt.xlabel('URL')
plt.ylabel('Conteo de H1')
plt.show()


# Guardar Resultados en JSON con formato
seo_df.to_json('advertools/seo_analysis_results.json', orient='records', lines=True, indent=4)
