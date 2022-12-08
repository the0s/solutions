# Find the longest branch of a linear traversed tree

def branch(tree):
    n = len(tree)
    if n <= 2:
        return max(tree)
    else:
        t = n//2
        return max(branch(tree[:t]), branch(tree[t:]))

def branch_level_splitter(x):
    i = 1
    st = []
    s = 0
    while(i <= len(x)):
        # print(s, i)
        st.append(x[s:i])
        s = i
        i = i*2 + 1
    return st

def longest_branch(x):
    branches = branch_level_splitter(x)
    total = 0
    for i in branches:
        total += branch(i)
        print("Total", total)
    return branches, total

if __name__ == "__main__":
    linear_tree = [1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, 1, -1, -1, 1]
    result, total = longest_branch(linear_tree)
    print(result, "TOTAL", total)
