import math as m

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
            List[float]: returns a tuple of the numerical values.
        """
        with open(self.filename, 'r', encoding='utf8') as file:
            output = []
            for line in enumerate(file):
                if ("\n" in line[0]) or ("#" in line[0]) or ("%" in line[0]):
                    pass
                elif isinstance(line) == int or isinstance(line) == float:
                    output.append(int(line))
                else:
                    output.append(str(line))
        return output

    def reader_plain(self):
        """Just reades the file and returns the lines as a list.

        Returns:
            List[str]: returns a list of the lines in the file.
        """
        with open(self.filename, 'r', encoding='utf8') as file:
            output = []
            for line in enumerate(file):
                if ("\n" in line[0]) or ("#" in line[0]) or ("%" in line[0]):
                    pass
                elif isinstance(line) == int or isinstance(line) == float:
                    output.append(int(line))
                else:
                    output.append(str(line))
        return output

    def parsing(self):
        """
        Parses the file and returns a list of the numerical values.
        Slightly formatted.

        Returns:
            List[List[str]]: returns a list of the numerical values.
        """
        output = []
        count = self.nr_of_data
        for i in range(self.skip_lines, len(self.reader())):
            if count == self.nr_of_data:
                output.append(self.reader()[i:i+self.nr_of_data+1])
                count = 0
            else:
                count += 1
        return output


class Rectok:
    """
    Creates the class containing all constructin components
    """

    def __init__(self):
        # --- Containment ---
        containment = FileReader("Containment.txt", 4, 5).reader()
        self.outer_radius = containment[0]
        self.containment_height = containment[1]
        self.containment_cut = containment[2]
        self.nr_layers = containment[3]
        self.containment_rest = FileReader("Containment.txt", 4, 5).parsing()

        # --- Solenoid ---
        solenoid = FileReader("Solenoid.txt", 0, 0).reader()
        self.solenoid_radius = solenoid[1]
        self.solenoid_height = solenoid[2]

        # --- Ports ---
        eq_port = FileReader("Equatorial_ports.txt", 4, 6).reader()
        self.nr_ports = eq_port[0]
        self.shape = eq_port[2]
        self.longer_rect = eq_port[3]
        self.eq_ports_rest = FileReader("Equatorial_ports.txt", 4, 6).parsing()

        # --- Limbs ---
        limbs = FileReader("Limbs.txt", 5, 4).reader()
        self.nr_limbs = limbs[0]
        self.limb_radius = self.outer_radius + limbs[2]
        self.limb_offset = 360/(self.nr_ports * 2) if limbs[4] == "yes" else 0
        self.limbs_rest = FileReader("Limbs.txt", 5, 4).parsing()

        # --- Limiter ---
        limiter = FileReader("Limiter.txt", 0, 0).reader()
        self.firstwall_thickness = self.containment_rest[self.nr_layers-1][3]
        self.limiter_gap = limiter[0]
        self.limiter_thickness = limiter[1]

        # --- Bounding box ---
        self.bbox_thickness = solenoid[3]

        # --- Limiter spheres ---
        self.sphere_radius = limbs[3]

        self.sum_outer_thickness_full = 0
        for apples in range(self.nr_layers):
            self.sum_outer_thickness_full += self.containment_rest[apples][3]

        self.sum_upper_thickness_full = 0
        for banannas in range(self.nr_layers):
            self.sum_upper_thickness_full += self.containment_rest[banannas][1]

        self.sum_lower_thickness_full = 0
        for cherries in range(self.nr_layers):
            self.sum_lower_thickness_full += self.containment_rest[cherries][2]

        self.sum_inner_thickness_full = 0
        for dates in range(self.nr_layers):
            self.sum_inner_thickness_full += self.containment_rest[dates][4]

    def central_solenoid(self):
        """
        Creates the central solenoid

        Returns:
            cadquery.cq.Workplane object: The central solenoid
        """
        solenoid = cq.Workplane("YX").\
            circle(self.solenoid_radius).\
            extrude(self.solenoid_height).\
            translate(Vector(0, 0, self.solenoid_height/2))
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
        angle = (2 * m.pi) / self.nr_ports
        deg_angle = (angle * index * 180) / m.pi

        x_poz = (self.outer_radius -
                 self.containment_rest[0][3]/2) * m.cos((angle) * index)
        y_poz = (self.outer_radius -
                 self.containment_rest[0][3]/2) * m.sin((angle) * index)

        port_depth = self.sum_outer_thickness_full * \
            (1/m.cos(m.radians(self.eq_ports_rest[index][2])) +
             1/m.cos(m.radians(self.eq_ports_rest[index][2])))

        # Constructing objects to be used for later addition and subtraction
        if self.shape == "square":
            port_nohole = cq.Workplane("XY").\
                box(port_depth * 4, self.eq_ports_rest[index]
                    [0], self.eq_ports_rest[index][0])
        elif self.shape == "rectangle_z":
            port_nohole = cq.Workplane("XY").\
                box(port_depth * 4,
                    self.eq_ports_rest[index][0], self.longer_rect)
        elif self.shape == "rectangle_y":
            port_nohole = cq.Workplane("XY").\
                box(port_depth * 4, self.longer_rect,
                    self.eq_ports_rest[index][0])
        else:
            raise Exception("no such object yet")

        port_end_cut_down = cq.Workplane("XY").\
            circle(self.outer_radius).\
            extrude(100).\
            translate(Vector(0, 0, -self.containment_height / 2 +
                             self.sum_lower_thickness_full - 100))

        port_end_cut_up = cq.Workplane("XY").\
            circle(self.outer_radius).\
            extrude(100).\
            translate(Vector(0, 0, self.containment_height / 2 -
                             self.sum_upper_thickness_full))

        port_cut = cq.Workplane("XY").\
            circle(self.outer_radius - self.sum_outer_thickness_full).\
            extrude(self.eq_ports_rest[index][0]*100).\
            translate(Vector(0, 0, -(self.eq_ports_rest[index][0]) * 100 / 2))

        allign_xy_port = self.sum_outer_thickness_full / \
            m.cos(m.radians(self.eq_ports_rest[index][3])) * m.sin(
                m.radians(self.eq_ports_rest[index][3]))

        # Here we cut the hole into the port
        port = port_nohole.translate(
            Vector(self.sum_outer_thickness_full, 0, 0))

        # Here we apply the rotations to the port
        port = port.rotate((0, -self.eq_ports_rest[index][0], 0),
                           (0, self.eq_ports_rest[index][0], 0),
                           -self.eq_ports_rest[index][2]).\
                    rotate((0, 0, -self.eq_ports_rest[index][0]),
                           (0, 0, self.eq_ports_rest[index][0]),
                           self.eq_ports_rest[index][3])

        # Here we translate the port to the proper radius then
        # cut away a containment shaped circular cylinder so that
        # in the final construction the ports will sit flush with
        # the inner containment wall

        if self.eq_ports_rest[index][2] < 0:
            port = port.translate(Vector(-self.outer_radius,
                                         -allign_xy_port - self.eq_ports_rest[index][5],
                                         self.eq_ports_rest[index][4])).\
                        cut(port_cut).\
                        cut(port_end_cut_up).\
                        translate(Vector(self.outer_radius - self.containment_rest[0][3] / 2,
                                         0,
                                         -self.eq_ports_rest[index][4]))
        else:
            port = port.translate(Vector(-self.outer_radius,
                                         -allign_xy_port - self.eq_ports_rest[index][5],
                                         self.eq_ports_rest[index][4])).\
                        cut(port_cut).\
                        cut(port_end_cut_down).\
                        translate(Vector(self.outer_radius - self.containment_rest[0][3] / 2,
                                         0,
                                         -self.eq_ports_rest[index][4]))

        # Inner wall alignemnt
        allign_z = self.sum_outer_thickness_full / \
            m.cos(m.radians(self.eq_ports_rest[index][2])) * \
            m.sin(m.radians(self.eq_ports_rest[index][2]))

        # Finally the persistent rotation of the final
        # geometry is applied (so all the ports face center)
        port = port.rotate((0, 0, self.eq_ports_rest[index][0]),
                           (0, 0, -self.eq_ports_rest[index][0]),
                           -180 - deg_angle).\
                    translate(Vector(x_poz,
                                     y_poz,
                                     self.eq_ports_rest[index][4] - allign_z))

        return port

    def containment_constructor(self, index: int):
        """A function that constructs cylindrical containment layers.

        Args:
            index (int): the layer to be created, 0 is the innermost,
            1 is the next layer out, etc.

        Returns:
            cadquery.cq.Workplane: the containment layer
        """

        # Thickness counters for easier function definition
        sum_upper_thickness = 0
        sum_lower_thickness = 0
        sum_outer_thickness = 0
        sum_inner_thickness = 0

        if index > 0:
            for i in range(index):
                sum_upper_thickness += self.containment_rest[i][1]
                sum_lower_thickness += self.containment_rest[i][2]
                sum_outer_thickness += self.containment_rest[i][3]
                sum_inner_thickness += self.containment_rest[i][4]

        horizontal_displacement = sum_outer_thickness + sum_inner_thickness
        vertical_displacement = sum_upper_thickness + sum_lower_thickness

        debelina_not = self.containment_rest[index][4]
        debelina_zun = self.containment_rest[index][3]
        debelina_gor = self.containment_rest[index][1]
        debelina_dol = self.containment_rest[index][2]

        sirina = self.outer_radius - self.solenoid_radius - horizontal_displacement
        visina = self.containment_height - vertical_displacement

        inner_r = self.solenoid_radius + sum_inner_thickness

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
            close().revolve(self.containment_cut)

        rezultat2 = cq.Workplane('XZ').polyline(pointsinner).\
            close().revolve(self.containment_cut)

        return rezultat.cut(rezultat2)

    def port(self, index: int):
        """Creates a port.

        Args:
            index (int): the port to be created, 0 is the one at angle 0,
            then the next one is at angle index/(nr_of_ports/360), etc.

        Returns:
            cadquery.cq.Workplane: a port.
        """

        angle = (2 * m.pi) / self.nr_ports
        deg_angle = (angle * index * 180) / m.pi

        x_poz = (self.outer_radius -
                 self.containment_rest[0][3]/2) * m.cos(angle * index)
        y_poz = (self.outer_radius -
                 self.containment_rest[0][3]/2) * m.sin(angle * index)

        allign_z_port = self.sum_outer_thickness_full / \
            m.cos(m.radians(self.eq_ports_rest[index][2])) * \
            m.sin(m.radians(self.eq_ports_rest[index][2]))

        if self.eq_ports_rest[index][2] != 0:
            port_depth = self.sum_outer_thickness_full / \
                m.cos(m.radians(self.eq_ports_rest[index][2])) * 2 + \
                    self.sum_outer_thickness_full / 4
        else:
            port_depth = self.sum_outer_thickness_full / \
                m.cos(m.radians(self.eq_ports_rest[index][3])) * 2 + \
                    self.sum_outer_thickness_full / 4

        # Constructing objects to be used for later addition and subtraction
        port_nohole = cq.Workplane("XY").box(
            port_depth, self.eq_ports_rest[index][0], self.eq_ports_rest[index][0])

        port_hole = cq.Workplane("XY").box(
            port_depth, self.eq_ports_rest[index][1], self.eq_ports_rest[index][1])

        port_end_cut_down = cq.Workplane("XY").circle(self.outer_radius).extrude(100).\
            translate(Vector(0, 0, -self.containment_height /
                      2+self.sum_lower_thickness_full-100))

        port_end_cut_up = cq.Workplane("XY").circle(self.outer_radius).extrude(100).\
            translate(Vector(0, 0, +self.containment_height /
                      2-self.sum_upper_thickness_full))

        port_cut = cq.Workplane("XY").\
                      circle(self.outer_radius - self.sum_outer_thickness_full).\
                      extrude(self.eq_ports_rest[index][0] * 100).\
                      translate(Vector(0,
                                       0,
                                       -self.eq_ports_rest[index][0] * 100 / 2))

        allign_xy_port = self.sum_outer_thickness_full / \
            m.cos(m.radians(self.eq_ports_rest[index][3])) * m.sin(
                m.radians(self.eq_ports_rest[index][3]))

        # Here we cut the hole into the port
        port = port_nohole.cut(port_hole).translate(
            Vector(self.sum_outer_thickness_full, 0, 0))

        # Here we apply the rotations to the port
        port = port.rotate((0, -self.eq_ports_rest[index][0], 0),
                           (0, self.eq_ports_rest[index][0], 0),
                           -self.eq_ports_rest[index][2]).\
                    rotate((0, 0, -self.eq_ports_rest[index][0]),
                           (0, 0, self.eq_ports_rest[index][0]),
                           self.eq_ports_rest[index][3])

        # Here we transalte the port to the proper radious
        # then cut away a containment shaped circular cylinder
        # so that in the final construction the ports will sit
        # flush with the inner containment wall

        if self.eq_ports_rest[index][2] < 0:
            port = port.translate(Vector(-self.outer_radius,
                                         -allign_xy_port - self.eq_ports_rest[index][5],
                                         self.eq_ports_rest[index][4])).\
                        cut(port_cut).\
                        cut(port_end_cut_up).\
                        translate(Vector(self.outer_radius - self.containment_rest[0][3] / 2,
                                         0,
                                         -self.eq_ports_rest[index][4]))
        else:
            port = port.translate(Vector(-self.outer_radius,
                                         -allign_xy_port - self.eq_ports_rest[index][5],
                                         self.eq_ports_rest[index][4])).\
                        cut(port_cut).\
                        cut(port_end_cut_down).\
                        translate(Vector(self.outer_radius - self.containment_rest[0][3] / 2,
                                         0,
                                         -self.eq_ports_rest[index][4]))

        # Finally the persistent rotation of the final
        # geometry is applied (so all the ports face center)

        port = port.rotate((0, 0, self.eq_ports_rest[index][0]),
                           (0, 0, -self.eq_ports_rest[index][0]),
                           -deg_angle + 180)

        return port.translate(Vector(x_poz, y_poz, self.eq_ports_rest[index][4] - allign_z_port))

    def transformer_limb(self, index: int):
        """Creates all transformer limbs and unions them together.

        Args:
            index (int): the limb to be created, 0 is the one at angle 0,
            1 is the one at angle/360/nr_of_ports, etc.

        Returns:
            cadquery.Workplane: the transformer limbs.
        """

        angle = (2 * m.pi) / self.nr_limbs
        deg_angle = (angle * index * 180) / m.pi

        transformer_limb = cq.Workplane("XY").\
            box(self.limbs_rest[index][0],
                self.limbs_rest[index][1],
                self.solenoid_height).\
            rotate((0, 0, -self.solenoid_height),
                   (0, 0, self.solenoid_height),
                   deg_angle)

        x_poz = (self.limb_radius) * m.cos(angle * index)
        y_poz = (self.limb_radius) * m.sin(angle * index)

        sphere_right = self.spheres(index=index)[0].\
            rotate((0, 0, -self.solenoid_height), (0, 0, self.solenoid_height), deg_angle).\
            translate(Vector(x_poz, y_poz, 0))

        sphere_left = self.spheres(index=index)[1].\
            rotate((0, 0, -self.solenoid_height), (0, 0, self.solenoid_height), deg_angle).\
            translate(Vector(x_poz, y_poz, 0))

        transformer_limb = transformer_limb.translate(Vector(x_poz, y_poz, 0))
        transformer_limb = transformer_limb.rotate((0, 0, -self.solenoid_height),
                                                   (0, 0, self.solenoid_height),
                                                   self.limb_offset)
        sphere_right = sphere_right.rotate((0, 0, -self.solenoid_height),
                                           (0, 0, self.solenoid_height),
                                           self.limb_offset)
        sphere_left = sphere_left.rotate((0, 0, -self.solenoid_height),
                                         (0, 0, self.solenoid_height),
                                         self.limb_offset)

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
        angle = (2 * m.pi) / self.nr_ports
        deg_angle = (angle * index * 180) / m.pi

        x_s = (self.outer_radius + self.containment_rest[0][3] / 2 - self.sum_outer_thickness_full +
               self.limiter_thickness / 2 + self.firstwall_thickness / 2) * m.cos(angle * index)
        y_s = (self.outer_radius + self.containment_rest[0][3] / 2 - self.sum_outer_thickness_full +
               self.limiter_thickness / 2 + self.firstwall_thickness / 2) * m.sin(angle * index)

        x_poz = (self.outer_radius + self.containment_rest[0][3] / 2 -
             self.sum_outer_thickness_full) * m.cos(angle * index)
        y_poz = (self.outer_radius + self.containment_rest[0][3] / 2 -
             self.sum_outer_thickness_full) * m.sin(angle * index)

        allign_z_port = self.sum_outer_thickness_full / \
            m.cos(m.radians(self.eq_ports_rest[index][2])) * \
            m.sin(m.radians(self.eq_ports_rest[index][2]))

        # Constructing objects to be used for later addition and subtraction
        firstwall = cq.Workplane("XY").\
            box(self.firstwall_thickness,
                self.eq_ports_rest[index][1] - self.limiter_gap,
                self.eq_ports_rest[index][1] - self.limiter_gap)

        firstwall_rear = cq.Workplane("XY").\
            box(self.limiter_thickness,
                self.eq_ports_rest[index][1] - self.limiter_gap,
                self.eq_ports_rest[index][1] - self.limiter_gap)

        # Here we apply the rotations to the port
        firstwall = firstwall.rotate((0, -self.eq_ports_rest[index][0], 0),
                                     (0, self.eq_ports_rest[index][0], 0),
                                     -self.eq_ports_rest[index][2]).\
                              rotate((0, 0, -self.eq_ports_rest[index][0]),
                                     (0, 0, self.eq_ports_rest[index][0]),
                                     self.eq_ports_rest[index][3])

        firstwall_rear = firstwall_rear.rotate((0, -self.eq_ports_rest[index][0], 0),
                                               (0, self.eq_ports_rest[index][0], 0),
                                               -self.eq_ports_rest[index][2]).\
                                        rotate((0, 0, -self.eq_ports_rest[index][0]),
                                               (0, 0, self.eq_ports_rest[index][0]),
                                               self.eq_ports_rest[index][3])

        # Finally the persistent rotation of the
        # final geometry is applied (so all the ports face center)
        firstwall = firstwall.rotate((0, 0, self.eq_ports_rest[index][0]),
                                     (0, 0, -self.eq_ports_rest[index][0]),
                                     -deg_angle+180)
        firstwall_rear = firstwall_rear.rotate((0, 0, self.eq_ports_rest[index][0]),
                                               (0, 0, -self.eq_ports_rest[index][0]),
                                               -deg_angle+180)
        firstwall = firstwall.translate(Vector(x_poz,
                                               y_poz,
                                               self.eq_ports_rest[index][4] - allign_z_port))
        firstwall_r = firstwall_rear.translate(Vector(x_s,
                                                      y_s,
                                                      self.eq_ports_rest[index][4] - allign_z_port))

        return firstwall, firstwall_r

    def bounding_box(self):
        """Creates the bounding box of the reactor.

        Returns:
            cadquery.cq.Workplane: the bounding box.
        """

        bounding_box_outer = cq.Workplane("XY").\
            box(self.limb_radius + self.outer_radius * 8 + self.bbox_thickness,
                self.limb_radius + self.outer_radius * 8 + self.bbox_thickness,
                self.solenoid_height * 4 + self.bbox_thickness)
        bounding_box_inner = cq.Workplane("XY").\
            box(self.limb_radius + self.outer_radius * 8,
                self.limb_radius + self.outer_radius * 8,
                self.solenoid_height * 4)

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

        sphere_right = cq.Workplane("XY").sphere(self.sphere_radius).translate(
            Vector(0, self.sphere_radius+self.limbs_rest[index][1]/2))
        sphere_left = cq.Workplane("XY").sphere(self.sphere_radius).translate(
            Vector(0, -self.sphere_radius-self.limbs_rest[index][1]/2))

        return sphere_right, sphere_left

    def plasma_source(self, distance_from_wall: float):
        """Creates the plasma source.

        Args:
            distance_from_wall (float): distance between the plasma
            source and the first wall.

        Returns:
            cadquery.cq.Workplane: the plasma source.
        """

        cyl_outer_r = self.outer_radius - self.sum_outer_thickness_full - distance_from_wall
        cyl_inner_r = self.solenoid_radius + self.sum_inner_thickness_full + distance_from_wall
        cyl_height = self.containment_height - self.sum_lower_thickness_full - \
            self.sum_upper_thickness_full - 2 * distance_from_wall

        cyl = cq.Workplane("XY").cylinder(cyl_height, cyl_outer_r).\
                 cut(cq.Workplane("XY").cylinder(cyl_height, cyl_inner_r))

        return cyl


class GeometryInjector:
    """
    A class that houses functions that inject
    monte carlo code into an input file.
    """
    def __init__(self, **kwargs):
        self.serpent_filepath = kwargs["file"]
        self.line_nr = kwargs["line_nr"]
        self.newfile = kwargs["newfile_location"]

    def inject_line(self, **kwargs):
        """
        Injects a line of code into a file.
        """
        # inject_line
        with open(self.serpent_filepath, "r", encoding='utf8') as file:
            contents = file.readlines()

        contents.insert(self.line_nr, kwargs["inject_string"])

        with open(self.newfile, "w", encoding='utf8') as file:
            contents = "".join(contents)
            file.write(contents)

        self.line_nr += 1

        file.close()

    def body(self, **kwargs):
        """
        Body inject function.
        """

        line = f"body {kwargs['body_name']} {kwargs['body_name']} {kwargs['material']}\n"

        self.inject_line(inject_string=line)

    def file(self, **kwargs):
        """
        After the body inject function.
        """

        line = f"file {kwargs['object_name']} { kwargs['filepath']} {kwargs['scale']} 0 0 0\n"

        self.inject_line(inject_string=line)

        if kwargs["last"] is not None:
            self.inject_line(inject_string="\n")
