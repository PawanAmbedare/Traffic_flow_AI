lane1=(0,0,300,600)
lane2=(300,0,600,600)
lane3=(600,0,900,600)

def check_emergency(ambulance):

    emergency=False
    lane=""

    for a in ambulance:

        cx=a[0]
        emergency=True

        if lane1[0]<cx<lane1[2]:
            lane="Lane1"

        elif lane2[0]<cx<lane2[2]:
            lane="Lane2"

        elif lane3[0]<cx<lane3[2]:
            lane="Lane3"

    return emergency,lane