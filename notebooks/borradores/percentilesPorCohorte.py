"""Percentiles de éxito dentro de cada cohorte de año de lanzamiento (Steam Games Dataset).

Cada juego se compara solo contra los lanzados el mismo año, para neutralizar
el sesgo de exposición: un juego de 2012 lleva 14 años acumulando reseñas y uno
de 2024 apenas dos.

Salidas (en Wrk/):
  percentilesCohorte_juegos.csv   una fila por juego con sus percentiles
  percentilesCohorte_resumen.csv  umbrales por cohorte (p50, p75, p90, p99...)
  percentilesCohorte.png          umbrales por cohorte y control de exposición
"""
from pathlib import Path
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

snapshotDate = pd.Timestamp("2026-11-19")   # versión del dataset
minAgeMonths = 12                           # excluir juegos con < 12 meses en tienda
minCohortSize = 200                         # años más pequeños se agrupan en una cohorte inicial
minReviewsRatio = 10                        # mínimo de reseñas para el percentil de % positivas

# ---------------------------------------------------------------- carga
gamesDf = pd.read_csv(dataPath, low_memory=False, keep_default_na=False, na_values=[""])
nTotal = len(gamesDf)

releaseDate = pd.to_datetime(gamesDf["release_date"], errors="coerce", format="mixed")
positiveCount = pd.to_numeric(gamesDf["positive"], errors="coerce")
negativeCount = pd.to_numeric(gamesDf["negative"], errors="coerce")

workDf = pd.DataFrame({
    "app_id": gamesDf["app_id"],
    "name": gamesDf["name"],
    "releaseDate": releaseDate,
    "positive": positiveCount,
    "negative": negativeCount,
})
workDf["reviewCount"] = workDf["positive"] + workDf["negative"]
workDf["ageDays"] = (snapshotDate - workDf["releaseDate"]).dt.days

# ---------------------------------------------------------------- filtros
validMask = workDf["releaseDate"].notna() & workDf["reviewCount"].notna()
cutoffDate = snapshotDate - pd.DateOffset(months=minAgeMonths)
ageMask = workDf["releaseDate"] <= cutoffDate
nNoDate = int((~validMask).sum())
nTooRecent = int((validMask & ~ageMask).sum())
workDf = workDf[validMask & ageMask].copy()
workDf["releaseYear"] = workDf["releaseDate"].dt.year.astype(int)

# ---------------------------------------------------------------- cohortes
yearSizes = workDf["releaseYear"].value_counts().sort_index()
bigYears = yearSizes[yearSizes >= minCohortSize].index
firstBigYear = int(bigYears.min())
workDf["cohort"] = workDf["releaseYear"].where(workDf["releaseYear"] >= firstBigYear, firstBigYear - 1)
cohortLabel = {firstBigYear - 1: f"≤{firstBigYear - 1}"}
workDf["cohortLabel"] = workDf["cohort"].map(lambda c: cohortLabel.get(c, str(c)))

# ---------------------------------------------------------------- percentiles
# Rango promedio: los empates (p. ej. los muchos juegos con 0 reseñas) reciben
# el percentil medio de su bloque, no el máximo ni el mínimo.
cohortGroup = workDf.groupby("cohort")
workDf["reviewPctlCohort"] = cohortGroup["reviewCount"].rank(pct=True, method="average") * 100
workDf["reviewPctlGlobal"] = workDf["reviewCount"].rank(pct=True, method="average") * 100

workDf["positiveRatio"] = np.where(workDf["reviewCount"] > 0,
                                   workDf["positive"] / workDf["reviewCount"].replace(0, np.nan), np.nan)
ratioMask = workDf["reviewCount"] >= minReviewsRatio
workDf["positivePctlCohort"] = np.nan
workDf.loc[ratioMask, "positivePctlCohort"] = (
    workDf[ratioMask].groupby("cohort")["positiveRatio"].rank(pct=True, method="average") * 100
)

workDf["topQuartileCohort"] = workDf["reviewPctlCohort"] >= 75
workDf["topDecileCohort"] = workDf["reviewPctlCohort"] >= 90

# ---------------------------------------------------------------- resumen por cohorte
def summarizeCohort(s):
    r = s["reviewCount"]
    ratio = s.loc[s["reviewCount"] >= minReviewsRatio, "positiveRatio"]
    return pd.Series({
        "n": len(s),
        "pctZero": (r == 0).mean() * 100,
        "p50": r.quantile(0.50),
        "p75": r.quantile(0.75),
        "p90": r.quantile(0.90),
        "p99": r.quantile(0.99),
        "nRatio": len(ratio),
        "medianPositiveRatio": ratio.median(),
        "medianAgeYears": s["ageDays"].median() / 365.25,
    })

summaryDf = (workDf.groupby(["cohort", "cohortLabel"]).apply(summarizeCohort, include_groups=False)
             .reset_index().sort_values("cohort"))
