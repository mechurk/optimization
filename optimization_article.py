#!/usr/bin/python
# -*- coding: utf-8 -*-
import pulp as p
import networkx as nx

Lp_prob = p.LpProblem('Problem', p.LpMinimize)

# --------------------------------------------------------------#
# known variables
building_ids = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']  # v
center_ids = building_ids  # u
heights = {'A': 2, 'B': 2, "C": 4, 'D': 2, 'E': 5, 'F': 6, 'G': 22, 'H': 32}  # h
footprints = {'A': 10, 'B': 10, "C": 10, 'D': 10, 'E': 10, 'F': 10, 'G': 10, 'H': 10}  # A
edges = [('A', 'B'), ('B', 'A'), ('B', 'C'), ('C', 'B'), ('C', 'D'), ('D', 'C'), ('D', 'E'), ('E', 'D'), ('E', 'F'),
         ('F', 'E'), ('F', 'G'), ('G', 'F'), ('G', 'H'), ('H', 'G')]  # E
roof_types = {'A': 1, 'B': 1, "C": 1, 'D': 1, 'E': 1, 'F': 1, 'G': 1, 'H': 1}  # Rt
roof_heights = {'A': 0, 'B': 8, "C": 4, 'D': 2, 'E': 1, 'F': 1, 'G': 1, 'H': 1}  # Rh
roof_volume_constant = {'A': 1, 'B': 1, "C": 1, 'D': 1, 'E': 1, 'F': 1, 'G': 1, 'H': 1}  # K
roof_orientation = {'A': 1, 'B': 1, "C": 1, 'D': 1, 'E': 1, 'F': 1, 'G': 1, 'H': 1}  # Ro

# --------------------------------------------------------------#
# variable parameters
body_volume_change_weight = 0.01  # WB objective function
roof_volume_change_weight = 0.1  # WR objective function
building_count = len(building_ids)  # M cf1, cf2
epsilon_roof_type = 1
epsilon_roof_orientation = 1
epsilon_roof_height = 11
epsilon_height = 9

# --------------------------------------------------------------#
# unknown variables

# Xuv
center_matrix = p.LpVariable.dicts("center_matrix", ((i, j) for i in building_ids for j in center_ids), lowBound=0,
                                   upBound=1, cat='Binary')
# deltaV
delta_volumes_matrix = p.LpVariable.dicts("delta_volume_matrix", ((i, j) for i in building_ids for j in center_ids),
                                          lowBound=0)
# Hu
height_center = p.LpVariable.dicts("height_center", ((j) for j in center_ids), lowBound=0)

# fa
flows = p.LpVariable.dicts("flows", ((j) for j in edges), lowBound=0)

# Fa
positive_flows = p.LpVariable.dicts("positive_flows", ((j) for j in edges), lowBound=0, upBound=1, cat='Binary')

# delta_v_roof
delta_roofs_volume_matrix = p.LpVariable.dicts("delta_roofs_heights_matrix",
                                               ((i, j) for i in building_ids for j in center_ids),
                                               lowBound=0)

# HRu
roofs_height_center = p.LpVariable.dicts("roofs_height_center", ((j) for j in center_ids), lowBound=0)


# --------------------------------------------------------------#
# define constraints

# --------------------------#
# constraints for aggregates
def cb1_one_building_id_all_center_ids(Lp_prob, building_id, center_ids):
    Lp_prob += p.lpSum(center_matrix[center_id, building_id] for center_id in center_ids) == 1


def cb1(Lp_prob, building_ids, center_ids):
    for building_id in building_ids:
        cb1_one_building_id_all_center_ids(Lp_prob, building_id, center_ids)


def cb2_two_building_ids_one_center_id(Lp_prob, first_building_id, second_building_id, center_id):
    Lp_prob += center_matrix[center_id, first_building_id] <= center_matrix[center_id, second_building_id]


