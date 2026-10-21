import random
import subprocess
from pathlib import Path


executable = Path(__file__).with_name("main.exe")
case_count = 0


def check(documents, query, k, expected=None):
    global case_count
    n = len(documents)
    d = len(query)
    lines = [f"{n} {d} {k}"]
    lines.extend(" ".join(map(str, document)) for document in documents)
    lines.append(" ".join(map(str, query)))
    completed = subprocess.run(
        [str(executable)],
        input="\n".join(lines) + "\n",
        text=True,
        capture_output=True,
        check=True,
        timeout=10,
    )
    actual = list(map(int, completed.stdout.split()))
    if expected is None:
        scores = [sum(a * b for a, b in zip(document, query)) for document in documents]
        remaining = set(range(n))
        expected = []
        for _ in range(k):
            best = max(remaining, key=lambda index: (scores[index], -index))
            expected.append(best + 1)
            remaining.remove(best)
    assert actual == expected, (actual, expected)
    case_count += 1


check([[7]], [-3], 1, [1])
check([[1, 0], [0, 1], [1, 1], [-1, -1]], [1, 1], 4, [3, 1, 2, 4])
check([[-3], [-1], [-2]], [1], 2, [2, 3])
check([[1, 2], [-2, 1], [4, -3]], [0, 0], 2, [1, 2])
check([[10000] * 100, [-10000] * 100, [0] * 100], [10000] * 100, 3, [1, 3, 2])

rng = random.Random(20261020)
for _ in range(200):
    n = rng.randint(1, 35)
    d = rng.randint(1, 20)
    documents = [[rng.randint(-10000, 10000) for _ in range(d)] for _ in range(n)]
    query = [rng.randint(-10000, 10000) for _ in range(d)]
    check(documents, query, rng.randint(1, n))

check([[10000] * 10 for _ in range(100000)], [10000] * 10, 100000, list(range(1, 100001)))
print(f"通过 {case_count} 组测试，包含随机输入、相同点积、负数、64 位整数及最大输入规模。")
