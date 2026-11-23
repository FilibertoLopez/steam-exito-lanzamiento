"""Gráfica: antigüedad del juego vs volumen de reseñas (Steam Games Dataset)."""
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
from matplotlib.ticker import MultipleLocator, FuncFormatter

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

gamesDf = pd.read_csv(dataPath, low_memory=False)
colNames = list(gamesDf.columns)
print("Columnas:", colNames)

dateCol = next(c for c in colNames if "release" in c.lower() and "date" in c.lower())
posCol = next(c for c in colNames if c.lower() in ("positive", "positive_reviews", "num_positive"))
negCol = next(c for c in colNames if c.lower() in ("negative", "negative_reviews", "num_negative"))
print("Usando:", dateCol, posCol, negCol)

releaseDate = pd.to_datetime(gamesDf[dateCol], errors="coerce", format="mixed")
snapshotDate = pd.Timestamp("2026-11-19")
reviewCount = pd.to_numeric(gamesDf[posCol], errors="coerce") + pd.to_numeric(gamesDf[negCol], errors="coerce")
ageYears = (snapshotDate - releaseDate).dt.days / 365.25

plotDf = pd.DataFrame({"ageYears": ageYears, "reviewCount": reviewCount}).dropna()
plotDf = plotDf[(plotDf["ageYears"] >= 0) & (plotDf["ageYears"] <= 30)]
print("Juegos graficados:", len(plotDf), "de", len(gamesDf))

plotDf["ageBin"] = np.floor(plotDf["ageYears"]).astype(int)
binStats = plotDf.groupby("ageBin")["reviewCount"].agg(
    n="size",
    median="median",
    q25=lambda s: s.quantile(0.25),
    q75=lambda s: s.quantile(0.75),
    q90=lambda s: s.quantile(0.90),
    pctZero=lambda s: (s == 0).mean() * 100,
    pctGe50=lambda s: (s >= 50).mean() * 100,
).reset_index()
binStats.to_csv(metricsDir / "antiguedadVsResenas_resumen.csv", index=False)
minBinSize = 30  # años con menos juegos no se trazan en las curvas
binStats = binStats[binStats["n"] >= minBinSize]
print(binStats.to_string(index=False))

spearmanRho = plotDf["ageYears"].corr(plotDf["reviewCount"], method="spearman")
print("Spearman rho:", round(spearmanRho, 3))

fig = plt.figure(figsize=(11, 9))
gridSpec = fig.add_gridspec(2, 2, height_ratios=[3, 1.3], width_ratios=[40, 1], hspace=0.28, wspace=0.03)
axMain = fig.add_subplot(gridSpec[0, 0])
axPct = fig.add_subplot(gridSpec[1, 0], sharex=axMain)
axCbar = fig.add_subplot(gridSpec[0, 1])
hb = axMain.hexbin(plotDf["ageYears"], np.log10(plotDf["reviewCount"] + 1),
                   gridsize=(60, 35), bins="log", cmap="Blues", mincnt=1)
fig.colorbar(hb, cax=axCbar, label="Número de juegos (escala log)")
binCenter = binStats["ageBin"] + 0.5
axMain.plot(binCenter, np.log10(binStats["median"] + 1), color="#D9480F", lw=2.2, marker="o", ms=4, label="Mediana por año (años con n ≥ 30)")
axMain.fill_between(binCenter, np.log10(binStats["q25"] + 1), np.log10(binStats["q75"] + 1),
                    color="#D9480F", alpha=0.18, label="Rango intercuartil")
axMain.plot(binCenter, np.log10(binStats["q90"] + 1), color="#D9480F", lw=1.2, ls="--", label="Percentil 90")
axMain.axhline(np.log10(51), color="#444", lw=1, ls=":", label="Umbral de 50 reseñas")
tickVals = [0, 1, 10, 100, 1_000, 10_000, 100_000, 1_000_000]
axMain.set_yticks(np.log10(np.array(tickVals) + 1))
axMain.set_yticklabels(["0", "1", "10", "100", "1 mil", "10 mil", "100 mil", "1 M"])
axMain.set_ylabel("Reseñas totales (positivas + negativas)")
axMain.set_xlabel("Años desde el lanzamiento", fontsize=10)
axMain.set_title(f"Antigüedad del juego vs volumen de reseñas en Steam\n"
                 f"n = {len(plotDf):,} juegos · Spearman ρ = {spearmanRho:.2f} · corte al {snapshotDate.date()}",
                 fontsize=13)
axMain.legend(loc="upper right", fontsize=9, framealpha=0.9)
axMain.grid(alpha=0.25)

axPct.bar(binCenter, binStats["pctGe50"], width=0.8, color="#1C7ED6", alpha=0.8, label="% con ≥ 50 reseñas")
axPct.plot(binCenter, binStats["pctZero"], color="#C92A2A", marker="o", ms=3, lw=1.5, label="% con 0 reseñas")
axPct.set_ylabel("% de juegos")
axPct.set_xlabel(f"Antigüedad del juego (años desde su lanzamiento hasta el {snapshotDate.strftime('%d/%m/%Y')})", fontsize=11)
for ax in (axMain, axPct):
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.tick_params(axis="x", labelbottom=True, labelsize=9)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, pos: f"{int(v)}"))
axPct.xaxis.set_major_formatter(FuncFormatter(lambda v, pos: f"{int(v)}"))
axPct.tick_params(axis="x", labelsize=9)
axPct.set_ylim(0, 125)
axPct.set_yticks([0, 25, 50, 75, 100])
axPct.set_xlim(0, binStats["ageBin"].max() + 1)
axPct.legend(loc="upper center", ncol=2, fontsize=9, framealpha=0.95)
axPct.grid(alpha=0.25)

fig.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.07)
outPng = figuresDir / "antiguedadVsResenas.png"
fig.savefig(outPng, dpi=160)
print("Guardado:", outPng)
