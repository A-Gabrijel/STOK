import build as reactor
import math as m
import os
import time
import shutil
import cadquery as cq

line_start = 28
det_line_start = 68

# serpent file to inject geometry into
doti_file = "inp_and_geometry/NEW.i"
write_to = "inp_and_geometry/dotis_torun/NEWremade.i"

# get syspath for geometry dir creation if not already created
syspath = os.getcwd()
directorySTEP = "inp_and_geometry/steps"
directorySTL = "inp_and_geometry/stls"
pathSTEP = os.path.join(syspath,directorySTEP)
pathSTL = os.path.join(syspath,directorySTL)

inject = reactor.GeometryInjector(file=doti_file, line_nr=line_start, newfile_location=write_to)

# try creating step and stl folder if it's already made, clears them.
try:
    os.mkdir(pathSTEP)
except FileExistsError:
    shutil.rmtree(pathSTEP)
    os.mkdir(pathSTEP)
"""
try:
    os.mkdir(pathSTL)
except FileExistsError:
    shutil.rmtree(pathSTL)
    os.mkdir(pathSTL)
"""

#    Creation of rectok components
# ------------------------------------------------------------------------------
# -- Bounding box --
bbox_name = "bbox"
cyl1 = cq.Workplane().circle(100000).extrude(100000).translate(cq.Vector(0,0,-50000))
cyl2 = cq.Workplane().circle(90000).extrude(90000).translate(cq.Vector(0,0,-90000/2))
cyl1 = cyl1.cut(cyl2)
cq.exporters.export(cyl1, "inp_and_geometry/steps/{}.step".format(bbox_name))

    # code injection
inject.Body(body_name=bbox_name, material="m21_1")
inject.File(filepath="stls/{}.stl".format(bbox_name),
            object_name=bbox_name, scale=1, last="yes")
# ------------------------------------------------------------------------------
# -- Plasma --
plasma = reactor.rectok().PlasmaSrc(distance_from_wall = 50.0)
cq.exporters.export(plasma, "inp_and_geometry/steps/plasma.step")

    # code injection
inject.Body(body_name="plasma", material="void")
inject.File(filepath="stls/plasma.stl", object_name="plasma", scale=1, last=1)
# ------------------------------------------------------------------------------
# -- Solenoid --
solenoid_name = "solenoid"
solenoid = reactor.rectok().CentralSolenoid()
cq.exporters.export(solenoid, "inp_and_geometry/steps/{}.step".format(solenoid_name))

    # code injection
inject.Body(body_name=solenoid_name, material="m8_1")
inject.File(filepath="stls/{}.stl".format(solenoid_name),
            object_name=solenoid_name, scale=1, last="yes")
# ------------------------------------------------------------------------------
# -- Openings --
openings = cq.Workplane("XY")
for openings_index in range(reactor.rectok().nr_ports):
    openings = openings.union(reactor.rectok().Openings(index = openings_index))
# ------------------------------------------------------------------------------
# -- Containment --
containment_mat = ("m10_1", "m12_1", "m11_1", "m10_2", "m13_1", "m6_1", "void", "m14_1")
containment_piece = 0
for cont_index in range(reactor.rectok().nr_layers):
    containment_name = "containment{}".format(cont_index + 1)
    containment_piece = reactor.rectok().ContConstrFunct(index = cont_index).cut(openings)
    cq.exporters.export(containment_piece, "inp_and_geometry/steps/{}.step".format(containment_name))

    # code injection
    inject.Body(body_name=containment_name, material=containment_mat[cont_index])
    inject.File(filepath="stls/{}.stl".format(containment_name),
                object_name=containment_name, scale=1, last=1)
# ------------------------------------------------------------------------------
# -- limbs --
# since limbs are all the same material we can combine them into a single body
limb_name = "limb"
sphere_name = "sphere"
inject.Body(body_name=limb_name, material="m8_1")
inject.File(filepath="stls/limb.stl", object_name=limb_name, scale=1, last=1)
limbs = reactor.rectok().TransLimb(index = 0)[0]
limb_index = 1
for limb_index in range(reactor.rectok().nr_limbs):
    limbs = limbs.union(reactor.rectok().TransLimb(index = limb_index)[0])
cq.exporters.export(limbs, "inp_and_geometry/steps/limb.step")
# ------------------------------------------------------------------------------
# -- Spherical detectors --
inject_detectors = reactor.GeometryInjector(file=doti_file, line_nr=det_line_start, newfile_location=write_to)
for sphere_index in range(reactor.rectok().nr_limbs):
    sphere_right = reactor.rectok().TransLimb(index = sphere_index)[1]
    cq.exporters.export(sphere_right, "inp_and_geometry/steps/sphere{}.step".format(sphere_index*2))

    # code injection
    inject_detectors.Body(body_name="sphere{}".format(sphere_index*2), material="void")
    inject_detectors.File(filepath="stls/sphere{}.stl".format(sphere_index*2), object_name="sphere{}".format(sphere_index*2), scale=1, last=0)
    # ---
    sphere_left = reactor.rectok().TransLimb(index = sphere_index)[2]
    cq.exporters.export(sphere_left, "inp_and_geometry/steps/sphere{}.step".format(sphere_index*2+1))

    # code injection
    inject_detectors.Body(body_name="sphere{}".format(sphere_index*2+1), material="void")
    inject_detectors.File(filepath="stls/sphere{}.stl".format(sphere_index*2+1), object_name="sphere{}".format(sphere_index*2+1), scale=1, last=0)
# ------------------------------------------------------------------------------
