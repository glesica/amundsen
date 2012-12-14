from itertools import izip
from random import uniform
from numpy import array

from util import weighted_sample


class World2D(object):
    def __init__(self, map_fname):
        with open(map_fname, 'r') as map_file:
            width = None
            height = None
            walls = set()
            beacons = set()

            for name, data in imap(lambda x: x.split(' ', 1), map_file):
                # World dimensions
                if name == 'dimensions':
                    width, height = eval(data)

                # Wall/barrier segment
                if name == 'walls':
                    previous = None
                    for v in data.split():
                        if previous is None:
                            previous = eval(v)
                            first = previous
                            continue
                        current = eval(v)
                        walls.add(previous + current)
                        previous = current
                        
                # Beacon
                if name == 'beacons':
                    for b in data.split():
                        beacons.add(eval(b))

            self.width = width
            self.height = height

            walls.add((0, 0, width, 0))
            walls.add((width, 0, width, height))
            walls.add((width, height, 0, height))
            walls.add((0, height, 0, 0))

            self.walls = tuple(walls)
            self.beacons = tuple(beacons)

    def particle_weight(self, particle, reading):
        """
        Returns the raw weight to be applied to the given particle based on the
        given sensor reading.
        """
        pass


class CardinalSensor(object):
    EAST  = 0
    NORTH = 90
    WEST  = 180
    SOUTH = 270

    def __init__(self, direction, max_range=0):
        self.direction = direction
        self.max_range = max_range

    def reading(self, location, world):
        pass

    def weight(self, particle, world, reading):
        pass


class Robot2D(object):
    def __init__(self, x, y, n, world, sensors):
        self.position = (x, y)
        self.particle_count = n
        self.world = world
        self.sensors = tuple(sensors)
        self.particles = array([
            (uniform(0, world.width), uniform(0, world.height)) for _ in xrange(n)
        ])

    def resample(dx, dy):
        pos = (self.position[0] + dx, self.position[1] + dy)
        readings = (s.reading(pos, self.world) for s in self.sensors)
        particles = []
        weights = []
        for px, py in self.particles:
            # Move particle
            particle = (px + dx, py + dy)
            particles.append(particle)
            # Compute particle weight
            weights.append(sum(s.weight(particle, self.world, r) for s, r in izip(self.sensors, readings)))
        # Normalize weights and resample
        self.particles = weighted_sample(particles, weights)















