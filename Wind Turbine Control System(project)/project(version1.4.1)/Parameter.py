#==============================================================================
# # output of parameter
# @parameter TimeSeries
# @parameter WindSpeed                           : It is wind speed. unit: m/s( Meters per second).
# @parameter RPM                                 : The output of revolutions per minute.
# @parameter Power                               : The output of power.
# 
# # parameter
# @parameter CurrentTime                         : The current period of time.  unit: ms ( millisecond )
# @parameter TimeDelta                           : '△t' The variation of time.
# @parameter MonmentIntertia                     : 'I'  It is monment of intertia of monmentIntertia. unit: m/s( Meters per second).
# @parameter CutOutRPM                           : The rpm of cut out.
# @parameter CutOutPower                         : The power of cut out.
# @parameter Rho                                 : 'ρ'
# @parameter A                                   : The diameter of fan blades.
# @parameter TorqueMachine                       : The torque of machine.
# 
# # data of Mode_ThreePhaseShortCircuit
# @parameter WindSpeed_ThreePhaseShortCircuit    : The reference of WindSpeed in three phase short circuit mode.
# @parameter eff_g_ThreePhaseShortCircuit        : 'η'  It is internal friction coefficient of generation.(ThreePhaseShortCircuit) 
# @parameter eff_e_ThreePhaseShortCircuit        : 'η'  It is internal friction coefficient of electricity efficiency.(ThreePhaseShortCircuit) 
# @parameter RPM_ThreePhaseShortCircuit          : The reference of rpm in three phase short circuit mode.
# @parameter Tg_ThreePhaseShortCircuit           : The torque of generation. (ThreePhaseShortCircuit)
# @parameter Tsr_ThreePhaseShortCircuit          :
# @parameter Cp_ThreePhaseShortCircuit           : 
#
# # data of Mode_MaxPower
# @parameter WindSpeed_MaxPower                  : The reference of WindSpeed in MaxPower Mode.
# @parameter Cp_MaxPower                         : 
# @parameter eff_g_MaxPower                      : 'η'  It is internal friction coefficient of generation.(MaxPower)
# @parameter eff_e_MaxPower                      : 'η'  It is internal friction coefficient of electricity efficiency.(MaxPower)
# @parameter Tg_MaxPower                         : The torque of Generation. (MaxPower)
#
# # data of Mode_MaxTorqueCurrent                
# @parameter Tsr__MaxTorqueCurrent               :
# @parameter Cp_MaxTorqueCurrent                   
# @parameter eff_g_MaxTorqueCurrent              : 'η'  It is internal friction coefficient of generation.(MaxTorqueCurrent)
# @parameter eff_e_MaxTorqueCurrent              : 'η'  It is internal friction coefficient of electricity efficiency.(MaxTorqueCurrent)
# @parameter TorqueGeneration_MaxTorqueCurrent   : The torque of generation.(MaxTorqueCurrent)
#==============================================================================


# output of parameter
TimeSeries = []
WindSpeed  = []
RPM        = []
Power      = []



# # Append the Reference initial value
TimeSeries.append(0)
WindSpeed.append(0)
RPM.append(0.0001)
Power.append(0)
RPM.append(0.0001)
Power.append(0)

# temp stack
ModeStack  = []
TsrStack = []
CpStack  = []
TbStack  = []
TgStack  = []
TmStack  = []
TtotalStack  = []
eff_gStack = []
eff_eStack = []

ModeStack.append("default value")
TsrStack.append(0)
CpStack.append(0)
TbStack.append(0)
TgStack.append(0)
TmStack.append(0)
TtotalStack.append(0)
eff_gStack.append(0)
eff_eStack.append(0)




#==============================================================================
# # 
# RPM.append(0.0001)
# Power.pop(0)
# 
#==============================================================================


#parameter
MaxWindSpeed_ThreePhaseShortCircuit = 8
CurrentTime     = 1
TimeDelta       = 0.01
MonmentIntertia = 0.7
CutOutRPM       = 400
CutOutPower     = 3300
MaxMagBrake     = 42
Rho             = 1.293
D               = 3.7
A               = 10.74665
TorqueMachine   = 175






# Create Table

# Mode_ThreePhaseShortCircuit
WindSpeed_ThreePhaseShortCircuit = []
eff_g_ThreePhaseShortCircuit     = 0
eff_e_ThreePhaseShortCircuit     = 0.9

RPM_ThreePhaseShortCircuit       = []
Tg_ThreePhaseShortCircuit        = []


Tsr_ThreePhaseShortCircuit       = []
Cp_ThreePhaseShortCircuit        = []



# Mode_MaxPower
RPMtoEffg_MaxPower = []
eff_g_MaxPower     = []
eff_e_MaxPower     = 0.9

RPMtoTG_MaxPower       = []
Tg_MaxPower        = []

Tsr_MaxPower       = []
Cp_MaxPower        = []



# Mode_MaxTorqueCurrent
RPM__MaxTorqueCurrent  = []
eff_g_MaxTorqueCurrent = []
eff_e_MaxTorqueCurrent = 0.9

Tsr_MaxTorqueCurrent = []
Cp_MaxTorqueCurrent   = []

TorqueGenerator_MaxTorqueCurrent = 110




def RemoveDefaultValue():
    TimeSeries.pop(0)
    WindSpeed.pop(0)
    RPM.pop(0)
    Power.pop(0)