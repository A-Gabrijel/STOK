import cadquery as cq
import cq_editor as cqe

import stok_modules as stok
from stok_modules import ContainmentParameters, SolenoidParameters, DivertorParameters
from stok_modules import PortParameters, LimbParameters, LimiterParameters

main = stok.STOK((ContainmentParameters(), SolenoidParameters(), PortParameters(),
                  LimbParameters(), LimiterParameters(), DivertorParameters()))

show_object(main.divertor_backwall())
show_object(main.containment_with_divertor_and_ports()[0])
show_object(main.divertor_firstwall())
show_object(main.containment_with_divertor_and_ports()[7])
show_object(main.limiter_firstwall())
show_object(main.limiter_backwall())
