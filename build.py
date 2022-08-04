import math as m

import cadquery as cq
from cadquery import Vector


class filereader:
    """
    Reads the input file, in the future this will be depricated.
    """

    def __init__(self, filename: str, skip_lines: int, nr_of_data: int):
        self.filename = filename
        self.skip_lines = skip_lines
        self.nr_of_data = nr_of_data

    def reader(self):
        with open(self.filename, "r") as file:
            output = []
            for i, line in enumerate(file):
                if ("\n" in line[0]) or ("#" in line[0]) or ("%" in line[0]):
                    pass
                else:
                    output.append(eval(line))
        return output

    def readerplain(self):
        with open(self.filename, "r") as file:
            output = []
            for i, line in enumerate(file):
                if ("\n" in line[0]) or ("#" in line[0]) or ("%" in line[0]):
                    pass
                else:
                    output.append(line)
        return output

    def parsing(self):
        output = []
        count = self.nr_of_data
        for i in range(self.skip_lines, len(self.reader())):
            if count == self.nr_of_data:
                output.append(self.reader()[i:i+self.nr_of_data+1])
                count = 0
            else:
                count += 1
        return output

    def iterator(**kwargs):
        directory = kwargs["directory"]
        files = []
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                files.append(f)

        return files


class rectok:
    def __init__(self):
        # --- Containment ---
        containment = filereader("Containment.txt", 4, 5).reader()
        self.outer_radius = containment[0]
        self.containment_height = containment[1]
        self.containment_cut = containment[2]
        self.nr_layers = containment[3]
        self.containment_rest = filereader("Containment.txt", 4, 5).parsing()

        # --- Solenoid ---
        solenoid = filereader("Solenoid.txt", 0, 0).reader()
        self.solenoid_radius = solenoid[1]
        self.solenoid_height = solenoid[2]

        # --- Ports ---
        eq_port = filereader("Equatorial_ports.txt", 4, 6).reader()
        self.nr_ports = eq_port[0]
        self.shape = eq_port[2]
        self.longer_rect = eq_port[3]
        self.eq_ports_rest = filereader("Equatorial_ports.txt", 4, 6).parsing()

        # --- Limbs ---
        limbs = filereader("Limbs.txt", 5, 4).reader()
        self.nr_limbs = limbs[0]
        self.limb_radius = self.outer_radius + limbs[2]
        self.limb_offset = 360/(self.nr_ports * 2) if limbs[4] == "yes" else 0
        self.limbs_rest = filereader("Limbs.txt", 5, 4).parsing()

        # --- Limiter ---
        limiter = filereader("Limiter.txt", 0, 0).reader()
        self.firstwall_thickness = self.containment_rest[self.nr_layers-1][3]
        self.limiter_gap = limiter[0]
        self.limiter_thickness = limiter[1]

        # --- Bounding box ---
        self.bbox_thickness = solenoid[3]

        # --- Limiter spheres ---
        self.sphere_radius = limbs[3]

        self.SumOuterThickness_Full = 0
        for a in range(self.nr_layers):
            self.SumOuterThickness_Full += self.containment_rest[a][3]

        self.SumUpperThickness_Full = 0
        for b in range(self.nr_layers):
            self.SumUpperThickness_Full += self.containment_rest[b][1]

        self.SumLowerThickness_Full = 0
        for c in range(self.nr_layers):
            self.SumLowerThickness_Full += self.containment_rest[c][2]

        self.SumInnerThickness_Full = 0
        for d in range(self.nr_layers):
            self.SumInnerThickness_Full += self.containment_rest[d][4]

    def CentralSolenoid(self):
        solenoid = cq.Workplane("YX").\
            circle(self.solenoid_radius).\
            extrude(self.solenoid_height).\
            translate(Vector(0, 0, self.solenoid_height/2))
        return solenoid

    def Openings(self, **kwargs):

        angle = (2*m.pi)/self.nr_ports
        degAngle = (angle*kwargs["index"]*180)/m.pi

        x = (self.outer_radius -
             self.containment_rest[0][3]/2)*m.cos((angle)*kwargs["index"])
        y = (self.outer_radius -
             self.containment_rest[0][3]/2)*m.sin((angle)*kwargs["index"])

        port_depth = self.SumOuterThickness_Full * \
            (1/m.cos(m.radians(self.eq_ports_rest[kwargs["index"]][2])) + 1/m.cos(
                m.radians(self.eq_ports_rest[kwargs["index"]][2])))

        # Constructing objects to be used for later addition and subtraction
        if self.shape == "square":
            port_nohole = cq.Workplane("XY").\
                box(port_depth*4, self.eq_ports_rest[kwargs["index"]]
                    [0], self.eq_ports_rest[kwargs["index"]][0])
        elif self.shape == "rectangle_z":
            port_nohole = cq.Workplane("XY").\
                box(port_depth*4,
                    self.eq_ports_rest[kwargs["index"]][0], self.longer_rect)
        elif self.shape == "rectangle_y":
            port_nohole = cq.Workplane("XY").\
                box(port_depth*4, self.longer_rect,
                    self.eq_ports_rest[kwargs["index"]][0])
        else:
            raise Exception("no such object yet")

        port_endcutDOWN = cq.Workplane("XY").\
            circle(self.outer_radius).\
            extrude(100).\
            translate(Vector(0, 0, -self.containment_height /
                      2 + self.SumLowerThickness_Full - 100))

        port_endcutUP = cq.Workplane("XY").\
            circle(self.outer_radius).\
            extrude(100).\
            translate(Vector(0, 0, +self.containment_height /
                      2 - self.SumUpperThickness_Full))

        port_cut = cq.Workplane("XY").\
            circle(self.outer_radius-self.SumOuterThickness_Full).\
            extrude(self.eq_ports_rest[kwargs["index"]][0]*100).\
            translate(
                Vector(0, 0, -(self.eq_ports_rest[kwargs["index"]][0])*100/2))

        allignXYport = self.SumOuterThickness_Full / \
            m.cos(m.radians(self.eq_ports_rest[kwargs["index"]][3])) * m.sin(
                m.radians(self.eq_ports_rest[kwargs["index"]][3]))

        # Here we cut the hole into the port
        port = port_nohole.translate(Vector(self.SumOuterThickness_Full, 0, 0))

        # Here we apply the rotations to the port
        port = port.rotate((0, -self.eq_ports_rest[kwargs["index"]][0], 0), (0, self.eq_ports_rest[kwargs["index"]][0], 0), -self.eq_ports_rest[kwargs["index"]][2]).\
            rotate((0, 0, -self.eq_ports_rest[kwargs["index"]][0]), (0, 0,
                   self.eq_ports_rest[kwargs["index"]][0]), self.eq_ports_rest[kwargs["index"]][3])

        # Here we translate the port to the proper radius then cut away a containment shaped circular cylinder so that in the final construction the ports will sit flush with the inner containment wall
        if self.eq_ports_rest[kwargs["index"]][2] < 0:
            port = port.translate(Vector(-self.outer_radius, -allignXYport-self.eq_ports_rest[kwargs["index"]][5], self.eq_ports_rest[kwargs["index"]][4])).\
                cut(port_cut).cut(port_endcutUP).\
                translate(Vector(
                    self.outer_radius-self.containment_rest[0][3]/2, 0, -self.eq_ports_rest[kwargs["index"]][4]))
        else:
            port = port.translate(Vector(-self.outer_radius, -allignXYport-self.eq_ports_rest[kwargs["index"]][5], self.eq_ports_rest[kwargs["index"]][4])).\
                cut(port_cut).cut(port_endcutDOWN).\
                translate(Vector(
                    self.outer_radius-self.containment_rest[0][3]/2, 0, -self.eq_ports_rest[kwargs["index"]][4]))

        # Inner wall alignemnt
        allignZ = self.SumOuterThickness_Full / \
            m.cos(m.radians(self.eq_ports_rest[kwargs["index"]][2])) * m.sin(
                m.radians(self.eq_ports_rest[kwargs["index"]][2]))

        # Finally the persistent rotation of the final geometry is applied (so all the ports face center)
        port = port.rotate((0, 0, self.eq_ports_rest[kwargs["index"]][0]), (0, 0, -self.eq_ports_rest[kwargs["index"]][0]), -180-degAngle).\
            translate(
                Vector(x, y, self.eq_ports_rest[kwargs["index"]][4] - allignZ))

        return port

    def ContConstrFunct(self, **kwargs):

        # Thickness counters for easier function definition
        SumUpperThickness = 0
        SumLowerThickness = 0
        SumOuterThickness = 0
        SumInnerThickness = 0

        if kwargs["index"] > 0:
            for i in range(kwargs["index"]):
                SumUpperThickness += self.containment_rest[i][1]
                SumLowerThickness += self.containment_rest[i][2]
                SumOuterThickness += self.containment_rest[i][3]
                SumInnerThickness += self.containment_rest[i][4]

        horizontal_displacement = SumOuterThickness + SumInnerThickness
        vertical_displacement = SumUpperThickness + SumLowerThickness

        debelinaNot = self.containment_rest[kwargs["index"]][4]
        debelinaZun = self.containment_rest[kwargs["index"]][3]
        debelinaGor = self.containment_rest[kwargs["index"]][1]
        debelinaDol = self.containment_rest[kwargs["index"]][2]

        sirina = self.outer_radius - self.solenoid_radius - horizontal_displacement
        visina = self.containment_height - vertical_displacement

        InnerR = self.solenoid_radius + SumInnerThickness

        vertical_alignment = (-SumUpperThickness+SumLowerThickness)/2

        pointsouter = [
            (sirina/2+InnerR+sirina/2, visina/2),
            (sirina/2+InnerR+sirina/2, -visina/2),
            (-sirina/2+InnerR+sirina/2, -visina/2),
            (-sirina/2+InnerR+sirina/2, visina/2),
            (sirina/2+InnerR+sirina/2, visina/2)
        ]

        pointsinner = [
            (sirina/2-debelinaZun+InnerR+sirina/2, visina/2-debelinaGor),
            (sirina/2-debelinaZun+InnerR+sirina/2, -visina/2+debelinaDol),
            (-sirina/2+debelinaNot+InnerR+sirina/2, -visina/2+debelinaDol),
            (-sirina/2+debelinaNot+InnerR+sirina/2, visina/2-debelinaGor),
            (sirina/2-debelinaZun+InnerR+sirina/2, visina/2-debelinaGor)
        ]

        rezultat = cq.Workplane('XZ').polyline(pointsouter).\
            close().revolve(self.containment_cut)

        rezultat2 = cq.Workplane('XZ').polyline(pointsinner).\
            close().revolve(self.containment_cut)

        return rezultat.cut(rezultat2)

    def Port(self, **kwargs):

        angle = (2*m.pi)/self.nr_ports
        degAngle = (angle*kwargs["index"]*180)/m.pi

        x = (self.outer_radius -
             self.containment_rest[0][3]/2)*m.cos(angle*kwargs["index"])
        y = (self.outer_radius -
             self.containment_rest[0][3]/2)*m.sin(angle*kwargs["index"])

        allignZport = self.SumOuterThickness_Full / \
            m.cos(m.radians(self.eq_ports_rest[kwargs["index"]][2])) * m.sin(
                m.radians(self.eq_ports_rest[kwargs["index"]][2]))

        port_depth = self.SumOuterThickness_Full/m.cos(m.radians(self.eq_ports_rest[kwargs["index"]][2]))*2 + self.SumOuterThickness_Full/4 if self.eq_ports_rest[kwargs["index"]
                                                                                                                                                                  ][2] != 0 else self.SumOuterThickness_Full/m.cos(m.radians(self.eq_ports_rest[kwargs["index"]][3]))*2 + self.SumOuterThickness_Full/4

        # Constructing objects to be used for later addition and subtraction
        port_nohole = cq.Workplane("XY").box(
            port_depth, self.eq_ports_rest[kwargs["index"]][0], self.eq_ports_rest[kwargs["index"]][0])

        port_hole = cq.Workplane("XY").box(
            port_depth, self.eq_ports_rest[kwargs["index"]][1], self.eq_ports_rest[kwargs["index"]][1])

        port_endcutDOWN = cq.Workplane("XY").circle(self.outer_radius).extrude(100).\
            translate(Vector(0, 0, -self.containment_height /
                      2+self.SumLowerThickness_Full-100))

        port_endcutUP = cq.Workplane("XY").circle(self.outer_radius).extrude(100).\
            translate(Vector(0, 0, +self.containment_height /
                      2-self.SumUpperThickness_Full))

        port_cut = cq.Workplane("XY").circle(self.outer_radius-self.SumOuterThickness_Full).extrude(self.eq_ports_rest[kwargs["index"]][0]*100).\
            translate(
                Vector(0, 0, -self.eq_ports_rest[kwargs["index"]][0]*100/2))

        allignXYport = self.SumOuterThickness_Full / \
            m.cos(m.radians(self.eq_ports_rest[kwargs["index"]][3])) * m.sin(
                m.radians(self.eq_ports_rest[kwargs["index"]][3]))

        # Here we cut the hole into the port
        port = port_nohole.cut(port_hole).translate(
            Vector(self.SumOuterThickness_Full, 0, 0))

        # Here we apply the rotations to the port
        port = port.rotate((0, -self.eq_ports_rest[kwargs["index"]][0], 0), (0, self.eq_ports_rest[kwargs["index"]][0], 0), -self.eq_ports_rest[kwargs["index"]][2]).\
            rotate((0, 0, -self.eq_ports_rest[kwargs["index"]][0]), (0, 0,
                   self.eq_ports_rest[kwargs["index"]][0]), self.eq_ports_rest[kwargs["index"]][3])

        # Here we transalte the port to the proper radious then cut away a containment shaped circular cylinder so that in the final construction the ports will sit flush with the inner containment wall
        if self.eq_ports_rest[kwargs["index"]][2] < 0:
            port = port.translate(Vector(-self.outer_radius, -allignXYport-self.eq_ports_rest[kwargs["index"]][5], self.eq_ports_rest[kwargs["index"]][4])).\
                cut(port_cut).cut(port_endcutUP).\
                translate(Vector(
                    self.outer_radius-self.containment_rest[0][3]/2, 0, -self.eq_ports_rest[kwargs["index"]][4]))
        else:
            port = port.translate(Vector(-self.outer_radius, -allignXYport-self.eq_ports_rest[kwargs["index"]][5], self.eq_ports_rest[kwargs["index"]][4])).\
                cut(port_cut).cut(port_endcutDOWN).\
                translate(Vector(
                    self.outer_radius-self.containment_rest[0][3]/2, 0, -self.eq_ports_rest[kwargs["index"]][4]))

        # Finally the persistent rotation of the final geometry is applied (so all the ports face center)
        port = port.rotate((0, 0, self.eq_ports_rest[kwargs["index"]][0]), (
            0, 0, -self.eq_ports_rest[kwargs["index"]][0]), -degAngle+180)

        return port.translate(Vector(x, y, self.eq_ports_rest[kwargs["index"]][4]-allignZport))

    def TransLimb(self, **kwargs):

        angle = (2*m.pi)/self.nr_limbs
        degAngle = (angle*kwargs["index"]*180)/m.pi

        transformer_limb = cq.Workplane("XY").box(self.limbs_rest[kwargs["index"]][0], self.limbs_rest[kwargs["index"]][1], self.solenoid_height).\
            rotate((0, 0, -self.solenoid_height),
                   (0, 0, self.solenoid_height), degAngle)

        x = (self.limb_radius)*m.cos(angle*kwargs["index"])
        y = (self.limb_radius)*m.sin(angle*kwargs["index"])

        sphere_right = self.Spheres(index=kwargs["index"])[0].\
            rotate((0, 0, -self.solenoid_height), (0, 0, self.solenoid_height), degAngle).\
            translate(Vector(x, y, 0))

        sphere_left = self.Spheres(index=kwargs["index"])[1].\
            rotate((0, 0, -self.solenoid_height), (0, 0, self.solenoid_height), degAngle).\
            translate(Vector(x, y, 0))

        transformer_limb = transformer_limb.translate(Vector(x, y, 0))

        return transformer_limb.rotate((0, 0, -self.solenoid_height), (0, 0, self.solenoid_height), self.limb_offset), sphere_right.rotate((0, 0, -self.solenoid_height), (0, 0, self.solenoid_height), self.limb_offset), sphere_left.rotate((0, 0, -self.solenoid_height), (0, 0, self.solenoid_height), self.limb_offset)

    def Limiter(self, **kwargs):

        # Firstwall construction

        angle = (2*m.pi)/self.nr_ports
        degAngle = (angle*kwargs["index"]*180)/m.pi

        x_s = (self.outer_radius+self.containment_rest[0][3]/2-self.SumOuterThickness_Full +
               self.limiter_thickness/2+self.firstwall_thickness/2)*m.cos(angle*kwargs["index"])
        y_s = (self.outer_radius+self.containment_rest[0][3]/2-self.SumOuterThickness_Full +
               self.limiter_thickness/2+self.firstwall_thickness/2)*m.sin(angle*kwargs["index"])

        x = (self.outer_radius+self.containment_rest[0][3]/2 -
             self.SumOuterThickness_Full)*m.cos(angle*kwargs["index"])
        y = (self.outer_radius+self.containment_rest[0][3]/2 -
             self.SumOuterThickness_Full)*m.sin(angle*kwargs["index"])

        allignZport = self.SumOuterThickness_Full / \
            m.cos(m.radians(self.eq_ports_rest[kwargs["index"]][2])) * m.sin(
                m.radians(self.eq_ports_rest[kwargs["index"]][2]))

        # Constructing objects to be used for later addition and subtraction
        firstwall = cq.Workplane("XY").box(
            self.firstwall_thickness, self.eq_ports_rest[kwargs["index"]][1] - self.limiter_gap, self.eq_ports_rest[kwargs["index"]][1] - self.limiter_gap)

        firstwall_rear = cq.Workplane("XY").box(
            self.limiter_thickness, self.eq_ports_rest[kwargs["index"]][1] - self.limiter_gap, self.eq_ports_rest[kwargs["index"]][1] - self.limiter_gap)

        port_endcutDOWN = cq.Workplane("XY").circle(self.outer_radius).extrude(100).\
            translate(Vector(0, 0, -self.containment_height /
                      2+self.SumLowerThickness_Full-100))

        port_endcutUP = cq.Workplane("XY").circle(self.outer_radius).extrude(100).\
            translate(Vector(0, 0, +self.containment_height /
                      2-self.SumUpperThickness_Full))

        port_cut = cq.Workplane("XY").circle(self.outer_radius-self.SumOuterThickness_Full).extrude(self.eq_ports_rest[kwargs["index"]][0]*100).\
            translate(
                Vector(0, 0, -self.eq_ports_rest[kwargs["index"]][0]*100/2))

        allignXYport = self.SumOuterThickness_Full / \
            m.cos(m.radians(self.eq_ports_rest[kwargs["index"]][3])) * m.sin(
                m.radians(self.eq_ports_rest[kwargs["index"]][3]))

        # Here we apply the rotations to the port
        firstwall = firstwall.rotate((0, -self.eq_ports_rest[kwargs["index"]][0], 0), (0, self.eq_ports_rest[kwargs["index"]][0], 0), -self.eq_ports_rest[kwargs["index"]][2]).\
            rotate((0, 0, -self.eq_ports_rest[kwargs["index"]][0]), (0, 0,
                   self.eq_ports_rest[kwargs["index"]][0]), self.eq_ports_rest[kwargs["index"]][3])

        firstwall_rear = firstwall_rear.rotate((0, -self.eq_ports_rest[kwargs["index"]][0], 0), (0, self.eq_ports_rest[kwargs["index"]][0], 0), -self.eq_ports_rest[kwargs["index"]][2]).\
            rotate((0, 0, -self.eq_ports_rest[kwargs["index"]][0]), (0, 0,
                   self.eq_ports_rest[kwargs["index"]][0]), self.eq_ports_rest[kwargs["index"]][3])

        # Finally the persistent rotation of the final geometry is applied (so all the ports face center)
        firstwall = firstwall.rotate((0, 0, self.eq_ports_rest[kwargs["index"]][0]), (
            0, 0, -self.eq_ports_rest[kwargs["index"]][0]), -degAngle+180)
        firstwall_rear = firstwall_rear.rotate((0, 0, self.eq_ports_rest[kwargs["index"]][0]), (
            0, 0, -self.eq_ports_rest[kwargs["index"]][0]), -degAngle+180)

        return [firstwall.translate(Vector(x, y, self.eq_ports_rest[kwargs["index"]][4] - allignZport)), firstwall_rear.translate(Vector(x_s, y_s, self.eq_ports_rest[kwargs["index"]][4] - allignZport))]

    def BoundingBox(self, **kwargs):

        bounding_box_outer = cq.Workplane("XY").box(self.limb_radius+self.outer_radius * 8 + self.bbox_thickness,
                                                    self.limb_radius+self.outer_radius * 8 + self.bbox_thickness, self.solenoid_height * 4 + self.bbox_thickness)
        bounding_box_inner = cq.Workplane("XY").box(
            self.limb_radius+self.outer_radius * 8, self.limb_radius+self.outer_radius * 8, self.solenoid_height * 4)

        bounding_box = bounding_box_outer.cut(bounding_box_inner)

        return bounding_box

    def Spheres(self, **kwargs):

        sphere_right = cq.Workplane("XY").sphere(self.sphere_radius).translate(
            Vector(0, self.sphere_radius+self.limbs_rest[kwargs["index"]][1]/2))
        sphere_left = cq.Workplane("XY").sphere(self.sphere_radius).translate(
            Vector(0, -self.sphere_radius-self.limbs_rest[kwargs["index"]][1]/2))

        return sphere_right, sphere_left

    def PlasmaSrc(self, **kwargs):

        distance_from_wall = kwargs["distance_from_wall"]

        cyl_outer_r = self.outer_radius - self.SumOuterThickness_Full - distance_from_wall
        cyl_inner_r = self.solenoid_radius + \
            self.SumInnerThickness_Full + distance_from_wall
        cyl_height = self.containment_height - self.SumLowerThickness_Full - \
            self.SumUpperThickness_Full - 2*distance_from_wall
        print(cyl_inner_r)
        print(cyl_outer_r)
        print(cyl_height)

        cyl = cq.Workplane("XY").cylinder(cyl_height, cyl_outer_r).cut(
            cq.Workplane("XY").cylinder(cyl_height, cyl_inner_r))

        return cyl


class GeometryInjector():
    def __init__(self, **kwargs):

        self.serpent_filepath = kwargs["file"]
        self.line_nr = kwargs["line_nr"]
        self.newfile = kwargs["newfile_location"]

    def InjectLine(self, **kwargs):
        # inject_line

        with open(self.serpent_filepath, "r") as f:
            contents = f.readlines()

        contents.insert(self.line_nr, kwargs["inject_string"])

        with open(self.newfile, "w") as f:
            contents = "".join(contents)
            f.write(contents)

        self.line_nr += 1

        f.close()

    def Body(self, **kwargs):

        line = "body {} {} {}\n".format(
            kwargs["body_name"], kwargs["body_name"], kwargs["material"])

        self.InjectLine(inject_string=line)

    def File(self, **kwargs):

        line = "file {} \"{}\" {} 0 0 0\n".format(
            kwargs["object_name"], kwargs["filepath"], kwargs["scale"])

        self.InjectLine(inject_string=line)

        if kwargs["last"] != None:
            self.InjectLine(inject_string="\n")