def cb2(Lp_prob, building_ids, center_ids):
    for index in (range(len(building_ids))):
        for first_building_id in building_ids:
            cb2_two_building_ids_one_center_id(Lp_prob, first_building_id, building_ids[index], center_ids[index])


# --------------------------#
# constraints for neighborhood
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


# --------------------------#
# constraints for better visual view -depends on height of building
def ch2(Lp_prob, center_ids, building_ids):
    for center_id in center_ids:
        for building_id in building_ids:
            Lp_prob += center_matrix[center_id, building_id] * (height_center[center_id] - heights[building_id]) >= 0


def ch3(Lp_prob, center_ids, building_ids):
    for center_id in center_ids:
        for building_id in building_ids:
            Lp_prob += center_matrix[center_id, building_id] * (heights[building_id] - height_center[center_id]) >= 0


# --------------------------#
# constraints for height of aggregated body of building
def c_delta_V_one_building_one_center(Lp_prob, building_id, center_id):
    Lp_prob += delta_volumes_matrix[center_id, building_id] >= (heights[building_id] - height_center[center_id]) * \
               footprints[building_id] - (
                       1 - center_matrix[center_id, building_id]) * MB[building_id]
    Lp_prob += delta_volumes_matrix[center_id, building_id] >= -(heights[building_id] - height_center[center_id]) * \
               footprints[building_id] - (
                       1 - center_matrix[center_id, building_id]) * MB[building_id]


def c_delta_V(Lp_prob, building_ids, center_ids):
    for building_id in building_ids:
        for center_id in center_ids:
            c_delta_V_one_building_one_center(Lp_prob, building_id, center_id)


# --------------------------#
# constraints aggregated buildings with similar or same roof (depends on epsilon_roof_type)
def rooftypes(Lp_prob, center_ids, buiding_ids, roof_types):
    for center_id in center_ids:
        for building_id in building_ids:
            Lp_prob += center_matrix[center_id, building_id] * (
                    roof_types[center_id] - roof_types[building_id]) <= epsilon_roof_type
            Lp_prob += center_matrix[center_id, building_id] * (
                    roof_types[center_id] - roof_types[building_id]) >= -epsilon_roof_type


# --------------------------#
# constraints limiting aggregation of buildings which heights difference is bigger than epsilon_(roof)_height
def hard_body_height(Lp_prob, center_ids, buiding_ids, heights):
    for center_id in center_ids:
        for building_id in building_ids:
            Lp_prob += center_matrix[center_id, building_id] * (
                    heights[center_id] - heights[building_id]) <= epsilon_height
            Lp_prob += center_matrix[center_id, building_id] * (
                    heights[center_id] - heights[building_id]) >= -epsilon_height


def hard_roof_height(Lp_prob, center_ids, buiding_ids, roof_heights):
    for center_id in center_ids:
        for building_id in building_ids:
            Lp_prob += center_matrix[center_id, building_id] * (
                    roof_heights[center_id] - roof_heights[building_id]) <= epsilon_roof_height
            Lp_prob += center_matrix[center_id, building_id] * (
                    roof_heights[center_id] - roof_heights[building_id]) >= -epsilon_roof_height


# --------------------------#
# constraints for height of aggregated roof object of buildings
def delta_v_roof_one_building_one_center(Lp_prob, building_id, center_id):
    Lp_prob += delta_roofs_volume_matrix[center_id, building_id] >= (
            roof_heights[building_id] - roofs_height_center[center_id]) * roof_volume_constant[building_id] - (
                       1 - center_matrix[center_id, building_id]) * MR[building_id]
    Lp_prob += delta_roofs_volume_matrix[center_id, building_id] >= -(
            roof_heights[building_id] - roofs_height_center[center_id]) * roof_volume_constant[building_id] - (
                       1 - center_matrix[center_id, building_id]) * MR[building_id]


def delta_v_roof(Lp_prob, building_ids, center_ids):
    for building_id in building_ids:
        for center_id in center_ids:
            delta_v_roof_one_building_one_center(Lp_prob, building_id, center_id)