summaryDf.to_csv(metricsDir / "percentilesCohorte_resumen.csv", index=False)

outCols = ["app_id", "name", "releaseDate", "releaseYear", "cohortLabel", "ageDays",
           "reviewCount", "reviewPctlCohort", "reviewPctlGlobal", "topQuartileCohort",
           "topDecileCohort", "positiveRatio", "positivePctlCohort"]
workDf[outCols].to_csv(processedDir / "percentilesCohorte_juegos.csv", index=False)

# ---------------------------------------------------------------- control de exposición
rhoRaw = workDf["ageDays"].corr(workDf["reviewCount"], method="spearman")
rhoGlobalPctl = workDf["ageDays"].corr(workDf["reviewPctlGlobal"], method="spearman")
rhoCohortPctl = workDf["ageDays"].corr(workDf["reviewPctlCohort"], method="spearman")
# Exposición residual dentro del año (enero vs diciembre)
withinRho = workDf.groupby("cohort").apply(
    lambda s: s["ageDays"].corr(s["reviewCount"], method="spearman"), include_groups=False)
shareTopQuartile = workDf.groupby("cohortLabel", sort=False)["topQuartileCohort"].mean() * 100

# ---------------------------------------------------------------- gráfica
fig, (axThr, axAge) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={"height_ratios": [3, 2], "hspace": 0.35})
xPos = np.arange(len(summaryDf))
for col, color, label in [("p50", "#868E96", "Mediana (p50)"), ("p75", "#1C7ED6", "p75 (cuartil superior)"),
                          ("p90", "#D9480F", "p90 (decil superior)"), ("p99", "#5F3DC4", "p99")]:
    axThr.plot(xPos, summaryDf[col] + 1, marker="o", ms=4, lw=2, color=color, label=label)
axThr.set_yscale("log")
axThr.set_xticks(xPos)
axThr.set_xticklabels(summaryDf["cohortLabel"], rotation=45, ha="right")
axThr.set_ylabel("Reseñas totales + 1 (escala log)")
axThr.set_title("Reseñas necesarias para alcanzar cada percentil dentro de su cohorte de lanzamiento\n"
                f"n = {len(workDf):,} juegos con ≥ {minAgeMonths} meses en tienda · corte al {snapshotDate.date()}",
                fontsize=12)
axThr.grid(alpha=0.25, which="both")
axThr.legend(fontsize=9)
axZero = axThr.twinx()
axZero.bar(xPos, summaryDf["pctZero"], color="#C92A2A", alpha=0.12, width=0.8)
axZero.set_ylabel("% de juegos con 0 reseñas (barras)", color="#C92A2A")
axZero.set_ylim(0, 100)

ageBin = np.floor(workDf["ageDays"] / 365.25).astype(int)
ageView = pd.DataFrame({"ageBin": ageBin, "global": workDf["reviewPctlGlobal"], "cohorte": workDf["reviewPctlCohort"]})
ageMed = ageView.groupby("ageBin")[["global", "cohorte"]].median()
ageMed = ageMed[ageView["ageBin"].value_counts().sort_index() >= 30]
axAge.plot(ageMed.index, ageMed["global"], marker="o", color="#868E96", lw=2,
           label=f"Percentil global (ρ edad = {rhoGlobalPctl:.2f})")
axAge.plot(ageMed.index, ageMed["cohorte"], marker="o", color="#D9480F", lw=2,
           label=f"Percentil dentro de la cohorte (ρ edad = {rhoCohortPctl:.2f})")
axAge.axhline(50, color="#444", ls=":", lw=1)
axAge.set_xlabel("Años desde el lanzamiento")
axAge.set_ylabel("Percentil mediano de reseñas")
axAge.set_ylim(0, 100)
axAge.set_title("Control: el percentil por cohorte elimina la tendencia con la antigüedad", fontsize=12)
axAge.grid(alpha=0.25)
axAge.legend(fontsize=9, loc="upper left")
fig.savefig(figuresDir / "percentilesCohorte.png", dpi=150, bbox_inches="tight")

# ---------------------------------------------------------------- reporte
pd.set_option("display.width", 200)
print(f"Filas totales: {nTotal:,} | sin fecha o reseñas: {nNoDate:,} | < {minAgeMonths} meses: {nTooRecent:,} | analizadas: {len(workDf):,}")
print(f"Cohorte inicial agrupada: ≤{firstBigYear - 1} (años con < {minCohortSize} juegos)")
print(f"Spearman edad vs reseñas: {rhoRaw:.3f} | vs percentil global: {rhoGlobalPctl:.3f} | vs percentil por cohorte: {rhoCohortPctl:.3f}")
print("Spearman edad vs reseñas DENTRO de cada cohorte:")
print(withinRho.round(3).to_string())
print("% en cuartil superior por cohorte:")
print(shareTopQuartile.round(1).to_string())
print(summaryDf.round(2).to_string(index=False))
print("Juegos con percentil de % positivas:", int(ratioMask.sum()))
