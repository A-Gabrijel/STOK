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
    solenoid_radius: float = FileReader("stok_config.txt").read[ContainmentParameters.nr_layers*2+3]
    solenoid_height: float = FileReader("stok_config.txt").read[ContainmentParameters.nr_layers*2+4]
    bbox_thickness: float = FileReader("stok_config.txt").read[ContainmentParameters.nr_layers*2+5]

@dataclass(order=True, frozen=True)
class PortParameters:
    """Class that contains the parameters for the ports.

    Args:
        nr_ports: int
        z_side: float
        y_side: float
    """
    nr_ports: int = int(FileReader("stok_config.txt").read[ContainmentParameters.nr_layers*2+6])
    z_side: float = FileReader("stok_config.txt").read[ContainmentParameters.nr_layers*2+7]
    y_side: float = FileReader("stok_config.txt").read[ContainmentParameters.nr_layers*2+8]

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
    nr_limbs: int = int(FileReader("stok_config.txt").read[ContainmentParameters.nr_layers*2+9])
    limb_radius: float = ContainmentParameters.outer_radius + \
        FileReader("stok_config.txt").read[ContainmentParameters.nr_layers*2+10]
    sphere_radius: float = FileReader("stok_config.txt").read[ContainmentParameters.nr_layers*2+11]
    limb_dimensions: LimbDimensiones = LimbDimensiones(
        FileReader("stok_config.txt").read[ContainmentParameters.nr_layers*2+12],
        FileReader("stok_config.txt").read[ContainmentParameters.nr_layers*2+13],
        FileReader("stok_config.txt").read[ContainmentParameters.nr_layers*2+14]
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
    limiter_gap: float = FileReader("stok_config.txt").read[ContainmentParameters.nr_layers*2+16]
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
    divertor_thickness: float = FileReader("stok_config.txt").\
        read[ContainmentParameters.nr_layers*2+18]
    divertor_width: float = FileReader("stok_config.txt").read[ContainmentParameters.nr_layers*2+19]
    divertor_gap: float = FileReader("stok_config.txt").read[ContainmentParameters.nr_layers*2+20]
    divertor_firstwall_thickness: float = FileReader("stok_config.txt").\
        read[ContainmentParameters.nr_layers*2+21]
    divertor_shape: float = FileReader("stok_config.txt").read[ContainmentParameters.nr_layers*2+22]

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
            translate(Vector((-1)*ContainmentParameters.outer_radius-extrusion_depth*0.1, 0, 0))

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

    def transformer_limbs(self) -> cq.Workplane:
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
                Vector(LimbParameters.limb_radius +
                       ContainmentParameters.outer_radius, LimbParameters.sphere_radius +
                       LimbParameters.limb_dimensions.limb_width/2))
        sphere_left = cq.Workplane("XY").\
            sphere(LimbParameters.sphere_radius).\
            translate(
                Vector(LimbParameters.limb_radius +
                       ContainmentParameters.outer_radius, -LimbParameters.sphere_radius -
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
                self.sphere_pair()[0].rotate((0,0,1),(0,0,-1),i*360/LimbParameters.nr_limbs + 22.5),
                self.sphere_pair()[1].rotate((0,0,1),(0,0,-1),i*360/LimbParameters.nr_limbs + 22.5)
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

    def divertor_firstwall(self):
        # TODO: finish this function.
        """The firstwall of the divertor - i.e. the plasma facing component.

        Returns:
            cq.Workplane: The component.
        """

        return 0

    def divertor_backwall(self):
        # TODO: finish this function.
        pass

    def export_stl(self, the_solid: str,
                   max_triangle_size: float,
                   filename: str) -> None:
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
        gmsh.model.occ.importShapes(the_solid)

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
