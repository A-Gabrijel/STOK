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
    Reads the input file, in the future this will be depricated.
    """

    def __init__(self, filename: str, skip_lines: int, nr_of_data: int):
        self.filename = filename
        self.skip_lines = skip_lines
        self.nr_of_data = nr_of_data

    def reader(self):
        """
        Reads a file and checks for numerical values,
        then returns a list of the numerical values.

        Returns:
            List[float, str]: returns a tuple of the numerical values.
        """
        with open(self.filename, 'r', encoding='utf8') as file:
            output: List[str, float] = []
            for line in enumerate(file):
                if ("\n" in line[0]) or ("#" in line[0]) or ("%" in line[0]):
                    pass
                elif isinstance(line) == int or isinstance(line) == float:
                    output.append(float(line))
                else:
                    output.append(str(line))
        return output

    def reader_plain(self):
        """Just reades the file and returns the lines as a list.

        Returns:
            List[str,float]: returns a list of the lines in the file.
        """
        with open(self.filename, 'r', encoding='utf8') as file:
            output: List[str, float] = []
            for line in enumerate(file):
                if ("\n" in line[0]) or ("#" in line[0]) or ("%" in line[0]):
                    pass
                elif isinstance(line) == int or isinstance(line) == float:
                    output.append(float(line))
                else:
                    output.append(str(line))
        return output

    def parsing(self):
        """
        Parses the file and returns a list of the numerical values.
        Slightly formatted.

        Returns:
            List[List[str, float]]: returns a list of the numerical values.
        """
        output: List[List[str, float]] = []
        count = self.nr_of_data
        for i in range(self.skip_lines, len(self.reader())):
            if count == self.nr_of_data:
                output.append(self.reader()[i:i+self.nr_of_data+1])
                count = 0
            else:
                count += 1
        return output

@dataclasses.dataclass
class ContainmentParameters:
    """
    Class that contains the parameters for the containment.
    """

    containment: List[float] = FileReader("Containment.txt", 4, 5).reader()
    outer_radius: float = containment[0]
    containment_height: float = containment[1]
    containment_cut: float = containment[2]
    nr_layers: int = int(containment[3])
    containment_rest: List[List[float]] = FileReader("Containment.txt", 4, 5).parsing()

@dataclasses.dataclass
class SolenoidParameters:
    """
    Class that contains the parameters for the solenoid.
    """

    solenoid: List[float] = FileReader("Solenoid.txt", 0, 0).reader()
    solenoid_radius: float = solenoid[1]
    solenoid_height: float = solenoid[2]

@dataclasses.dataclass
class PortParameters:
    """
    Class that contains the parameters for the ports.
    """

    eq_port: List[str] = FileReader("Equatorial_ports.txt", 4, 6).reader()
    nr_ports: int = int(eq_port[0])
    shape: str = eq_port[2]
    longer_rect: float = float(eq_port[3])
    eq_ports_rest: List[List[float]] = FileReader("Equatorial_ports.txt", 4, 6).parsing()

@dataclasses.dataclass
class LimbParameters:
    """
    Class that contains the parameters for the limbs.
    """

    limbs: List[float] = FileReader("Limbs.txt", 5, 4).reader()
    nr_limbs: int = int(limbs[0])
    limb_radius: float = ContainmentParameters.outer_radius + limbs[2]
    limb_offset: float = 360/(PortParameters.nr_ports * 2) if limbs[4] == "yes" else 0
    limbs_rest: List[List[float]] = FileReader("Limbs.txt", 5, 4).parsing()
    sphere_radius: float = limbs[3]

@dataclasses.dataclass
class LimiterParameters:
    """
    Class that contains the parameters for the limiter.
    """

    limiter = FileReader("Limiter.txt", 0, 0).reader()
    firstwall_thickness = ContainmentParameters.\
        containment_rest[ContainmentParameters.nr_layers-1][3]
    limiter_gap = limiter[0]
    limiter_thickness = limiter[1]

@dataclasses.dataclass
class BboxParameters:
    """
    Class that contains the parameters for the bounding box.
    """

    bbox_thickness: float = SolenoidParameters.solenoid[3]

@dataclasses.dataclass
class SumOfThicknesess:
    """
    Class that sums up the containment thicknesess.
    """

    sum_outer_thickness_full: float = 0.0
    for apples in range(ContainmentParameters.nr_layers):
        sum_outer_thickness_full += ContainmentParameters.containment_rest[apples][3]

    sum_upper_thickness_full: float = 0.0
    for banannas in range(ContainmentParameters.nr_layers):
        sum_upper_thickness_full += ContainmentParameters.containment_rest[banannas][1]

    sum_lower_thickness_full: float = 0.0
    for cherries in range(ContainmentParameters.nr_layers):
        sum_lower_thickness_full += ContainmentParameters.containment_rest[cherries][2]

    sum_inner_thickness_full: float = 0.0
    for dates in range(ContainmentParameters.nr_layers):
        sum_inner_thickness_full += ContainmentParameters.containment_rest[dates][4]

class Rectok:
    # TODO: Ditch the index thing and modify all functions from
    # previous way of doing things, i.e. subscripting lists,
    # to the one-variable-for-all way.

    """
    Creates the class containing all construction components.
    """

    def central_solenoid(self):
        """
        Creates the central solenoid

        Returns:
            cadquery.cq.Workplane object: The central solenoid
        """

        solenoid = cq.Workplane("YX").\
            circle(SolenoidParameters.solenoid_radius).\
            extrude(SolenoidParameters.solenoid_height).\
            translate(Vector(0, 0, SolenoidParameters.solenoid_height/2))
        return solenoid

    def openings(self, index: int):
        """
        Creates the boxes to cut out the openings in the containment.

        Args:
            index (int): the port to be created, 0 is the port at
            angle 0, 1 is the port at angle 1, etc.

        Raises:
            Exception: when there is no such port shape

        Returns:
            cadquery.cq.Workplane: the openings
        """

        angle = (2 * m.pi) / PortParameters.nr_ports
        deg_angle = (angle * index * 180) / m.pi

        x_poz = (ContainmentParameters.outer_radius -
                 ContainmentParameters.containment_rest[0][3]/2) * m.cos((angle) * index)
        y_poz = (ContainmentParameters.outer_radius -
                 ContainmentParameters.containment_rest[0][3]/2) * m.sin((angle) * index)

        port_depth = SumOfThicknesess.sum_outer_thickness_full * \
            (1/m.cos(m.radians(PortParameters.eq_ports_rest[index][2])) +
             1/m.cos(m.radians(PortParameters.eq_ports_rest[index][2])))

        # Constructing objects to be used for later addition and subtraction
        if PortParameters.shape == "square":
            port_nohole = cq.Workplane("XY").\
                box(port_depth * 4, PortParameters.eq_ports_rest[index]
                    [0], PortParameters.eq_ports_rest[index][0])
        elif PortParameters.shape == "rectangle_z":
            port_nohole = cq.Workplane("XY").\
                box(port_depth * 4,
                    PortParameters.eq_ports_rest[index][0], PortParameters.longer_rect)
        elif PortParameters.shape == "rectangle_y":
            port_nohole = cq.Workplane("XY").\
                box(port_depth * 4, PortParameters.longer_rect,
                    PortParameters.eq_ports_rest[index][0])
        else:
            raise Exception("no such object yet")

        port_end_cut_down = cq.Workplane("XY").\
            circle(ContainmentParameters.outer_radius).\
            extrude(100).\
            translate(Vector(0, 0, -ContainmentParameters.containment_height / 2 +
                             SumOfThicknesess.sum_lower_thickness_full - 100))

        port_end_cut_up = cq.Workplane("XY").\
            circle(ContainmentParameters.outer_radius).\
            extrude(100).\
            translate(Vector(0, 0, ContainmentParameters.containment_height / 2 -
                             SumOfThicknesess.sum_upper_thickness_full))

        port_cut = cq.Workplane("XY").\
            circle(ContainmentParameters.outer_radius - SumOfThicknesess.sum_outer_thickness_full).\
            extrude(PortParameters.eq_ports_rest[index][0]*100).\
            translate(Vector(0, 0, -(PortParameters.eq_ports_rest[index][0]) * 100 / 2))

        allign_xy_port = SumOfThicknesess.sum_outer_thickness_full / \
            m.cos(m.radians(PortParameters.eq_ports_rest[index][3])) * m.sin(
                m.radians(PortParameters.eq_ports_rest[index][3]))

        # Here we cut the hole into the port
        port = port_nohole.translate(
            Vector(SumOfThicknesess.sum_outer_thickness_full, 0, 0))

        # Here we apply the rotations to the port
        port = port.rotate((0, -PortParameters.eq_ports_rest[index][0], 0),
                           (0, PortParameters.eq_ports_rest[index][0], 0),
                           -PortParameters.eq_ports_rest[index][2]).\
                    rotate((0, 0, -PortParameters.eq_ports_rest[index][0]),
                           (0, 0, PortParameters.eq_ports_rest[index][0]),
                           PortParameters.eq_ports_rest[index][3])

        # Here we translate the port to the proper radius then
        # cut away a containment shaped circular cylinder so that
        # in the final construction the ports will sit flush with
        # the inner containment wall

        if PortParameters.eq_ports_rest[index][2] < 0:
            port = port.translate(Vector(-ContainmentParameters.outer_radius,
                                         -allign_xy_port - PortParameters.eq_ports_rest[index][5],
                                         PortParameters.eq_ports_rest[index][4])).\
                        cut(port_cut).\
                        cut(port_end_cut_up).\
                        translate(Vector(ContainmentParameters.outer_radius -\
                                         ContainmentParameters.containment_rest[0][3] / 2,
                                         0,
                                         -PortParameters.eq_ports_rest[index][4]))
        else:
            port = port.translate(Vector(-ContainmentParameters.outer_radius,
                                         -allign_xy_port - PortParameters.eq_ports_rest[index][5],
                                         PortParameters.eq_ports_rest[index][4])).\
                        cut(port_cut).\
                        cut(port_end_cut_down).\
                        translate(Vector(ContainmentParameters.outer_radius -\
                                         ContainmentParameters.containment_rest[0][3] / 2,
                                         0,
                                         -PortParameters.eq_ports_rest[index][4]))

        # Inner wall alignemnt
        allign_z = SumOfThicknesess.sum_outer_thickness_full / \
            m.cos(m.radians(PortParameters.eq_ports_rest[index][2])) * \
            m.sin(m.radians(PortParameters.eq_ports_rest[index][2]))

        # Finally the persistent rotation of the final
        # geometry is applied (so all the ports face center)
        port = port.rotate((0, 0, PortParameters.eq_ports_rest[index][0]),
                           (0, 0, -PortParameters.eq_ports_rest[index][0]),
                           -180 - deg_angle).\
                    translate(Vector(x_poz,
                                     y_poz,
                                     PortParameters.eq_ports_rest[index][4] - allign_z))

        return port

    def containment_constructor(self, index: int):
        # TODO: contaiment constructor to be simpler and done
        # with cylinders.
        """A function that constructs cylindrical containment layers.

        Args:
            index (int): the layer to be created, 0 is the innermost,
            1 is the next layer out, etc.

        Returns:
            cadquery.cq.Workplane: the containment layer
        """

        # Thickness counters for easier function definition
        sum_upper_thickness = 0.0
        sum_lower_thickness = 0.0
        sum_outer_thickness = 0.0
        sum_inner_thickness = 0.0

        if index > 0:
            for i in range(index):
                sum_upper_thickness += ContainmentParameters.containment_rest[i][1]
                sum_lower_thickness += ContainmentParameters.containment_rest[i][2]
                sum_outer_thickness += ContainmentParameters.containment_rest[i][3]
                sum_inner_thickness += ContainmentParameters.containment_rest[i][4]

        horizontal_displacement = sum_outer_thickness + sum_inner_thickness
        vertical_displacement = sum_upper_thickness + sum_lower_thickness

        debelina_not = ContainmentParameters.containment_rest[index][4]
        debelina_zun = ContainmentParameters.containment_rest[index][3]
        debelina_gor = ContainmentParameters.containment_rest[index][1]
        debelina_dol = ContainmentParameters.containment_rest[index][2]

        sirina = ContainmentParameters.outer_radius -\
            SolenoidParameters.solenoid_radius - horizontal_displacement
        visina = ContainmentParameters.containment_height - vertical_displacement

        inner_r = SolenoidParameters.solenoid_radius + sum_inner_thickness

        pointsouter = [
            (sirina/2 + inner_r + sirina/2, visina/2),
            (sirina/2 + inner_r + sirina/2, -visina/2),
            (-sirina/2 + inner_r + sirina/2, -visina/2),
            (-sirina/2 + inner_r + sirina/2, visina/2),
            (sirina/2 + inner_r + sirina/2, visina/2)
        ]

        pointsinner = [
            (sirina/2 - debelina_zun + inner_r + sirina/2, visina/2 - debelina_gor),
            (sirina/2 - debelina_zun + inner_r + sirina/2, -visina/2 + debelina_dol),
            (-sirina/2 + debelina_not + inner_r + sirina/2, -visina/2 + debelina_dol),
            (-sirina/2 + debelina_not + inner_r + sirina/2, visina/2 - debelina_gor),
            (sirina/2 - debelina_zun + inner_r + sirina/2, visina/2 - debelina_gor)
        ]

        rezultat = cq.Workplane('XZ').polyline(pointsouter).\
            close().revolve(ContainmentParameters.containment_cut)

        rezultat2 = cq.Workplane('XZ').polyline(pointsinner).\
            close().revolve(ContainmentParameters.containment_cut)

        return rezultat.cut(rezultat2)

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

    def transformer_limb(self, index: int):
        """Creates all transformer limbs and unions them together.

        Args:
            index (int): the limb to be created, 0 is the one at angle 0,
            1 is the one at angle/360/nr_of_ports, etc.

        Returns:
            cadquery.Workplane: the transformer limbs.
        """

        angle = (2 * m.pi) / LimbParameters.nr_limbs
        deg_angle = (angle * index * 180) / m.pi

        transformer_limb = cq.Workplane("XY").\
            box(LimbParameters.limbs_rest[index][0],
                LimbParameters.limbs_rest[index][1],
                SolenoidParameters.solenoid_height).\
            rotate((0, 0, -SolenoidParameters.solenoid_height),
                   (0, 0, SolenoidParameters.solenoid_height),
                   deg_angle)

        x_poz = (LimbParameters.limb_radius) * m.cos(angle * index)
        y_poz = (LimbParameters.limb_radius) * m.sin(angle * index)

        sphere_right = self.spheres(index=index)[0].\
            rotate((0, 0, -SolenoidParameters.solenoid_height),
                   (0, 0, SolenoidParameters.solenoid_height), deg_angle).\
            translate(Vector(x_poz, y_poz, 0))

        sphere_left = self.spheres(index=index)[1].\
            rotate((0, 0, -SolenoidParameters.solenoid_height),
                   (0, 0, SolenoidParameters.solenoid_height), deg_angle).\
            translate(Vector(x_poz, y_poz, 0))

        transformer_limb = transformer_limb.translate(Vector(x_poz, y_poz, 0))
        transformer_limb = transformer_limb.rotate((0, 0, -SolenoidParameters.solenoid_height),
                                                   (0, 0, SolenoidParameters.solenoid_height),
                                                   LimbParameters.limb_offset)
        sphere_right = sphere_right.rotate((0, 0, -SolenoidParameters.solenoid_height),
                                           (0, 0, SolenoidParameters.solenoid_height),
                                           LimbParameters.limb_offset)
        sphere_left = sphere_left.rotate((0, 0, -SolenoidParameters.solenoid_height),
                                         (0, 0, SolenoidParameters.solenoid_height),
                                         LimbParameters.limb_offset)

        return transformer_limb, sphere_right, sphere_left

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
