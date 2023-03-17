n = int(input())
a = list(map(int, input().split()))
result = 0

for i in range(n):
    s = 0
    d = []
    for j in range(i, n):
        s += a[j]
        if s == 0:
            result += 1
            break
        d.append(j)
    if j in d:
        result += 1
print(result)