lane1=(0,0,300,600)
lane2=(300,0,600,600)
lane3=(600,0,900,600)

def count_lanes(vehicles):

    lane1_count=0
    lane2_count=0
    lane3_count=0

    for v in vehicles:

        cx=v[0]

        if lane1[0]<cx<lane1[2]:
            lane1_count+=1

        elif lane2[0]<cx<lane2[2]:
            lane2_count+=1

        elif lane3[0]<cx<lane3[2]:
            lane3_count+=1

    return lane1_count,lane2_count,lane3_count