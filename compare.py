import ast
import argparse
import re


def LevensteinDistance(first: list, second: list) -> float:
    dp = [[0] * len(second) for i in range(len(first))]
    for i in range(len(first)):
        dp[i][0] = i
    for i in range(len(second)):
        dp[0][i] = i
    for j in range(1, len(second)):
        for i in range(1, len(first)):
            if first[i] == second[j]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + 1)
    return 1 - (dp[len(first) - 1][len(second) - 1]) / max(len(first), len(second))


class Visitor(ast.NodeVisitor):
    def __init__(self):
        pass



parser = argparse.ArgumentParser(description="checks the plagiarism percent")
parser.add_argument("input", metavar="input", type=str, help='enter input file path')
parser.add_argument("output", metavar="output", type=str, help='enter output file path')
args = parser.parse_args()

input_file = args.input
output = args.output

with open(input_file) as f, open(output, 'w') as o:
    for line in f:
        path1, path2 = line.split()
        with open(path1) as p1, open(path2) as p2:
            sample1 = p1.read().lower()
            sample1 = re.sub("_", "", sample1)
            sample2 = p2.read().lower()
            sample2 = re.sub("_", "", sample2)
            tree = ast.parse(sample1)
            tree2 = ast.parse(sample2)

            visitor = Visitor()
            visitor.visit(tree)
            structure = visitor.get_res()
            structure[0].sort()


            visitor2 = Visitor()
            visitor2.visit(tree2)
            structure2 = visitor2.get_res()
            structure2[0].sort()


            o.write(str(LevensteinDistance(structure[0], structure2[0])) + '\n')
