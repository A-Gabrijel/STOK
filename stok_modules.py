"""The STOK builder, text file search and inject functions to use when
generating STOK."""
from dataclasses import dataclass, field
from os import cpu_count
from typing import List, Tuple

import cadquery as cq
import gmsh
from cadquery import Vector


class FileReader:
    """
    Reads the input file.
    """

    def __init__(self, *args):
        self.filename = args[0]
        self.read = self.reader()

    def reader(self) -> List[float]:
        """
        Reads a file and checks for numerical values,
        then returns a list of the numerical values.

        Returns:
            List[float, str]: returns a tuple of the numerical values.
        """
        with open(self.filename, 'r', encoding='utf8') as file:
            output: List[float] = []
            for i, line in enumerate(file):
                if ("\n" in line[0]) or ("#" in line[0]) or ("%" in line[0]):
                    pass
                else:
                    output.append(float(line))
        return output


@dataclass(order=True, frozen=True)
class Layer:
    """Layer class, used to store the data for each layer.

    Args:
        upper_lower_outer: float
        inner: float
    """
    upper_lower_outer: float
    inner: float


def layers_all() -> Tuple:
    """Returns a list of Layer objects.

    Args:
        args: float

    Returns:
        List[Layer]: returns a list of Layer objects.
    """
    output: List = []
    nr_layers = int(FileReader('stok_config.txt').read[2])
    for i in range(3, nr_layers*2+3, 2):
        output.append(Layer(FileReader("stok_config.txt").read[i],
                            FileReader("stok_config.txt").read[i+1]))
    return tuple(output)


@dataclass(order=True, frozen=True)
class ContainmentParameters:
    """A class to store the parameters for the containment.

    Args:
        outer_radius: float
        containment_height: float
        nr_layers: int
        layers: List[Layer]
        distance_from_plasma: float
    """
    outer_radius: float = FileReader("stok_config.txt").read[0]
    containment_height: float = FileReader("stok_config.txt").read[1]
    nr_layers: int = int(FileReader("stok_config.txt").read[2])
    distance_from_plasma: float = FileReader("stok_config.txt").read[-1]
    layers: Tuple = field(default=layers_all())


@dataclass(order=True, frozen=True)
class SolenoidParameters:
    """Class that contains the parameters for the solenoid.

    Args:
        solenoid_radius: float
        solenoid_height: float
    """
    solenoid_radius: float = FileReader(
        "stok_config.txt").read[ContainmentParameters.nr_layers*2+3]
    solenoid_height: float = FileReader(
        "stok_config.txt").read[ContainmentParameters.nr_layers*2+4]
    bbox_thickness: float = FileReader(
        "stok_config.txt").read[ContainmentParameters.nr_layers*2+5]


@dataclass(order=True, frozen=True)
class PortParameters:
    """Class that contains the parameters for the ports.

    Args:
        nr_ports: int
        z_side: float
        y_side: float
    """
    nr_ports: int = int(FileReader(
        "stok_config.txt").read[ContainmentParameters.nr_layers*2+6])
    z_side: float = FileReader(
        "stok_config.txt").read[ContainmentParameters.nr_layers*2+7]
    y_side: float = FileReader(
        "stok_config.txt").read[ContainmentParameters.nr_layers*2+8]


@dataclass(order=True, frozen=True)
class LimbDimensiones:
    """Class that contains the dimensions for the limbs.

    Args:
        limb_length: float
        limb_height: float
        limb_width: float
    """
    limb_length: float
    limb_width: float
    limb_height: float


@dataclass(order=True, frozen=True)
class LimbParameters:
    """Class that contains the parameters for the limbs.

    Args:
        nr_limbs: int
        limb_radius: float -> at what radius the limbs are placed.
        sphere_radius: float -> the radius of the spheres next to the limb.
    """
    nr_limbs: int = int(FileReader(
        "stok_config.txt").read[ContainmentParameters.nr_layers*2+9])
    limb_radius: float = ContainmentParameters.outer_radius + \
        FileReader(
            "stok_config.txt").read[ContainmentParameters.nr_layers*2+10]
    sphere_radius: float = FileReader(
        "stok_config.txt").read[ContainmentParameters.nr_layers*2+11]
    limb_dimensions: LimbDimensiones = LimbDimensiones(
        FileReader(
            "stok_config.txt").read[ContainmentParameters.nr_layers*2+12],
        FileReader(
            "stok_config.txt").read[ContainmentParameters.nr_layers*2+13],
        FileReader(
            "stok_config.txt").read[ContainmentParameters.nr_layers*2+14]
        if FileReader("stok_config.txt").read[ContainmentParameters.nr_layers*2+14] != 0.0
        else SolenoidParameters.solenoid_height)


