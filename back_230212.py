import sys
import math


class Drone:
    def __init__(self, id, x, y, id_player, mire):
        self.id = id
        self.x = x
        self.y = y
        self.id_player = id_player
        self.mire = mire

    def __str__(self):
        return "Drone id: {} | X: {} | Y: {} | id_player: {}".format(self.id, self.x, self.y, self.id_player)

    def getZone(self):
        for zone in zones_list:
            if math.sqrt((zone.x - self.x)**2 + (zone.y - self.y)**2) <= 100:
                return zone
        return -1

    def getDistance(self, zone):
        return math.sqrt((self.x - zone.x)**2 + (self.y - zone.y)**2)

    def getZonePlusProche(self):
        return sorted([zone for zone in zones_list], key=lambda x: x.getDistance(self), reverse=False)[0]


class Zone:
    def __init__(self, id, x, y, control_id):
        self.id = id
        self.x = x
        self.y = y
        self.control_id = control_id

    def __str__(self):
        return "Zone id: {} \t| X: {} \t| Y: {} \t| Control id: {}".format(self.id, self.x, self.y, self.control_id)

    def getDrones(self):
        return [drone for drone in drones_list if math.sqrt((drone.x - self.x)**2 + (drone.y - self.y)**2) <= 100]

    def getPoids(self):
        poids = []
        for id_player in range(n_players):
            poid_player = 0
            for drone in self.getDrones():
                if drone.id_player == id_player:
                    poid_player += 1
            poids.append(poid_player)
        return poids

    def getNbPlayers(self):
        return len(self.getPoids())

    def getMonPoid(self):
        return self.getPoids()[myId]

    def getPoidAdverseMax(self):
        return max([poid for i, poid in enumerate(self.getPoids()) if i != myId])

    def getBalance(self):
        return self.getMonPoid() - self.getPoidAdverseMax()

    def getDistance(self, drone):
        return math.sqrt((self.x - drone.x)**2 + (self.y - drone.y)**2)

    def getDronePlusProche(self):
        return sorted([drone for drone in drones_list], key=lambda x: x.getDistance(self), reverse=False)[0]


def getDroneById(i):
    return [drone for drone in drones_list if drone.id == i][0]


def getZoneById(i):
    return [zone for zone in zones_list if zone.id == i][0]

# on cible les zone à investir


def zonesCibles():
    r = []
    for z in zones_list:
        if z.getBalance() in [0, -1] or z.getNbPlayers() == 0:
            if z.control_id != myId:
                r.append(z)
    return sorted(r, key=lambda x: len(x.getDrones()), reverse=False)


def zonesCiblesVides():
    r = []
    for z in zonesCibles():
        if z.control_id != myId and z.getPoidAdverseMax == 0:
            r.append(z)
    return r

# on définit les drones à mobiliser


def dronesLibres():
    r = []
    for zone in zones_list:
        if zone.control_id == myId:
            if zone.getBalance() > 0:
                for drone in zone.getDrones():
                    if drone.id_player == myId:
                        r.append(drone)
        if zone.control_id != myId:
            if zone.getBalance() < 0:
                for drone in zone.getDrones():
                    if drone.id_player == myId:
                        r.append(drone)
    return r


n_players, myId, n_drones, n_zones = [int(i) for i in input().split()]
# print([n_players, myId, n_drones, n_zones], file=sys.stderr, flush=True)

zones_list = []
for i in range(n_zones):
    x, y = [int(j) for j in input().split()]
    zones_list.append(Zone(i, x, y, -1))

drones_list = []
for i in range(n_players):
    for j in range(n_drones):
        drones_list.append(Drone(i*n_drones + j, 0, 0, i, [0, 0]))


tour = 0
# game loop
while True:
    tour += 1
    for i in range(n_zones):
        # ID of the team controlling the zone (0, 1, 2, or 3) or -1 if it is not controlled. The zones are given in the same order as in the initialization.
        tid = int(input())
        getZoneById(i).control_id = tid

    for i in range(n_players):
        for j in range(n_drones):
            dx, dy = [int(k) for k in input().split()]
            drone_id = i*n_drones + j
            getDroneById(drone_id).x = dx
            getDroneById(drone_id).y = dy
            # print([dx,dy], file=sys.stderr, flush=True)

    out_list = []
    if tour < 50:
        for zone in zones_list:
            zone.getDronePlusProche().mire = [zone.x, zone.y]

        for drone in drones_list:
            if drone.id_player == myId:
                if drone.mire == [0, 0]:
                    zone_visee = [zone for zone in sorted(
                        zones_list, key=lambda x: x.getDistance(drone))][0]
                    drone.mire = [zone_visee.x, zone_visee.y]

    if tour % 10 in [i in range(n_players)]:
        # for zone in zones_list:
        #     if zone.getNbPlayers()>2:
        #         for drone in zone.getDrones():
        #             if drone.id_player == myId and len(zonesCibles()) > 0:
        #                 drone.mire = [zonesCibles()[0].x, zonesCibles()[0].y]
        if len(zonesCibles()) > 0:
            for i, drone in enumerate(dronesLibres()):
                if i < len(zonesCibles()):
                    drone.mire = [zonesCibles()[i].x, zonesCibles()[i].y]
                    print('=========allo=========',
                          file=sys.stderr, flush=True)
                    print('=========allo=========',
                          file=sys.stderr, flush=True)
                    print('=========allo=========',
                          file=sys.stderr, flush=True)

# ===============
    for drone in drones_list:
        if drone.id_player == myId:
            out_list.append(drone.mire)

    for out in out_list:
        print(*out)

    print('n_players, myId, n_drones, n_zones = ' +
          str([n_players, myId, n_drones, n_zones]), file=sys.stderr, flush=True)
    print('coord_zones =  ' + str([[z.x, z.y]
          for z in zones_list]), file=sys.stderr, flush=True)
    print('coord_drones = ' + str([[d.x, d.y]
          for d in drones_list]), file=sys.stderr, flush=True)
    print('---', file=sys.stderr, flush=True)
    print('zones cibles : ------', file=sys.stderr, flush=True)
    for z in zonesCibles():
        print(z, file=sys.stderr, flush=True)
    print('drones libres : ------', file=sys.stderr, flush=True)
    for d in dronesLibres():
        print(d, file=sys.stderr, flush=True)
