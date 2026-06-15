import pandas as pd
from models import Candidate
import random
import time

def get_presets():
    return {
        "Small (n=12, k=5, B=100jt)": {
            "n": 12, "k": 5, "B": 100_000_000,
            "candidates": [
                Candidate(1, "Andi", 15_000_000), Candidate(2, "Budi", 25_000_000),
                Candidate(3, "Citra", 10_000_000), Candidate(4, "Dewi", 30_000_000),
                Candidate(5, "Eka", 20_000_000), Candidate(6, "Fajar", 35_000_000),
                Candidate(7, "Gita", 12_000_000), Candidate(8, "Hani", 28_000_000),
                Candidate(9, "Irfan", 18_000_000), Candidate(10, "Joko", 22_000_000),
                Candidate(11, "Kiki", 40_000_000), Candidate(12, "Lina", 16_000_000),
            ]
        },
        "Medium (n=18, k=7, B=140jt)": {
            "n": 18, "k": 7, "B": 140_000_000,
            "candidates": [
                Candidate(1, "Andi", 15_000_000), Candidate(2, "Budi", 25_000_000),
                Candidate(3, "Citra", 10_000_000), Candidate(4, "Dewi", 30_000_000),
                Candidate(5, "Eka", 20_000_000), Candidate(6, "Fajar", 35_000_000),
                Candidate(7, "Gita", 12_000_000), Candidate(8, "Hani", 28_000_000),
                Candidate(9, "Irfan", 18_000_000), Candidate(10, "Joko", 22_000_000),
                Candidate(11, "Kiki", 40_000_000), Candidate(12, "Lina", 16_000_000),
                Candidate(13, "Mamat", 14_000_000), Candidate(14, "Nana", 24_000_000),
                Candidate(15, "Ovi", 31_000_000), Candidate(16, "Putu", 19_000_000),
                Candidate(17, "Qori", 27_000_000), Candidate(18, "Riko", 21_000_000),
            ]
        },
        "Large (n=24, k=9, B=180jt)": {
            "n": 24, "k": 9, "B": 180_000_000,
            "candidates": [
                Candidate(1, "Andi", 15_000_000), Candidate(2, "Budi", 25_000_000),
                Candidate(3, "Citra", 10_000_000), Candidate(4, "Dewi", 30_000_000),
                Candidate(5, "Eka", 20_000_000), Candidate(6, "Fajar", 35_000_000),
                Candidate(7, "Gita", 12_000_000), Candidate(8, "Hani", 28_000_000),
                Candidate(9, "Irfan", 18_000_000), Candidate(10, "Joko", 22_000_000),
                Candidate(11, "Kiki", 40_000_000), Candidate(12, "Lina", 16_000_000),
                Candidate(13, "Mamat", 14_000_000), Candidate(14, "Nana", 24_000_000),
                Candidate(15, "Ovi", 31_000_000), Candidate(16, "Putu", 19_000_000),
                Candidate(17, "Qori", 27_000_000), Candidate(18, "Riko", 21_000_000),
                Candidate(19, "Soni", 33_000_000), Candidate(20, "Tio", 26_000_000),
                Candidate(21, "Uli", 11_000_000), Candidate(22, "Vina", 29_000_000),
                Candidate(23, "Wawan", 17_000_000), Candidate(24, "Xena", 38_000_000),
            ]
        }
    }

def generate_random_candidates(n):
    random.seed(time.time_ns())
    names_pool = ["Andi", "Budi", "Citra", "Dewi", "Eka", "Fajar", "Gita", "Hani", 
                  "Irfan", "Joko", "Kiki", "Lina", "Mamat", "Nana", "Ovi", "Putu", 
                  "Qori", "Riko", "Soni", "Tio", "Uli", "Vina", "Wawan", "Xena",
                  "Yanto", "Zelda", "Abdi", "Bella", "Candra", "Dina", "Edi", "Fitri"]
    candidates = []
    for i in range(1, n + 1):
        name = names_pool[i - 1] if i - 1 < len(names_pool) else f"K{i}"
        cost = random.randint(10, 100) * 1_000_000
        candidates.append(Candidate(i, name, cost))
    return candidates

def candidates_to_df(candidates):
    data = [{"ID": c.id, "Nama": c.name, "Biaya (Rp)": f"{c.cost:,}".replace(',', '.')} for c in candidates]
    return pd.DataFrame(data)

def df_to_candidates(df):
    candidates = []
    for _, row in df.iterrows():
        cost_str = str(row["Biaya (Rp)"]).replace('.', '').replace(',', '').replace('Rp', '').strip()
        try:
            cost = int(cost_str)
        except ValueError:
            cost = 0
        candidates.append(Candidate(int(row["ID"]), str(row["Nama"]), cost))
    return candidates
