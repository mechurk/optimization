import pulp as p

Lp_prob = p.LpProblem('Problem', p.LpMinimize)

building_ids = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']  # v
center_ids = building_ids  # u
heights = {'A': 1, 'B': 1, "C": 1, 'D': 1, 'E': 1, 'F': 1, 'G': 1, 'H': 1}
footprints = {'A': 1, 'B': 1, "C": 1, 'D': 1, 'E': 1, 'F': 1, 'G': 1, 'H': 1}
M = {'A': 10000, 'B': 10000, "C": 10000, 'D': 10000, 'E': 10000, 'F': 10000, 'G': 10000, 'H': 10000 }
edges = [('A', 'B'), ('B', 'A'), ('B', 'C'), ('C', 'B'), ('C', 'D'), ('D', 'C'), ('E', 'F'), ('F', 'E'), ('F', 'G'),
         ('G', 'F'), ('G', 'H'), ('H', 'G')]


volume_change_weight = 0.1
building_count = len(building_ids)
# Xuv
center_matrix = p.LpVariable.dicts("center_matrix", ((i, j) for i in building_ids for j in center_ids), lowBound=0,
                                   upBound=1, cat='Binary')
# deltaV
delta_volumes_matrix = p.LpVariable.dicts("delta_volume_matrix", ((i, j) for i in building_ids for j in center_ids),
                                          lowBound=0)
# Hu
height_center = p.LpVariable.dicts("height_center", ((j) for j in center_ids), lowBound=0)

# fa
flows = p.LpVariable.dicts("flows", ((j) for j in edges))

# Fa
positive_flows = p.LpVariable.dicts("positive_flows", ((j) for j in edges), lowBound=0, upBound=1, cat='Binary')
print(flows)
print(positive_flows)


def cb1_one_building_id_all_center_ids(Lp_prob, building_id, center_ids):
    Lp_prob += p.lpSum(center_matrix[building_id, center_id] for center_id in center_ids) == 1


def cb1(Lp_prob, building_ids, center_ids):
    for building_id in building_ids:
        cb1_one_building_id_all_center_ids(Lp_prob, building_id, center_ids)


def cb2_two_building_ids_one_center_id(Lp_prob, first_building_id, second_building_id, center_id):
    Lp_prob += center_matrix[first_building_id, center_id] <= center_matrix[second_building_id, center_id]


def cb2(Lp_prob, building_ids, center_ids):
    for index in (range(len(building_ids))):
        for first_building_id in building_ids:
            cb2_two_building_ids_one_center_id(Lp_prob, first_building_id, building_ids[index], center_ids[index])


def c_delta_V_one_building_one_center(Lp_prob, building_id, center_id):
    Lp_prob += delta_volumes_matrix[building_id, center_id] >= (heights[building_id] - height_center[center_id]) * \
               footprints[building_id] - (
                       1 - center_matrix[building_id, center_id]) * M[building_id]
    Lp_prob += delta_volumes_matrix[building_id, center_id] >= -(heights[building_id] - height_center[center_id]) * \
               footprints[building_id] - (
                       1 - center_matrix[building_id, center_id]) * M[building_id]


def c_delta_V(Lp_prob, building_ids, center_ids):
    for building_id in building_ids:
        for center_id in center_ids:
            c_delta_V_one_building_one_center(Lp_prob, building_id, center_id)


def objective_function(Lp_prob, building_ids, center_ids):
    Lp_prob += p.lpSum(
        center_matrix[building_ids[index], center_ids[index]] for index in
        range(len(building_ids))) + (volume_change_weight * p.lpSum(
        delta_volumes_matrix))


def printProb(Lp_prob):
    for v in Lp_prob.variables():
        print(v.name, "=", v.varValue)
    print("Status:", p.LpStatus[Lp_prob.status])


def cf1(Lp_prob, edges, flows, positive_flows):
    for edge in edges:
        Lp_prob += building_count * positive_flows[edge] >= flows[edge]


def cf2(Lp_prob, flows, building_ids):
    for building_id in building_ids:
        outcoming_edges = [edge for edge in edges if edge[0] == building_id]
        incoming_edges = [edge for edge in edges if edge[1] == building_id]
        Lp_prob += p.lpSum(flows[edge] for edge in outcoming_edges) - p.lpSum(
            flows[edge] for edge in incoming_edges) >= 1 - center_matrix[building_id, building_id] * (
                           building_count + 1)
        Lp_prob += p.lpSum(flows[edge] for edge in outcoming_edges) - p.lpSum(
            flows[edge] for edge in incoming_edges) <= 1 - center_matrix[building_id, building_id]


def cf3(Lp_prob, edges, building_ids, positive_flows):
    for edge in edges:
        for building_id in building_ids:
            Lp_prob += center_matrix[building_id, edge[0]] >= center_matrix[building_id, edge[1]] + (
                    positive_flows[edge] - 1)


def cf4(Lp_prob, building_ids, edges, positive_flows):
    for building_id in building_ids:
        outcoming_edges = [edge for edge in edges if edge[0] == building_id]
        Lp_prob += center_matrix[building_id, building_id] + p.lpSum(
            positive_flows[edge] for edge in outcoming_edges) <= 1


cb1(Lp_prob, building_ids, center_ids)
cb2(Lp_prob, building_ids, center_ids)
c_delta_V(Lp_prob, building_ids, center_ids)
objective_function(Lp_prob, building_ids, center_ids)
cf1(Lp_prob, edges, flows, positive_flows)
cf2(Lp_prob, flows, building_ids)
cf3(Lp_prob, edges, building_ids, positive_flows)
cf4(Lp_prob, building_ids, edges, positive_flows)
# result
Lp_prob.solve()
print(Lp_prob)

printProb(Lp_prob)
print(p.value(Lp_prob.objective))
