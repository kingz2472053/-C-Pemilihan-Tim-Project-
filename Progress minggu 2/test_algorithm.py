import sys
from itertools import combinations
from models import Candidate
from algorithm import BranchAndBound

def make(costs):
    return [Candidate(i + 1, f"C{i + 1}", c) for i, c in enumerate(costs)]

def brute_force(candidates, k, B):
    best = None
    for combo in combinations(range(len(candidates)), k):
        total = sum(candidates[i].cost for i in combo)
        if total <= B and (best is None or total < best):
            best = total
    return best

def test_basic():
    cands = make([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120])
    bb = BranchAndBound(cands, k=5, B=200)
    res = bb.solve()
    bf = brute_force(cands, k=5, B=200)
    assert res.best_cost == bf, f"Expected {bf}, got {res.best_cost}"
    print(f"  [OK] test_basic passed — cost = {res.best_cost:,}")

def test_no_solution():
    cands = make([100] * 12)
    bb = BranchAndBound(cands, k=5, B=100)
    res = bb.solve()
    assert not res.is_feasible
    print("  [OK] test_no_solution passed")

def test_exact_budget():
    cands = make([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120])
    k, B = 5, 150
    bb = BranchAndBound(cands, k=k, B=B)
    res = bb.solve()
    assert res.best_cost <= B
    assert res.best_cost == brute_force(cands, k, B)
    print(f"  [OK] test_exact_budget passed — cost = {res.best_cost:,}")

def test_pruning_reduces_nodes():
    cands = make([i * 5_000_000 for i in range(1, 13)])
    k, B = 5, 100_000_000
    bb = BranchAndBound(cands, k=k, B=B)
    res = bb.solve()
    total_combos = len(list(combinations(range(12), k)))
    assert res.nodes_explored < total_combos * 5
    print(f"  [OK] test_pruning passed — nodes={res.nodes_explored}, bf_combos={total_combos}, pruned={res.nodes_pruned}")

def test_medium():
    import random
    rng = random.Random(7)
    names = [f"K{i}" for i in range(1, 19)]
    cands = [Candidate(i + 1, names[i], rng.randint(10, 100) * 1_000_000) for i in range(18)]
    sorted_c = sorted(c.cost for c in cands)
    B = sum(sorted_c[:6]) + 20_000_000
    bb = BranchAndBound(cands, k=6, B=B)
    res = bb.solve()
    bf = brute_force(cands, k=6, B=B)
    assert res.best_cost == bf, f"Expected {bf}, got {res.best_cost}"
    print(f"  [OK] test_medium passed — n=18, optimal={res.best_cost:,}")

def test_large():
    import random
    rng = random.Random(42)
    names = [f"L{i}" for i in range(1, 25)]
    cands = [Candidate(i + 1, names[i], rng.randint(10, 100) * 1_000_000) for i in range(24)]
    sorted_c = sorted(c.cost for c in cands)
    B = sum(sorted_c[:8]) + 35_000_000
    bb = BranchAndBound(cands, k=8, B=B)
    res = bb.solve()
    bf = brute_force(cands, k=8, B=B)
    assert res.best_cost == bf, f"Expected {bf}, got {res.best_cost}"
    print(f"  [OK] test_large passed — n=24, optimal={res.best_cost:,} in {res.elapsed_sec*1000:.2f} ms")

def test_alternative_teams():
    cands = make([10, 10, 20, 20, 30, 30, 40, 40, 50, 50, 60, 60])
    bb = BranchAndBound(cands, k=5, B=200)
    res = bb.solve()
    alts = bb.get_alternative_teams()
    assert len(alts) > 1
    for a in alts:
        assert a["cost"] == res.best_cost
    print(f"  [OK] test_alternative_teams passed — Found {len(alts)} alternative teams")

def run_all():
    print("\n" + "=" * 50)
    print("  UNIT TEST — Branch & Bound Algorithm")
    print("=" * 50)
    tests = [
        test_basic,
        test_no_solution,
        test_exact_budget,
        test_pruning_reduces_nodes,
        test_medium,
        test_large,
        test_alternative_teams
    ]
    passed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except AssertionError as e:
            print(f"  [FAIL] {t.__name__} FAILED: {e}")
        except Exception as e:
            print(f"  [FAIL] {t.__name__} ERROR: {e}")
    print(f"\n  Hasil: {passed}/{len(tests)} test passed")
    print("=" * 50 + "\n")
    return passed == len(tests)

if __name__ == "__main__":
    ok = run_all()
    sys.exit(0 if ok else 1)
