from game_logic import GameState
from tree import build_game_tree, tree_to_text, count_nodes, count_leaf_nodes

g = GameState()
g.generate(6)

tree = build_game_tree(g, max_depth=2)

print(tree_to_text(tree))
print("Nodes:", count_nodes(tree))
print("Leaves:", count_leaf_nodes(tree))