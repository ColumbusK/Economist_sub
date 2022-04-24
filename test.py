dic1 = {"a": 3}
dic2 = {"b": 4}

print(dic1 == dic2)


ls1 = [1,2,3]
set1 = set(ls1)
set2 = {2,3,4}

for ele in set2:
    set1.add(ele)

print(set1)

ls1.clear()
print(ls1)