"""Build the two small input files from the official ESCO v1.2.1 CSV download.

Usage:  python src/prepare_esco_data.py --esco-dir PATH_TO_ESCO_CSV_FOLDER --out data
ESCO download: https://esco.ec.europa.eu/en/use-esco/download  (CSV, English, v1.2.1)
Needs: occupations_en.csv, occupationSkillRelations_en.csv
"""
import argparse, os
import pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--esco-dir", required=True)
    ap.add_argument("--out", default="data")
    a = ap.parse_args()
    occ = pd.read_csv(os.path.join(a.esco_dir, "occupations_en.csv"), dtype=str).fillna("")
    occ = occ[(occ.conceptType == "Occupation") & (occ.status == "released")].copy()
    occ = occ.rename(columns={"conceptUri": "occ_uri", "preferredLabel": "title"})
    occ["isco4"] = occ["iscoGroup"].str.strip()
    occ["alt_labels"] = occ["altLabels"].str.replace("\n", "; ")
    occ = occ[["occ_uri", "isco4", "title", "alt_labels", "description"]].reset_index(drop=True)
    rel = pd.read_csv(os.path.join(a.esco_dir, "occupationSkillRelations_en.csv"), dtype=str).fillna("")
    rel = rel[(rel.relationType == "essential") & (rel.occupationUri.isin(occ.occ_uri))]
    rel = rel.rename(columns={"occupationUri": "occ_uri", "skillLabel": "skill"})[["occ_uri", "skill"]]
    os.makedirs(a.out, exist_ok=True)
    occ.to_csv(os.path.join(a.out, "esco_occupations_text.csv"), index=False)
    rel.to_csv(os.path.join(a.out, "esco_essential_skills.csv"), index=False)
    print(len(occ), "occupations;", len(rel), "essential occupation-skill links")

if __name__ == "__main__":
    main()
