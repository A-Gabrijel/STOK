"""
The STOK builder, text file search and inject functions to use when
generating STOK.
"""
import dataclasses
import math as m
from typing import List

import cadquery as cq
from cadquery import Vector


class FileReader:
    """
    Reads the input file.
    """

    def __init__(self, *args):
        self.filename = args[0]

    def reader(self):
        """
        Reads a file and checks for numerical values,
        then returns a list of the numerical values.

        Returns:
            List[float, str]: returns a tuple of the numerical values.
        """
        with open(self.filename, 'r', encoding='utf8') as file:
            output: List[str, float] = []
            for i, line in enumerate(file):
                if ("\n" in line[0]) or ("#" in line[0]) or ("%" in line[0]):
                    pass
                else:
                    output.append(float(line))
        return output

@dataclasses.dataclass
class Layer:
    """Layer class, used to store the data for each layer.

    Args:
        upper_lower_outer: float
        inner: float
    """
    upper_lower_outer: float
    inner: float

class ContainmentParameters:
    """A class to store the parameters for the containment.

    Args:
        outer_radius: float
        containment_height: float
        nr_layers: int
        layers: List[Layer]
    """
    config = FileReader("stok_config.txt").reader()
    outer_radius: float = config[0]
    containment_height: float = config[1]
    nr_layers: int = int(config[2])
    layers: List[Layer] = []
    for i in range(3, nr_layers*2+3, 2):
        layers.append(Layer(config[i], config[i+1]))

class SolenoidParameters:
    """Class that contains the parameters for the solenoid.

    Args:
        solenoid_radius: float
        solenoid_height: float
    """
    solenoid_start: int = ContainmentParameters.nr_layers*2+3
    solenoid: List[float] = FileReader("stok_config.txt").reader()
    solenoid_radius: float = solenoid[solenoid_start]
    solenoid_height: float = solenoid[solenoid_start+1]
    bbox_thickness: float = solenoid[solenoid_start+2]

class PortParameters:
    """
    Class that contains the parameters for the ports.

    Args:
        nr_ports: int
        z_side: float
        y_side: float
    """
    port_start: int = SolenoidParameters.solenoid_start+3
    eq_port: List[float] = FileReader("stok_config.txt").reader()
    nr_ports: int = int(eq_port[port_start])
    z_side: float = eq_port[port_start+1]
    y_side: float = eq_port[port_start+2]

@dataclasses.dataclass
class LimbDimensiones:
    """
    Class that contains the dimensions for the limbs.

    Args:
        limb_length: float
        limb_height: float
        limb_width: float
    """
    limb_length: float
    limb_width: float
    limb_height: float

class LimbParameters:
    """
    Class that contains the parameters for the limbs.

    Args:
        nr_limbs: int
        limb_radius: float -> at what radius the limbs are placed.
        limb_offset: float -> the offset of the limbs from the center. /*TODO: depricate*/
        limb_rest: List[List[float]] -> a list of lists of floats that
        contain other parameters. /*TODO: depricate*/
        sphere_radius: float -> the radius of the spheres next to the limb.
    """
    limb_start: int = PortParameters.port_start+3
    limbs: List[float] = FileReader("stok_config.txt").reader()
    nr_limbs: int = int(limbs[limb_start])
    limb_radius: float = ContainmentParameters.outer_radius + limbs[limb_start+1]
    sphere_radius: float = limbs[limb_start+2]
    limb_dimensions: LimbDimensiones = LimbDimensiones(
        limbs[limb_start+3], limbs[limb_start+4], limbs[limb_start+5])

class LimiterParameters:
    """
    Class that contains the parameters for the limiter.

    Attributes:
        firstwall_thickness: float
        limiter_gap: float
        limiter_thickness: float
    """
    limiter_start: int = LimbParameters.limb_start+6
    limiter: List[float] = FileReader("stok_config.txt").reader()
    firstwall_thickness: float = limiter[limiter_start]
    limiter_gap: float = limiter[limiter_start+1]
    limiter_thickness: float = limiter[limiter_start+2]

