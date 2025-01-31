def get_count(data):
    data = data.split('\n')
    for row in data:
        elements = row.split(',')
        if elements[0] == 'col1':
            continue
        elements = [int(e) for e in elements]
        col_elements.append(elements)
        # print(sum(elements))

data = """col1,col2,col3
1,2,3
4,5,6
7,8,9"""

col_elements = []
get_count(data)

for x in range(0,3):
    col_wise_sum = []
    for y in range(0,3):
        col_wise_sum.append(col_elements[y][x])
    print(sum(col_wise_sum))