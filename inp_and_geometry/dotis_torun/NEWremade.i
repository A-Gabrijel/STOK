set title "RECTOK (trying to correct)"

% -- Surface definitions
surf 1 cyl 0 0 100000 -50000 50000 % max surface def

surf 2 inf % infinite boundary

% -- Cell definitions
cell 1 0 fill 1 -1 % fill inside of test area
cell 2 0 outside 1 % outside test area

cell 3 99 void -2

% -- Solid definitions
solid 2 1 2
10 4 5 4 3 2
1 10E-5

% -- Main body definition
body plasma plasma void
file plasma "stls/plasma.stl" 1 0 0 0

body solenoid solenoid m8_1
file solenoid "stls/solenoid.stl" 1 0 0 0

body containment1 containment1 m10_1
file containment1 "stls/containment1.stl" 1 0 0 0

body containment2 containment2 m12_1
file containment2 "stls/containment2.stl" 1 0 0 0

body containment3 containment3 m11_1
file containment3 "stls/containment3.stl" 1 0 0 0

body containment4 containment4 m10_2
file containment4 "stls/containment4.stl" 1 0 0 0

body containment5 containment5 m13_1
file containment5 "stls/containment5.stl" 1 0 0 0

body containment6 containment6 m6_1
file containment6 "stls/containment6.stl" 1 0 0 0

body containment7 containment7 void
file containment7 "stls/containment7.stl" 1 0 0 0

body containment8 containment8 m14_1
file containment8 "stls/containment8.stl" 1 0 0 0

body limb limb m8_1
file limb "stls/limb.stl" 1 0 0 0

solid 2 2 99
10 4 5 4 3 2
1 10E-20

% -- Spherical detectors definition
body sphere0 sphere0 m23_1
file sphere0 "stls/sphere0.stl" 1 0 0 0

body sphere1 sphere1 void
file sphere1 "stls/sphere1.stl" 1 0 0 0

body sphere2 sphere2 m23_1
file sphere2 "stls/sphere2.stl" 1 0 0 0

body sphere3 sphere3 m23_1
file sphere3 "stls/sphere3.stl" 1 0 0 0

body sphere4 sphere4 m23_1
file sphere4 "stls/sphere4.stl" 1 0 0 0

body sphere5 sphere5 m23_1
file sphere5 "stls/sphere5.stl" 1 0 0 0

body sphere6 sphere6 m23_1
file sphere6 "stls/sphere6.stl" 1 0 0 0

body sphere7 sphere7 m23_1
file sphere7 "stls/sphere7.stl" 1 0 0 0

body sphere8 sphere8 m23_1
file sphere8 "stls/sphere8.stl" 1 0 0 0

body sphere9 sphere9 m23_1
file sphere9 "stls/sphere9.stl" 1 0 0 0

body sphere10 sphere10 m23_1
file sphere10 "stls/sphere10.stl" 1 0 0 0

body sphere11 sphere11 m23_1
file sphere11 "stls/sphere11.stl" 1 0 0 0

body sphere12 sphere12 m23_1
file sphere12 "stls/sphere12.stl" 1 0 0 0

body sphere13 sphere13 m23_1
file sphere13 "stls/sphere13.stl" 1 0 0 0

body sphere14 sphere14 m23_1
file sphere14 "stls/sphere14.stl" 1 0 0 0

body sphere15 sphere15 m23_1
file sphere15 "stls/sphere15.stl" 1 0 0 0

% -- Source definition
src stokplasma n 
    sc plasma
    sz -1470 1470
    srad 1765 4080
    sp 0 0 0
    se 14.1

% -- Detector definitions


%det dt1 n
%    du 1
%    dx -8800 8800 850
%    dy -8800 8800 850

det F1                     % Flux detector
mesh 8 -4 F1 3 1760 1760   % Plot detector scores

det dt1 n dm m23_1 dc sphere0
det dt2 n dc sphere1
det dt3 n dc sphere2

% -- Cross section library file pat and other set thingys
set acelib "/home/f8/xs/xsserpent/sss_jeff311u.xsdata"

set nps  10000 100
set gcu -1
set lost 1000

set dt 0

% -- Material volumes
set mcvol 10000000

% -- Material definitions
include "serpentinput.inp"
