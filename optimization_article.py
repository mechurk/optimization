import pulp as p

Lp_prob = p.LpProblem('Problem', p.LpMinimize)

building_ids = ['A', 'B', 'C', 'D']  # v
centers = ['a', 'b', 'c', 'd']  # u
heights = {'A': 5, 'B': 6, "C": 88, 'D': 83}
footprints = {'A': 1, 'B': 1, "C": 1, 'D': 1}
M = {'A': 10000, 'B': 10000, "C": 10000, 'D': 10000}

# Xuv
center_matrix = p.LpVariable.dicts("center_matrix", ((i, j) for i in building_ids for j in centers), lowBound=0,
                                   upBound=1, cat='Binary')
# deltaV
delta_volumes_matrix = p.LpVariable.dicts("delta_volume_matrix", ((i, j) for i in building_ids for j in centers), lowBound=0)
# Hu
height_center = p.LpVariable.dicts("height_center", ((j) for j in centers), lowBound=0)
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
Lp_prob += delta_volumes_matrix['A', 'a'] >= (heights['A'] - height_center['a']) * footprints['A'] - (
            1 - center_matrix['A', 'a']) * M['A']
Lp_prob += delta_volumes_matrix['A', 'a'] >= -(heights['A'] - height_center['a']) * footprints['A'] - (
            1 - center_matrix['A', 'a']) * M['A']

Lp_prob += delta_volumes_matrix['B', 'a'] >= (heights['B'] - height_center['a']) * footprints['B'] - (
            1 - center_matrix['B', 'a']) * M['B']
Lp_prob += delta_volumes_matrix['B', 'a'] >= -(heights['B'] - height_center['a']) * footprints['B'] - (
            1 - center_matrix['B', 'a']) * M['B']

Lp_prob += delta_volumes_matrix['C', 'a'] >= (heights['C'] - height_center['a']) * footprints['C'] - (
            1 - center_matrix['C', 'a']) * M['C']
Lp_prob += delta_volumes_matrix['C', 'a'] >= -(heights['C'] - height_center['a']) * footprints['C'] - (
            1 - center_matrix['C', 'a']) * M['C']

Lp_prob += delta_volumes_matrix['D', 'a'] >= (heights['D'] - height_center['a']) * footprints['D'] - (
            1 - center_matrix['D', 'a']) * M['D']
Lp_prob += delta_volumes_matrix['D', 'a'] >= -(heights['D'] - height_center['a']) * footprints['D'] - (
            1 - center_matrix['D', 'a']) * M['D']


Lp_prob += delta_volumes_matrix['A', 'b'] >= (heights['A'] - height_center['b']) * footprints['A'] - (
            1 - center_matrix['A', 'b']) * M['A']
Lp_prob += delta_volumes_matrix['A', 'b'] >= -(heights['A'] - height_center['b']) * footprints['A'] - (
            1 - center_matrix['A', 'b']) * M['A']

Lp_prob += delta_volumes_matrix['B', 'b'] >= (heights['B'] - height_center['b']) * footprints['B'] - (
            1 - center_matrix['B', 'b']) * M['B']
Lp_prob += delta_volumes_matrix['B', 'b'] >= -(heights['B'] - height_center['b']) * footprints['B'] - (
            1 - center_matrix['B', 'b']) * M['B']

Lp_prob += delta_volumes_matrix['C', 'b'] >= (heights['C'] - height_center['b']) * footprints['C'] - (
            1 - center_matrix['C', 'b']) * M['C']
Lp_prob += delta_volumes_matrix['C', 'b'] >= -(heights['C'] - height_center['b']) * footprints['C'] - (
            1 - center_matrix['C', 'b']) * M['C']

Lp_prob += delta_volumes_matrix['D', 'b'] >= (heights['D'] - height_center['b']) * footprints['D'] - (
            1 - center_matrix['D', 'b']) * M['D']
Lp_prob += delta_volumes_matrix['D', 'b'] >= -(heights['D'] - height_center['b']) * footprints['D'] - (
            1 - center_matrix['D', 'b']) * M['D']


Lp_prob += delta_volumes_matrix['A', 'c'] >= (heights['A'] - height_center['c']) * footprints['A'] - (
            1 - center_matrix['A', 'c']) * M['A']
Lp_prob += delta_volumes_matrix['A', 'c'] >= -(heights['A'] - height_center['c']) * footprints['A'] - (
            1 - center_matrix['A', 'c']) * M['A']

Lp_prob += delta_volumes_matrix['B', 'c'] >= (heights['B'] - height_center['c']) * footprints['B'] - (
            1 - center_matrix['B', 'c']) * M['B']
Lp_prob += delta_volumes_matrix['B', 'c'] >= -(heights['B'] - height_center['c']) * footprints['B'] - (
            1 - center_matrix['B', 'c']) * M['B']

Lp_prob += delta_volumes_matrix['C', 'c'] >= (heights['C'] - height_center['c']) * footprints['C'] - (
            1 - center_matrix['C', 'c']) * M['C']
Lp_prob += delta_volumes_matrix['C', 'c'] >= -(heights['C'] - height_center['c']) * footprints['C'] - (
            1 - center_matrix['C', 'c']) * M['C']

Lp_prob += delta_volumes_matrix['D', 'c'] >= (heights['D'] - height_center['c']) * footprints['D'] - (
            1 - center_matrix['D', 'c']) * M['D']
Lp_prob += delta_volumes_matrix['D', 'c'] >= -(heights['D'] - height_center['c']) * footprints['D'] - (
            1 - center_matrix['D', 'c']) * M['D']


Lp_prob += delta_volumes_matrix['A', 'd'] >= (heights['A'] - height_center['d']) * footprints['A'] - (
            1 - center_matrix['A', 'd']) * M['A']
Lp_prob += delta_volumes_matrix['A', 'd'] >= -(heights['A'] - height_center['d']) * footprints['A'] - (
            1 - center_matrix['A', 'd']) * M['A']

Lp_prob += delta_volumes_matrix['B', 'd'] >= (heights['B'] - height_center['d']) * footprints['B'] - (
            1 - center_matrix['B', 'd']) * M['B']
Lp_prob += delta_volumes_matrix['B', 'd'] >= -(heights['B'] - height_center['d']) * footprints['B'] - (
            1 - center_matrix['B', 'd']) * M['B']

Lp_prob += delta_volumes_matrix['C', 'd'] >= (heights['C'] - height_center['d']) * footprints['C'] - (
            1 - center_matrix['C', 'd']) * M['C']
Lp_prob += delta_volumes_matrix['C', 'd'] >= -(heights['C'] - height_center['d']) * footprints['C'] - (
            1 - center_matrix['C', 'd']) * M['C']

Lp_prob += delta_volumes_matrix['D', 'd'] >= (heights['D'] - height_center['d']) * footprints['D'] - (
            1 - center_matrix['D', 'd']) * M['D']
Lp_prob += delta_volumes_matrix['D', 'd'] >= -(heights['D'] - height_center['d']) * footprints['D'] - (
            1 - center_matrix['D', 'd']) * M['D']

Lp_prob+=center_matrix['A','a']+center_matrix['B','b']+center_matrix['C','c']+center_matrix['D','d']+p.lpSum(delta_volumes_matrix)


#vysledek
Lp_prob.solve()
print (Lp_prob)

def printProb( Lp_prob ):
    for v in Lp_prob.variables():
       print (v.name, "=", v.varValue)
    print ("Status:", p.LpStatus[ Lp_prob.status ])

printProb(Lp_prob)
print (p.value(Lp_prob.objective))
