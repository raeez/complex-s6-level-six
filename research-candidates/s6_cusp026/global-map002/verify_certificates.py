"""Verify retained Smith certificates with independent integer arithmetic."""
from fractions import Fraction
from pathlib import Path
import json


def product(left, right):
    if not left:
        return []
    if not right:
        return [[] for row in left]
    return [[sum(a * b for a, b in zip(row, column))
             for column in zip(*right)] for row in left]


def determinant(matrix):
    rows = [[Fraction(value) for value in row] for row in matrix]
    result = Fraction(1)
    for i in range(len(rows)):
        pivot = next((j for j in range(i, len(rows)) if rows[j][i]), None)
        if pivot is None:
            return 0
        if pivot != i:
            rows[i], rows[pivot] = rows[pivot], rows[i]
            result = -result
        value = rows[i][i]
        result *= value
        for j in range(i + 1, len(rows)):
            factor = rows[j][i] / value
            rows[j] = [a - factor * b for a, b in zip(rows[j], rows[i])]
    assert result.denominator == 1
    return int(result)


record = Path(__file__).resolve().parents[3] / "reports/research/s6_cusp026/global-map002/exact-checks.json"
data = json.loads(record.read_text())
certificates = []
def collect(value):
    if isinstance(value, dict):
        if all(key in value for key in ["matrix", "left", "right", "diagonal", "factors"]):
            certificates.append(value)
        for child in value.values():
            collect(child)
    elif isinstance(value, list):
        for child in value:
            collect(child)
collect(data)
for certificate in certificates:
    matrix, left, right, diagonal = [certificate[key] for key in ["matrix", "left", "right", "diagonal"]]
    assert abs(determinant(left)) == abs(determinant(right)) == 1
    assert product(product(left, matrix), right) == diagonal
    factors = []
    for i, row in enumerate(diagonal):
        for j, value in enumerate(row):
            assert i == j or value == 0
        if i < len(row) and row[i]:
            factors.append(abs(row[i]))
    assert factors == certificate["factors"]
    assert all(b % a == 0 for a, b in zip(factors, factors[1:]))
print(json.dumps({"verified_certificates": len(certificates), "arithmetic": "standard-library integers and rational elimination", "result": "all certificates passed"}, indent=2))
