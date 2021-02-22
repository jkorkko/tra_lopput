def ask_file():
        print("\nType the name of the input file. For example \"test.txt\".")
        while(True):
            try:
                print("")
                input_file = input("Name of the file: ")
                if input_file[-4:] == ".txt":
                    #Get rid of imported lib trough FileNotFoundError?
                    with open(input_file) as test:
                        pass
                    return input_file
                else:
                    print("Expecing a .txt file.")
                    continue
            except FileNotFoundError:
                print("No", input_file, "in directory.")
                continue


def read_file(data, graph):
    '''
    Open & read info from the given input file.
    '''
    with open(data) as input_file:
        input_file = input_file.readlines()
        vertice, edge = input_file.pop(0).split()
        DESTINATION = int(input_file.pop(-1))
        for i in input_file:
            i = i.split()
            i = tuple(map(int, i))
            graph.append((i[0] - 1, i[1] - 1, i[2]))
        graph.sort(key=lambda edge: edge[2])
        return vertice, DESTINATION, graph


def find(cycle, start):
    '''
    This function is made by Neelam Yadav
    https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/
    '''
    if cycle[start] == start:
        return start
    return find(cycle, cycle[start])


def create_mst(graph, VERTICES):
    '''
    Create minimum spanning tree.

    This function is based on code made by Neelam Yadav
    https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/
    '''
    mst = []    #minimum spanninfg tree representation
    cycle = []  #prevent creating cycles in mst
    level = []  #nodes attached to each other
    j, found = 0, 0
    for i in range(VERTICES):
        cycle.append(i)
        level.append(0)
        mst.append([])
    while found < VERTICES - 1:
        start, end, height = graph[j]
        j += 1
        start_index = find(cycle, start)
        end_index = find(cycle, end)
        if start_index != end_index:
            mst[start].append((end, height))
            mst[end].append((start, height))
            found += 1
            if level[start_index] > level[end_index]:
                cycle[end_index] = start_index
            elif level[start_index] < level[end_index]:
                cycle[start_index] = end_index
            else:
                cycle[end_index] = start_index
                level[start_index] += 1
    return mst


def find_path(mst, DESTINATION):
    '''
    Find path from point 1 to destination from
    minimum spanning tree
    '''
    path, heights = [0], []
    while path[-1] != DESTINATION:
        if len(mst[path[-1]]) == 0:
            path.pop(-1)
            heights.pop(-1)
            continue
        else:
            new_vertice, new_height = mst[path[-1]][0]
            path.append(new_vertice)
            heights.append(new_height)
        mst[new_vertice].remove((path[-2], new_height))
        mst[path[-2]].pop(0)
    for v in path:
        print(v + 1)
    return max(heights)


def main():
    '''
    Run algorithm
    '''
    graph = []  #full map representation
    input_file = ask_file()
    VERTICES, DESTINATION, graph = read_file(input_file, graph)
    mst = create_mst(graph, int(VERTICES))
    print("reitti:")
    answer = find_path(mst, DESTINATION - 1)
    print("matalimman reitin korkein kohta", answer)


main()
