"""Gráfica: mediana de reseñas por género y por categoría de Steam."""
from pathlib import Path
import json
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Fuente latina + respaldo CJK (macOS: Hiragino/PingFang; Linux: Noto CJK). Solo las instaladas.
installedFonts = {f.name for f in fm.fontManager.ttflist}
cjkFonts = [f for f in ("Hiragino Sans GB", "PingFang SC", "Arial Unicode MS", "Noto Sans CJK SC", "Noto Sans CJK JP") if f in installedFonts]
plt.rcParams["font.family"] = ["DejaVu Sans"] + cjkFonts
from matplotlib.ticker import FuncFormatter

baseDir = Path("/Users/lvadmin/Documents/prs/fld/Maestría CC/Semestre 03/Clase.Aprendizaje de Máquina/Proyecto Final")
dataPath = baseDir / "Datos" / "steam_games.csv.gz"
# Rutas del repositorio (este script vive en notebooks/borradores/)
repoDir = Path(__file__).resolve().parents[2]
figuresDir = repoDir / "reports" / "figures"
metricsDir = repoDir / "reports" / "metrics"
processedDir = repoDir / "data" / "processed"
interimDir = repoDir / "data" / "interim"
for outPath in (figuresDir, metricsDir, processedDir, interimDir):
    outPath.mkdir(parents=True, exist_ok=True)

snapshotDate = pd.Timestamp("2026-11-19")
minGroupSize = 300      # grupos con menos juegos no se grafican
maxCategories = 25      # categorías más frecuentes a mostrar
minAgeYears = 3         # filtro de exposición para el segundo marcador

gamesDf = pd.read_csv(dataPath, usecols=["app_id", "release_date", "positive", "negative", "genres", "categories"],
                      low_memory=False)
gamesDf["reviewCount"] = pd.to_numeric(gamesDf["positive"], errors="coerce") + pd.to_numeric(gamesDf["negative"], errors="coerce")
releaseDate = pd.to_datetime(gamesDf["release_date"], errors="coerce", format="mixed")
gamesDf["ageYears"] = (snapshotDate - releaseDate).dt.days / 365.25


def parseLabels(rawValue):
    """Devuelve una lista de pares (id, descripción) a partir de JSON con objetos o con textos."""
    if not isinstance(rawValue, str) or not rawValue.strip():
        return []
    try:
        parsedList = json.loads(rawValue)
    except json.JSONDecodeError:
        return []
    labelPairs = []
    for item in parsedList:
        if isinstance(item, dict):
            labelPairs.append((str(item.get("id", item.get("description"))), str(item.get("description", "")).strip()))
        elif isinstance(item, str):
            labelPairs.append((item.strip(), item.strip()))
    return labelPairs


def groupStats(columnName):
    """Explota la columna multi-etiqueta y calcula estadísticos de reseñas por etiqueta."""
    pairSeries = gamesDf[columnName].map(parseLabels)
    # nombre canónico por id: la descripción más frecuente (algunas filas vienen localizadas)
    nameCounter = {}
    for pairList in pairSeries:
        for labelId, labelName in pairList:
            nameCounter.setdefault(labelId, Counter())[labelName] += 1
    canonicalName = {labelId: counter.most_common(1)[0][0] for labelId, counter in nameCounter.items()}

    longDf = pd.DataFrame({
        "app_id": gamesDf["app_id"].repeat(pairSeries.map(len)).values,
        "labelId": [labelId for pairList in pairSeries for labelId, _ in pairList],
    }).drop_duplicates()
    longDf["label"] = longDf["labelId"].map(canonicalName)
    longDf = longDf.merge(gamesDf[["app_id", "reviewCount", "ageYears"]], on="app_id").dropna(subset=["reviewCount"])

    allStats = longDf.groupby("label")["reviewCount"].agg(
        n="size", median="median", q25=lambda s: s.quantile(0.25), q75=lambda s: s.quantile(0.75))
    matureStats = longDf[longDf["ageYears"] >= minAgeYears].groupby("label")["reviewCount"].agg(
        nMature="size", medianMature="median",
        q25Mature=lambda s: s.quantile(0.25), q75Mature=lambda s: s.quantile(0.75))
    statsDf = allStats.join(matureStats).reset_index()
    statsDf = statsDf[(statsDf["n"] >= minGroupSize) & (statsDf["nMature"] >= minGroupSize)]
    statsDf["pctRecent"] = 100 * (1 - statsDf["nMature"] / statsDf["n"])
    return statsDf


genreStats = groupStats("genres")
categoryStats = groupStats("categories").nlargest(maxCategories, "n")
genreStats.to_csv(metricsDir / "medianaResenasPorGenero.csv", index=False)
categoryStats.to_csv(metricsDir / "medianaResenasPorCategoria.csv", index=False)

overallMedian = gamesDf["reviewCount"].median()
overallMatureMedian = gamesDf.loc[gamesDf["ageYears"] >= minAgeYears, "reviewCount"].median()
print("Mediana global:", overallMedian, "| mediana global con ≥", minAgeYears, "años:", overallMatureMedian)
print(genreStats.sort_values("median", ascending=False).to_string(index=False))
print(categoryStats.sort_values("median", ascending=False).to_string(index=False))

