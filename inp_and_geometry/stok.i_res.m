
% Increase counter:

if (exist('idx', 'var'));
  idx = idx + 1;
else;
  idx = 1;
end;

% Version, title and date:

VERSION                   (idx, [1: 14])  = 'Serpent 2.1.32' ;
COMPILE_DATE              (idx, [1: 20])  = 'Dec 20 2021 18:51:07' ;
DEBUG                     (idx, 1)        = 0 ;
TITLE                     (idx, [1: 26])  = 'RECTOK (trying to correct)' ;
CONFIDENTIAL_DATA         (idx, 1)        = 0 ;
INPUT_FILE_NAME           (idx, [1:  6])  = 'stok.i' ;
WORKING_DIRECTORY         (idx, [1: 49])  = '/home/serpent/Desktop/STOKv0.32b/inp_and_geometry' ;
HOSTNAME                  (idx, [1:  2])  = 'vb' ;
CPU_TYPE                  (idx, [1: 41])  = 'Intel(R) Core(TM) i5-10210U CPU @ 1.60GHz' ;
CPU_MHZ                   (idx, 1)        = 2112.0 ;
START_DATE                (idx, [1: 24])  = 'Mon Jul 18 16:27:04 2022' ;
COMPLETE_DATE             (idx, [1: 24])  = 'Mon Jul 18 16:32:04 2022' ;

% Run parameters:

POP                       (idx, 1)        = 2000 ;
BATCHES                   (idx, 1)        = 100 ;
SRC_NORM_MODE             (idx, 1)        = 2 ;
SEED                      (idx, 1)        = 1658154424625 ;
UFS_MODE                  (idx, 1)        = 0 ;
UFS_ORDER                 (idx, 1)        = 1.00000;
NEUTRON_TRANSPORT_MODE    (idx, 1)        = 1 ;
PHOTON_TRANSPORT_MODE     (idx, 1)        = 0 ;
GROUP_CONSTANT_GENERATION (idx, 1)        = 1 ;
B1_CALCULATION            (idx, [1:  3])  = [ 0 0 0 ];
B1_BURNUP_CORRECTION      (idx, 1)        = 0 ;

CRIT_SPEC_MODE            (idx, 1)        = 0 ;
IMPLICIT_REACTION_RATES   (idx, 1)        = 1 ;

% Optimization:

OPTIMIZATION_MODE         (idx, 1)        = 4 ;
RECONSTRUCT_MICROXS       (idx, 1)        = 1 ;
RECONSTRUCT_MACROXS       (idx, 1)        = 1 ;
DOUBLE_INDEXING           (idx, 1)        = 0 ;
MG_MAJORANT_MODE          (idx, 1)        = 0 ;

% Parallelization:

MPI_TASKS                 (idx, 1)        = 1 ;
OMP_THREADS               (idx, 1)        = 4 ;
MPI_REPRODUCIBILITY       (idx, 1)        = 0 ;
OMP_REPRODUCIBILITY       (idx, 1)        = 1 ;
OMP_HISTORY_PROFILE       (idx, [1:   4]) = [  9.99380E-01  9.92380E-01  1.00330E+00  1.00494E+00  ];
SHARE_BUF_ARRAY           (idx, 1)        = 0 ;
SHARE_RES2_ARRAY          (idx, 1)        = 1 ;
OMP_SHARED_QUEUE_LIM      (idx, 1)        = 0 ;

% File paths:

XS_DATA_FILE_PATH         (idx, [1: 41])  = '/home/f8/xs/xsserpent/sss_jeff311u.xsdata' ;
DECAY_DATA_FILE_PATH      (idx, [1:  3])  = 'N/A' ;
SFY_DATA_FILE_PATH        (idx, [1:  3])  = 'N/A' ;
NFY_DATA_FILE_PATH        (idx, [1:  3])  = 'N/A' ;
BRA_DATA_FILE_PATH        (idx, [1:  3])  = 'N/A' ;

% Collision and reaction sampling (neutrons/photons):