# --------------------------#
# constraints limiting aggregation if buildings which orientations difference is bigger than epsilon_roof_orientation
def rooforientation(Lp_prob, center_ids, buiding_ids, roof_orientation):
    for center_id in center_ids:
        for building_id in building_ids:
            Lp_prob += center_matrix[center_id, building_id] * (
                    roof_orientation[center_id] - roof_orientation[building_id]) <= epsilon_roof_orientation
            Lp_prob += center_matrix[center_id, building_id] * (
                    roof_orientation[center_id] - roof_orientation[building_id]) >= -epsilon_roof_orientation


# --------------------------------------------------------------#
# define objective funciton
def objective_function(Lp_prob, building_ids, center_ids):
    Lp_prob += p.lpSum(
        center_matrix[center_ids[index], building_ids[index]] for index in
        range(len(building_ids))) + (body_volume_change_weight * p.lpSum(
        delta_volumes_matrix)) + (roof_volume_change_weight * p.lpSum(
        delta_roofs_volume_matrix))


# --------------------------------------------------------------#
# calculate MR and MB variables, variables are needed in condition delta_v_roof and c_delta_v
def calculate_M_vo_volume(bld_nb, height, footprints):
    # create graf and calculate connected components and create lis of these components
    G = nx.Graph()
    for i in bld_nb:
        G.add_node(i[0])

        bld = i[0]

        for a in i:
            if a != bld and G.has_edge(bld, a) == 0:
                # print (a)
                G.add_edge(bld, a)

    n = nx.number_connected_components(G)
    con = nx.connected_components(G)
    cc = list(con)

    # dict
    M = {}
    M_all = {}

    # find maximum and minimum hight value in component
    for block in cc:
        heights_block = [0]
        for building in block:
            for h in height:
                if h == building:
                    heights_block.append(height[h])
        max_block = max(heights_block)
        min_block = min(heights_block)
        # print(heights_block)

        # calculate max (height[h]-min_block,max_block-height[h]) and add to dict M
        for building in block:
            h_set = []
            for h in height:
                if h == building:
                    minimum = height[h] - min_block
                    maximum = max_block - height[h]
                    h_set.append(minimum)
                    h_set.append(maximum)
                    total_h = max(h_set)
                    M[h] = total_h

    # print (M)
    # multiply M value with footprint
    for par in M:
        for footprint in footprints:
            if par == footprint:
                M_final = M[par] * footprints[footprint]
                M_all[footprint] = M_final

    return (M_all)


# --------------------------------------------------------------#
# print solved variables
def printProb(Lp_prob):
    for v in Lp_prob.variables():
        print(v.name, "=", v.varValue)
    print("Status:", p.LpStatus[Lp_prob.status])


# calculate MR and MB
MB = calculate_M_vo_volume(edges, heights, footprints)
MR = calculate_M_vo_volume(edges, roof_heights, roof_volume_constant)

# call constraints
cb1(Lp_prob, building_ids, center_ids)
cb2(Lp_prob, building_ids, center_ids)
c_delta_V(Lp_prob, building_ids, center_ids)
cf1(Lp_prob, edges, flows, positive_flows)
cf2(Lp_prob, flows, building_ids)
cf3(Lp_prob, edges, building_ids, positive_flows)
cf4(Lp_prob, building_ids, edges, positive_flows)
# ch2(Lp_prob, center_ids, center_ids)
# ch3(Lp_prob, center_ids, center_ids)
rooftypes(Lp_prob, center_ids, building_ids, roof_types)
hard_body_height(Lp_prob, center_ids, building_ids, heights)
delta_v_roof(Lp_prob, building_ids, center_ids)
hard_roof_height(Lp_prob, center_ids, building_ids, roof_heights)
rooforientation(Lp_prob, center_ids, building_ids, roof_orientation)

# call ojective function
objective_function(Lp_prob, building_ids, center_ids)

# result, print
Lp_prob.solve()
print(Lp_prob)
printProb(Lp_prob)
print(p.value(Lp_prob.objective))