class STOK():
    # TODO: Ditch the index thing and modify all functions from
    # previous way of doing things, i.e. subscripting lists,
    # to the one-variable-for-all way.
    """Creates the class containing all construction components."""
    def central_solenoid(self) -> cq.Workplane:
        """
        Creates the central solenoid

        Returns:
            cadquery.cq.Workplane object: The central solenoid
        """

        solenoid: cq.Workplane = cq.Workplane("YX").\
            circle(SolenoidParameters.solenoid_radius).\
            extrude(SolenoidParameters.solenoid_height).\
            translate(Vector(0, 0, SolenoidParameters.solenoid_height/2))
        return solenoid

    def opening(self) -> cq.Workplane:
        """Creates a single component taht is used to create the opening.

        Returns:
            cadquery.cq.Workplane object: The component.
        """
        # First the opening geometry is created.
        opening: cq.Workplane = cq.Workplane("YZ").\
            rect(PortParameters.y_side, PortParameters.z_side)

        # Then the opening extrusion depth is calculated and
        # the port is extruded.
        extrusion_depth: float = 0.0

        for i in range(ContainmentParameters.nr_layers):
            extrusion_depth = extrusion_depth +\
                ContainmentParameters.layers[i].upper_lower_outer

        # We extrude.
        opening = opening.extrude(extrusion_depth+extrusion_depth*0.5)

        # We position it in the correct place.
        opening = opening.\
            translate(Vector(-ContainmentParameters.outer_radius-extrusion_depth*0.1, 0, 0))

        return opening

    def openings(self) -> cq.Workplane:
        """Creates the full array of port cutting components.

        Returns:
            cq.Workplane: The array of port cutting components.
        """
        # Here we call the opening_member function to create a single
        # opening cutter and then rotate it via the Z axis to achieve
        # the port.
        openings = self.opening()

        for i in range(1, PortParameters.nr_ports):
            openings = openings.union(self.opening().\
                rotate((0, 0, 1),(0, 0, -1), i*360/PortParameters.nr_ports))

        return openings

    def create_torus(self, inner_r, outer_r, height) -> cq.Workplane:
        """Creates a rectangular torus.

        Args:
            inner_r (_type_): inner radius of the torus.
            outer_r (_type_): outer radius of the torus.
            height (_type_): the height of the torus.

        Returns:
            cq.Workplane: the torus.
        """
        # First we create the innermost and outermost containment cylinder
        # and subtract one from the other.
        cylinner: cq.Workplane = cq.Workplane("XY").\
            cylinder(height, inner_r)
        cylouter: cq.Workplane = cq.Workplane("XY").\
            cylinder(height, outer_r)
        torus: cq.Workplane = cylouter.cut(cylinner)

        return torus

    def containment_layer(self, layer_nr) -> cq.Workplane:
        """Containment layer creation function.

        Args:
            layer_nr (_type_): which layer to create.

        Returns:
            cq.Workplane: the layer.
        """
        # Creating a containment layer from a smaller and a bigger
        # tourus.
        inner_r: float = SolenoidParameters.solenoid_radius
        outer_r: float = ContainmentParameters.outer_radius
        height: float = ContainmentParameters.containment_height
        if layer_nr == 0:
            bigger_tourus: cq.Workplane = self.create_torus(
                inner_r=inner_r, outer_r=outer_r, height=height)
            smaller_torus: cq.Workplane = self.create_torus(
                inner_r=inner_r+ContainmentParameters.layers[layer_nr].inner,
                outer_r=outer_r-ContainmentParameters.layers[layer_nr].upper_lower_outer,
                height=height-ContainmentParameters.layers[layer_nr].upper_lower_outer*2)
        else:
            for i in range(layer_nr):
                inner_r = inner_r + ContainmentParameters.layers[i].inner
                outer_r = outer_r - ContainmentParameters.layers[i].upper_lower_outer
                height = height - ContainmentParameters.layers[i].upper_lower_outer*2
            bigger_tourus = self.create_torus(
                inner_r=inner_r, outer_r=outer_r, height=height)
            smaller_torus = self.create_torus(
                inner_r=inner_r+ContainmentParameters.layers[layer_nr].inner,
                outer_r=outer_r-ContainmentParameters.layers[layer_nr].upper_lower_outer,
                height=height-ContainmentParameters.layers[layer_nr].upper_lower_outer*2)

        containment: cq.Workplane = bigger_tourus.cut(smaller_torus)

        return containment

    def containment(self) -> List[cq.Workplane]:
        """Creates the containment layer array with no port openings.

        Returns:
            List[cq.Workplane]: the containment layer list.
        """
        containment: List[cq.Workplane] = []
        for i in range(ContainmentParameters.nr_layers):
            containment.append(self.containment_layer(i))

        return containment

    def containment_with_ports(self) -> List[cq.Workplane]:
        """Creates the containment layer array with port openings.

        Returns:
            List[cq.Workplane]: the containment layer list.
        """
        containment: List[cq.Workplane] = []
        for i in range(ContainmentParameters.nr_layers):
            containment.append(self.containment_layer(i).cut(self.openings()))

        return containment


    def port(self, index: int):
        # TODO: simplify port constructor function.
        """Creates a port.

        Args:
            index (int): the port to be created, 0 is the one at angle 0,
            then the next one is at angle index/(nr_of_ports/360), etc.

        Returns:
            cadquery.cq.Workplane: a port.
        """

        angle = (2 * m.pi) / PortParameters.nr_ports
        deg_angle = (angle * index * 180) / m.pi

        x_poz = (ContainmentParameters.outer_radius -
                 ContainmentParameters.containment_rest[0][3]/2) * m.cos(angle * index)
        y_poz = (ContainmentParameters.outer_radius -
                 ContainmentParameters.containment_rest[0][3]/2) * m.sin(angle * index)

        allign_z_port = SumOfThicknesess.sum_outer_thickness_full / \
            m.cos(m.radians(PortParameters.eq_ports_rest[index][2])) * \
            m.sin(m.radians(PortParameters.eq_ports_rest[index][2]))

        if PortParameters.eq_ports_rest[index][2] != 0:
            port_depth = SumOfThicknesess.sum_outer_thickness_full / \
                m.cos(m.radians(PortParameters.eq_ports_rest[index][2])) * 2 + \
                    SumOfThicknesess.sum_outer_thickness_full / 4
        else:
            port_depth = SumOfThicknesess.sum_outer_thickness_full / \
                m.cos(m.radians(PortParameters.eq_ports_rest[index][3])) * 2 + \
                    SumOfThicknesess.sum_outer_thickness_full / 4

        # Constructing objects to be used for later addition and subtraction
        port_nohole = cq.Workplane("XY").box(
            port_depth,
            PortParameters.eq_ports_rest[index][0],
            PortParameters.eq_ports_rest[index][0])

        port_hole = cq.Workplane("XY").box(
            port_depth,
            PortParameters.eq_ports_rest[index][1],
            PortParameters.eq_ports_rest[index][1])

        port_end_cut_down = cq.Workplane("XY").\
            circle(ContainmentParameters.outer_radius).extrude(100).\
            translate(Vector(0, 0, -ContainmentParameters.containment_height /
                2+SumOfThicknesess.sum_lower_thickness_full-100))

        port_end_cut_up = cq.Workplane("XY").\
            circle(ContainmentParameters.outer_radius).extrude(100).\
            translate(Vector(0, 0, +ContainmentParameters.containment_height /
                2-SumOfThicknesess.sum_upper_thickness_full))

        port_cut = cq.Workplane("XY").\
            circle(ContainmentParameters.outer_radius - SumOfThicknesess.sum_outer_thickness_full).\
            extrude(PortParameters.eq_ports_rest[index][0] * 100).\
            translate(Vector(0, 0,
                -PortParameters.eq_ports_rest[index][0] * 100 / 2))

        allign_xy_port = SumOfThicknesess.sum_outer_thickness_full / \
            m.cos(m.radians(PortParameters.eq_ports_rest[index][3])) * m.sin(
                m.radians(PortParameters.eq_ports_rest[index][3]))

        # Here we cut the hole into the port
        port = port_nohole.cut(port_hole).translate(
            Vector(SumOfThicknesess.sum_outer_thickness_full, 0, 0))

        # Here we apply the rotations to the port
        port = port.rotate((0, -PortParameters.eq_ports_rest[index][0], 0),
                           (0, PortParameters.eq_ports_rest[index][0], 0),
                           -PortParameters.eq_ports_rest[index][2]).\
                    rotate((0, 0, -PortParameters.eq_ports_rest[index][0]),
                           (0, 0, PortParameters.eq_ports_rest[index][0]),
                           PortParameters.eq_ports_rest[index][3])

        # Here we transalte the port to the proper radious
        # then cut away a containment shaped circular cylinder
        # so that in the final construction the ports will sit
        # flush with the inner containment wall

        if PortParameters.eq_ports_rest[index][2] < 0:
            port = port.translate(Vector(
                -ContainmentParameters.outer_radius,
                -allign_xy_port - PortParameters.eq_ports_rest[index][5],
                PortParameters.eq_ports_rest[index][4])).\
                        cut(port_cut).\
                        cut(port_end_cut_up).\
                        translate(Vector(ContainmentParameters.outer_radius -\
                            ContainmentParameters.containment_rest[0][3] / 2,
                            0, -PortParameters.eq_ports_rest[index][4]))
        else:
            port = port.translate(Vector(
                -ContainmentParameters.outer_radius,
                -allign_xy_port - PortParameters.eq_ports_rest[index][5],
                PortParameters.eq_ports_rest[index][4])).\
                        cut(port_cut).\
                        cut(port_end_cut_down).\
                        translate(Vector(ContainmentParameters.outer_radius -\
                            ContainmentParameters.containment_rest[0][3] / 2,
                            0, -PortParameters.eq_ports_rest[index][4]))

        # Finally the persistent rotation of the final
        # geometry is applied (so all the ports face center)

        port = port.rotate((0, 0, PortParameters.eq_ports_rest[index][0]),
                           (0, 0, -PortParameters.eq_ports_rest[index][0]),
                           -deg_angle + 180)

        return port.translate(Vector(x_poz, y_poz,
                                     PortParameters.eq_ports_rest[index][4] - allign_z_port))

    def transformer_limbs(self):
        """
        This method constructs the transformer limbs.

        Returns:
            cadquery.cq.Workplane: a union of transformer limbs.
        """
        # First we create a box with the correct dimensions.
        box: cq.Workplane = cq.Workplane("XY").box(
            LimbParameters.limb_dimensions.limb_length,
            LimbParameters.limb_dimensions.limb_width,
            LimbParameters.limb_dimensions.limb_height)

        # Then we moove the box to the correct position.
        box = box.translate(
            Vector(LimbParameters.limb_radius+ContainmentParameters.outer_radius,0,0))

        # And we construct the full limb union.
        transformer_limbs: cq.Workplane = box
        for i in range(1, LimbParameters.nr_limbs):
            transformer_limbs = transformer_limbs.\
                union(box.rotate((0, 0, 0), (0, 0, 1), 360/LimbParameters.nr_limbs*i))

        # Apply the 22.5 deg offset from the limbs.
        transformer_limbs = transformer_limbs.rotate((0, 0, 1), (0, 0, -1), 22.5)

        return transformer_limbs

    def limiter(self, index: int):
        """
        Creates all the limiter parts and unions them together.

        Args:
            index (int): the limiter to be created, 0 is the one at angle 0,
            1 is the one at angle/360/nr_of_ports, etc.

        Returns:
            cadquery.cq.Workplane: the limiters.
        """

        # Firstwall construction
        angle = (2 * m.pi) / PortParameters.nr_ports
        deg_angle = (angle * index * 180) / m.pi

        x_s = (ContainmentParameters.outer_radius +
               ContainmentParameters.containment_rest[0][3] / 2 -
               SumOfThicknesess.sum_outer_thickness_full +
               LimiterParameters.limiter_thickness / 2 +
               LimiterParameters.firstwall_thickness / 2) * m.cos(angle * index)
        y_s = (ContainmentParameters.outer_radius +
               ContainmentParameters.containment_rest[0][3] / 2 -
               SumOfThicknesess.sum_outer_thickness_full +
               LimiterParameters.limiter_thickness / 2 +
               LimiterParameters.firstwall_thickness / 2) * m.sin(angle * index)

        x_poz = (ContainmentParameters.outer_radius +
                 ContainmentParameters.containment_rest[0][3] / 2 -
                 SumOfThicknesess.sum_outer_thickness_full) * m.cos(angle * index)
        y_poz = (ContainmentParameters.outer_radius +
                 ContainmentParameters.containment_rest[0][3] / 2 -
                 SumOfThicknesess.sum_outer_thickness_full) * m.sin(angle * index)

        allign_z_port = SumOfThicknesess.sum_outer_thickness_full / \
            m.cos(m.radians(PortParameters.eq_ports_rest[index][2])) * \
            m.sin(m.radians(PortParameters.eq_ports_rest[index][2]))

        # Constructing objects to be used for later addition and subtraction
        firstwall = cq.Workplane("XY").\
            box(LimiterParameters.firstwall_thickness,
                PortParameters.eq_ports_rest[index][1] - LimiterParameters.limiter_gap,
                PortParameters.eq_ports_rest[index][1] - LimiterParameters.limiter_gap)

        firstwall_rear = cq.Workplane("XY").\
            box(LimiterParameters.limiter_thickness,
                PortParameters.eq_ports_rest[index][1] - LimiterParameters.limiter_gap,
                PortParameters.eq_ports_rest[index][1] - LimiterParameters.limiter_gap)

        # Here we apply the rotations to the port
        firstwall = firstwall.rotate((0, -PortParameters.eq_ports_rest[index][0], 0),
                                     (0, PortParameters.eq_ports_rest[index][0], 0),
                                     -PortParameters.eq_ports_rest[index][2]).\
                              rotate((0, 0, -PortParameters.eq_ports_rest[index][0]),
                                     (0, 0, PortParameters.eq_ports_rest[index][0]),
                                     PortParameters.eq_ports_rest[index][3])

        firstwall_rear = firstwall_rear.rotate((0, -PortParameters.eq_ports_rest[index][0], 0),
                                               (0, PortParameters.eq_ports_rest[index][0], 0),
                                               -PortParameters.eq_ports_rest[index][2]).\
                                        rotate((0, 0, -PortParameters.eq_ports_rest[index][0]),
                                               (0, 0, PortParameters.eq_ports_rest[index][0]),
                                               PortParameters.eq_ports_rest[index][3])

        # Finally the persistent rotation of the
        # final geometry is applied (so all the ports face center)
        firstwall = firstwall.rotate((0, 0, PortParameters.eq_ports_rest[index][0]),
                                     (0, 0, -PortParameters.eq_ports_rest[index][0]),
                                     -deg_angle+180)
        firstwall_rear = firstwall_rear.rotate((0, 0, PortParameters.eq_ports_rest[index][0]),
                                               (0, 0, -PortParameters.eq_ports_rest[index][0]),
                                               -deg_angle+180)
        firstwall = firstwall.translate(Vector(
            x_poz, y_poz, PortParameters.eq_ports_rest[index][4] - allign_z_port))
        firstwall_r = firstwall_rear.translate(Vector(
            x_s, y_s, PortParameters.eq_ports_rest[index][4] - allign_z_port))

        return firstwall, firstwall_r

    def bounding_box(self):
        """Creates the bounding box of the reactor.

        Returns:
            cadquery.cq.Workplane: the bounding box.
        """

        bounding_box_outer = cq.Workplane("XY").\
            box(LimbParameters.limb_radius +
                ContainmentParameters.outer_radius * 8 +
                BboxParameters.bbox_thickness,
                LimbParameters.limb_radius +
                ContainmentParameters.outer_radius * 8 +
                BboxParameters.bbox_thickness,
                SolenoidParameters.solenoid_height * 4 +
                BboxParameters.bbox_thickness)
        bounding_box_inner = cq.Workplane("XY").\
            box(LimbParameters.limb_radius +
                ContainmentParameters.outer_radius * 8,
                LimbParameters.limb_radius +
                ContainmentParameters.outer_radius * 8,
                SolenoidParameters.solenoid_height * 4)

        bounding_box = bounding_box_outer.cut(bounding_box_inner)

        return bounding_box

    def spheres(self, index: int):
        """
        Creates spheres, that represent spherical detectors,
        that are used with the limbs.

        Args:
            index (int): the sphere to be created, 0 is the one at angle 0, etc.

        Returns:
            cadquery.cq.Workplane: the spheres.
        """

        sphere_right = cq.Workplane("XY").\
            sphere(LimbParameters.sphere_radius).\
            translate(
                Vector(0, LimbParameters.sphere_radius +
                       LimbParameters.limbs_rest[index][1]/2))
        sphere_left = cq.Workplane("XY").\
            sphere(LimbParameters.sphere_radius).\
            translate(
                Vector(0, -LimbParameters.sphere_radius -
                       LimbParameters.limbs_rest[index][1]/2))

        return sphere_right, sphere_left

    def plasma_source(self, distance_from_wall: float):
        """Creates the plasma source.

        Args:
            distance_from_wall (float): distance between the plasma
            source and the first wall.

        Returns:
            cadquery.cq.Workplane: the plasma source.
        """

        cyl_outer_r = ContainmentParameters.outer_radius -\
            SumOfThicknesess.sum_outer_thickness_full - distance_from_wall
        cyl_inner_r = SolenoidParameters.solenoid_radius +\
            SumOfThicknesess.sum_inner_thickness_full + distance_from_wall
        cyl_height = ContainmentParameters.containment_height -\
            SumOfThicknesess.sum_lower_thickness_full - \
            SumOfThicknesess.sum_upper_thickness_full - 2 * distance_from_wall

        cyl = cq.Workplane("XY").cylinder(cyl_height, cyl_outer_r).\
                 cut(cq.Workplane("XY").cylinder(cyl_height, cyl_inner_r))

        return cyl

# TODO: add divertor constructor here
