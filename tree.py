from dataclasses import dataclass, field
from typing import List, Optional

from game_logic import GameState


@dataclass
class TreeNode:
    state: GameState
    depth: int = 0
    move_index: Optional[int] = None
    move_pair: Optional[str] = None
    replacement: Optional[str] = None
    points_gained: int = 0
    children: List["TreeNode"] = field(default_factory=list)

    def is_terminal(self) -> bool:
        return self.state.game_over

    def expand(self) -> List["TreeNode"]:
        """
        Ģenerē visus bērnmezglus no pašreizējā stāvokļa,
        balstoties uz visiem legālajiem gājieniem.
        """
        if self.children:
            return self.children

        if self.state.game_over:
            return self.children

        legal_moves = self.state.get_legal_moves()

        for move in legal_moves:
            child_state = self.state.copy()
            original_pair = child_state.s[move:move + 2]

            pair, replacement, pts = child_state.apply_move(move)

            child = TreeNode(
                state=child_state,
                depth=self.depth + 1,
                move_index=move,
                move_pair=original_pair if original_pair else pair,
                replacement=replacement,
                points_gained=pts,
            )
            self.children.append(child)

        return self.children


def build_game_tree(root_state: GameState, max_depth: int) -> TreeNode:
    """
    Uzbūvē spēles koku līdz noteiktam dziļumam.
    """
    root = TreeNode(state=root_state.copy(), depth=0)
    _build_recursive(root, max_depth)
    return root


def _build_recursive(node: TreeNode, max_depth: int):
    if node.depth >= max_depth:
        return

    if node.state.game_over:
        return

    children = node.expand()
    for child in children:
        _build_recursive(child, max_depth)


def count_nodes(node: TreeNode) -> int:
    total = 1
    for child in node.children:
        total += count_nodes(child)
    return total


def count_leaf_nodes(node: TreeNode) -> int:
    if not node.children:
        return 1
    return sum(count_leaf_nodes(child) for child in node.children)


def tree_to_text(node: TreeNode, indent: int = 0) -> str:
    """
    Pārvērš koku teksta formā.
    Noder debugam un atskaites skaidrojumam.
    """
    prefix = "  " * indent

    if node.move_index is None:
        move_info = "ROOT"
    else:
        move_info = (
            f"move@{node.move_index}: "
            f"{node.move_pair} -> {node.replacement} "
            f"(+{node.points_gained})"
        )

    line = (
        f"{prefix}{move_info} | "
        f"turn={node.state.turn} | "
        f"s='{node.state.s}' | "
        f"O={node.state.score['O']} X={node.state.score['X']} | "
        f"game_over={node.state.game_over}"
    )

    lines = [line]
    for child in node.children:
        lines.append(tree_to_text(child, indent + 1))

    return "\n".join(lines)


def get_root_summary(node: TreeNode) -> str:
    return (
        f"Root: s='{node.state.s}', turn={node.state.turn}, "
        f"O={node.state.score['O']}, X={node.state.score['X']}, "
        f"children={len(node.children)}"
    )