MEAN_SRC_WGT              (idx, [1:   4]) = [  1.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
SOURCE_SAMPLING_EFF       (idx, [1:   4]) = [  1.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
MIN_MACROXS               (idx, [1:   4]) = [  5.00000E-02 0.0E+00  0.00000E+00 0.0E+00 ];
DT_THRESH                 (idx, [1:  2])  = [  9.00000E-01  9.00000E-01 ];
ST_FRAC                   (idx, [1:   4]) = [  4.07242E-01 0.00123  0.00000E+00 0.0E+00 ];
DT_FRAC                   (idx, [1:   4]) = [  5.92758E-01 0.00084  0.00000E+00 0.0E+00 ];
DT_EFF                    (idx, [1:   4]) = [  4.38396E-01 0.00084  0.00000E+00 0.0E+00 ];
REA_SAMPLING_EFF          (idx, [1:   4]) = [  1.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
REA_SAMPLING_FAIL         (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
TOT_COL_EFF               (idx, [1:   4]) = [  3.35913E-01 0.00120  0.00000E+00 0.0E+00 ];
AVG_TRACKING_LOOPS        (idx, [1:   8]) = [  7.66329E+00 0.00409  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
AVG_TRACKS                (idx, [1:   4]) = [  1.04845E+02 0.00178  0.00000E+00 0.0E+00 ];
AVG_REAL_COL              (idx, [1:   4]) = [  1.04808E+02 0.00178  0.00000E+00 0.0E+00 ];
AVG_VIRT_COL              (idx, [1:   4]) = [  2.07212E+02 0.00177  0.00000E+00 0.0E+00 ];
AVG_SURF_CROSS            (idx, [1:   4]) = [  6.07743E+01 0.00269  0.00000E+00 0.0E+00 ];
LOST_PARTICLES            (idx, 1)        = 0 ;

% STL geometries:

STL_RAY_TEST              (idx, [1:  10]) = [  5.31143E-03 0.00408  3.34375E-04 0.01611  1.10488E-07 0.62214  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
STL_ENFORCE_ST            (idx, 1)        = 0 ;

% Run statistics:

CYCLE_IDX                 (idx, 1)        = 100 ;
SIMULATED_HISTORIES       (idx, 1)        = 2000 ;
SIMULATION_COMPLETED      (idx, 1)        = 1 ;

% Running times:

TOT_CPU_TIME              (idx, 1)        =  1.91239E+01 ;
RUNNING_TIME              (idx, 1)        =  4.99780E+00 ;
INIT_TIME                 (idx, [1:  2])  = [  2.20950E-01  2.20950E-01 ];
PROCESS_TIME              (idx, [1:  2])  = [  3.60000E-03  3.60000E-03 ];
TRANSPORT_CYCLE_TIME      (idx, [1:  3])  = [  4.77325E+00  4.77325E+00  0.00000E+00 ];
MPI_OVERHEAD_TIME         (idx, [1:  2])  = [  0.00000E+00  0.00000E+00 ];
ESTIMATED_RUNNING_TIME    (idx, [1:  2])  = [  4.99460E+00  0.00000E+00 ];
CPU_USAGE                 (idx, 1)        = 3.82646 ;
TRANSPORT_CPU_USAGE       (idx, [1:   2]) = [  3.96167E+00 0.00185 ];
OMP_PARALLEL_FRAC         (idx, 1)        =  9.54560E-01 ;

% Memory usage:

AVAIL_MEM                 (idx, 1)        = 5057.06 ;
ALLOC_MEMSIZE             (idx, 1)        = 1242.40;
MEMSIZE                   (idx, 1)        = 1162.44;
XS_MEMSIZE                (idx, 1)        = 614.04;
MAT_MEMSIZE               (idx, 1)        = 57.47;
RES_MEMSIZE               (idx, 1)        = 31.44;
IFC_MEMSIZE               (idx, 1)        = 0.00;
MISC_MEMSIZE              (idx, 1)        = 122.28;
UNKNOWN_MEMSIZE           (idx, 1)        = 337.20;
UNUSED_MEMSIZE            (idx, 1)        = 79.96;

% Geometry parameters:

TOT_CELLS                 (idx, 1)        = 4 ;
UNION_CELLS               (idx, 1)        = 0 ;

% Neutron energy grid:

NEUTRON_ERG_TOL           (idx, 1)        =  0.00000E+00 ;
NEUTRON_ERG_NE            (idx, 1)        = 197557 ;
NEUTRON_EMIN              (idx, 1)        =  1.00000E-11 ;
NEUTRON_EMAX              (idx, 1)        =  2.00000E+01 ;

% Unresolved resonance probability table sampling:

URES_DILU_CUT             (idx, 1)        =  1.00000E-09 ;
URES_EMIN                 (idx, 1)        =  1.00000E+37 ;
URES_EMAX                 (idx, 1)        = -1.00000E+37 ;
URES_AVAIL                (idx, 1)        = 2 ;
URES_USED                 (idx, 1)        = 0 ;

% Nuclides and reaction channels:

TOT_NUCLIDES              (idx, 1)        = 44 ;
TOT_TRANSPORT_NUCLIDES    (idx, 1)        = 44 ;
TOT_DOSIMETRY_NUCLIDES    (idx, 1)        = 0 ;
TOT_DECAY_NUCLIDES        (idx, 1)        = 0 ;
TOT_PHOTON_NUCLIDES       (idx, 1)        = 0 ;
TOT_REA_CHANNELS          (idx, 1)        = 1293 ;
TOT_TRANSMU_REA           (idx, 1)        = 0 ;

% Neutron physics options:

USE_DELNU                 (idx, 1)        = 0 ;
USE_URES                  (idx, 1)        = 0 ;
USE_DBRC                  (idx, 1)        = 0 ;
IMPL_CAPT                 (idx, 1)        = 0 ;
IMPL_NXN                  (idx, 1)        = 1 ;
IMPL_FISS                 (idx, 1)        = 0 ;
DOPPLER_PREPROCESSOR      (idx, 1)        = 0 ;
TMS_MODE                  (idx, 1)        = 0 ;
SAMPLE_FISS               (idx, 1)        = 1 ;
SAMPLE_CAPT               (idx, 1)        = 1 ;
SAMPLE_SCATT              (idx, 1)        = 1 ;

% Energy deposition:

EDEP_MODE                 (idx, 1)        = 0 ;
EDEP_DELAYED              (idx, 1)        = 1 ;
EDEP_KEFF_CORR            (idx, 1)        = 1 ;
EDEP_LOCAL_EGD            (idx, 1)        = 0 ;
EDEP_COMP                 (idx, [1:  9])  = [ 0 0 0 0 0 0 0 0 0 ];
EDEP_CAPT_E               (idx, 1)        =  0.00000E+00 ;

% Radioactivity data:

TOT_ACTIVITY              (idx, 1)        =  0.00000E+00 ;
TOT_DECAY_HEAT            (idx, 1)        =  0.00000E+00 ;
TOT_SF_RATE               (idx, 1)        =  0.00000E+00 ;
ACTINIDE_ACTIVITY         (idx, 1)        =  0.00000E+00 ;
ACTINIDE_DECAY_HEAT       (idx, 1)        =  0.00000E+00 ;
FISSION_PRODUCT_ACTIVITY  (idx, 1)        =  0.00000E+00 ;
FISSION_PRODUCT_DECAY_HEAT(idx, 1)        =  0.00000E+00 ;
INHALATION_TOXICITY       (idx, 1)        =  0.00000E+00 ;
INGESTION_TOXICITY        (idx, 1)        =  0.00000E+00 ;
ACTINIDE_INH_TOX          (idx, 1)        =  0.00000E+00 ;
ACTINIDE_ING_TOX          (idx, 1)        =  0.00000E+00 ;
FISSION_PRODUCT_INH_TOX   (idx, 1)        =  0.00000E+00 ;
FISSION_PRODUCT_ING_TOX   (idx, 1)        =  0.00000E+00 ;
SR90_ACTIVITY             (idx, 1)        =  0.00000E+00 ;
TE132_ACTIVITY            (idx, 1)        =  0.00000E+00 ;
I131_ACTIVITY             (idx, 1)        =  0.00000E+00 ;
I132_ACTIVITY             (idx, 1)        =  0.00000E+00 ;
CS134_ACTIVITY            (idx, 1)        =  0.00000E+00 ;
CS137_ACTIVITY            (idx, 1)        =  0.00000E+00 ;
PHOTON_DECAY_SOURCE       (idx, 1)        =  0.00000E+00 ;
NEUTRON_DECAY_SOURCE      (idx, 1)        =  0.00000E+00 ;
ALPHA_DECAY_SOURCE        (idx, 1)        =  0.00000E+00 ;
ELECTRON_DECAY_SOURCE     (idx, 1)        =  0.00000E+00 ;

% Normalization coefficient:

NORM_COEF                 (idx, [1:   4]) = [  4.57689E-04 0.00219  0.00000E+00 0.0E+00 ];

% Analog reaction rate estimators:

CONVERSION_RATIO          (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];

% Neutron balance (particles/weight):

BALA_SRC_NEUTRON_SRC     (idx, [1:  2])  = [ 200000 2.00000E+05 ];
BALA_SRC_NEUTRON_FISS    (idx, [1:  2])  = [ 0 0.00000E+00 ];
BALA_SRC_NEUTRON_NXN     (idx, [1:  2])  = [ 0 1.88950E+04 ];
BALA_SRC_NEUTRON_VR      (idx, [1:  2])  = [ 0 0.00000E+00 ];
BALA_SRC_NEUTRON_TOT     (idx, [1:  2])  = [ 200000 2.18895E+05 ];

BALA_LOSS_NEUTRON_CAPT    (idx, [1:  2])  = [ 192707 2.10838E+05 ];
BALA_LOSS_NEUTRON_FISS    (idx, [1:  2])  = [ 0 0.00000E+00 ];
BALA_LOSS_NEUTRON_LEAK    (idx, [1:  2])  = [ 7293 8.05700E+03 ];
BALA_LOSS_NEUTRON_CUT     (idx, [1:  2])  = [ 0 0.00000E+00 ];
BALA_LOSS_NEUTRON_ERR     (idx, [1:  2])  = [ 0 0.00000E+00 ];
BALA_LOSS_NEUTRON_TOT     (idx, [1:  2])  = [ 200000 2.18895E+05 ];

BALA_NEUTRON_DIFF         (idx, [1:  2])  = [ 0 0.00000E+00 ];

% Normalized total reaction rates (neutrons):

TOT_POWER                 (idx, [1:   2]) = [  1.96811E-20 0.03248 ];
TOT_POWDENS               (idx, [1:   2]) = [  5.68864E-26 0.03248 ];
TOT_GENRATE               (idx, [1:   2]) = [  1.93262E-09 0.03276 ];
TOT_FISSRATE              (idx, [1:   2]) = [  6.17760E-10 0.03248 ];
TOT_CAPTRATE              (idx, [1:   2]) = [  9.63145E-01 0.00048 ];
TOT_ABSRATE               (idx, [1:   2]) = [  9.63145E-01 0.00048 ];
TOT_SRCRATE               (idx, [1:   2]) = [  9.15377E-01 0.00219 ];
TOT_FLUX                  (idx, [1:   2]) = [  1.25801E+03 0.00299 ];
TOT_PHOTON_PRODRATE       (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
TOT_LEAKRATE              (idx, [1:   2]) = [  3.68547E-02 0.01244 ];
ALBEDO_LEAKRATE           (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
TOT_LOSSRATE              (idx, [1:   2]) = [  1.00000E+00 0.0E+00 ];
TOT_CUTRATE               (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
TOT_RR                    (idx, [1:   2]) = [  1.08353E+02 0.00151 ];
INI_FMASS                 (idx, 1)        =  3.45972E-01 ;
TOT_FMASS                 (idx, 1)        =  3.45972E-01 ;

% Six-factor formula:

SIX_FF_ETA                (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
SIX_FF_F                  (idx, [1:   2]) = [  1.10448E-02 0.08441 ];
SIX_FF_P                  (idx, [1:   2]) = [  8.39054E-02 0.00765 ];
SIX_FF_EPSILON            (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
SIX_FF_LF                 (idx, [1:   2]) = [  9.62060E-01 0.00051 ];
SIX_FF_LT                 (idx, [1:   2]) = [  9.97562E-01 0.00012 ];
SIX_FF_KINF               (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
SIX_FF_KEFF               (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];

% Fission neutron and energy production:

NUBAR                     (idx, [1:   2]) = [  3.12567E+00 0.00306 ];
FISSE                     (idx, [1:   2]) = [  1.98847E+02 0.0E+00 ];

% Criticality eigenvalues:

ANA_KEFF                  (idx, [1:   6]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
IMP_KEFF                  (idx, [1:   2]) = [  2.11524E-09 0.03279 ];
COL_KEFF                  (idx, [1:   2]) = [  2.11320E-09 0.03294 ];
ABS_KEFF                  (idx, [1:   2]) = [  2.11524E-09 0.03279 ];
ABS_KINF                  (idx, [1:   2]) = [  2.20527E-09 0.03294 ];
ANA_EXT_K                 (idx, [1:  20]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
SRC_MULT                  (idx, [1:   2]) = [  1.00000E+00 0.0E+00 ];
MEAN_NGEN                 (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
PROMPT_CHAIN_LENGTH       (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
GEOM_ALBEDO               (idx, [1:   6]) = [  1.00000E+00 0.0E+00  1.00000E+00 0.0E+00  1.00000E+00 0.0E+00 ];

% ALF (Average lethargy of neutrons causing fission):
% Based on E0 = 2.000000E+01 MeV

ANA_ALF                   (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
IMP_ALF                   (idx, [1:   2]) = [  8.16651E-01 0.01987 ];

% EALF (Energy corresponding to average lethargy of neutrons causing fission):

ANA_EALF                  (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
IMP_EALF                  (idx, [1:   2]) = [  8.94698E+00 0.01491 ];

% AFGE (Average energy of neutrons causing fission):

ANA_AFGE                  (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
IMP_AFGE                  (idx, [1:   2]) = [  1.11567E+01 0.00857 ];

% Forward-weighted delayed neutron parameters:

PRECURSOR_GROUPS          (idx, 1)        = 0 ;
FWD_ANA_BETA_ZERO         (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
FWD_ANA_LAMBDA            (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];

% Beta-eff using Meulekamp's method:

ADJ_MEULEKAMP_BETA_EFF    (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
ADJ_MEULEKAMP_LAMBDA      (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];

% Adjoint weighted time constants using Nauchi's method:

IFP_CHAIN_LENGTH          (idx, 1)        = 15 ;
ADJ_NAUCHI_GEN_TIME       (idx, [1:   6]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
ADJ_NAUCHI_LIFETIME       (idx, [1:   6]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
ADJ_NAUCHI_BETA_EFF       (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
ADJ_NAUCHI_LAMBDA         (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];

% Adjoint weighted time constants using IFP:

ADJ_IFP_GEN_TIME          (idx, [1:   6]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
ADJ_IFP_LIFETIME          (idx, [1:   6]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
ADJ_IFP_IMP_BETA_EFF      (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
ADJ_IFP_IMP_LAMBDA        (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
ADJ_IFP_ANA_BETA_EFF      (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
ADJ_IFP_ANA_LAMBDA        (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
ADJ_IFP_ROSSI_ALPHA       (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];

% Adjoint weighted time constants using perturbation technique:

ADJ_PERT_GEN_TIME         (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
ADJ_PERT_LIFETIME         (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
ADJ_PERT_BETA_EFF         (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
ADJ_PERT_ROSSI_ALPHA      (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];

% Inverse neutron speed :

ANA_INV_SPD               (idx, [1:   2]) = [  9.68051E-08 0.00891 ];

% Analog slowing-down and thermal neutron lifetime (total/prompt/delayed):

ANA_SLOW_TIME             (idx, [1:   6]) = [  3.65264E-04 0.00645  3.65264E-04 0.00645  0.00000E+00 0.0E+00 ];
ANA_THERM_TIME            (idx, [1:   6]) = [  7.76432E-04 0.01240  7.76432E-04 0.01240  0.00000E+00 0.0E+00 ];
ANA_THERM_FRAC            (idx, [1:   6]) = [  9.38400E-02 0.00694  9.38400E-02 0.00694  0.00000E+00 0.0E+00 ];
ANA_DELAYED_EMTIME        (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
ANA_MEAN_NCOL             (idx, [1:   4]) = [  1.04808E+02 0.00178  0.00000E+00 0.0E+00 ];

% Group constant generation:

GC_UNIVERSE_NAME          (idx, [1:  1])  = '0' ;

% Micro- and macro-group structures:

MICRO_NG                  (idx, 1)        = 70 ;
MICRO_E                   (idx, [1:  71]) = [  2.00000E+01  6.06550E+00  3.67900E+00  2.23100E+00  1.35300E+00  8.21000E-01  5.00000E-01  3.02500E-01  1.83000E-01  1.11000E-01  6.74300E-02  4.08500E-02  2.47800E-02  1.50300E-02  9.11800E-03  5.50000E-03  3.51910E-03  2.23945E-03  1.42510E-03  9.06898E-04  3.67262E-04  1.48728E-04  7.55014E-05  4.80520E-05  2.77000E-05  1.59680E-05  9.87700E-06  4.00000E-06  3.30000E-06  2.60000E-06  2.10000E-06  1.85500E-06  1.50000E-06  1.30000E-06  1.15000E-06  1.12300E-06  1.09700E-06  1.07100E-06  1.04500E-06  1.02000E-06  9.96000E-07  9.72000E-07  9.50000E-07  9.10000E-07  8.50000E-07  7.80000E-07  6.25000E-07  5.00000E-07  4.00000E-07  3.50000E-07  3.20000E-07  3.00000E-07  2.80000E-07  2.50000E-07  2.20000E-07  1.80000E-07  1.40000E-07  1.00000E-07  8.00000E-08  6.70000E-08  5.80000E-08  5.00000E-08  4.20000E-08  3.50000E-08  3.00000E-08  2.50000E-08  2.00000E-08  1.50000E-08  1.00000E-08  5.00000E-09  1.00000E-11 ];

MACRO_NG                  (idx, 1)        = 2 ;
MACRO_E                   (idx, [1:   3]) = [  1.00000E+37  6.25000E-07  0.00000E+00 ];

% Micro-group spectrum:

INF_MICRO_FLX             (idx, [1: 140]) = [  1.19338E+07 0.00080  6.17338E+05 0.01174  8.27209E+05 0.00332  1.29381E+06 0.00728  1.89022E+06 0.00938  2.44483E+06 0.00641  2.37239E+06 0.00663  2.27596E+06 0.01085  2.38565E+06 0.00288  2.03907E+06 0.00122  2.00985E+06 0.00445  1.69846E+06 0.00636  1.47110E+06 0.00819  1.44382E+06 0.00464  1.42478E+06 0.00560  1.13886E+06 0.00852  1.15433E+06 0.00307  1.15329E+06 0.00751  1.12514E+06 0.01019  2.10083E+06 0.00993  1.92320E+06 0.00388  1.36781E+06 0.01455  8.61617E+05 0.00636  9.90285E+05 0.00904  9.26418E+05 0.00642  7.50394E+05 0.01822  1.28822E+06 0.00850  2.64787E+05 0.01901  3.02054E+05 0.01396  2.58753E+05 0.01274  1.46840E+05 0.02304  2.52926E+05 0.02351  1.64440E+05 0.02360  1.41274E+05 0.01731  2.73189E+04 0.07424  2.71457E+04 0.05526  2.80777E+04 0.11032  2.94686E+04 0.03150  2.83741E+04 0.06100  2.65116E+04 0.02758  2.87406E+04 0.10899  2.59436E+04 0.06424  5.60664E+04 0.01896  8.39932E+04 0.03394  1.07712E+05 0.05958  2.81344E+05 0.01710  2.89447E+05 0.01559  2.87266E+05 0.03174  1.58680E+05 0.03198  1.02521E+05 0.02685  7.07377E+04 0.03266  7.19084E+04 0.03198  1.09111E+05 0.03194  1.09478E+05 0.01521  1.46002E+05 0.01876  1.37941E+05 0.04887  1.27599E+05 0.03911  5.78017E+04 0.01934  3.18072E+04 0.03448  2.03091E+04 0.10451  1.63228E+04 0.08254  1.42581E+04 0.06160  1.11019E+04 0.07485  6.15657E+03 0.10297  5.56196E+03 0.10495  4.96397E+03 0.13641  2.67688E+03 0.14026  2.34808E+03 0.08851  1.80348E+03 0.23123  5.75408E+02 0.43932 ];

% Integral parameters:

INF_KINF                  (idx, [1:   2]) = [  2.20463E-09 0.01373 ];

% Flux spectra in infinite geometry:

INF_FLX                   (idx, [1:   4]) = [  1.21723E+03 0.00177  4.08777E+01 0.01743 ];
INF_FISS_FLX              (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Reaction cross sections:

INF_TOT                   (idx, [1:   4]) = [  8.75810E-02 0.00114  4.35500E-02 0.00759 ];
INF_CAPT                  (idx, [1:   4]) = [  7.31805E-04 0.00164  1.78329E-03 0.01636 ];
INF_ABS                   (idx, [1:   4]) = [  7.31805E-04 0.00164  1.78329E-03 0.01636 ];
INF_FISS                  (idx, [1:   4]) = [  5.07955E-13 0.01130  0.00000E+00 0.0E+00 ];
INF_NSF                   (idx, [1:   4]) = [  1.58915E-12 0.01312  0.00000E+00 0.0E+00 ];
INF_NUBAR                 (idx, [1:   4]) = [  3.12832E+00 0.00320  0.00000E+00 0.0E+00 ];
INF_KAPPA                 (idx, [1:   4]) = [  1.98847E+02 5.9E-09  0.00000E+00 0.0E+00 ];
INF_INVV                  (idx, [1:   4]) = [  4.91658E-08 0.00549  1.51825E-06 0.00359 ];

% Total scattering cross sections:

INF_SCATT0                (idx, [1:   4]) = [  8.68496E-02 0.00114  4.17462E-02 0.00743 ];
INF_SCATT1                (idx, [1:   4]) = [  4.60323E-03 0.00287  1.50736E-03 0.03321 ];
INF_SCATT2                (idx, [1:   4]) = [  2.20039E-03 0.00178  1.02500E-04 0.12719 ];
INF_SCATT3                (idx, [1:   4]) = [  8.09750E-04 0.00794  1.43665E-06 1.00000 ];
INF_SCATT4                (idx, [1:   4]) = [  5.41657E-04 0.01068  3.64093E-05 0.41097 ];
INF_SCATT5                (idx, [1:   4]) = [  2.70441E-04 0.01486  3.66755E-05 0.83669 ];
INF_SCATT6                (idx, [1:   4]) = [  1.64798E-04 0.04131  2.12272E-05 0.58376 ];
INF_SCATT7                (idx, [1:   4]) = [  9.19424E-05 0.07479  2.33232E-05 0.37854 ];

% Total scattering production cross sections:

INF_SCATTP0               (idx, [1:   4]) = [  8.69206E-02 0.00114  4.17462E-02 0.00743 ];
INF_SCATTP1               (idx, [1:   4]) = [  4.60464E-03 0.00286  1.50736E-03 0.03321 ];
INF_SCATTP2               (idx, [1:   4]) = [  2.20054E-03 0.00177  1.02500E-04 0.12719 ];
INF_SCATTP3               (idx, [1:   4]) = [  8.09705E-04 0.00778  1.43665E-06 1.00000 ];
INF_SCATTP4               (idx, [1:   4]) = [  5.41528E-04 0.01087  3.64093E-05 0.41097 ];
INF_SCATTP5               (idx, [1:   4]) = [  2.70580E-04 0.01445  3.66755E-05 0.83669 ];
INF_SCATTP6               (idx, [1:   4]) = [  1.64929E-04 0.04146  2.12272E-05 0.58376 ];
INF_SCATTP7               (idx, [1:   4]) = [  9.21751E-05 0.07556  2.33232E-05 0.37854 ];

% Diffusion parameters:

INF_TRANSPXS              (idx, [1:   4]) = [  1.87764E-02 0.00166  4.14749E-02 0.00814 ];
INF_DIFFCOEF              (idx, [1:   4]) = [  1.77530E+01 0.00166  8.03911E+00 0.00811 ];

% Reduced absoption and removal:

INF_RABSXS                (idx, [1:   4]) = [  6.60758E-04 0.00169  1.78329E-03 0.01636 ];
INF_REMXS                 (idx, [1:   4]) = [  8.59258E-04 0.00173  3.75640E-03 0.00815 ];

% Poison cross sections:

INF_I135_YIELD            (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_XE135_YIELD           (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_PM147_YIELD           (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_PM148_YIELD           (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_PM148M_YIELD          (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_PM149_YIELD           (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_SM149_YIELD           (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_I135_MICRO_ABS        (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_XE135_MICRO_ABS       (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_PM147_MICRO_ABS       (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_PM148_MICRO_ABS       (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_PM148M_MICRO_ABS      (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_PM149_MICRO_ABS       (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_SM149_MICRO_ABS       (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_XE135_MACRO_ABS       (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_SM149_MACRO_ABS       (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Poison decay constants:

PM147_LAMBDA              (idx, 1)        =  0.00000E+00 ;
PM148_LAMBDA              (idx, 1)        =  0.00000E+00 ;
PM148M_LAMBDA             (idx, 1)        =  0.00000E+00 ;
PM149_LAMBDA              (idx, 1)        =  0.00000E+00 ;
I135_LAMBDA               (idx, 1)        =  0.00000E+00 ;
XE135_LAMBDA              (idx, 1)        =  0.00000E+00 ;
XE135M_LAMBDA             (idx, 1)        =  0.00000E+00 ;
I135_BR                   (idx, 1)        =  0.00000E+00 ;

% Fission spectra:

INF_CHIT                  (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_CHIP                  (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_CHID                  (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Scattering matrixes:

INF_S0                    (idx, [1:   8]) = [  8.67217E-02 0.00114  1.27886E-04 0.01091  1.95259E-03 0.00489  3.97936E-02 0.00763 ];
INF_S1                    (idx, [1:   8]) = [  4.62701E-03 0.00280 -2.37759E-05 0.01495 -2.31495E-04 0.03690  1.73886E-03 0.02488 ];
INF_S2                    (idx, [1:   8]) = [  2.20485E-03 0.00194 -4.46093E-06 0.10256 -7.07034E-05 0.04639  1.73203E-04 0.06072 ];
INF_S3                    (idx, [1:   8]) = [  8.11143E-04 0.00796 -1.39345E-06 0.02507 -4.55747E-05 0.14504  4.70114E-05 0.59105 ];
INF_S4                    (idx, [1:   8]) = [  5.42446E-04 0.01020 -7.88946E-07 0.42371 -1.09914E-05 0.55967  4.74007E-05 0.28028 ];
INF_S5                    (idx, [1:   8]) = [  2.70601E-04 0.01464 -1.59988E-07 1.00000 -6.83878E-07 1.00000  3.73593E-05 0.79762 ];
INF_S6                    (idx, [1:   8]) = [  1.65062E-04 0.04067 -2.64489E-07 0.56249 -5.37440E-06 0.24847  2.66016E-05 0.42029 ];
INF_S7                    (idx, [1:   8]) = [  9.18283E-05 0.07596  1.14095E-07 1.00000 -2.71062E-06 1.00000  2.60338E-05 0.35473 ];

% Scattering production matrixes:

INF_SP0                   (idx, [1:   8]) = [  8.67928E-02 0.00114  1.27886E-04 0.01091  1.95259E-03 0.00489  3.97936E-02 0.00763 ];
INF_SP1                   (idx, [1:   8]) = [  4.62841E-03 0.00278 -2.37759E-05 0.01495 -2.31495E-04 0.03690  1.73886E-03 0.02488 ];
INF_SP2                   (idx, [1:   8]) = [  2.20500E-03 0.00193 -4.46093E-06 0.10256 -7.07034E-05 0.04639  1.73203E-04 0.06072 ];
INF_SP3                   (idx, [1:   8]) = [  8.11099E-04 0.00781 -1.39345E-06 0.02507 -4.55747E-05 0.14504  4.70114E-05 0.59105 ];
INF_SP4                   (idx, [1:   8]) = [  5.42317E-04 0.01039 -7.88946E-07 0.42371 -1.09914E-05 0.55967  4.74007E-05 0.28028 ];
INF_SP5                   (idx, [1:   8]) = [  2.70740E-04 0.01424 -1.59988E-07 1.00000 -6.83878E-07 1.00000  3.73593E-05 0.79762 ];
INF_SP6                   (idx, [1:   8]) = [  1.65193E-04 0.04082 -2.64489E-07 0.56249 -5.37440E-06 0.24847  2.66016E-05 0.42029 ];
INF_SP7                   (idx, [1:   8]) = [  9.20610E-05 0.07673  1.14095E-07 1.00000 -2.71062E-06 1.00000  2.60338E-05 0.35473 ];

% Micro-group spectrum:

B1_MICRO_FLX              (idx, [1: 140]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Integral parameters:

B1_KINF                   (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
B1_KEFF                   (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
B1_B2                     (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
B1_ERR                    (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];

% Critical spectra in infinite geometry:

B1_FLX                    (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_FISS_FLX               (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Reaction cross sections:

B1_TOT                    (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_CAPT                   (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_ABS                    (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_FISS                   (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_NSF                    (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_NUBAR                  (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_KAPPA                  (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_INVV                   (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Total scattering cross sections:

B1_SCATT0                 (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATT1                 (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATT2                 (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATT3                 (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATT4                 (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATT5                 (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATT6                 (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATT7                 (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Total scattering production cross sections:

B1_SCATTP0                (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATTP1                (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATTP2                (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATTP3                (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATTP4                (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATTP5                (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATTP6                (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATTP7                (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Diffusion parameters:

B1_TRANSPXS               (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_DIFFCOEF               (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Reduced absoption and removal:

B1_RABSXS                 (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_REMXS                  (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Poison cross sections:

B1_I135_YIELD             (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_XE135_YIELD            (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_PM147_YIELD            (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_PM148_YIELD            (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_PM148M_YIELD           (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_PM149_YIELD            (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SM149_YIELD            (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_I135_MICRO_ABS         (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_XE135_MICRO_ABS        (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_PM147_MICRO_ABS        (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_PM148_MICRO_ABS        (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_PM148M_MICRO_ABS       (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_PM149_MICRO_ABS        (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SM149_MICRO_ABS        (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_XE135_MACRO_ABS        (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SM149_MACRO_ABS        (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Fission spectra:

B1_CHIT                   (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_CHIP                   (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_CHID                   (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Scattering matrixes:

B1_S0                     (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_S1                     (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_S2                     (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_S3                     (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_S4                     (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_S5                     (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_S6                     (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_S7                     (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Scattering production matrixes:

B1_SP0                    (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SP1                    (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SP2                    (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SP3                    (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SP4                    (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SP5                    (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SP6                    (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SP7                    (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Additional diffusion parameters:

CMM_TRANSPXS              (idx, [1:   4]) = [  1.81213E-02 0.00223  6.32635E-02 0.05359 ];
CMM_TRANSPXS_X            (idx, [1:   4]) = [  1.39624E-02 0.00480  5.32344E-02 0.10495 ];
CMM_TRANSPXS_Y            (idx, [1:   4]) = [  1.59056E-02 0.00336  9.64596E-02 0.29448 ];
CMM_TRANSPXS_Z            (idx, [1:   4]) = [  3.22039E-02 0.00213  6.76230E-02 0.04522 ];
CMM_DIFFCOEF              (idx, [1:   4]) = [  1.83949E+01 0.00223  5.32742E+00 0.05142 ];
CMM_DIFFCOEF_X            (idx, [1:   4]) = [  2.38759E+01 0.00478  6.52683E+00 0.09825 ];
CMM_DIFFCOEF_Y            (idx, [1:   4]) = [  2.09579E+01 0.00337  4.48518E+00 0.22072 ];
CMM_DIFFCOEF_Z            (idx, [1:   4]) = [  1.03509E+01 0.00213  4.97025E+00 0.04566 ];

% Delayed neutron parameters (Meulekamp method):

BETA_EFF                  (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
LAMBDA                    (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];

