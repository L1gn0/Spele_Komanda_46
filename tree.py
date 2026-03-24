class GameNode:
    def __init__(self, state, player, children=None):
        self.state = state
        self.player = player
        self.children = children if children else []


def make_state(string, turn="O"):
    return {"board": string, "turn": turn}


def get_possible_moves(state):
    board = state["board"]
    moves = []
    for i in range(len(board)):
        if board[i] == "X":
            new_board = board[:i] + "O" + board[i+1:]
            moves.append(new_board)
    return moves


def switch_player(player):
    return "X" if player == "O" else "O"


def build_game_tree(state, depth, ai_player):
    if depth == 0:
        return GameNode(state, state["turn"])

    node = GameNode(state, state["turn"])

    moves = get_possible_moves(state)
    for move in moves:
        child_state = {
            "board": move,
            "turn": switch_player(state["turn"])
        }
        child_node = build_game_tree(child_state, depth - 1, ai_player)
        node.children.append(child_node)

    return node


def tree_to_text(node, level=0):
    result = "  " * level + f"{node.state['board']} ({node.player})\n"
    for child in node.children:
        result += tree_to_text(child, level + 1)
    return result


def tree_to_dot(node):
    lines = ["digraph G {"]
    counter = {"id": 0}

    def traverse(n, parent_id=None):
        node_id = counter["id"]
        counter["id"] += 1

        label = n.state["board"]
        lines.append(f'  node{node_id} [label="{label}"];')

        if parent_id is not None:
            lines.append(f"  node{parent_id} -> node{node_id};")

        for child in n.children:
            traverse(child, node_id)

    traverse(node)
    lines.append("}")
    return "\n".join(lines)
