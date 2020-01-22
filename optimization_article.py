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
# Cb1
Lp_prob += center_matrix['A', 'a'] + center_matrix['A', 'b'] + center_matrix['A', 'c'] + center_matrix['A', 'd'] == 1
Lp_prob += center_matrix['B', 'a'] + center_matrix['B', 'b'] + center_matrix['B', 'c'] + center_matrix['B', 'd'] == 1
Lp_prob += center_matrix['C', 'a'] + center_matrix['C', 'b'] + center_matrix['C', 'c'] + center_matrix['C', 'd'] == 1
Lp_prob += center_matrix['D', 'a'] + center_matrix['D', 'b'] + center_matrix['D', 'c'] + center_matrix['D', 'd'] == 1

# Cb2
Lp_prob += center_matrix['B', 'a'] <= center_matrix['A', 'a']
Lp_prob += center_matrix['C', 'a'] <= center_matrix['A', 'a']
Lp_prob += center_matrix['D', 'a'] <= center_matrix['A', 'a']
Lp_prob += center_matrix['A', 'b'] <= center_matrix['B', 'b']
Lp_prob += center_matrix['C', 'b'] <= center_matrix['B', 'b']
Lp_prob += center_matrix['D', 'b'] <= center_matrix['B', 'b']
Lp_prob += center_matrix['A', 'c'] <= center_matrix['C', 'c']
Lp_prob += center_matrix['B', 'c'] <= center_matrix['C', 'c']
Lp_prob += center_matrix['D', 'c'] <= center_matrix['C', 'c']
Lp_prob += center_matrix['A', 'd'] <= center_matrix['D', 'd']
Lp_prob += center_matrix['B', 'd'] <= center_matrix['D', 'd']
Lp_prob += center_matrix['C', 'd'] <= center_matrix['D', 'd']


# CdeltaV
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


c_delta_V(Lp_prob, building_ids, center_ids)

Lp_prob += center_matrix['A', 'a'] + center_matrix['B', 'b'] + center_matrix['C', 'c'] + center_matrix[
    'D', 'd'] + p.lpSum(delta_volumes_matrix)

# vysledek
Lp_prob.solve()
print(Lp_prob)


def printProb(Lp_prob):
    for v in Lp_prob.variables():
        print(v.name, "=", v.varValue)
    print("Status:", p.LpStatus[Lp_prob.status])


printProb(Lp_prob)
print(p.value(Lp_prob.objective))
