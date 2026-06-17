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

def demo_basic():
    print("=" * 60)
    print("  DEMO PEMILIHAN TIM PROYEK — Branch & Bound (Minggu 1)")
    print("=" * 60)

    candidates = [
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
    ]

    k = 5
    B = 100_000_000

    print(f"\n  Jumlah kandidat (n) : {len(candidates)}")
    print(f"  Ukuran tim (k)      : {k}")
    print(f"  Anggaran maks (B)   : Rp {B:,}")

    print("\n  DAFTAR KANDIDAT:")
    print(f"  {'No':>4}  {'Nama':<14} {'Biaya (Rp)':>14}")
    print("  " + "-" * 36)
    for c in candidates:
        print(f"  {c.id:>4}  {c.name:<14} {c.cost:>14,}")

    bb = BranchAndBound(candidates, k, B)
    result = bb.solve()

    print("\n" + "=" * 60)
    print("  OUTPUT 1 — TIM TERPILIH & TOTAL BIAYA")
    print("=" * 60)

    if result.is_feasible:
        print("\n  TIM TERPILIH:")
        print(f"  {'Nama':<14} {'Biaya (Rp)':>14}")
        print("  " + "-" * 30)
        for idx in result.best_team:
            c = bb.candidates[idx]
            print(f"  {c.name:<14} {c.cost:>14,}")
        print("  " + "-" * 30)
        print(f"  {'Total Biaya':<14} {result.best_cost:>14,}")
        print(f"  {'Sisa Anggaran':<14} {B - result.best_cost:>14,}")
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

if __name__ == "__main__":
    demo_basic()
    print("\n\n")
    run_all()
