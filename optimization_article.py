#!/usr/bin/python
# -*- coding: utf-8 -*-
import pulp as p
import networkx as nx

Lp_prob = p.LpProblem('Problem', p.LpMinimize)

# --------------------------------------------------------------#
# known variables
"""
building_ids = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']  # v
center_ids = building_ids  # u
heights = {'A': 2, 'B': 2, "C": 4, 'D': 2, 'E': 5, 'F': 6, 'G': 22, 'H': 32}  # Bh
footprints = {'A': 50, 'B': 45, "C": 2, 'D': 4, 'E': 10, 'F': 10, 'G': 10, 'H': 10}  # A
edges = [('A', 'B'), ('B', 'A'), ('B', 'C'), ('C', 'B'), ('C', 'D'), ('D', 'C'), ('D', 'E'), ('E', 'D'), ('E', 'F'),
         ('F', 'E'), ('F', 'G'), ('G', 'F'), ('G', 'H'), ('H', 'G')]  # E
roof_types = {'A': 1, 'B': 1, "C": 1, 'D': 1, 'E': 1, 'F': 1, 'G': 4, 'H': 4}  # Rt
roof_heights = {'A': 2, 'B': 2, "C": 1, 'D': 1, 'E': 22, 'F': 1, 'G': 1, 'H': 1} # Rh
roof_volume_constant = {'A': 12, 'B': 12, "C": 1, 'D': 22, 'E': 1, 'F': 1, 'G': 1, 'H': 1}  # K
roof_orientation = {'A': 1, 'B': 1, "C": 1, 'D': 1, 'E': 1, 'F': 1, 'G': 1, 'H': 1}  # Ro

building_ids= ['695579e4-2cce-44fb-b613-ee8eec5dcdf2', 'e1f5f600-b6ce-4fb9-8079-7865e78eec2d', '287656ae-ee2b-4c7c-89d1-cef38cbed432', '1b4cef2d-8b82-47de-aa0c-f09562a32b0d', '8e553652-d60a-4045-968a-0f046bbc048a', 'ee1629f1-c492-4199-8dfa-f9f350cab517', '27fe06e5-ce2e-4745-b9b9-60128ad3f11c', '57f6f188-4668-44f7-8321-1cad15547544', 'fac65978-11e1-472f-bcb3-b34589e1eb1b', '0e09ee42-5d0a-4787-8e33-4c1763561d3c', 'd94dbd08-6576-449d-b2bb-4798836999d3', 'e26814de-1d67-483a-a20e-48241767b44c', '01cdbd77-6b90-4d6d-b56c-12c0be103d3c', 'b0b8f62e-f3ae-4332-ba2e-b7a17b89ddda', 'b73b03e6-9b14-4dab-9a12-c22a8728e43e', '3acaf0bd-02a6-4e70-8118-55774ed9878e']
heights= {'695579e4-2cce-44fb-b613-ee8eec5dcdf2': 17.449999982201, '57f6f188-4668-44f7-8321-1cad15547544': 12.079999987678399, '0e09ee42-5d0a-4787-8e33-4c1763561d3c': 12.5199999872296, 'b73b03e6-9b14-4dab-9a12-c22a8728e43e': 6.099999993778, 'b0b8f62e-f3ae-4332-ba2e-b7a17b89ddda': 6.039999993839199, 'ee1629f1-c492-4199-8dfa-f9f350cab517': 9.2299999905854, '3acaf0bd-02a6-4e70-8118-55774ed9878e': 5.9699999939106, '01cdbd77-6b90-4d6d-b56c-12c0be103d3c': 12.2399999875152, 'fac65978-11e1-472f-bcb3-b34589e1eb1b': 10.019999989779599, '287656ae-ee2b-4c7c-89d1-cef38cbed432': 12.9199999868216, 'e26814de-1d67-483a-a20e-48241767b44c': 5.889999993992199, 'd94dbd08-6576-449d-b2bb-4798836999d3': 13.2399999864952, '1b4cef2d-8b82-47de-aa0c-f09562a32b0d': 16.449999983220998, 'e1f5f600-b6ce-4fb9-8079-7865e78eec2d': 6.009999993869799, '8e553652-d60a-4045-968a-0f046bbc048a': 15.899999983782, '27fe06e5-ce2e-4745-b9b9-60128ad3f11c': 9.959999989840801}
footprints= {'695579e4-2cce-44fb-b613-ee8eec5dcdf2': 25.39349994819723, '57f6f188-4668-44f7-8321-1cad15547544': 84.96249982667646, '0e09ee42-5d0a-4787-8e33-4c1763561d3c': 16.71809996589501, 'b73b03e6-9b14-4dab-9a12-c22a8728e43e': 74.3871998482501, 'b0b8f62e-f3ae-4332-ba2e-b7a17b89ddda': 29.135599940563424, 'ee1629f1-c492-4199-8dfa-f9f350cab517': 49.265999899497324, '3acaf0bd-02a6-4e70-8118-55774ed9878e': 39.198599920034845, '01cdbd77-6b90-4d6d-b56c-12c0be103d3c': 68.95859985932444, 'fac65978-11e1-472f-bcb3-b34589e1eb1b': 30.85499993705579, '287656ae-ee2b-4c7c-89d1-cef38cbed432': 14.20999997101161, 'e26814de-1d67-483a-a20e-48241767b44c': 43.295399911677414, 'd94dbd08-6576-449d-b2bb-4798836999d3': 78.1149998406454, '1b4cef2d-8b82-47de-aa0c-f09562a32b0d': 14.101499971232936, 'e1f5f600-b6ce-4fb9-8079-7865e78eec2d': 44.84399990851826, '8e553652-d60a-4045-968a-0f046bbc048a': 43.29989991166818, '27fe06e5-ce2e-4745-b9b9-60128ad3f11c': 61.87439987377623}
edges= [('695579e4-2cce-44fb-b613-ee8eec5dcdf2', '1b4cef2d-8b82-47de-aa0c-f09562a32b0d'), ('695579e4-2cce-44fb-b613-ee8eec5dcdf2', 'fac65978-11e1-472f-bcb3-b34589e1eb1b'), ('1b4cef2d-8b82-47de-aa0c-f09562a32b0d', 'fac65978-11e1-472f-bcb3-b34589e1eb1b'), ('fac65978-11e1-472f-bcb3-b34589e1eb1b', '1b4cef2d-8b82-47de-aa0c-f09562a32b0d'), ('e1f5f600-b6ce-4fb9-8079-7865e78eec2d', '27fe06e5-ce2e-4745-b9b9-60128ad3f11c'), ('e1f5f600-b6ce-4fb9-8079-7865e78eec2d', '57f6f188-4668-44f7-8321-1cad15547544'), ('27fe06e5-ce2e-4745-b9b9-60128ad3f11c', '57f6f188-4668-44f7-8321-1cad15547544'), ('57f6f188-4668-44f7-8321-1cad15547544', '27fe06e5-ce2e-4745-b9b9-60128ad3f11c'), ('287656ae-ee2b-4c7c-89d1-cef38cbed432', 'ee1629f1-c492-4199-8dfa-f9f350cab517'), ('287656ae-ee2b-4c7c-89d1-cef38cbed432', '27fe06e5-ce2e-4745-b9b9-60128ad3f11c'), ('ee1629f1-c492-4199-8dfa-f9f350cab517', '27fe06e5-ce2e-4745-b9b9-60128ad3f11c'), ('27fe06e5-ce2e-4745-b9b9-60128ad3f11c', 'ee1629f1-c492-4199-8dfa-f9f350cab517'), ('1b4cef2d-8b82-47de-aa0c-f09562a32b0d', '695579e4-2cce-44fb-b613-ee8eec5dcdf2'), ('1b4cef2d-8b82-47de-aa0c-f09562a32b0d', 'e26814de-1d67-483a-a20e-48241767b44c'), ('695579e4-2cce-44fb-b613-ee8eec5dcdf2', 'e26814de-1d67-483a-a20e-48241767b44c'), ('e26814de-1d67-483a-a20e-48241767b44c', '695579e4-2cce-44fb-b613-ee8eec5dcdf2'), ('8e553652-d60a-4045-968a-0f046bbc048a', '57f6f188-4668-44f7-8321-1cad15547544'), ('8e553652-d60a-4045-968a-0f046bbc048a', '01cdbd77-6b90-4d6d-b56c-12c0be103d3c'), ('57f6f188-4668-44f7-8321-1cad15547544', '01cdbd77-6b90-4d6d-b56c-12c0be103d3c'), ('01cdbd77-6b90-4d6d-b56c-12c0be103d3c', '57f6f188-4668-44f7-8321-1cad15547544'), ('ee1629f1-c492-4199-8dfa-f9f350cab517', '287656ae-ee2b-4c7c-89d1-cef38cbed432'), ('ee1629f1-c492-4199-8dfa-f9f350cab517', 'b73b03e6-9b14-4dab-9a12-c22a8728e43e'), ('287656ae-ee2b-4c7c-89d1-cef38cbed432', 'b73b03e6-9b14-4dab-9a12-c22a8728e43e'), ('b73b03e6-9b14-4dab-9a12-c22a8728e43e', '287656ae-ee2b-4c7c-89d1-cef38cbed432'), ('27fe06e5-ce2e-4745-b9b9-60128ad3f11c', 'e1f5f600-b6ce-4fb9-8079-7865e78eec2d'), ('27fe06e5-ce2e-4745-b9b9-60128ad3f11c', '287656ae-ee2b-4c7c-89d1-cef38cbed432'), ('e1f5f600-b6ce-4fb9-8079-7865e78eec2d', '287656ae-ee2b-4c7c-89d1-cef38cbed432'), ('287656ae-ee2b-4c7c-89d1-cef38cbed432', 'e1f5f600-b6ce-4fb9-8079-7865e78eec2d'), ('57f6f188-4668-44f7-8321-1cad15547544', 'e1f5f600-b6ce-4fb9-8079-7865e78eec2d'), ('57f6f188-4668-44f7-8321-1cad15547544', '8e553652-d60a-4045-968a-0f046bbc048a'), ('e1f5f600-b6ce-4fb9-8079-7865e78eec2d', '8e553652-d60a-4045-968a-0f046bbc048a'), ('8e553652-d60a-4045-968a-0f046bbc048a', 'e1f5f600-b6ce-4fb9-8079-7865e78eec2d'), ('fac65978-11e1-472f-bcb3-b34589e1eb1b', '695579e4-2cce-44fb-b613-ee8eec5dcdf2'), ('fac65978-11e1-472f-bcb3-b34589e1eb1b', 'd94dbd08-6576-449d-b2bb-4798836999d3'), ('695579e4-2cce-44fb-b613-ee8eec5dcdf2', 'd94dbd08-6576-449d-b2bb-4798836999d3'), ('d94dbd08-6576-449d-b2bb-4798836999d3', '695579e4-2cce-44fb-b613-ee8eec5dcdf2'), ('0e09ee42-5d0a-4787-8e33-4c1763561d3c', '01cdbd77-6b90-4d6d-b56c-12c0be103d3c'), ('0e09ee42-5d0a-4787-8e33-4c1763561d3c', 'b0b8f62e-f3ae-4332-ba2e-b7a17b89ddda'), ('01cdbd77-6b90-4d6d-b56c-12c0be103d3c', 'b0b8f62e-f3ae-4332-ba2e-b7a17b89ddda'), ('b0b8f62e-f3ae-4332-ba2e-b7a17b89ddda', '01cdbd77-6b90-4d6d-b56c-12c0be103d3c'), ('d94dbd08-6576-449d-b2bb-4798836999d3', 'fac65978-11e1-472f-bcb3-b34589e1eb1b'), ('d94dbd08-6576-449d-b2bb-4798836999d3', '3acaf0bd-02a6-4e70-8118-55774ed9878e'), ('fac65978-11e1-472f-bcb3-b34589e1eb1b', '3acaf0bd-02a6-4e70-8118-55774ed9878e'), ('3acaf0bd-02a6-4e70-8118-55774ed9878e', 'fac65978-11e1-472f-bcb3-b34589e1eb1b'), ('e26814de-1d67-483a-a20e-48241767b44c', '1b4cef2d-8b82-47de-aa0c-f09562a32b0d'), ('e26814de-1d67-483a-a20e-48241767b44c', 'b0b8f62e-f3ae-4332-ba2e-b7a17b89ddda'), ('1b4cef2d-8b82-47de-aa0c-f09562a32b0d', 'b0b8f62e-f3ae-4332-ba2e-b7a17b89ddda'), ('b0b8f62e-f3ae-4332-ba2e-b7a17b89ddda', '1b4cef2d-8b82-47de-aa0c-f09562a32b0d'), ('01cdbd77-6b90-4d6d-b56c-12c0be103d3c', '8e553652-d60a-4045-968a-0f046bbc048a'), ('01cdbd77-6b90-4d6d-b56c-12c0be103d3c', '0e09ee42-5d0a-4787-8e33-4c1763561d3c'), ('8e553652-d60a-4045-968a-0f046bbc048a', '0e09ee42-5d0a-4787-8e33-4c1763561d3c'), ('0e09ee42-5d0a-4787-8e33-4c1763561d3c', '8e553652-d60a-4045-968a-0f046bbc048a'), ('b0b8f62e-f3ae-4332-ba2e-b7a17b89ddda', '0e09ee42-5d0a-4787-8e33-4c1763561d3c'), ('b0b8f62e-f3ae-4332-ba2e-b7a17b89ddda', 'e26814de-1d67-483a-a20e-48241767b44c'), ('0e09ee42-5d0a-4787-8e33-4c1763561d3c', 'e26814de-1d67-483a-a20e-48241767b44c'), ('e26814de-1d67-483a-a20e-48241767b44c', '0e09ee42-5d0a-4787-8e33-4c1763561d3c'), ('b73b03e6-9b14-4dab-9a12-c22a8728e43e', 'ee1629f1-c492-4199-8dfa-f9f350cab517'), ('b73b03e6-9b14-4dab-9a12-c22a8728e43e', '3acaf0bd-02a6-4e70-8118-55774ed9878e'), ('ee1629f1-c492-4199-8dfa-f9f350cab517', '3acaf0bd-02a6-4e70-8118-55774ed9878e'), ('3acaf0bd-02a6-4e70-8118-55774ed9878e', 'ee1629f1-c492-4199-8dfa-f9f350cab517'), ('3acaf0bd-02a6-4e70-8118-55774ed9878e', 'd94dbd08-6576-449d-b2bb-4798836999d3'), ('3acaf0bd-02a6-4e70-8118-55774ed9878e', 'b73b03e6-9b14-4dab-9a12-c22a8728e43e'), ('d94dbd08-6576-449d-b2bb-4798836999d3', 'b73b03e6-9b14-4dab-9a12-c22a8728e43e'), ('b73b03e6-9b14-4dab-9a12-c22a8728e43e', 'd94dbd08-6576-449d-b2bb-4798836999d3')]
roof_types= {'695579e4-2cce-44fb-b613-ee8eec5dcdf2': 2, '57f6f188-4668-44f7-8321-1cad15547544': 2, '0e09ee42-5d0a-4787-8e33-4c1763561d3c': 2, 'b73b03e6-9b14-4dab-9a12-c22a8728e43e': 5, 'b0b8f62e-f3ae-4332-ba2e-b7a17b89ddda': 1, 'ee1629f1-c492-4199-8dfa-f9f350cab517': 1, '3acaf0bd-02a6-4e70-8118-55774ed9878e': 1, '01cdbd77-6b90-4d6d-b56c-12c0be103d3c': 2, 'fac65978-11e1-472f-bcb3-b34589e1eb1b': 3, '287656ae-ee2b-4c7c-89d1-cef38cbed432': 1, 'e26814de-1d67-483a-a20e-48241767b44c': 3, 'd94dbd08-6576-449d-b2bb-4798836999d3': 2, '1b4cef2d-8b82-47de-aa0c-f09562a32b0d': 2, 'e1f5f600-b6ce-4fb9-8079-7865e78eec2d': 3, '8e553652-d60a-4045-968a-0f046bbc048a': 2, '27fe06e5-ce2e-4745-b9b9-60128ad3f11c': 2}
roof_heights= {'695579e4-2cce-44fb-b613-ee8eec5dcdf2': 0, '57f6f188-4668-44f7-8321-1cad15547544': 0, '0e09ee42-5d0a-4787-8e33-4c1763561d3c': 0, 'b73b03e6-9b14-4dab-9a12-c22a8728e43e': 2.7999999971440004, 'b0b8f62e-f3ae-4332-ba2e-b7a17b89ddda': 2.7999999971439995, 'ee1629f1-c492-4199-8dfa-f9f350cab517': 3.1299999968074, '3acaf0bd-02a6-4e70-8118-55774ed9878e': 2.7999999971440004, '01cdbd77-6b90-4d6d-b56c-12c0be103d3c': 0, 'fac65978-11e1-472f-bcb3-b34589e1eb1b': 3.659999996266799, '287656ae-ee2b-4c7c-89d1-cef38cbed432': 3.4099999965217993, 'e26814de-1d67-483a-a20e-48241767b44c': 2.7999999971439995, 'd94dbd08-6576-449d-b2bb-4798836999d3': 0, '1b4cef2d-8b82-47de-aa0c-f09562a32b0d': 0, 'e1f5f600-b6ce-4fb9-8079-7865e78eec2d': 2.799999997144, '8e553652-d60a-4045-968a-0f046bbc048a': 0, '27fe06e5-ce2e-4745-b9b9-60128ad3f11c': 0}
roof_volume_constant= {'695579e4-2cce-44fb-b613-ee8eec5dcdf2': 0, '57f6f188-4668-44f7-8321-1cad15547544': 0, '0e09ee42-5d0a-4787-8e33-4c1763561d3c': 0, 'b73b03e6-9b14-4dab-9a12-c22a8728e43e': 24.858666615954988, 'b0b8f62e-f3ae-4332-ba2e-b7a17b89ddda': 9.711866646854475, 'ee1629f1-c492-4199-8dfa-f9f350cab517': 16.421999966499104, '3acaf0bd-02a6-4e70-8118-55774ed9878e': 13.066199973344949, '01cdbd77-6b90-4d6d-b56c-12c0be103d3c': 0, 'fac65978-11e1-472f-bcb3-b34589e1eb1b': 15.427499968527895, '287656ae-ee2b-4c7c-89d1-cef38cbed432': 4.7366666570038705, 'e26814de-1d67-483a-a20e-48241767b44c': 21.647699955838707, 'd94dbd08-6576-449d-b2bb-4798836999d3': 0, '1b4cef2d-8b82-47de-aa0c-f09562a32b0d': 0, 'e1f5f600-b6ce-4fb9-8079-7865e78eec2d': 22.42199995425913, '8e553652-d60a-4045-968a-0f046bbc048a': 0, '27fe06e5-ce2e-4745-b9b9-60128ad3f11c': 0}
roof_orientation= {'695579e4-2cce-44fb-b613-ee8eec5dcdf2': 0, '57f6f188-4668-44f7-8321-1cad15547544': 0, '0e09ee42-5d0a-4787-8e33-4c1763561d3c': 0, 'b73b03e6-9b14-4dab-9a12-c22a8728e43e': 90, 'b0b8f62e-f3ae-4332-ba2e-b7a17b89ddda': 0, 'ee1629f1-c492-4199-8dfa-f9f350cab517': 0, '3acaf0bd-02a6-4e70-8118-55774ed9878e': 0, '01cdbd77-6b90-4d6d-b56c-12c0be103d3c': 0, 'fac65978-11e1-472f-bcb3-b34589e1eb1b': 270, '287656ae-ee2b-4c7c-89d1-cef38cbed432': 0, 'e26814de-1d67-483a-a20e-48241767b44c': 270, 'd94dbd08-6576-449d-b2bb-4798836999d3': 0, '1b4cef2d-8b82-47de-aa0c-f09562a32b0d': 0, 'e1f5f600-b6ce-4fb9-8079-7865e78eec2d': 270, '8e553652-d60a-4045-968a-0f046bbc048a': 0, '27fe06e5-ce2e-4745-b9b9-60128ad3f11c': 0}
"""
building_ids= ['79615526-6220-4335-ac09-4bdb5a237674', 'f9cb7f9c-306d-4216-91ad-6d87731c9378', '4cf97ade-edb8-423f-ae9b-9e0dc40d1c33', '03f93f78-06c3-4ade-8e1b-88048bd44518', 'a3922dc9-1358-422f-9a36-f2b0ed1b7007', '9e2f56e9-4a68-4e8d-abd3-db267a08af55', 'b7ae7209-f16d-49af-a5ce-3fde62a4661c', 'ef59ec4d-c8dd-486a-a3dc-fe86624629fa', 'b239cf98-9f36-4732-a74f-cf8680517ca0', '4b34d78e-5da8-488c-984e-d13ad38b0dd7', 'f9cb7f9c-306d-4216-91ad-6d87731c9378.zRAY9JKncyAlfVYMU86K']
heights= {'b7ae7209-f16d-49af-a5ce-3fde62a4661c': 12.979999986760399, '4cf97ade-edb8-423f-ae9b-9e0dc40d1c33': 11.8099999879538, '03f93f78-06c3-4ade-8e1b-88048bd44518': 10.387079989405168, 'ef59ec4d-c8dd-486a-a3dc-fe86624629fa': 13.129999986607402, 'a3922dc9-1358-422f-9a36-f2b0ed1b7007': 11.9399999878212, '79615526-6220-4335-ac09-4bdb5a237674': 12.369999987382599, 'f9cb7f9c-306d-4216-91ad-6d87731c9378': 11.119999988657598, 'b239cf98-9f36-4732-a74f-cf8680517ca0': 12.199999987556, '9e2f56e9-4a68-4e8d-abd3-db267a08af55': 13.449999986280998, 'f9cb7f9c-306d-4216-91ad-6d87731c9378.zRAY9JKncyAlfVYMU86K': 11.119999988657598, '4b34d78e-5da8-488c-984e-d13ad38b0dd7': 12.1299999876274}
footprints= {'b7ae7209-f16d-49af-a5ce-3fde62a4661c': 55.420799886941566, '4cf97ade-edb8-423f-ae9b-9e0dc40d1c33': 82.20239983230705, '03f93f78-06c3-4ade-8e1b-88048bd44518': 161.56799967040064, 'ef59ec4d-c8dd-486a-a3dc-fe86624629fa': 56.51799988470337, 'a3922dc9-1358-422f-9a36-f2b0ed1b7007': 68.19869986087475, '79615526-6220-4335-ac09-4bdb5a237674': 86.55299982343188, 'f9cb7f9c-306d-4216-91ad-6d87731c9378': 74.03759984896335, 'b239cf98-9f36-4732-a74f-cf8680517ca0': 66.53879986426081, '9e2f56e9-4a68-4e8d-abd3-db267a08af55': 82.14389983242638, 'f9cb7f9c-306d-4216-91ad-6d87731c9378.zRAY9JKncyAlfVYMU86K': 74.03759984896335, '4b34d78e-5da8-488c-984e-d13ad38b0dd7': 56.09199988557243}
edges= [('79615526-6220-4335-ac09-4bdb5a237674', 'a3922dc9-1358-422f-9a36-f2b0ed1b7007'), ('79615526-6220-4335-ac09-4bdb5a237674', 'f9cb7f9c-306d-4216-91ad-6d87731c9378.zRAY9JKncyAlfVYMU86K'), ('a3922dc9-1358-422f-9a36-f2b0ed1b7007', 'f9cb7f9c-306d-4216-91ad-6d87731c9378.zRAY9JKncyAlfVYMU86K'), ('f9cb7f9c-306d-4216-91ad-6d87731c9378.zRAY9JKncyAlfVYMU86K', 'a3922dc9-1358-422f-9a36-f2b0ed1b7007'), ('f9cb7f9c-306d-4216-91ad-6d87731c9378', 'b7ae7209-f16d-49af-a5ce-3fde62a4661c'), ('f9cb7f9c-306d-4216-91ad-6d87731c9378', 'ef59ec4d-c8dd-486a-a3dc-fe86624629fa'), ('f9cb7f9c-306d-4216-91ad-6d87731c9378', '4b34d78e-5da8-488c-984e-d13ad38b0dd7'), ('b7ae7209-f16d-49af-a5ce-3fde62a4661c', 'ef59ec4d-c8dd-486a-a3dc-fe86624629fa'), ('b7ae7209-f16d-49af-a5ce-3fde62a4661c', '4b34d78e-5da8-488c-984e-d13ad38b0dd7'), ('ef59ec4d-c8dd-486a-a3dc-fe86624629fa', 'b7ae7209-f16d-49af-a5ce-3fde62a4661c'), ('ef59ec4d-c8dd-486a-a3dc-fe86624629fa', '4b34d78e-5da8-488c-984e-d13ad38b0dd7'), ('4b34d78e-5da8-488c-984e-d13ad38b0dd7', 'b7ae7209-f16d-49af-a5ce-3fde62a4661c'), ('4b34d78e-5da8-488c-984e-d13ad38b0dd7', 'ef59ec4d-c8dd-486a-a3dc-fe86624629fa'), ('4cf97ade-edb8-423f-ae9b-9e0dc40d1c33', 'a3922dc9-1358-422f-9a36-f2b0ed1b7007'), ('4cf97ade-edb8-423f-ae9b-9e0dc40d1c33', 'b7ae7209-f16d-49af-a5ce-3fde62a4661c'), ('4cf97ade-edb8-423f-ae9b-9e0dc40d1c33', 'b239cf98-9f36-4732-a74f-cf8680517ca0'), ('a3922dc9-1358-422f-9a36-f2b0ed1b7007', 'b7ae7209-f16d-49af-a5ce-3fde62a4661c'), ('a3922dc9-1358-422f-9a36-f2b0ed1b7007', 'b239cf98-9f36-4732-a74f-cf8680517ca0'), ('b7ae7209-f16d-49af-a5ce-3fde62a4661c', 'a3922dc9-1358-422f-9a36-f2b0ed1b7007'), ('b7ae7209-f16d-49af-a5ce-3fde62a4661c', 'b239cf98-9f36-4732-a74f-cf8680517ca0'), ('b239cf98-9f36-4732-a74f-cf8680517ca0', 'a3922dc9-1358-422f-9a36-f2b0ed1b7007'), ('b239cf98-9f36-4732-a74f-cf8680517ca0', 'b7ae7209-f16d-49af-a5ce-3fde62a4661c'), ('03f93f78-06c3-4ade-8e1b-88048bd44518', '9e2f56e9-4a68-4e8d-abd3-db267a08af55'), ('03f93f78-06c3-4ade-8e1b-88048bd44518', 'f9cb7f9c-306d-4216-91ad-6d87731c9378.zRAY9JKncyAlfVYMU86K'), ('9e2f56e9-4a68-4e8d-abd3-db267a08af55', 'f9cb7f9c-306d-4216-91ad-6d87731c9378.zRAY9JKncyAlfVYMU86K'), ('f9cb7f9c-306d-4216-91ad-6d87731c9378.zRAY9JKncyAlfVYMU86K', '9e2f56e9-4a68-4e8d-abd3-db267a08af55'), ('a3922dc9-1358-422f-9a36-f2b0ed1b7007', '79615526-6220-4335-ac09-4bdb5a237674'), ('a3922dc9-1358-422f-9a36-f2b0ed1b7007', '4cf97ade-edb8-423f-ae9b-9e0dc40d1c33'), ('79615526-6220-4335-ac09-4bdb5a237674', '4cf97ade-edb8-423f-ae9b-9e0dc40d1c33'), ('4cf97ade-edb8-423f-ae9b-9e0dc40d1c33', '79615526-6220-4335-ac09-4bdb5a237674'), ('9e2f56e9-4a68-4e8d-abd3-db267a08af55', '03f93f78-06c3-4ade-8e1b-88048bd44518'), ('9e2f56e9-4a68-4e8d-abd3-db267a08af55', '4b34d78e-5da8-488c-984e-d13ad38b0dd7'), ('03f93f78-06c3-4ade-8e1b-88048bd44518', '4b34d78e-5da8-488c-984e-d13ad38b0dd7'), ('4b34d78e-5da8-488c-984e-d13ad38b0dd7', '03f93f78-06c3-4ade-8e1b-88048bd44518'), ('b7ae7209-f16d-49af-a5ce-3fde62a4661c', 'f9cb7f9c-306d-4216-91ad-6d87731c9378'), ('b7ae7209-f16d-49af-a5ce-3fde62a4661c', '4cf97ade-edb8-423f-ae9b-9e0dc40d1c33'), ('b7ae7209-f16d-49af-a5ce-3fde62a4661c', 'b239cf98-9f36-4732-a74f-cf8680517ca0'), ('f9cb7f9c-306d-4216-91ad-6d87731c9378', '4cf97ade-edb8-423f-ae9b-9e0dc40d1c33'), ('f9cb7f9c-306d-4216-91ad-6d87731c9378', 'b239cf98-9f36-4732-a74f-cf8680517ca0'), ('4cf97ade-edb8-423f-ae9b-9e0dc40d1c33', 'f9cb7f9c-306d-4216-91ad-6d87731c9378'), ('4cf97ade-edb8-423f-ae9b-9e0dc40d1c33', 'b239cf98-9f36-4732-a74f-cf8680517ca0'), ('b239cf98-9f36-4732-a74f-cf8680517ca0', 'f9cb7f9c-306d-4216-91ad-6d87731c9378'), ('b239cf98-9f36-4732-a74f-cf8680517ca0', '4cf97ade-edb8-423f-ae9b-9e0dc40d1c33'), ('ef59ec4d-c8dd-486a-a3dc-fe86624629fa', 'f9cb7f9c-306d-4216-91ad-6d87731c9378'), ('ef59ec4d-c8dd-486a-a3dc-fe86624629fa', '4b34d78e-5da8-488c-984e-d13ad38b0dd7'), ('f9cb7f9c-306d-4216-91ad-6d87731c9378', '4b34d78e-5da8-488c-984e-d13ad38b0dd7'), ('4b34d78e-5da8-488c-984e-d13ad38b0dd7', 'f9cb7f9c-306d-4216-91ad-6d87731c9378'), ('b239cf98-9f36-4732-a74f-cf8680517ca0', '4cf97ade-edb8-423f-ae9b-9e0dc40d1c33'), ('b239cf98-9f36-4732-a74f-cf8680517ca0', 'b7ae7209-f16d-49af-a5ce-3fde62a4661c'), ('4cf97ade-edb8-423f-ae9b-9e0dc40d1c33', 'b7ae7209-f16d-49af-a5ce-3fde62a4661c'), ('b7ae7209-f16d-49af-a5ce-3fde62a4661c', '4cf97ade-edb8-423f-ae9b-9e0dc40d1c33'), ('4b34d78e-5da8-488c-984e-d13ad38b0dd7', 'f9cb7f9c-306d-4216-91ad-6d87731c9378'), ('4b34d78e-5da8-488c-984e-d13ad38b0dd7', '9e2f56e9-4a68-4e8d-abd3-db267a08af55'), ('4b34d78e-5da8-488c-984e-d13ad38b0dd7', 'ef59ec4d-c8dd-486a-a3dc-fe86624629fa'), ('f9cb7f9c-306d-4216-91ad-6d87731c9378', '9e2f56e9-4a68-4e8d-abd3-db267a08af55'), ('f9cb7f9c-306d-4216-91ad-6d87731c9378', 'ef59ec4d-c8dd-486a-a3dc-fe86624629fa'), ('9e2f56e9-4a68-4e8d-abd3-db267a08af55', 'f9cb7f9c-306d-4216-91ad-6d87731c9378'), ('9e2f56e9-4a68-4e8d-abd3-db267a08af55', 'ef59ec4d-c8dd-486a-a3dc-fe86624629fa'), ('ef59ec4d-c8dd-486a-a3dc-fe86624629fa', 'f9cb7f9c-306d-4216-91ad-6d87731c9378'), ('ef59ec4d-c8dd-486a-a3dc-fe86624629fa', '9e2f56e9-4a68-4e8d-abd3-db267a08af55'), ('f9cb7f9c-306d-4216-91ad-6d87731c9378.zRAY9JKncyAlfVYMU86K', '79615526-6220-4335-ac09-4bdb5a237674'), ('f9cb7f9c-306d-4216-91ad-6d87731c9378.zRAY9JKncyAlfVYMU86K', '03f93f78-06c3-4ade-8e1b-88048bd44518'), ('79615526-6220-4335-ac09-4bdb5a237674', '03f93f78-06c3-4ade-8e1b-88048bd44518'), ('03f93f78-06c3-4ade-8e1b-88048bd44518', '79615526-6220-4335-ac09-4bdb5a237674')]
roof_types= {'b7ae7209-f16d-49af-a5ce-3fde62a4661c': 4, '4cf97ade-edb8-423f-ae9b-9e0dc40d1c33': 5, '03f93f78-06c3-4ade-8e1b-88048bd44518': 5, 'ef59ec4d-c8dd-486a-a3dc-fe86624629fa': 4, 'a3922dc9-1358-422f-9a36-f2b0ed1b7007': 5, '79615526-6220-4335-ac09-4bdb5a237674': 1, 'f9cb7f9c-306d-4216-91ad-6d87731c9378': 4, 'b239cf98-9f36-4732-a74f-cf8680517ca0': 4, '9e2f56e9-4a68-4e8d-abd3-db267a08af55': 1, 'f9cb7f9c-306d-4216-91ad-6d87731c9378.zRAY9JKncyAlfVYMU86K': 4, '4b34d78e-5da8-488c-984e-d13ad38b0dd7': 5}
roof_heights= {'b7ae7209-f16d-49af-a5ce-3fde62a4661c': 2.809999997133799, '4cf97ade-edb8-423f-ae9b-9e0dc40d1c33': 2.6299999973174017, '03f93f78-06c3-4ade-8e1b-88048bd44518': 1.8560519981068246, 'ef59ec4d-c8dd-486a-a3dc-fe86624629fa': 2.6599999972868016, 'a3922dc9-1358-422f-9a36-f2b0ed1b7007': 2.309999997643798, '79615526-6220-4335-ac09-4bdb5a237674': 3.3399999965931997, 'f9cb7f9c-306d-4216-91ad-6d87731c9378': 2.029999997929398, 'b239cf98-9f36-4732-a74f-cf8680517ca0': 2.8699999970725987, '9e2f56e9-4a68-4e8d-abd3-db267a08af55': 3.2199999967155986, 'f9cb7f9c-306d-4216-91ad-6d87731c9378.zRAY9JKncyAlfVYMU86K': 2.0299999979293997, '4b34d78e-5da8-488c-984e-d13ad38b0dd7': 2.949999996991002}
roof_volume_constant= {'b7ae7209-f16d-49af-a5ce-3fde62a4661c': 27.710399943470787, '4cf97ade-edb8-423f-ae9b-9e0dc40d1c33': 33.334533265330855, '03f93f78-06c3-4ade-8e1b-88048bd44518': 75.70199984556761, 'ef59ec4d-c8dd-486a-a3dc-fe86624629fa': 28.258999942351686, 'a3922dc9-1358-422f-9a36-f2b0ed1b7007': 26.343749946258814, '79615526-6220-4335-ac09-4bdb5a237674': 28.850999941143957, 'f9cb7f9c-306d-4216-91ad-6d87731c9378': 37.01879992448168, 'b239cf98-9f36-4732-a74f-cf8680517ca0': 33.269399932130405, '9e2f56e9-4a68-4e8d-abd3-db267a08af55': 27.381299944142125, 'f9cb7f9c-306d-4216-91ad-6d87731c9378.zRAY9JKncyAlfVYMU86K': 37.01879992448168, '4b34d78e-5da8-488c-984e-d13ad38b0dd7': 20.473333291567773}
roof_orientation= {'b7ae7209-f16d-49af-a5ce-3fde62a4661c': 90, '4cf97ade-edb8-423f-ae9b-9e0dc40d1c33': 90, '03f93f78-06c3-4ade-8e1b-88048bd44518': 90, 'ef59ec4d-c8dd-486a-a3dc-fe86624629fa': 90, 'a3922dc9-1358-422f-9a36-f2b0ed1b7007': 90, '79615526-6220-4335-ac09-4bdb5a237674': 0, 'f9cb7f9c-306d-4216-91ad-6d87731c9378': 90, 'b239cf98-9f36-4732-a74f-cf8680517ca0': 90, '9e2f56e9-4a68-4e8d-abd3-db267a08af55': 0, 'f9cb7f9c-306d-4216-91ad-6d87731c9378.zRAY9JKncyAlfVYMU86K': 90, '4b34d78e-5da8-488c-984e-d13ad38b0dd7': 90}

