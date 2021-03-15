def ask_file():
    '''
    Kysy käyttäjältä syötetiedostoa
    '''
    print("\n Anna syötetiedoston nimi. Esimerkiksi: \"test.txt\".")
    while(True):
        try:
            print("")
            input_file = input(" Tiedoston nimi: ")
            if input_file[-4:] == ".txt":
                # Varmista, että tiedosto löytyy kansiosta
                with open(input_file) as test:
                    pass
                return input_file
            else:
                print(" Odotetaan \".txt\"-tiedostoa.")
                continue
        except FileNotFoundError:
            print(" Tiedostoa", input_file, "ei löydy kansiosta.")
            continue


def read_file(data):
    '''
    Lue graafi syötteestä.
    '''
    graph = []
    with open(data) as input_file:
        input_file = input_file.readlines()
        vertice, edge = input_file.pop(0).split()
        DESTINATION = int(input_file.pop(-1))
        # Luo lista kaikista graafin sivuista
        # nousevassa järjetyksessä.
        for i in input_file:
            i = i.split()
            i = tuple(map(int, i))
            graph.append((i[0] - 1, i[1] - 1, i[2]))
        graph.sort(key=lambda edge: edge[2])
        return vertice, DESTINATION, graph


def find(cycle, start):
    '''
    Etsi vanhempi.

    -Tämän funktion on tehnyt Neelam Yadav-
    https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/
    '''
    if cycle[start] == start:
        return start
    return find(cycle, cycle[start])


def create_mst(graph, VERTICES):
    '''
    Muodosta minimivirittäväpuu Kruskalin algoritmilla.

    -Osa funktiosta perustuu Neelam Yadavin tekemään koodiin-
    https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/
    '''
    mst = []    # minimivirittävä puu
    cycle = []
    level = []
    j, found = 0, 0
    # Alusta listat oikeilla arvoilla
    for i in range(VERTICES):
        cycle.append(i)
        level.append(0)
        mst.append([])
    while found < VERTICES - 1:
        start, end, height = graph[j]
        j += 1
        # Etsi vanhemmat käyttäen Path Compressionia
        start_index = find(cycle, start)
        end_index = find(cycle, end)
        # -Jos tosi, sivu ei luo piiriä, lisätään mst:hen.
        # -Jos epätosi, hylkää sivu.
        if start_index != end_index:
            mst[start].append((end, height))
            mst[end].append((start, height))
            found += 1
            # Path Compression
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
    Etsi reitti kaupungista 1 määränpäähän
    minimivirittävästä puusta käyttäen syvyyshakua.
    '''
    path, heights = [0], []
    while path[-1] != DESTINATION:
        if len(mst[path[-1]]) == 0:
            # Polku päättyi umpikujaan, palataan takaisin päin
            path.pop(-1)
            heights.pop(-1)
            continue
        else:
            # Uusi sivu löydettiin
            new_vertice, new_height = mst[path[-1]][0]
            path.append(new_vertice)
            heights.append(new_height)
        # Poista tutkitut sivut
        mst[new_vertice].remove((path[-2], new_height))
        mst[path[-2]].pop(0)
    for v in path:
        print("", v + 1)
    return max(heights)


def main():
    input_file = ask_file()
    VERTICES, DESTINATION, graph = read_file(input_file)
    mst = create_mst(graph, int(VERTICES))
    print(" reitti:")
    answer = find_path(mst, DESTINATION - 1)
    print(" vastaus:", answer)


main()
