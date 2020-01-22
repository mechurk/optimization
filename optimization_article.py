import pulp as p

Lp_prob = p.LpProblem('Problem', p.LpMinimize)

building_ids = ['A', 'B', 'C', 'D']  # v
center_ids = ['a', 'b', 'c', 'd']  # u
heights = {'A': 5, 'B': 6, "C": 88, 'D': 83}
footprints = {'A': 1, 'B': 1, "C": 1, 'D': 1}
M = {'A': 10000, 'B': 10000, "C": 10000, 'D': 10000}

# Xuv
center_matrix = p.LpVariable.dicts("center_matrix", ((i, j) for i in building_ids for j in center_ids), lowBound=0,
                                   upBound=1, cat='Binary')
# deltaV
delta_volumes_matrix = p.LpVariable.dicts("delta_volume_matrix", ((i, j) for i in building_ids for j in center_ids),
                                          lowBound=0)
# Hu
height_center = p.LpVariable.dicts("height_center", ((j) for j in center_ids), lowBound=0)
print(height_center)

print(center_matrix)


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
        center_matrix[building_ids[index], center_ids[index]] for index in range(len(building_ids))) + p.lpSum(
        delta_volumes_matrix)


def printProb(Lp_prob):
    for v in Lp_prob.variables():
        print(v.name, "=", v.varValue)
    print("Status:", p.LpStatus[Lp_prob.status])


cb1(Lp_prob, building_ids, center_ids)
cb2(Lp_prob, building_ids, center_ids)
c_delta_V(Lp_prob, building_ids, center_ids)
objective_function(Lp_prob, building_ids, center_ids)

# result
Lp_prob.solve()
print(Lp_prob)

printProb(Lp_prob)
print(p.value(Lp_prob.objective))
