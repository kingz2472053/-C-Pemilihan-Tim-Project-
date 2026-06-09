from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Candidate:
    id: int
    name: str
    cost: int

    def __repr__(self):
        return f"Candidate(id={self.id}, name={self.name!r}, cost={self.cost:,})"

    def display(self) -> str:
        return f"[{self.id:>2}] {self.name:<14} Rp {self.cost:>12,}"

@dataclass
class BBNode:
    node_id: int
    parent_id: Optional[int]
    level: int
    selected: List[int]
    total_cost: int
    lower_bound: int
    pruned: bool = False
    is_solution: bool = False
    label: str = ""

@dataclass
class SolveResult:
    best_team: List[int]
    best_cost: int
    is_feasible: bool
    nodes_explored: int
    nodes_pruned: int
    nodes_feasible: int
    elapsed_sec: float
    tree_nodes: List[BBNode] = field(default_factory=list)
    all_solutions: List[dict] = field(default_factory=list)