@dataclass(order=True, frozen=True)
class LimiterParameters:
    """Class that contains the parameters for the limiter.

    Attributes:
        firstwall_thickness: float
        limiter_gap: float
        limiter_thickness: float
    """
    firstwall_thickness: float = FileReader("stok_config.txt").\
        read[ContainmentParameters.nr_layers*2+15]
    limiter_gap: float = FileReader(
        "stok_config.txt").read[ContainmentParameters.nr_layers*2+16]
    limiter_thickness: float = FileReader("stok_config.txt").\
        read[ContainmentParameters.nr_layers*2+17]


@dataclass(order=True, frozen=True)
class DivertorParameters:
    """A class that contains the parameters for the divertor.

    Attributes:
        divertor_thickness: float
        divertor_gap: float or bool
        divertor_firstwall_thickness: float
        TODO divertor_shape: float
    """
    divertor_firstwall_thickness: float = FileReader("stok_config.txt").\
        read[ContainmentParameters.nr_layers*2+18]
    divertor_width: float = FileReader(
        "stok_config.txt").read[ContainmentParameters.nr_layers*2+19]
    divertor_gap: float = FileReader(
        "stok_config.txt").read[ContainmentParameters.nr_layers*2+20]
    divertor_thickness: float = FileReader("stok_config.txt").\
        read[ContainmentParameters.nr_layers*2+21]
    # divertor_shape: float = FileReader( TODO: add shape to divertor.
    #     "stok_config.txt").read[ContainmentParameters.nr_layers*2+22]


