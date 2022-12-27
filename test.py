import cadquery as cq

import stok_modules as stok
from stok_modules import ContainmentParameters, SolenoidParameters, DivertorParameters
from stok_modules import PortParameters, LimbParameters, LimiterParameters

main = stok.STOK((ContainmentParameters(), SolenoidParameters(), PortParameters(),
                  LimbParameters(), LimiterParameters(), DivertorParameters()))

show_object(main.divertor_firstwall().add(main.containment_with_divertor_and_ports()[1]).add(main.divertor_backwall()))
