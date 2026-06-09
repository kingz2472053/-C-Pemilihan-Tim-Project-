import time
from typing import List
from models import Candidate, BBNode, SolveResult


class BranchAndBound:
    def __init__(self, candidates: List[Candidate], k: int, B: int):
        self.candidates = sorted(candidates, key=lambda c: c.cost)
        self.k = k
        self.B = B
        self.n = len(candidates)
        self._best_cost = float('inf')
        self._best_team = []
        self._node_counter = 0
        self._nodes_explored = 0
        self._nodes_pruned = 0
        self._nodes_feasible = 0
        self._tree_nodes = []
        self._all_solutions = []

    def solve(self) -> SolveResult:
        t0 = time.perf_counter()
        self._bb(level=0, selected=[], total_cost=0, parent_id=None)
        elapsed = time.perf_counter() - t0

        return SolveResult(
            best_team=self._best_team,
            best_cost=self._best_cost if self._best_team else 0,
            is_feasible=bool(self._best_team),
            nodes_explored=self._nodes_explored,
            nodes_pruned=self._nodes_pruned,
            nodes_feasible=self._nodes_feasible,
            elapsed_sec=elapsed,
            tree_nodes=self._tree_nodes,
            all_solutions=self._all_solutions,
        )

    def _lower_bound(self, selected, next_level):
        needed = self.k - len(selected)
        current_cost = sum(self.candidates[i].cost for i in selected)

        if needed <= 0:
            return current_cost

        available = [
            self.candidates[i].cost
            for i in range(next_level, self.n)
            if i not in selected
        ]
        if len(available) < needed:
            return 10**18

        return current_cost + sum(available[:needed])

    def _new_node_id(self):
        self._node_counter += 1
        return self._node_counter

    def _bb(self, level, selected, total_cost, parent_id):
        self._nodes_explored += 1
        node_id = self._new_node_id()
        lb = self._lower_bound(selected, level)

        node = BBNode(
            node_id=node_id,
            parent_id=parent_id,
            level=len(selected),
            selected=list(selected),
            total_cost=total_cost,
            lower_bound=lb,
            label=(f"[{','.join(str(self.candidates[i].id) for i in selected)}]"
                   if selected else "root"),
        )

        if len(selected) == self.k:
            self._nodes_feasible += 1
            if total_cost <= self._best_cost and total_cost <= self.B:
                if total_cost < self._best_cost:
                    self._best_cost = total_cost
                    self._best_team = list(selected)
                node.is_solution = True
                self._all_solutions.append({
                    "team": list(selected),
                    "cost": total_cost,
                })
            self._tree_nodes.append(node)
            return

        remaining_slots = self.k - len(selected)
        remaining_cands = self.n - level

        if remaining_cands < remaining_slots:
            self._nodes_pruned += 1
            node.pruned = True
            self._tree_nodes.append(node)
            return

        if lb > self._best_cost or lb > self.B:
            self._nodes_pruned += 1
            node.pruned = True
            self._tree_nodes.append(node)
            return

        self._tree_nodes.append(node)
        for i in range(level, self.n - remaining_slots + 1):
            new_cost = total_cost + self.candidates[i].cost
            if new_cost <= self.B:
                self._bb(i + 1, selected + [i], new_cost, node_id)

    def get_alternative_teams(self):
        if not self._all_solutions:
            return []
        best = self._best_cost
        return [s for s in self._all_solutions if s["cost"] == best]
