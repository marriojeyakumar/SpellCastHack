import string

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def startsWith(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

def getAdjacentTiles(row, col, board):
    adjacentTiles = []
    for i in range(max(0, row - 1), min(len(board), row + 2)):
        for j in range(max(0, col - 1), min(len(board[0]), col + 2)):
            if i != row or j != col:
                adjacentTiles.append((i, j))
    return adjacentTiles

def optimized_dfs(row, col, board, seen, currentWord, currentScore, maxScore, trie, letterToPoints):
    if (row, col) in seen or not trie.startsWith(currentWord + board[row][col]):
        return

    seen.add((row, col))
    letter = board[row][col]
    currentWord += letter
    currentScore += letterToPoints[letter]

    if trie.search(currentWord) and currentScore > maxScore['score']:
        maxScore['score'] = currentScore
        maxScore['word'] = currentWord

    for (nextRow, nextCol) in getAdjacentTiles(row, col, board):
        optimized_dfs(nextRow, nextCol, board, seen.copy(), currentWord, currentScore, maxScore, trie, letterToPoints)

    seen.remove((row, col))

def findHighest(board, trie, letterToPoints):
    maxScore = {'word': '', 'score': 0}
    for row in range(len(board)):
        for col in range(len(board[0])):
            optimized_dfs(row, col, board, set(), "", 0, maxScore, trie, letterToPoints)
    return maxScore['word'], maxScore['score']

def build_trie_from_file(file_path):
    trie = Trie()
    with open(file_path, 'r') as file:
        for word in file:
            trie.insert(word.strip().lower())
    return trie

letterToPoints = {char: value for char, value in zip(string.ascii_lowercase, [1, 4, 5, 3, 1, 5, 3, 4, 1, 7, 3, 3, 4, 2, 1, 4, 8, 2, 2, 2, 4, 5, 5, 7, 4, 8])}

words = build_trie_from_file('validWords.txt')


board = [
    ["z", "e", "o", "r", "g"],
    ["j", "n", "r", "l", "r"],
    ["a", "i", "a", "m", "i"],
    ["h", "e", "i", "i", "s"],
    ["h", "e", "u", "v", "a"]
]

highest_scoring_word, score = findHighest(board, words, letterToPoints)
print(f"Highest scoring word: {highest_scoring_word}, Score: {score}")