class STOK():
    """The class containing all construction components."""

    def __init__(self, param_tup: Tuple) -> None:
        type_tuple = list(map(type, param_tup))
        if type_tuple == [ContainmentParameters, SolenoidParameters, PortParameters,
                          LimbParameters, LimiterParameters, DivertorParameters]:
            self.containment_parameters = param_tup[0]
            self.solenoid_parameters = param_tup[1]
            self.port_parameters = param_tup[2]
            self.limb_parameters = param_tup[3]
            self.limiter_parameters = param_tup[4]
            self.divertor_parameters = param_tup[5]
        else:
            raise TypeError("Wrong input types, expected type ContainmentParameters, SolenoidParameters, PortParameters, LimbParameters, LimiterParameters, DivertorParameters in that order.")

    def central_solenoid(self) -> cq.Workplane:
        """Creates the central solenoid, its parameters
        are controlled by the SolenoidParameters class.

        Returns:
            cadquery.cq.Workplane object: The central solenoid
        """

        solenoid: cq.Workplane = cq.Workplane("YX").\
            circle(self.solenoid_parameters.solenoid_radius).\
            extrude(self.solenoid_parameters.solenoid_height).\
            translate(Vector(0, 0, self.solenoid_parameters.solenoid_height/2))
        return solenoid

    def opening(self, gap: float) -> cq.Workplane:
        """Creates a single component that is used to create an opening.
        Parameters are controlled by the PortParameters class.

        Args:
            gap (float): how much on each side will the cutter be smaller
            used when creating limiter components.

        Returns:
            cadquery.cq.Workplane object: The component.
        """

        # First the opening geometry is created.
        opening: cq.Workplane = cq.Workplane("YZ").\
            rect(self.port_parameters.y_side-gap,
                 self.port_parameters.z_side-gap)

        # Then the opening extrusion depth is calculated and
        # the port is extruded.
        extrusion_depth: float = 0.0

        for i in range(self.containment_parameters.nr_layers):
            extrusion_depth = extrusion_depth +\
                self.containment_parameters.layers[i].upper_lower_outer

        # We extrude.
        opening = opening.extrude(extrusion_depth+extrusion_depth*0.5)

        # We position it in the correct place.
        opening = opening.\
            translate(Vector((-1)*self.containment_parameters.
                             outer_radius-extrusion_depth*0.1, 0, 0))

        return opening

    def openings(self) -> cq.Workplane:
        """Creates the full array of port cutting components its parameters
        are controlled via the PortParameters class.

        Returns:
            cq.Workplane: The array of port cutting components.
        """
        # We call the opening function which gives us
        # a an opening cutter object, which we then rotate
        # into position. Gap is 0 because there is no gap.
        openings = self.opening(gap=0)

        for i in range(1, self.port_parameters.nr_ports):
            openings = openings.\
                union(self.opening(gap=0).
                      rotate((0, 0, 1), (0, 0, -1), i*360/self.port_parameters.nr_ports))

        return openings

    def create_torus(self, inner_r: float, outer_r: float, height: float) -> cq.Workplane:
        """Creates a rectangular torus.

        Args:
            inner_r (float): inner radius of the torus.
            outer_r (float): outer radius of the torus.
            height (float): the height of the torus.

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

    def containment_layer(self, layer_nr: int) -> cq.Workplane:
        """Containment layer creation function.

        Args:
            layer_nr (int): which layer to create.

        Returns:
            cq.Workplane: the layer.
        """
        # Creating a containment layer from a smaller and a bigger
        # tourus.
        inner_r: float = self.solenoid_parameters.solenoid_radius
        outer_r: float = self.containment_parameters.outer_radius
        height: float = self.containment_parameters.containment_height
        # If we are at layer 0 we use the base parameters of inner and outer radius
        # if not then we use the other ones.
        if layer_nr == 0:
            bigger_tourus: cq.Workplane = self.create_torus(
                inner_r=inner_r, outer_r=outer_r, height=height)
            smaller_torus: cq.Workplane = self.create_torus(
                inner_r=inner_r +
                self.containment_parameters.layers[layer_nr].inner,
                outer_r=outer_r -
                self.containment_parameters.layers[layer_nr].upper_lower_outer,
                height=height-self.containment_parameters.layers[layer_nr].upper_lower_outer*2)
        else:
            for i in range(layer_nr):
                inner_r = inner_r + self.containment_parameters.layers[i].inner
                outer_r = outer_r - \
                    self.containment_parameters.layers[i].upper_lower_outer
                height = height - \
                    self.containment_parameters.layers[i].upper_lower_outer*2
            bigger_tourus = self.create_torus(
                inner_r=inner_r, outer_r=outer_r, height=height)
            smaller_torus = self.create_torus(
                inner_r=inner_r +
                self.containment_parameters.layers[layer_nr].inner,
                outer_r=outer_r -
                self.containment_parameters.layers[layer_nr].upper_lower_outer,
                height=height-self.containment_parameters.layers[layer_nr].upper_lower_outer*2)
        # Here we cut the smaller torus from the bigger one, creating our containment layer.
        containment: cq.Workplane = bigger_tourus.cut(smaller_torus)

        return containment

    def containment(self) -> List[cq.Workplane]:
        """Creates the containment layer array with no port openings its parameters
        are controlled via the ContaimentParameters class.

        Returns:
            List (cq.Workplane): the containment layer list.
        """

        containment: List[cq.Workplane] = []
        for i in range(self.containment_parameters.nr_layers):
            containment.append(self.containment_layer(i))

        return containment

    def containment_with_ports(self) -> List[cq.Workplane]:
        """Creates the containment layer array with port openings its parameters
        are controlled via the ContaimentParameters class and the PortParameters
        class.

        Returns:
            List (cq.Workplane): the containment layer list.
        """
        containment: List[cq.Workplane] = []
        for i in range(self.containment_parameters.nr_layers):
            containment.append(self.containment_layer(i).cut(self.openings()))

        return containment

    def containment_with_divertor(self) -> List[cq.Workplane]:
        """Creates the containment layer array with divertor openings its parameters
        are controlled via the ContaimentParameters class and the PortParameters
        class.

        Returns:
            List (cq.Workplane): the containment layer list.
        """
        containment: List[cq.Workplane] = []
        for i in range(self.containment_parameters.nr_layers):
            containment.append(self.containment_layer(
                i).cut(self.divertor_cutter()))

        return containment

    def containment_with_divertor_and_ports(self) -> List[cq.Workplane]:
        """Creates the containment layer array with divertor and port openings its parameters
        are controlled via the ContaimentParameters class and the PortParameters
        class.

        Returns:
            List (cq.Workplane): the containment layer list.
        """
        containment: List[cq.Workplane] = []
        for i in range(self.containment_parameters.nr_layers):
            containment.append(self.containment_layer(i).
                               cut(self.openings()).cut(self.divertor_cutter()))

        return containment

    def transformer_limbs(self) -> cq.Workplane:
        """This method constructs the transformer limbs using the parameters
        defined in the LimbParameter class.

        Returns:
            cadquery.cq.Workplane: a union of transformer limbs.
        """

        # First we create a box with the correct dimensions.
        box: cq.Workplane = cq.Workplane("XY").box(
            self.limb_parameters.limb_dimensions.limb_length,
            self.limb_parameters.limb_dimensions.limb_width,
            self.limb_parameters.limb_dimensions.limb_height)

        # Then we moove the box to the correct position.
        box = box.translate(
            Vector(self.limb_parameters.limb_radius+self.containment_parameters.outer_radius, 0, 0))

        # And we construct the full limb union.
        transformer_limbs: cq.Workplane = box
        for i in range(1, self.limb_parameters.nr_limbs):
            transformer_limbs = transformer_limbs.\
                union(box.rotate((0, 0, 0), (0, 0, 1),
                      360/self.limb_parameters.nr_limbs*i))

        # Apply the 22.5 deg offset from the limbs.
        transformer_limbs = transformer_limbs.rotate(
            (0, 0, 1), (0, 0, -1), 22.5)

        return transformer_limbs

    def limiter_firstwall_openings(self):
        """Creates the full array of port cutting components
        with the gap thickness parameter.

        Returns:
            cq.Workplane: The array of port cutting components.
        """

        # Here we call the opening_member function to create a single
        # opening cutter and then rotate it via the Z axis to achieve
        # the port.
        openings = self.opening(gap=self.limiter_parameters.limiter_gap)

        for i in range(1, self.port_parameters.nr_ports):
            openings = openings.\
                union(self.opening(gap=self.limiter_parameters.limiter_gap).
                      rotate((0, 0, 1), (0, 0, -1), i*360/self.port_parameters.nr_ports))

        return openings

    def limiter_firstwall(self) -> cq.Workplane:
        """A function that creates the firstwall limiter set parameters are
        controlled via the self.limiter_parameters class.

        Returns:
            cadquery.cq.Workplane: the firstwall.
        """

        # First we calculate the position of the firstwall of the cont.
        outer_sum = 0.0
        for i in range(self.containment_parameters.nr_layers):
            outer_sum = outer_sum + \
                self.containment_parameters.layers[i].upper_lower_outer
        firstwall_torus: cq.Workplane = self.create_torus(
            inner_r=self.containment_parameters.outer_radius-outer_sum,
            outer_r=self.containment_parameters.outer_radius-outer_sum +
            self.limiter_parameters.firstwall_thickness,
            height=self.solenoid_parameters.solenoid_height)
        # Then we create the firstwall pieces and intersect them with the torus.
        firstwall = firstwall_torus.intersect(
            self.limiter_firstwall_openings())

        return firstwall

    def limiter_backwall(self) -> cq.Workplane:
        """Creates the back of the limiter from the firstwall onwards parameters are
        controlled via the LimiterParameters class.

        Returns:
            cq.Workplane: The backwall.
        """

        # First we create a box with the correct dimensions.
        outer_sum = 0.0
        for i in range(self.containment_parameters.nr_layers):
            outer_sum = outer_sum + \
                self.containment_parameters.layers[i].upper_lower_outer
        firstwall_torus: cq.Workplane = self.create_torus(
            inner_r=self.containment_parameters.outer_radius-outer_sum +
            self.limiter_parameters.firstwall_thickness,
            outer_r=self.containment_parameters.outer_radius-outer_sum +
            self.limiter_parameters.limiter_thickness +
            self.limiter_parameters.firstwall_thickness,
            height=self.solenoid_parameters.solenoid_height)
        # Then we create the firstwall pieces and intersect them with the torus.
        backwall = firstwall_torus.intersect(self.limiter_firstwall_openings())

        return backwall

    def bounding_box(self) -> cq.Workplane:
        """Creates the bounding box of the reactor parameters accessed
        form the SolenoidParameters class.

        Returns:
            cadquery.cq.Workplane: the bounding box.
        """

        bounding_box_outer = cq.Workplane("XY").\
            box(self.limb_parameters.limb_radius +
                self.containment_parameters.outer_radius * 8 +
                self.solenoid_parameters.bbox_thickness,
                self.limb_parameters.limb_radius +
                self.containment_parameters.outer_radius * 8 +
                self.solenoid_parameters.bbox_thickness,
                self.solenoid_parameters.solenoid_height * 4 +
                self.solenoid_parameters.bbox_thickness)
        bounding_box_inner = cq.Workplane("XY").\
            box(self.limb_parameters.limb_radius +
                self.containment_parameters.outer_radius * 8,
                self.limb_parameters.limb_radius +
                self.containment_parameters.outer_radius * 8,
                self.solenoid_parameters.solenoid_height * 4)

        bounding_box = bounding_box_outer.cut(bounding_box_inner)

        return bounding_box

    def sphere_pair(self) -> Tuple[cq.Workplane, cq.Workplane]:
        """Creates spheres, that represent spherical detectors,
        that are used with the limbs parameters are accessed form
        the PortParameters class.

        Args:
            index (int): the sphere to be created, 0 is the one at angle 0, etc.

        Returns:
            cadquery.cq.Workplane: the spheres.
        """

        sphere_right = cq.Workplane("XY").\
            sphere(self.limb_parameters.sphere_radius).\
            translate(
                Vector(self.limb_parameters.limb_radius +
                       self.containment_parameters.outer_radius,
                       self.limb_parameters.sphere_radius +
                       self.limb_parameters.limb_dimensions.limb_width/2))
        sphere_left = cq.Workplane("XY").\
            sphere(self.limb_parameters.sphere_radius).\
            translate(
                Vector(self.limb_parameters.limb_radius +
                       self.containment_parameters.outer_radius,
                       -self.limb_parameters.sphere_radius -
                       self.limb_parameters.limb_dimensions.limb_width/2))

        return sphere_right, sphere_left

    def sphere_pair_array(self) -> List[List[cq.Workplane]]:
        """Creates an array of sphere pairs.

        Returns:
            List[Tuple[cq.Workplane, cq.Workplane]]: the sphere pair array.
        """

        sphere_pair_array: List[List[cq.Workplane]] = []
        for i in range(self.limb_parameters.nr_limbs):
            sphere_pair_array.append([
                self.sphere_pair()[0].rotate((0, 0, 1), (0, 0, -1),
                                             i*360/self.limb_parameters.nr_limbs + 22.5),
                self.sphere_pair()[1].rotate((0, 0, 1), (0, 0, -1),
                                             i*360/self.limb_parameters.nr_limbs + 22.5)
            ])

        return sphere_pair_array

    def plasma_source(self) -> cq.Workplane:
        """Creates the plasma source parameters are located in the ContainmentParameters
        class.

        Args:
            distance_from_wall (float): distance between the plasma
            source and the first wall.

        Returns:
            cadquery.cq.Workplane: the plasma source.
        """

        inner_r: float = self.solenoid_parameters.solenoid_radius
        outer_r: float = self.containment_parameters.outer_radius
        height: float = self.containment_parameters.containment_height

        for i in range(self.containment_parameters.nr_layers):
            inner_r = inner_r + self.containment_parameters.layers[i].inner
            outer_r = outer_r - \
                self.containment_parameters.layers[i].upper_lower_outer
            height = height - \
                self.containment_parameters.layers[i].upper_lower_outer*2
        smaller_torus = self.create_torus(
            inner_r=inner_r+self.containment_parameters.layers[-1].
            inner+self.containment_parameters.distance_from_plasma,
            outer_r=outer_r-self.containment_parameters.layers[-1].
            upper_lower_outer-self.containment_parameters.distance_from_plasma,
            height=height-self.containment_parameters.layers[-1].
            upper_lower_outer*2-self.containment_parameters.distance_from_plasma*2)

        return smaller_torus

    def centering_of_divertor(self) -> Tuple[float, float]:
        """The outer and inner radius for the positioning of
        the divertor are calculated.

        Returns:
            Tuple[float, float]: the inner and outer radius.
        """

        inner_sum: float = 0.0
        outer_sum: float = 0.0
        # First we calculate the summ of all thicknesess for the inner and outer radius.
        for i in range(self.containment_parameters.nr_layers):
            inner_sum = inner_sum + self.containment_parameters.layers[i].inner
            outer_sum = outer_sum + \
                self.containment_parameters.layers[i].upper_lower_outer
        # Then we add the radius of the containment to each
        inner_sum = inner_sum + self.solenoid_parameters.solenoid_radius
        outer_sum = self.containment_parameters.outer_radius - outer_sum

        return inner_sum, outer_sum

    def divertor_cutter(self) -> cq.Workplane:
        """Creates the containment cuting component for divertor placement,
        its parameters are contained in the DivertorParameters class.

        Returns:
            cq.Workplane: The component.
        """

        inner_sum, outer_sum = self.centering_of_divertor()
        center_point = (inner_sum + outer_sum)/2
        # Now that we have the inner and outer radius we have the position of the divertor
        # and we can create a torus that cuts the containment layers.
        cutter_torus = self.create_torus(center_point-self.divertor_parameters.divertor_width,
                                         center_point+self.divertor_parameters.divertor_width,
                                         self.solenoid_parameters.solenoid_height).\
            translate(Vector(0, 0, -self.solenoid_parameters.solenoid_height/2))

        return cutter_torus

    def divertor_firstwall(self) -> cq.Workplane:
        """The firstwall of the divertor - i.e. the plasma facing component.

        Returns:
            cq.Workplane: The component.
        """

        # We start by creating a torus that is the thickness of the firstwall and
        # has the calculated inner and outer radius. This is the same as in the divertor_cutter.
        inner_sum, outer_sum = self.centering_of_divertor()
        center_point = (inner_sum + outer_sum)/2
        # Now that we have our center point, we can create the torus, that is the firstwall.
        firstwall_torus = self.create_torus(center_point-self.divertor_parameters.divertor_width +
                                            self.divertor_parameters.divertor_gap,
                                            center_point+self.divertor_parameters.divertor_width -
                                            self.divertor_parameters.divertor_gap,
                                            self.divertor_parameters.divertor_firstwall_thickness).\
            translate(Vector(0, 0,
                             -self.divertor_parameters.divertor_firstwall_thickness/2 -
                             self.containment_parameters.containment_height/2 - outer_sum +
                             self.containment_parameters.outer_radius))

        return firstwall_torus

    def divertor_backwall(self) -> cq.Workplane:
        """The backwall of the divertor - i.e. the component behind the
        plasma facing component.

        Returns:
            cq.Workplane: The component.
        """

        # We start by creating a torus that is the thickness of the backwall and
        # has the calculated inner and outer radius. This is the same as in the divertor_cutter.
        inner_sum, outer_sum = self.centering_of_divertor()
        center_point = (inner_sum + outer_sum)/2
        # Now that we have our center point, we can create the torus, that is the backwall.
        backwall_torus = self.create_torus(center_point-self.divertor_parameters.divertor_width +
                                           self.divertor_parameters.divertor_gap,
                                           center_point+self.divertor_parameters.divertor_width -
                                           self.divertor_parameters.divertor_gap,
                                           self.divertor_parameters.divertor_thickness).\
            translate(Vector(0, 0,
                             -self.divertor_parameters.divertor_thickness/2 -
                             self.divertor_parameters.divertor_firstwall_thickness -
                             self.containment_parameters.containment_height/2 - outer_sum +
                             self.containment_parameters.outer_radius))

        return backwall_torus

    def export_to_stl(self, the_solid: str,
                   max_triangle_size: float,
                   filename: str) -> None:
        # TODO: gmsh/model/occ/importShapesNativePointer for direct CQ to OCC,
        # no step conversion needed mby sorta kinda doesnt work.
        # TODO: make it so the_solid object passed can also be a cq.Workplane object
        # by checking if it is, creating a .step intermediate file and then exporting
        # it to .stl while either caching or deleting the intermediate .step file.
        """Exports a step file as an stl file.

        Args:
            the_solid (str): the step file to be exported.
            max_triangle_size (float): the maximum size of the side of a triangle.
            filename (str): the name of the file.
        """
        cpus = cpu_count()

        gmsh.initialize()
        gmsh.model.add("member")

        # Import the step file as a OCCT shape.
        gmsh.model.occ.importShapesNativePointer(the_solid)

        # Push the solid to the gmsh model.
        gmsh.model.occ.synchronize()

        # Finally, let's specify a global mesh size and mesh the partitioned model:
        #gmsh.option.setNumber("Mesh.MeshSizeMin", 3)
        gmsh.option.setNumber("Mesh.MeshSizeMax", max_triangle_size)

        # Set nr of cores to run on.
        gmsh.option.setNumber("General.NumThreads", cpus)

        # Type of meshing algorithm.
        gmsh.option.setNumber("Mesh.Algorithm", 6)
        gmsh.option.setNumber("Mesh.AngleToleranceFacetOverlap", 0.1)

        # Generate surface mesh.
        gmsh.model.mesh.generate(2)

        # Write the mesh to file.
        gmsh.write(filename)
        gmsh.finalize()
