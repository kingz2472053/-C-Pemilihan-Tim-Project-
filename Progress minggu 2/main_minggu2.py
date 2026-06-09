import random
import time
from models import Candidate
from algorithm import BranchAndBound
from test_algorithm import run_all

def print_search_tree(result, candidates, max_display=40):
    nodes = result.tree_nodes
    if not nodes:
        print("  (Tidak ada node untuk ditampilkan)")
        return

    node_map = {}
    children = {}
    root_id = None

    for n in nodes:
        node_map[n.node_id] = n
        if n.parent_id is None:
            root_id = n.node_id
        else:
            if n.parent_id not in children:
                children[n.parent_id] = []
            children[n.parent_id].append(n.node_id)

    if root_id is None:
        print("  (Root node tidak ditemukan)")
        return

    count = [0]

    def _print_node(nid, prefix, is_last):
        if count[0] >= max_display:
            return
        count[0] += 1

        n = node_map[nid]
        connector = "`-- " if is_last else "|-- "

        if n.is_solution:
            status = "<< SOLUSI OPTIMAL >>"
        elif n.pruned:
            status = "[DIPANGKAS]"
        else:
            status = "[AKTIF]"

        team_str = n.label if n.label else "root"
        cost_str = f"Biaya=Rp {n.total_cost:,}" if n.total_cost > 0 else "Biaya=Rp 0"
        lb_str = f"LB=Rp {n.lower_bound:,}"

        print(f"  {prefix}{connector}{team_str}  {cost_str}  {lb_str}  {status}")

        kids = children.get(nid, [])
        for i, kid in enumerate(kids):
            ext = "    " if is_last else "|   "
            _print_node(kid, prefix + ext, i == len(kids) - 1)

    _print_node(root_id, "", True)

    if count[0] >= max_display:
        remaining = len(nodes) - max_display
        print(f"\n  ... (ditampilkan {max_display} dari {len(nodes)} node, {remaining} node lainnya tidak ditampilkan)")

def print_alternative_teams(bb, result):
    alternatives = bb.get_alternative_teams()
    if len(alternatives) <= 1:
        print("\n  Tidak ada tim alternatif lain dengan biaya yang sama.")
        return

    print(f"\n  Ditemukan {len(alternatives)} kombinasi tim dengan biaya optimal yang sama (Rp {result.best_cost:,}):")
    print(f"  {'No':>4}  {'Anggota Tim':<40} {'Total Biaya (Rp)':>16}")
    print("  " + "-" * 64)

    for i, sol in enumerate(alternatives, 1):
        names = ", ".join(bb.candidates[idx].name for idx in sol["team"])
        marker = " << terpilih" if sol["team"] == result.best_team else ""
        print(f"  {i:>4}  {names:<40} {sol['cost']:>16,}{marker}")

PRESETS = {
    "1": {
        "name": "Small (n=12)",
        "candidates": [
            Candidate(1, "Andi", 15_000_000),
            Candidate(2, "Budi", 25_000_000),
            Candidate(3, "Citra", 10_000_000),
            Candidate(4, "Dewi", 30_000_000),
            Candidate(5, "Eka", 20_000_000),
            Candidate(6, "Fajar", 35_000_000),
            Candidate(7, "Gita", 12_000_000),
            Candidate(8, "Hani", 28_000_000),
            Candidate(9, "Irfan", 18_000_000),
            Candidate(10, "Joko", 22_000_000),
            Candidate(11, "Kiki", 40_000_000),
            Candidate(12, "Lina", 16_000_000),
        ],
        "k": 5,
        "B": 100_000_000
    },
    "2": {
        "name": "Medium (n=18)",
        "candidates": [
            Candidate(1, "Andi", 15_000_000),
            Candidate(2, "Budi", 25_000_000),
            Candidate(3, "Citra", 10_000_000),
            Candidate(4, "Dewi", 30_000_000),
            Candidate(5, "Eka", 20_000_000),
            Candidate(6, "Fajar", 35_000_000),
            Candidate(7, "Gita", 12_000_000),
            Candidate(8, "Hani", 28_000_000),
            Candidate(9, "Irfan", 18_000_000),
            Candidate(10, "Joko", 22_000_000),
            Candidate(11, "Kiki", 40_000_000),
            Candidate(12, "Lina", 16_000_000),
            Candidate(13, "Mamat", 14_000_000),
            Candidate(14, "Nana", 24_000_000),
            Candidate(15, "Ovi", 31_000_000),
            Candidate(16, "Putu", 19_000_000),
            Candidate(17, "Qori", 27_000_000),
            Candidate(18, "Riko", 21_000_000),
        ],
        "k": 7,
        "B": 140_000_000
    },
    "3": {
        "name": "Large (n=24)",
        "candidates": [
            Candidate(1, "Andi", 15_000_000),
            Candidate(2, "Budi", 25_000_000),
            Candidate(3, "Citra", 10_000_000),
            Candidate(4, "Dewi", 30_000_000),
            Candidate(5, "Eka", 20_000_000),
            Candidate(6, "Fajar", 35_000_000),
            Candidate(7, "Gita", 12_000_000),
            Candidate(8, "Hani", 28_000_000),
            Candidate(9, "Irfan", 18_000_000),
            Candidate(10, "Joko", 22_000_000),
            Candidate(11, "Kiki", 40_000_000),
            Candidate(12, "Lina", 16_000_000),
            Candidate(13, "Mamat", 14_000_000),
            Candidate(14, "Nana", 24_000_000),
            Candidate(15, "Ovi", 31_000_000),
            Candidate(16, "Putu", 19_000_000),
            Candidate(17, "Qori", 27_000_000),
            Candidate(18, "Riko", 21_000_000),
            Candidate(19, "Soni", 33_000_000),
            Candidate(20, "Tio", 26_000_000),
            Candidate(21, "Uli", 11_000_000),
            Candidate(22, "Vina", 29_000_000),
            Candidate(23, "Wawan", 17_000_000),
            Candidate(24, "Xena", 38_000_000),
        ],
        "k": 9,
        "B": 180_000_000
    }
}

