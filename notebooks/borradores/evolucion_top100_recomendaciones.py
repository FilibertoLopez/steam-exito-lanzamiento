"""Evolución (nov 2021 – oct 2026) de las reseñas mensuales en Steam de los 100 juegos
con más recomendaciones en steam_games.csv.gz (dataset de Kaggle, 19-nov-2026).
Paso 1 descarga el historial mensual de Steam (appreviewhistogram); paso 2 dibuja las gráficas.
Puede ejecutarse desde cualquier carpeta: las rutas son absolutas o relativas al repositorio."""
from pathlib import Path
baseDir = Path("/Users/lvadmin/Documents/prs/fld/Maestría CC/Semestre 03/Clase.Aprendizaje de Máquina/Proyecto Final")
dataPath = baseDir / "Datos" / "steam_games.csv.gz"
# Rutas del repositorio (este script vive en notebooks/borradores/)
repoDir = Path(__file__).resolve().parents[2]
figuresDir = repoDir / "reports" / "figures"
metricsDir = repoDir / "reports" / "metrics"
processedDir = repoDir / "data" / "processed"
interimDir = repoDir / "data" / "interim"
for outPath in (figuresDir, metricsDir, processedDir, interimDir):
    outPath.mkdir(parents=True, exist_ok=True)
# ===== Paso 1: ranking y descarga =====
import pandas as pd, requests, json, time, re
df=pd.read_csv(dataPath,usecols=['app_id','name','recommendations','positive','negative','release_date'])
df['n']=df.positive+df.negative
t=df.nlargest(200,'recommendations').copy()
t['key']=t.name.str.strip().str.lower()
t=t.sort_values(['recommendations','n'],ascending=False)
# dedupe: same name -> keep larger n
t=t[t.app_id!=2995920]  # It Takes Two Friend's Pass: duplicado sin reseñas propias
t=t.sort_values('n',ascending=False).drop_duplicates('key').sort_values('recommendations',ascending=False)
top=t.head(100).reset_index(drop=True); top['rank']=top.index+1
top.to_csv(interimDir / 'top100.csv',index=False)
rows=[]
for a in top.app_id:
    for k in range(3):
        try:
            d=requests.get(f'https://store.steampowered.com/appreviewhistogram/{a}?l=english&review_score_preference=0',timeout=20).json()['results']
            for r in d['rollups']: rows.append((a,r['date'],r['recommendations_up'],r['recommendations_down']))
            break
        except Exception as e: time.sleep(2)
    time.sleep(0.3)
h=pd.DataFrame(rows,columns=['app_id','ts','up','down']); h.to_csv(interimDir / 'hist.csv',index=False)
print(h.app_id.nunique(), len(h)); print(top[['rank','name','recommendations']].to_string())

# ===== Paso 2: gráficas =====
import pandas as pd, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.colors as mc, matplotlib.dates as md
# Fuente latina + respaldo CJK (macOS: Hiragino/PingFang; Linux: Noto CJK). Solo las instaladas.
import matplotlib.font_manager as fm
installedFonts = {f.name for f in fm.fontManager.ttflist}
cjkFonts = [f for f in ('Hiragino Sans GB', 'PingFang SC', 'Arial Unicode MS', 'Noto Sans CJK SC', 'Noto Sans CJK JP') if f in installedFonts]
plt.rcParams['font.family'] = ['DejaVu Sans'] + cjkFonts
top=pd.read_csv(interimDir / 'top100.csv'); h=pd.read_csv(interimDir / 'hist.csv')
h['mes']=pd.to_datetime(h.ts,unit='s').dt.to_period('M').dt.to_timestamp()
h=h.groupby(['app_id','mes'],as_index=False)[['up','down']].sum(); h['tot']=h.up+h.down
meses=pd.date_range('2021-11-01','2026-10-01',freq='MS')
M=h.pivot(index='app_id',columns='mes',values='tot').reindex(index=top.app_id,columns=meses)
rel=pd.to_datetime(top.set_index('app_id').release_date,errors='coerce')
# before launch -> NaN ; after launch missing month -> 0
for a in M.index:
    r=M.loc[a]; fm=r.first_valid_index()
    if fm is not None: M.loc[a, r.index>=fm]=r[r.index>=fm].fillna(0)
