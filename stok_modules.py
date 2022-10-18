"""The STOK builder, text file search and inject functions to use when
generating STOK."""
import dataclasses
from typing import List, Tuple

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
            output: List[float] = []
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
    distance_from_plasma: float = config[-1]

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
    """Class that contains the parameters for the ports.

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
    """Class that contains the dimensions for the limbs.

    Args:
        limb_length: float
        limb_height: float
        limb_width: float
    """
    limb_length: float
    limb_width: float
    limb_height: float

class LimbParameters:
    """Class that contains the parameters for the limbs.

    Args:
        nr_limbs: int
        limb_radius: float -> at what radius the limbs are placed.
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
    """Class that contains the parameters for the limiter.

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

class DivertorParameters:
    """A class that contains the parameters for the divertor.

    Attributes:
        divertor_thickness: float
        divertor_gap: float or bool
        divertor_firstwall_thickness: float
        TODO divertor_shape: float
    """
    divertor_start: int = LimiterParameters.limiter_start+3
    divertor: List[float] = FileReader("stok_config.txt").reader()
    divertor_thickness: float = divertor[divertor_start+3]
    divertor_width: float = divertor[divertor_start+1]
    divertor_gap: float = divertor[divertor_start+2]
    divertor_firstwall_thickness: float = divertor[divertor_start]
    divertor_shape: float = divertor[divertor_start+4]

class STOK():
    """The class containing all construction components."""
    def central_solenoid(self) -> cq.Workplane:
        """Creates the central solenoid, its parameters
        are controlled by the SolenoidParameters class.

        Returns:
            cadquery.cq.Workplane object: The central solenoid
        """

        solenoid: cq.Workplane = cq.Workplane("YX").\
            circle(SolenoidParameters.solenoid_radius).\
            extrude(SolenoidParameters.solenoid_height).\
            translate(Vector(0, 0, SolenoidParameters.solenoid_height/2))
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
            rect(PortParameters.y_side-gap, PortParameters.z_side-gap)

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
        """Creates the full array of port cutting components its parameters
        are controlled via the PortParameters class.

        Returns:
            cq.Workplane: The array of port cutting components.
        """
        # We call the opening function which gives us
        # a an opening cutter object, which we then rotate
        # into position. Gap is 0 because there is no gap.
        openings = self.opening(gap=0)

        for i in range(1, PortParameters.nr_ports):
            openings = openings.union(self.opening(gap=0).\
                rotate((0, 0, 1),(0, 0, -1), i*360/PortParameters.nr_ports))

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
        inner_r: float = SolenoidParameters.solenoid_radius
        outer_r: float = ContainmentParameters.outer_radius
        height: float = ContainmentParameters.containment_height
        # If we are at layer 0 we use the base parameters of inner and outer radius
        # if not then we use the other ones.
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
        for i in range(ContainmentParameters.nr_layers):
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
        for i in range(ContainmentParameters.nr_layers):
            containment.append(self.containment_layer(i).cut(self.openings()))

        return containment

    def transformer_limbs(self):
        """This method constructs the transformer limbs using the parameters
        defined in the LimbParameter class.

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
    def limiter_firstwall_openings(self):
        """Creates the full array of port cutting components
        with the gap thickness parameter.

        Returns:
            cq.Workplane: The array of port cutting components.
        """

        # Here we call the opening_member function to create a single
        # opening cutter and then rotate it via the Z axis to achieve
        # the port.
        openings = self.opening(gap=LimiterParameters.limiter_gap)

        for i in range(1, PortParameters.nr_ports):
            openings = openings.union(self.opening(gap=LimiterParameters.limiter_gap).\
                rotate((0, 0, 1),(0, 0, -1), i*360/PortParameters.nr_ports))

        return openings

    def limiter_firstwall(self) -> cq.Workplane:
        """A function that creates the firstwall limiter set parameters are
        controlled via the LimiterParameters class.

        Returns:
            cadquery.cq.Workplane: the firstwall.
        """

        # First we calculate the position of the firstwall of the cont.
        outer_sum = 0.0
        for i in range(ContainmentParameters.nr_layers):
            outer_sum = outer_sum + ContainmentParameters.layers[i].upper_lower_outer
        firstwall_torus: cq.Workplane = self.create_torus(
            inner_r=ContainmentParameters.outer_radius-outer_sum,
            outer_r=ContainmentParameters.outer_radius-outer_sum+\
                LimiterParameters.firstwall_thickness,
            height=SolenoidParameters.solenoid_height)
        # Then we create the firstwall pieces and intersect them with the torus.
        firstwall = firstwall_torus.intersect(self.limiter_firstwall_openings())

        return firstwall

    def limiter_backwall(self) -> cq.Workplane:
        """Creates the back of the limiter from the firstwall onwards parameters are
        controlled via the LimiterParameters class.

        Returns:
            cq.Workplane: The backwall.
        """

        # First we create a box with the correct dimensions.
        outer_sum = 0.0
        for i in range(ContainmentParameters.nr_layers):
            outer_sum = outer_sum + ContainmentParameters.layers[i].upper_lower_outer
        firstwall_torus: cq.Workplane = self.create_torus(
            inner_r=ContainmentParameters.outer_radius-outer_sum+\
                LimiterParameters.firstwall_thickness,
            outer_r=ContainmentParameters.outer_radius-outer_sum+\
                LimiterParameters.limiter_thickness+LimiterParameters.firstwall_thickness,
            height=SolenoidParameters.solenoid_height)
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
            box(LimbParameters.limb_radius +
                ContainmentParameters.outer_radius * 8 +
                SolenoidParameters.bbox_thickness,
                LimbParameters.limb_radius +
                ContainmentParameters.outer_radius * 8 +
                SolenoidParameters.bbox_thickness,
                SolenoidParameters.solenoid_height * 4 +
                SolenoidParameters.bbox_thickness)
        bounding_box_inner = cq.Workplane("XY").\
            box(LimbParameters.limb_radius +
                ContainmentParameters.outer_radius * 8,
                LimbParameters.limb_radius +
                ContainmentParameters.outer_radius * 8,
                SolenoidParameters.solenoid_height * 4)

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
            sphere(LimbParameters.sphere_radius).\
            translate(
                Vector(LimbParameters.limb_radius, LimbParameters.sphere_radius +
                       LimbParameters.limb_dimensions.limb_width/2))
        sphere_left = cq.Workplane("XY").\
            sphere(LimbParameters.sphere_radius).\
            translate(
                Vector(LimbParameters.limb_radius, -LimbParameters.sphere_radius -
                       LimbParameters.limb_dimensions.limb_width/2))

        return sphere_right, sphere_left

    def sphere_pair_array(self) -> List[List[cq.Workplane]]:
        """Creates an array of sphere pairs.

        Returns:
            List[Tuple[cq.Workplane, cq.Workplane]]: the sphere pair array.
        """

        sphere_pair_array: List[List[cq.Workplane]] = []
        for i in range(LimbParameters.nr_limbs):
            sphere_pair_array.append([
                self.sphere_pair()[0].rotate((0,0,1),(0,0,-1),i*360/LimbParameters.nr_limbs),
                self.sphere_pair()[1].rotate((0,0,1),(0,0,-1),i*360/LimbParameters.nr_limbs)
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

        inner_r: float = SolenoidParameters.solenoid_radius
        outer_r: float = ContainmentParameters.outer_radius
        height: float = ContainmentParameters.containment_height

        for i in range(ContainmentParameters.nr_layers):
            inner_r = inner_r + ContainmentParameters.layers[i].inner
            outer_r = outer_r - ContainmentParameters.layers[i].upper_lower_outer
            height = height - ContainmentParameters.layers[i].upper_lower_outer*2
        smaller_torus = self.create_torus(
            inner_r=inner_r+ContainmentParameters.layers[-1].\
                inner+ContainmentParameters.distance_from_plasma,
            outer_r=outer_r-ContainmentParameters.layers[-1].\
                upper_lower_outer-ContainmentParameters.distance_from_plasma,
            height=height-ContainmentParameters.layers[-1].\
                upper_lower_outer*2-ContainmentParameters.distance_from_plasma*2)

        return smaller_torus

    def divertor_cutter(self) -> cq.Workplane:
        """Creates the divertor component its parameters are contained in the DivertorParameters
        class.

        Returns:
            cq.Workplane: The component.
        """

        inner_sum: float = 0.0
        outer_sum: float = 0.0
        # First we calculate the summ of all thicknesess for the inner and outer radius.
        for i in range(ContainmentParameters.nr_layers):
            inner_sum = inner_sum + ContainmentParameters.layers[i].inner
            outer_sum = outer_sum + ContainmentParameters.layers[i].upper_lower_outer
        # Then we add the radius of the containment to each
        inner_sum = inner_sum + SolenoidParameters.solenoid_radius
        outer_sum = outer_sum + ContainmentParameters.outer_radius
        center_point = (inner_sum + outer_sum)/2
        # Now that we have the inner and outer radius we have the position of the divertor
        # and we can create a torus that cuts the containment layers.
        cutter_torus = self.create_torus(center_point-DivertorParameters.divertor_thickness/2,
                                         center_point+DivertorParameters.divertor_thickness/2,
                                         SolenoidParameters.solenoid_height).\
                       translate(Vector(0,0,-SolenoidParameters.solenoid_height/2))

        return cutter_torus
    
    def divertor(self):
        # TODO: finish this.
        pass
