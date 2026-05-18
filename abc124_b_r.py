n = int(input())
h = list(map(int,input().split()))
max_count = 1
count = 0
for i in h:
    if i >= max_count:
        max_count = i
        count += 1
print(count)