def get_int_input(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = input(prompt).strip()
            if not val:
                print("  [Error] Input tidak boleh kosong.")
                continue
            val_int = int(val)
            if min_val is not None and val_int < min_val:
                print(f"  [Error] Nilai minimal adalah {min_val:,}.")
                continue
            if max_val is not None and val_int > max_val:
                print(f"  [Error] Nilai maksimal adalah {max_val:,}.")
                continue
            return val_int
        except ValueError:
            print("  [Error] Masukkan angka integer yang valid.")

def print_candidates(candidates):
    print("\n  DAFTAR KANDIDAT:")
    print(f"  {'No':>4}  {'Nama':<16} {'Biaya (Rp)':>16}")
    print("  " + "-" * 40)
    for i, c in enumerate(candidates, 1):
        print(f"  {i:>4}  {c.name:<16} Rp {c.cost:>13,}")
    print("  " + "-" * 40)

def run_solver(candidates, k, B):
    print("\n" + "=" * 60)
    print("  MENJALANKAN BRANCH & BOUND SOLVER...")
    print("=" * 60)
    
    bb = BranchAndBound(candidates, k, B)
    result = bb.solve()

    print("\n" + "=" * 60)
    print("  OUTPUT 1 — TIM TERPILIH & TOTAL BIAYA")
    print("=" * 60)

    if result.is_feasible:
        print("\n  TIM TERPILIH:")
        print(f"  {'Nama':<16} {'Biaya (Rp)':>16}")
        print("  " + "-" * 34)
        for idx in result.best_team:
            c = bb.candidates[idx]
            print(f"  {c.name:<16} Rp {c.cost:>13,}")
        print("  " + "-" * 34)
        print(f"  {'Total Biaya':<16} Rp {result.best_cost:>13,}")
        print(f"  {'Sisa Anggaran':<16} Rp {B - result.best_cost:>13,}")
    else:
        print("\n  [ERROR] Tidak ada tim yang memenuhi anggaran B.")

    print("\n" + "=" * 60)
    print("  OUTPUT 2 — RINGKASAN PROSES B&B")
    print("=" * 60)

    print(f"\n  Node dieksplorasi  : {result.nodes_explored:,}")
    print(f"  Node dipangkas     : {result.nodes_pruned:,}")
    print(f"  Solusi feasible    : {result.nodes_feasible:,}")
    eff = result.nodes_pruned / max(result.nodes_explored, 1) * 100
    print(f"  Efisiensi pruning  : {eff:.1f}%")
    print(f"  Waktu komputasi    : {result.elapsed_sec*1000:.4f} ms")

    print("\n" + "=" * 60)
    print("  FITUR TAMBAHAN — TIM ALTERNATIF DENGAN BIAYA SETARA")
    print("=" * 60)
    print_alternative_teams(bb, result)

    print("\n" + "=" * 60)
    print("  FITUR TAMBAHAN — PELACAK POHON PENCARIAN B&B (ASCII TREE)")
    print("=" * 60)
    print()
    print_search_tree(result, candidates, max_display=40)
    print("\n" + "=" * 60)

def main_menu():
    while True:
        print("\n" + "=" * 60)
        print("     SISTEM PEMILIHAN TIM PROYEK (BRANCH & BOUND) - MINGGU 1")
        print("=" * 60)
        print("  1. Gunakan Preset Dataset (Small/Medium/Large)")
        print("  2. Buat Dataset Kustom")
        print("  3. Jalankan Unit Test")
        print("  4. Keluar")
        print("=" * 60)
        choice = input("  Pilih opsi (1-4): ").strip()

        if choice == "1":
            print("\n  PILIH PRESET:")
            print("  1) Small (n=12, k=5, B=100.000.000)")
            print("  2) Medium (n=18, k=7, B=140.000.000)")
            print("  3) Large (n=24, k=9, B=180.000.000)")
            preset_choice = input("  Pilih preset (1-3): ").strip()
            if preset_choice not in PRESETS:
                print("  [Error] Pilihan preset tidak valid.")
                continue
            
            preset = PRESETS[preset_choice]
            candidates = preset["candidates"]
            k = preset["k"]
            B = preset["B"]
            
            print_candidates(candidates)
            print(f"  Parameter Tim Saat Ini: k={k}, B=Rp {B:,}")
            
            change = input("  Apakah ingin mengubah parameter tim (k dan B)? (y/n): ").strip().lower()
            if change == "y":
                k = get_int_input("  Masukkan k (ukuran tim, 5 <= k <= 10): ", 5, 10)
                if k > len(candidates):
                    print(f"  [Warning] k ({k}) tidak boleh lebih besar dari jumlah kandidat ({len(candidates)}). Diatur ke {len(candidates)}.")
                    k = len(candidates)
                B = get_int_input("  Masukkan B (anggaran maks, integer): ", 0)
            
            run_solver(candidates, k, B)
            
        elif choice == "2":
            print("\n" + "-" * 60)
            print("  MEMBUAT DATASET KUSTOM")
            print("-" * 60)
            n = get_int_input("  Masukkan jumlah kandidat n (n >= 12): ", 12)
            k = get_int_input("  Masukkan k (ukuran tim, 5 <= k <= 10): ", 5, 10)
            if k > n:
                print(f"  [Warning] k tidak boleh lebih besar dari n. k disesuaikan menjadi {n}.")
                k = n
            B = get_int_input("  Masukkan B (anggaran maks, integer): ", 0)
            
            print("\n  Opsi pengisian data kandidat:")
            print("  1) Input Manual Satu Per Satu")
            print("  2) Auto-Generate Data Kandidat Acak")
            input_mode = input("  Pilih opsi (1-2): ").strip()
            
            candidates = []
            if input_mode == "1":
                for i in range(1, n + 1):
                    print(f"\n  Kandidat ke-{i}:")
                    name = input(f"    Nama (default: K{i}): ").strip()
                    if not name:
                        name = f"K{i}"
                    cost = get_int_input(f"    Biaya untuk {name} (Rp): ", 0)
                    candidates.append(Candidate(i, name, cost))
            else:
                # Auto generate
                random.seed(time.time_ns())
                names_pool = ["Andi", "Budi", "Citra", "Dewi", "Eka", "Fajar", "Gita", "Hani", 
                              "Irfan", "Joko", "Kiki", "Lina", "Mamat", "Nana", "Ovi", "Putu", 
                              "Qori", "Riko", "Soni", "Tio", "Uli", "Vina", "Wawan", "Xena",
                              "Yanto", "Zelda", "Abdi", "Bella", "Candra", "Dina", "Edi", "Fitri"]
                for i in range(1, n + 1):
                    name = names_pool[i - 1] if i - 1 < len(names_pool) else f"K{i}"
                    cost = random.randint(10, 100) * 1_000_000
                    candidates.append(Candidate(i, name, cost))
                print(f"\n  [OK] Berhasil men-generate {n} kandidat secara acak.")
            
            print_candidates(candidates)
            run_solver(candidates, k, B)

        elif choice == "3":
            run_all()
            
        elif choice == "4":
            print("\n  Terima kasih telah menggunakan sistem pemilihan tim proyek!")
            break
        else:
            print("  [Error] Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main_menu()
