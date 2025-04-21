from itertools import combinations
from collections import defaultdict

def AnyUnreachableStates(phi, A, Q, q_start):
    visited = set()
    to_check = [q_start]
 
    while to_check: #O(|Q|)
        state = to_check.pop() #O(1)
        visited.add(state) #O(1)
        for a in A: #O(|A|)
            to_check_state = phi[(state, a)] #O(1)
            if to_check_state not in visited:
                visited.add(to_check_state) #O(1)
                to_check.append(to_check_state) #O(1)
    
    return len(visited) != len(Q) #O(1) + O(1)
# total = O(|Q| * |A|) 


def StatesEquivalentRec(A, phi, psi, q0, q1, Q_length, word_len = 0, word = ''): 
    word_len += 1
    for a in A:
        exit_q0_symbol, exit_q1_symbol = psi[(q0, a)], psi[(q1, a)]
        new_q0, new_q1 = phi[(q0, a)], phi[(q1, a)]
        new_word = word + str(a)

        #print('\nenter_symbol:', a)
        #print('word:', new_word)
        #print('exit_q0_symbol:', exit_q0_symbol, 'exit_q1_symbol:', exit_q1_symbol)
        #print('new_q0:', new_q0, 'new_q1:', new_q1)

        if exit_q0_symbol != exit_q1_symbol:
            print(new_word, '- word that indicates that states are not equivalent')
            return False
        if word_len < Q_length - 1: 
            res = StatesEquivalentRec(A, phi, psi, new_q0, new_q1, Q_length, word_len, new_word)
            if res == False: return False

    return True
# total = O(log(|Q| - 1))



def AnyEquivalentStates(Q, A, phi, psi):
    len_Q = len(Q)
    for q0, q1 in combinations(Q, 2):
        if StatesEquivalentRec(A, phi, psi, q0, q1, len_Q):
            return True
        print('states', q0, 'and', q1, 'are not equivalent')
    
    return False
# total = O(C{Q,2} * log(|Q| - 1))

def IsMinimized(Q, A, phi, psi, q_start):
    
    if AnyUnreachableStates(phi, A, Q, q_start):
        return False
    
    if AnyEquivalentStates(Q, A, phi, psi):
        return False
    
    return True
# total = O(|Q| * |A|) + O(C{Q,2} * log(|Q| - 1))


def build_intersect_source(schema_encoding, A, B, Q, phi, psi, q_start): 
    edges = defaultdict(list) 
    empty_empty_vertex = (('', ''), (q_start, q_start), ('', ''))

    start_vertex = empty_empty_vertex
    final_vertexes = []

    vertexes = [empty_empty_vertex]
    seen = set(empty_empty_vertex)

    for v in vertexes:
        len_v0 = len(v[0][0])
        len_v1 = len(v[0][1])
        for a1, a1_encoding in schema_encoding.items():
            a1_encoding_len = len(a1_encoding)

            if len_v0 > len_v1 and a1_encoding.startswith(v[0][0]):
                new_v0_suffix = ''
                new_v1_suffix = a1_encoding[len_v0:]
                new_v_suffixes = (new_v0_suffix, new_v1_suffix)
                
                new_v0_state = v[1][0]
                new_v1_state = phi[(v[1][1], a1)]
                new_v_states = (new_v0_state, new_v1_state)

                new_v0_exit_value = v[2][0]
                new_v1_exit_value = psi[(v[1][1], a1)]
                new_v_exit_values = (new_v0_exit_value, new_v1_exit_value)
                
                new_v = (new_v_suffixes, new_v_states, new_v_exit_values)

                if new_v not in seen:
                    seen.add(new_v)
                    vertexes.append(new_v)
                    if new_v_suffixes == ('', '') and new_v[2][0] == B[1] and new_v[2][1] == B[1]:
                        final_vertexes.append(new_v)

                new_edge_weight = ('', a1)
                edges[v].append((new_v, new_edge_weight))


            elif (len_v0 < len_v1 and a1_encoding.startswith(v[0][1])) or (len_v0 == 0 and len_v1 == 0):
                new_v1_suffix = ''
                new_v0_suffix = a1_encoding[len_v1:]
                new_v_suffixes = (new_v0_suffix, new_v1_suffix)

                new_v1_state = v[1][1]
                new_v0_state = phi[(v[1][0], a1)]
                new_v_states = (new_v0_state, new_v1_state)

                new_v1_exit_value = v[2][1]
                new_v0_exit_value = psi[(v[1][0], a1)]
                new_v_exit_values = (new_v0_exit_value, new_v1_exit_value)

                new_v = (new_v_suffixes, new_v_states, new_v_exit_values)

                if new_v not in seen:
                    seen.add(new_v)
                    vertexes.append(new_v)
                    if new_v_suffixes == ('', '') and new_v[2][0] == B[1] and new_v[2][1] == B[1]:
                        final_vertexes.append(new_v) 

                new_edge_weight = (a1, '')
                edges[v].append((new_v, new_edge_weight))


    return {'vertexes':vertexes, 
            'edges': edges, 
            'start_vertex': start_vertex,
            'final_vertexes': final_vertexes} 
# total = V = O(|A| * max|ai| * C{Q,2} * 4) + O(V * |A|)

def rec_get_edge_path_to_final(cur_vertex, final_vertexes, edges, seen=None, path=None):
    if seen is None:
        seen = set()
    if path is None:
        path = []

    seen = set(seen)
    seen.add(cur_vertex)

    if cur_vertex in final_vertexes: #O(E)
        len_path = len(path)
        if len_path % 2 == 0:
            for i in range(0, len_path, 2):
                #print(path[i][2], (path[i+1][2][1], path[i+1][2][0]))
                if path[i][2] != (path[i+1][2][1], path[i+1][2][0]):
                        return path

    for next_vertex, edge_weight in edges.get(cur_vertex, []):
        if next_vertex not in seen:
            new_path = path + [(cur_vertex, next_vertex, edge_weight)]  
            result = rec_get_edge_path_to_final(next_vertex, final_vertexes, edges, seen, new_path)
            if result:
                return result

    return None
# total = O(V) * ( O(E + V))




def is_automata_ambiguous(schema_encoding, A, B, Q, phi, psi, q_start):
    source_to_check = build_intersect_source(schema_encoding, A, B, Q, phi, psi, q_start)
    path = rec_get_edge_path_to_final(source_to_check['start_vertex'], 
                      source_to_check['final_vertexes'], 
                      source_to_check['edges'])
    if path:
        word1 = ''
        word2 = ''
        for v1, v2, weight in path:
            if weight[0] != '':
                word1 += f' {weight[0]}'
            else:
                word2 += f' {weight[1]}'
        print('word1:', word1)
        print('word2:', word2)
        return True
            #print(v1, '->', v2, 'weight:', weight)
    else:
        print("No path to final vertex found")
        return False

        
    