labels=[f"{r}. {n}" for r,n in zip(top['rank'],top.name.str.replace('™','').str.replace('®',''))]
# ---- heatmap
fig,ax=plt.subplots(figsize=(14,24))
cmap=plt.get_cmap('magma_r').copy(); cmap.set_bad('#e9e9ee')
im=ax.imshow(M.values+0.0,aspect='auto',cmap=cmap,norm=mc.LogNorm(vmin=100,vmax=M.max().max()),interpolation='nearest')
ax.set_yticks(range(100)); ax.set_yticklabels(labels,fontsize=8.5)
xt=[i for i,m in enumerate(meses) if m.month in (1,7)]
ax.set_xticks(xt); ax.set_xticklabels([meses[i].strftime('%b %Y').replace('Jan','ene').replace('Jul','jul') for i in xt],fontsize=10)
ax.set_xticks(np.arange(-.5,60,1),minor=True); ax.tick_params(which='minor',length=0)
cb=fig.colorbar(im,ax=ax,fraction=0.025,pad=0.015); cb.set_label('Reseñas nuevas en el mes (escala logarítmica)',fontsize=11)
ax.set_title('Reseñas mensuales en Steam de los 100 juegos con más recomendaciones\nnov 2021 – oct 2026 · ordenados por recomendaciones acumuladas al 19-nov-2026',fontsize=14,loc='left',pad=14)
fig.text(0.01,0.004,'Gris: el juego aún no salía en Steam. Fuente: dataset Steam Games (Kaggle, 19-nov-2026) para el ranking; historial mensual de reseñas de Steam (appreviewhistogram) para la evolución.',fontsize=9,color='#555')
fig.tight_layout(rect=(0,0.01,1,1)); fig.savefig(figuresDir / 'evolucion_top100_mapa_calor.png',dpi=130); plt.close()
# ---- lines top 10 + total
fig,(a1,a2)=plt.subplots(2,1,figsize=(16,11),gridspec_kw={'height_ratios':[1.5,1]})
cols=plt.get_cmap('tab10').colors
for i,(a,lab) in enumerate(zip(top.app_id[:10],labels[:10])):
    s=M.loc[a].rolling(3,min_periods=1).mean()
    a1.plot(meses,s,color=cols[i],lw=2,label=lab)
a1.set_yscale('log'); a1.set_ylabel('Reseñas nuevas por mes\n(media móvil de 3 meses, escala log)')
a1.set_title('Los 10 primeros: reseñas nuevas por mes',loc='left',fontsize=13)
a1.legend(fontsize=9.5,frameon=False,loc='upper left',bbox_to_anchor=(1.01,1)); a1.grid(alpha=.3,which='both')
tot=M.sum(); t10=M.iloc[:10].sum()
a2.stackplot(meses,t10/1e3,(tot-t10)/1e3,colors=['#3b5b92','#a9bde0'],labels=['Top 10','Lugares 11 a 100'])
a2.set_ylabel('Miles de reseñas nuevas por mes'); a2.set_title('Los 100 juegos en conjunto',loc='left',fontsize=13)
a2.legend(loc='upper left',frameon=False); a2.grid(alpha=.3)
for a in (a1,a2): a.xaxis.set_major_formatter(md.DateFormatter('%m/%Y')); a.set_xlim(meses[0],meses[-1]); a.spines[['top','right']].set_visible(False)
fig.suptitle('Evolución de las reseñas en Steam, nov 2021 – oct 2026',fontsize=15,x=0.01,ha='left')
fig.text(0.01,0.005,'Fuente: ranking del dataset Steam Games (Kaggle, 19-nov-2026); historial mensual de reseñas de Steam.',fontsize=9,color='#555')
fig.tight_layout(rect=(0,0.015,1,0.97)); fig.savefig(figuresDir / 'evolucion_top10_y_total.png',dpi=130); plt.close()
M.to_csv(metricsDir / 'resenas_mensuales_top100.csv')
print(tot.iloc[[0,12,24,36,48,59]]); print((M.iloc[:,-12:].sum(1)/M.sum(1)).sort_values().tail(8).rename(index=dict(zip(top.app_id,top.name))))
