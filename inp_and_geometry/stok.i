set title "RECTOK (trying to correct)"

% -- Surface definitions
surf 1  cyl 0 0 1000.0 -500.0 500.0 % max surface def and bbox
surf 12 cyl 0 0  995.0 -495.0 495.0 % bbox thickness

surf 2 inf % infinite boundary

% -- Cell definitions
cell 1 0 fill 1 -12 % fill inside of test area
cell 2 0 outside 1 % outside test area

cell 9 0 m21_1 -1 12

cell 3 99 void -2

% -- Solid definitions
solid 2 1 2
10 4 5 4 3 2
1 10E-5

% -- Main body definition
body solenoid solenoid m8_1
file solenoid "stls/solenoid.stl" 0.1 0 0 0

body containment1 containment1 m10_1
file containment1 "stls/containment1.stl" 0.1 0 0 0

body containment2 containment2 m12_1
file containment2 "stls/containment2.stl" 0.1 0 0 0

body containment3 containment3 m11_1
file containment3 "stls/containment3.stl" 0.1 0 0 0

body containment4 containment4 m10_2
file containment4 "stls/containment4.stl" 0.1 0 0 0

body containment5 containment5 m13_1
file containment5 "stls/containment5.stl" 0.1 0 0 0

body containment6 containment6 m6_1
file containment6 "stls/containment6.stl" 0.1 0 0 0

body containment7 containment7 void
file containment7 "stls/containment7.stl" 0.1 0 0 0

body containment8 containment8 m14_1
file containment8 "stls/containment8.stl" 0.1 0 0 0

body limb limb m8_1
file limb "stls/limb.stl" 0.1 0 0 0

solid 2 2 99
10 4 5 4 3 2
1 10E-20

% -- Spherical detectors definition
body sphere0 sphere0 void
file sphere0 "stls/sphere0.stl" 0.1 0 0 0

body sphere1 sphere1 void
file sphere1 "stls/sphere1.stl" 0.1 0 0 0

body sphere2 sphere2 void
file sphere2 "stls/sphere2.stl" 0.1 0 0 0

body sphere3 sphere3 void
file sphere3 "stls/sphere3.stl" 0.1 0 0 0

body sphere4 sphere4 void
file sphere4 "stls/sphere4.stl" 0.1 0 0 0

body sphere5 sphere5 void
file sphere5 "stls/sphere5.stl" 0.1 0 0 0

body sphere6 sphere6 void
file sphere6 "stls/sphere6.stl" 0.1 0 0 0

body sphere7 sphere7 void
file sphere7 "stls/sphere7.stl" 0.1 0 0 0

body sphere8 sphere8 void
file sphere8 "stls/sphere8.stl" 0.1 0 0 0

body sphere9 sphere9 void
file sphere9 "stls/sphere9.stl" 0.1 0 0 0

body sphere10 sphere10 void
file sphere10 "stls/sphere10.stl" 0.1 0 0 0

body sphere11 sphere11 void
file sphere11 "stls/sphere11.stl" 0.1 0 0 0

body sphere12 sphere12 void
file sphere12 "stls/sphere12.stl" 0.1 0 0 0

body sphere13 sphere13 void
file sphere13 "stls/sphere13.stl" 0.1 0 0 0

body sphere14 sphere14 void
file sphere14 "stls/sphere14.stl" 0.1 0 0 0

body sphere15 sphere15 void
file sphere15 "stls/sphere15.stl" 0.1 0 0 0

% -- Source definition
src stokplasma n 
    sp 300 0 0
    se 14.1

% -- Detector definitions
det dt1                    % Flux detector
mesh 8 -4 dt1 3 2000 2000  % Plot detector scores

det dt2 n dv 5.222E+05 dc sphere0 dc sphere1 dc sphere2 dc sphere3
          dc sphere4 dc sphere5 dc sphere6 dc sphere7
          dc sphere8 dc sphere9 dc sphere10 dc sphere11
          dc sphere12 dc sphere13 dc sphere14 dc sphere15

set nps  200000 100

% -- Material volumes
%set mcvol 100000

% -- Material definitions
include "materials.inp"
set acelib "/home/f8/xs/xsserpent/sss_jeff311u.xsdata"