symlogShift = 1  # se grafica valor + 1 en escala log para admitir medianas de 0
recentShareFlag = 75  # % de juegos con < minAgeYears años a partir del cual se marca la etiqueta
postLaunchLabels = {"Steam Trading Cards"}  # Steam la habilita después del lanzamiento según ventas y actividad
tickValues = [0, 1, 3, 10, 30, 100, 300, 1000, 3000]


def drawPanel(ax, statsDf, panelTitle):
    statsDf = statsDf.sort_values(["medianMature", "median"], ascending=True).reset_index(drop=True)
    yPos = np.arange(len(statsDf))
    ax.barh(yPos, statsDf["medianMature"] + symlogShift, color="#1C7ED6", alpha=0.85, height=0.65,
            label=f"Mediana, juegos con ≥ {minAgeYears} años")
    ax.errorbar(statsDf["medianMature"] + symlogShift, yPos,
                xerr=[statsDf["medianMature"] - statsDf["q25Mature"], statsDf["q75Mature"] - statsDf["medianMature"]],
                fmt="none", ecolor="#364FC7", elinewidth=1, capsize=2.5, alpha=0.7,
                label=f"Rango intercuartil, juegos con ≥ {minAgeYears} años")
    ax.scatter(statsDf["median"] + symlogShift, yPos, marker="D", s=26, color="#D9480F", zorder=3,
               label="Mediana, todos los juegos")
    ax.axvline(overallMatureMedian + symlogShift, color="#1C7ED6", ls=":", lw=1.2)
    ax.axvline(overallMedian + symlogShift, color="#D9480F", ls=":", lw=1.2)
    ax.set_yticks(yPos)
    def suffixFor(name, pctRecent):
        return " †" if name in postLaunchLabels else (" *" if pctRecent >= recentShareFlag else "")
    ax.set_yticklabels([f"{name}  (n={n:,}){suffixFor(name, p)}"
                        for name, n, p in zip(statsDf["label"], statsDf["n"], statsDf["pctRecent"])], fontsize=9)
    for tickLabel, name, pctRecent in zip(ax.get_yticklabels(), statsDf["label"], statsDf["pctRecent"]):
        if name in postLaunchLabels:
            tickLabel.set_color("#C92A2A"); tickLabel.set_fontweight("bold")
        elif pctRecent >= recentShareFlag:
            tickLabel.set_color("#868E96"); tickLabel.set_fontstyle("italic")
    ax.set_xscale("log")
    xMax = max(statsDf["q75Mature"].max(), statsDf["median"].max()) * 1.6
    ax.set_xlim(0.85, xMax)
    visibleTicks = [v for v in tickValues if v + symlogShift <= xMax]
    ax.set_xticks([v + symlogShift for v in visibleTicks])
    ax.set_xticklabels([f"{v:,}" for v in visibleTicks])
    ax.minorticks_off()
    ax.set_xlabel("Reseñas totales por juego (positivas + negativas, escala log)")
    ax.set_title(panelTitle, fontsize=12)
    ax.grid(axis="x", alpha=0.3)
    ax.set_ylim(-0.7, len(statsDf) - 0.3)


genreHeight = len(genreStats)
categoryHeight = len(categoryStats)
fig, (axGenre, axCategory) = plt.subplots(1, 2, figsize=(16, 0.36 * max(genreHeight, categoryHeight) + 2.6),
                                          gridspec_kw={"wspace": 0.75})
drawPanel(axGenre, genreStats, "Por género")
drawPanel(axCategory, categoryStats, f"Por categoría ({maxCategories} más frecuentes)")
handles, labels = axGenre.get_legend_handles_labels()
handles += [plt.Line2D([], [], color="#1C7ED6", ls=":"), plt.Line2D([], [], color="#D9480F", ls=":")]
labels += [f"Mediana global con ≥ {minAgeYears} años ({overallMatureMedian:,.0f})", f"Mediana global, todos ({overallMedian:,.0f})"]
fig.legend(handles, labels, loc="lower center", ncol=3, fontsize=9, frameon=False, bbox_to_anchor=(0.5, 0.035))
fig.text(0.5, 0.012, f"* Etiqueta gris: al menos el {recentShareFlag} % de sus juegos tiene menos de {minAgeYears} años; su mediana global refleja poca exposición.   "
         "† Steam la habilita después del lanzamiento según ventas y actividad: no es un predictor válido al lanzamiento.",
         ha="center", fontsize=8.5, color="#495057")
fig.suptitle(f"Mediana de reseñas por género y categoría en Steam\n"
             f"{gamesDf['reviewCount'].notna().sum():,} juegos · un juego cuenta en cada etiqueta que tenga · "
             f"barras ordenadas por la mediana de juegos con ≥ {minAgeYears} años · grupos con n ≥ {minGroupSize} · corte al {snapshotDate.strftime('%d/%m/%Y')}", fontsize=13)
fig.subplots_adjust(left=0.19, right=0.98, top=0.9, bottom=0.14)
outPng = figuresDir / "medianaResenasPorGenero.png"
fig.savefig(outPng, dpi=160)
print("Guardado:", outPng)
