import numpy

''' 
compute angle (in degrees) for p0p1p2 corner
Inputs:
    p0,p1,p2 - points in the form of [x,y]
'''


def calc_angle(p0, p1, p2):
    v0 = numpy.array(p0) - numpy.array(p1)
    v1 = numpy.array(p2) - numpy.array(p1)

    angle = numpy.math.atan2(numpy.linalg.det([v0, v1]), numpy.dot(v0, v1))
    return numpy.degrees(angle)


# http://stackoverflow.com/a/37865332/276093

def point_in_rectangle(point, rectangle):
    AB = vector(rectangle[0], rectangle[1])
    AP = vector(rectangle[0], point)
    BC = vector(rectangle[1], rectangle[2])
    BP = vector(rectangle[1], point)
    dotABAP = dot(AB, AP)
    dotABAB = dot(AB, AB)
    dotBCBP = dot(BC, BP)
    dotBCBC = dot(BC, BC)

    return 0 <= dotABAP <= dotABAB and 0 <= dotBCBP <= dotBCBC


def vector(p1, p2):
    return [(p2[0] - p1[0]), (p2[1] - p1[1])]


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1]
