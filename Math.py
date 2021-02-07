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
