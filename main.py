"""
Script to generate string art templates.
"""
from pathlib import Path
from joy import *
import math

# mm to pixels in inkscape units
mm = 300/79.375

HOLE_RADIUS = 1*mm
SLIT_LENGTH = 4*mm

SMALL_HOLE_RADIUS = 0.65*mm

def make_hole(hole_radius, slit_length):
    """Make a hole with a cirle and a line.

    The top of the hole will be at the origin.
    """
    y = hole_radius + slit_length
    return line(x1=0, y1=0, x2=0, y2=slit_length, stroke="black") + circle(x=0, y=y, r=hole_radius, stroke="black", fill="none")

def cycle_shape(shape, n):
    """Cycles the shape n times around the origin.
    """
    angle = 360/n
    shapes = [shape | rotate(angle*i) for i in range(n)]
    return combine(shapes)

def make_holes(n, radius, hole_radius, gap=0):
    """Make n holes around a circle of given radius.

    To have the holes inside the circle, specify the required gap.
    """
    r = radius-gap-hole_radius if gap else radius
    hole = circle(r=hole_radius, x=0, y=r, stroke="black", fill="none")
    return cycle_shape(hole, n)

def make_slits(n, radius, slit_length):
    """Makes n slits around a circle of given radius.
    """
    slit = line(x1=0, y1=radius, x2=0, y2=radius-slit_length, stroke="black")
    return cycle_shape(slit, n)

def make_circle(radius, num_holes, hole_radius=HOLE_RADIUS, slit_length=SLIT_LENGTH):
    c = circle(r=radius, stroke="red", fill="none")

    r = radius - slit_length - hole_radius
    holes = make_holes(num_holes, r, hole_radius, gap=slit_length)

    slits = make_slits(num_holes, radius, slit_length)
    return combine([c, holes, slits])

def make_concentric_circle(radius, n1, n2, hole_radius=SMALL_HOLE_RADIUS):
    c = circle(r=radius)


    holes1 = make_holes(n1, radius, hole_radius, gap=SLIT_LENGTH)
    holes2 = make_holes(n2, radius/2, hole_radius, gap=SLIT_LENGTH/2)
    return combine([c, holes1, holes2])

def _make_row(shape, n, shift):
    """Makes a row of shapes by repeated it shifting it n times."""
    # doesn't use joy's repeat because that doesn't work that great in inkscape
    shapes = [shape | translate(x=shift*i) for i in range(n)]
    return combine(shapes)

def make_hole_row(hole, n, length, gap):
    step = length / (n-1+2*gap)
    row0 = _make_row(hole, n, step)
    row = row0 | translate(x=-length/2+gap*step)
    return row

def make_polygon(n, side_length, num_holes, hole_radius=HOLE_RADIUS, slit_length=SLIT_LENGTH, gap_in_steps=1.5):
    side0 = line(x1=-side_length/2, y1=0, x2=side_length/2, y2=0, stroke="red")
    hole = make_hole(hole_radius=hole_radius, slit_length=slit_length)
    row = make_hole_row(hole, num_holes, side_length, gap=gap_in_steps)

    # height from origin
    angle = 2*math.pi/n
    d = side_length/2 / math.tan(angle/2)

    side = (side0 + row) | translate(y=-d)
    return cycle_shape(side, n)

def make_star(radius, n, num_holes):
    c = circle(r=radius, stroke="red", fill="none")
    hole = circle(r=0.6*mm, stroke="black", fill="none")
    step = radius/(num_holes+1)
    row = _make_row(hole, n=num_holes, shift=step) | translate(x=step)
    rows = cycle_shape(row, n)
    return c + rows

def write_shape(shape, filename):
    # translate joy's natural coordinate system to inkscapes computer coordinate system
    shape = shape | scale(x=1, y=-1)
    svg = shape.as_svg()
    Path(filename).write_text(svg)
    print("saved", filename)

def main():
    # circles
    C09 = make_circle(radius=25*mm, num_holes=9)
    C12 = make_circle(radius=27.5*mm, num_holes=12)
    C18 = make_circle(radius=30*mm, num_holes=18)
    C24 = make_circle(radius=35*mm, num_holes=24)
    C30 = make_circle(radius=40*mm, num_holes=30)
    C40 = make_circle(radius=45*mm, num_holes=40)
    C50 = make_circle(radius=50*mm, num_holes=50)
    C60 = make_circle(radius=60*mm, num_holes=60)
    C80 = make_circle(radius=80*mm, num_holes=80)

    # polygons
    P3 = make_polygon(n=3, side_length=90*mm, num_holes=12,
                      hole_radius=0.65*mm, slit_length=3*mm,
                      gap_in_steps=2.0)
    P4 = make_polygon(n=4, side_length=60*mm, num_holes=12,
                      hole_radius=0.65*mm, slit_length=3*mm,
                      gap_in_steps=2.0)

    P6 = make_polygon(n=6, side_length=45*mm, num_holes=10,
                      hole_radius=0.65*mm, slit_length=3*mm,
                      gap_in_steps=1.25)

    # stars
    S5 = make_star(radius=45*mm, n=5, num_holes=10)
    S6 = make_star(radius=45*mm, n=6, num_holes=10)
    S8 = make_star(radius=45*mm, n=8, num_holes=10)

    ## concentric circles
    CC1 = make_concentric_circle(radius=45*mm, n1=36, n2=36)
    CC2 = make_concentric_circle(radius=45*mm, n1=72, n2=36)

    Path("templates").mkdir(exist_ok=True)

    write_shape(C09, "templates/C09.svg")
    write_shape(C12, "templates/C12.svg")
    write_shape(C18, "templates/C18.svg")
    write_shape(C24, "templates/C24.svg")
    write_shape(C30, "templates/C30.svg")
    write_shape(C40, "templates/C40.svg")
    write_shape(C50, "templates/C50.svg")
    write_shape(C60, "templates/C60.svg")
    write_shape(C80, "templates/C80.svg")

    write_shape(P3, "templates/P3.svg")
    write_shape(P4, "templates/P4.svg")
    write_shape(P6, "templates/P6.svg")

    write_shape(S5, "templates/S5.svg")
    write_shape(S6, "templates/S6.svg")
    write_shape(S8, "templates/S8.svg")

    write_shape(CC1, "templates/CC1.svg")
    write_shape(CC2, "templates/CC2.svg")

if __name__ == "__main__":
    main()