center_ids = building_ids

# --------------------------------------------------------------#
# variable parameters
body_volume_change_weight = 0.01  # WB objective function
roof_volume_change_weight = 0.01  # WR objective function
building_count = len(building_ids)  # M cf1, cf2
epsilon_roof_type = 0
epsilon_roof_orientation = 1
epsilon_roof_height = 7
epsilon_height = 10

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
delta_roofs_volume_matrix = p.LpVariable.dicts("delta_roofs_volume_matrix",
                                               ((i, j) for i in building_ids for j in center_ids),
                                               lowBound=0)

# HRu
height_roof_center = p.LpVariable.dicts("height_roof_center", ((j) for j in center_ids), lowBound=0)


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
            roof_heights[building_id] - height_roof_center[center_id]) * roof_volume_constant[building_id] - (
                       1 - center_matrix[center_id, building_id]) * MR[building_id]
    Lp_prob += delta_roofs_volume_matrix[center_id, building_id] >= -(
            roof_heights[building_id] - height_roof_center[center_id]) * roof_volume_constant[building_id] - (
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
    solution ={}
    for v in Lp_prob.variables():
        print(v.name, "=", v.varValue)
        solution[v.name] = v.varValue

    print("Status:", p.LpStatus[Lp_prob.status])
    print ("solution_all=",solution)

# print solved variables
def create_txt_solution(Lp_prob):
    solution ={}
    file=open("solution.txt","w")
    for v in Lp_prob.variables():
        solve = str(v.name) + " = " + str(v.varValue)
        file.write(str(solve))
        file.write("\n")

    file.close()

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
#print(Lp_prob)
printProb(Lp_prob)
print(p.value(Lp_prob.objective))
create_txt_solution(Lp_prob)
