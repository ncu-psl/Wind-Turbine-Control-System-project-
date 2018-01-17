#==============================================================================
# @constant pi 3.141592653589793                                         : 'π'   pi from NumPy
#
# @parameter Tsr                                                         : 
# @parameter Cp                                                          :
# @parameter Tb                                                          : The torque of fan blade.
# @parameter Tg                                                          : The torque of generator.
# @parameter Tm                                                          : The torque of machine.
# @parameter Tt                                                          : The total torque.
# @parameter eff_g                                                       : 'η'  It is friction coefficient of generator.
# @parameter eff_e                                                       : 'η'  It is friction coefficient of electricity efficiency.
#
# @function Mode_ThreePhaseShortCircuit()                                : The mode of three phase short circuit.
# @function Mode_MaxPower()                                              : The mode of max power.
# @function Mode_MaxTorqueCurrent()                                      : The mode of max torque current.
# @function MaxTorqueCurrent_MagBrake()                                  : The mode of MaxTorqueCurrent_MagBrake.
# @function Mode_ThreePhaseShortCircuit_MagBrake()                       : The mode of Mode_ThreePhaseShortCircuit_MagBrake().
#
# # function of all modes
# @function TSR()                                                        : Calculate TSR
# @function TorqueBlade(Cp)                                              : Calculate the torque of fan blade with Cp.
# @function TotalTorque(Tb, Tg, Tm = 0)                                  : Calculate total torque with torque of fan blade, torque of generator, torque of machine.  
# @function CalculateRPM(Tt)                                             : Calculate the rpm with total Torque.
# @function CalculatePower(eff_g, eff_e, Tt)                             : Calculate the power with total Torque, friction coefficient of generator, friction coefficient of electricity efficiency.
# @function 
#
# # function of Mode_ThreePhaseShortCircuit
# @function Cp_ThreePhaseShortCircuit(Tsr)                               : Calculate Cp with TSR.(ThreePhaseShortCircuit)
# @function Tg_ThreePhaseShortCircuit()                                  : Calculate the torque of generator.(ThreePhaseShortCircuit)
# @function eff_g = eff_g_ThreePhaseShortCircuit()                       : 'η'  It is friction coefficient of generator.(ThreePhaseShortCircuit)
# @function eff_e = eff_e_ThreePhaseShortCircuit()                       : 'η'  It is friction coefficient of electricity efficiency.(ThreePhaseShortCircuit)
#
# # function of Mode_MaxPower
# @function Cp_MaxPower()                                                : Calculate Cp.(MaxPower)
# @function Tg_MaxPower()                                                : Calculate the torque of generator.(MaxPower)
# @function eff_g_MaxPower()                                             : 'η'  It is friction coefficient of generator.(MaxPower)
# @function eff_e_MaxPower()                                             : 'η'  It is friction coefficient of electricity efficiency.(MaxPower)
#
# # function of Mode_MaxTorqueCurrent
# @function Cp_MaxTorqueCurrent(Tsr)                                     : Calculate Cp with TSR.(MaxTorqueCurrent)
#
# @function getApproximation(index, domainlist, rangelist)               : Using index finds approximation.  f(x)=y, x={domainlist}, y=range, 
# @function getMargin(index, domainlist)                                 : Find marginal of index.
# @function getpointinLinearEquation(startx, starty, endx, endy, pointx) : Using two point of marginal find the linear equation.
#
# decision
# @function check_MaxWindSpeed_ThreePhaseShortCircuit()                  : Check WindSpeed < Parameter.WindSpeed_ThreePhaseShortCircuit is true or false now.
# @function check_RPM_Increase()                                         : Check rpm is increase.
# @function check_MaxMagBrake()                                          : Check rpm < rpm of MaxMagBrake is true or false now.
# @function check_CutOut()                                               : Check rpm > Parameter.CutOutRPM or power > Parameter.CutOutPower is true or false now.
# 
# return value
# @function CurrentWindSpeed(Time)                                       : return WindSpeed at Time.
# @function CurrentRPM(Time)                                             : return RPM at Time.
# @function CurrentPower(Time)                                           : return Power at Time.
#==============================================================================


from numpy import*
import Parameter

def appendStack(Tsr, Cp, Tb, Tg, Tm, Tt, eff_g, eff_e):
    Parameter.TsrStack.append(Tsr)
    Parameter.CpStack.append(Cp)
    Parameter.TbStack.append(Tb)
    Parameter.TmStack.append(Tm)
    Parameter.TgStack.append(Tg)
    Parameter.TtotalStack.append(Tt)
    Parameter.eff_gStack.append(eff_g)
    Parameter.eff_eStack.append(eff_e)



# five modes

def Mode_ThreePhaseShortCircuit(LastTime,LastWindSpeed, LastRPM, LastPower):
    CurrentTime = IncreaseTime(LastTime)
    CurrentWindSpeed = Parameter.WindSpeed[CurrentTime]
    Tsr   = TSR(LastWindSpeed, Parameter.D , CurrentWindSpeed)
    Cp    = CP(Tsr, Parameter.Tsr_ThreePhaseShortCircuit, Parameter.Cp_ThreePhaseShortCircuit)
    Tb    = TorqueBlade(Cp, Parameter.Rho, Parameter.A, CurrentWindSpeed, LastRPM)
    Tg    = TorqueGenerator(LastRPM, Parameter.RPM_ThreePhaseShortCircuit, Parameter.Tg_ThreePhaseShortCircuit)
    Tm    = 0
    Tt    = TotalTorque(Tb, Tg, Tm)
    CurrentRPM = CalculateRPM(Tt, LastRPM, Parameter.TimeDelta, Parameter.MonmentIntertia)
    eff_g = EFF_g(CurrentWindSpeed, Parameter.WindSpeed_ThreePhaseShortCircuit, Parameter.eff_g_ThreePhaseShortCircuit)
    eff_e = Parameter.eff_e_ThreePhaseShortCircuit
    CurrentPower = 0
    Parameter.Power.append(CurrentPower)
    appendStack(Tsr, Cp, Tb, Tg, Tm, Tt, eff_g, eff_e)
    return CurrentTime, CurrentWindSpeed, CurrentRPM, CurrentPower #Parameter.WindSpeed[Parameter.CurrentTime], Parameter.RPM[Parameter.CurrentTime], Parameter.Power[Parameter.CurrentTime] 
    

def Mode_MaxPower(LastTime,LastWindSpeed, LastRPM, LastPower):
    CurrentTime = IncreaseTime(LastTime)
    CurrentWindSpeed = Parameter.WindSpeed[CurrentTime]
    Tsr   = TSR(LastWindSpeed, Parameter.D , CurrentWindSpeed)
    Cp    = CP(Tsr, Parameter.Tsr_MaxPower, Parameter.Cp_MaxPower)
    Tb    = TorqueBlade(Cp, Parameter.Rho, Parameter.A, CurrentWindSpeed, LastRPM)
    Tg    = TorqueGenerator(LastRPM, Parameter.RPM_MaxPower, Parameter.Tg_MaxPower) 
    Tm    = 0
    Tt    = TotalTorque(Tb, Tg)
    CurrentRPM = CalculateRPM(Tt, LastRPM, Parameter.TimeDelta, Parameter.MonmentIntertia)
    eff_g = EFF_g(CurrentWindSpeed, Parameter.WindSpeed_MaxPower, Parameter.eff_g_MaxPower)
    eff_e = Parameter.eff_e_MaxPower
    CurrentPower = CalculatePower(CurrentRPM, eff_g, eff_e, Tg)
    appendStack(Tsr, Cp, Tb, Tg, Tm, Tt, eff_g, eff_e)
    return CurrentTime, CurrentWindSpeed, CurrentRPM, CurrentPower #Parameter.WindSpeed[Parameter.CurrentTime], Parameter.RPM[Parameter.CurrentTime], Parameter.Power[Parameter.CurrentTime] 
    
    
    
def Mode_MaxTorqueCurrent(LastTime,LastWindSpeed, LastRPM, LastPower):
    CurrentTime = IncreaseTime(LastTime)
    CurrentWindSpeed = Parameter.WindSpeed[CurrentTime]
    Tsr   = TSR(LastWindSpeed, Parameter.D , CurrentWindSpeed)
    Cp    = CP(Tsr, Parameter.Tsr__MaxTorqueCurrent, Parameter.Cp_MaxTorqueCurrent)
    Tb    = TorqueBlade(Cp, Parameter.Rho, Parameter.A, CurrentWindSpeed, LastRPM)
    
    Tg    = Parameter.TorqueGenerator_MaxTorqueCurrent
    Tm     = 0
    Tt    = TotalTorque(Tb, Tg)
    CurrentRPM = CalculateRPM(Tt, LastRPM, Parameter.TimeDelta, Parameter.MonmentIntertia)
    
    eff_g = Parameter.eff_g_MaxTorqueCurrent
    eff_e = Parameter.eff_e_MaxTorqueCurrent
    CurrentPower = CalculatePower(CurrentRPM, eff_g, eff_e, Tg)
    #Parameter.CurrentTime += 1
    appendStack(Tsr, Cp, Tb, Tg, Tm, Tt, eff_g, eff_e)
    return CurrentTime, CurrentWindSpeed, CurrentRPM, CurrentPower #Parameter.WindSpeed[Parameter.CurrentTime], Parameter.RPM[Parameter.CurrentTime], Parameter.Power[Parameter.CurrentTime]
    

def Mode_MaxTorqueCurrent_MagBrake(LastTime,LastWindSpeed, LastRPM, LastPower):
    CurrentTime = IncreaseTime(LastTime)
    CurrentWindSpeed = Parameter.WindSpeed[CurrentTime]
    Tsr   = TSR(LastWindSpeed, Parameter.D , CurrentWindSpeed)
    Cp    = CP(Tsr, Parameter.Tsr__MaxTorqueCurrent, Parameter.Cp_MaxTorqueCurrent)
    Tb    = TorqueBlade(Cp, Parameter.Rho, Parameter.A, CurrentWindSpeed, LastRPM)
    
    Tg    = Parameter.TorqueGenerator_MaxTorqueCurrent
    Tm    = Parameter.TorqueMachine
    Tt    = TotalTorque(Tb, Tg, Tm)
    CurrentRPM = CalculateRPM(Tt, LastRPM, Parameter.TimeDelta, Parameter.MonmentIntertia)
    eff_g = Parameter.eff_g_MaxTorqueCurrent
    eff_e = Parameter.eff_e_MaxTorqueCurrent
    CurrentPower = CalculatePower(CurrentRPM, eff_g, eff_e, Tg)
    appendStack(Tsr, Cp, Tb, Tg, Tm, Tt, eff_g, eff_e)
    return CurrentTime, CurrentWindSpeed, CurrentRPM, CurrentPower #Parameter.WindSpeed[Parameter.CurrentTime], Parameter.RPM[Parameter.CurrentTime], Parameter.Power[Parameter.CurrentTime]
    
def Mode_ThreePhaseShortCircuit_MagBrake(LastTime,LastWindSpeed, LastRPM, LastPower):
    CurrentTime = IncreaseTime(LastTime)
    CurrentWindSpeed = Parameter.WindSpeed[CurrentTime]
    Tsr   = TSR(LastWindSpeed, Parameter.D , CurrentWindSpeed)
    Cp    = CP(Tsr, Parameter.Tsr_ThreePhaseShortCircuit, Parameter.Cp_ThreePhaseShortCircuit)
    Tb    = TorqueBlade(Cp, Parameter.Rho, Parameter.A, CurrentWindSpeed, LastRPM)
    Tg    = TorqueGenerator(LastRPM, Parameter.RPM_ThreePhaseShortCircuit, Parameter.Tg_ThreePhaseShortCircuit)
    Tm    = Parameter.TorqueMachine
    Tt    = TotalTorque(Tb, Tg, Tm)
    CurrentRPM = CalculateRPM(Tt, LastRPM, Parameter.TimeDelta, Parameter.MonmentIntertia)
    eff_g = EFF_g(CurrentWindSpeed, Parameter.WindSpeed_ThreePhaseShortCircuit, Parameter.eff_g_ThreePhaseShortCircuit)
    eff_e = Parameter.eff_e_ThreePhaseShortCircuit
    CurrnetPower = 0
    Parameter.Power.append(CurrnetPower)
    appendStack(Tsr, Cp, Tb, Tg, Tm, Tt, eff_g, eff_e)
    return CurrentTime, CurrentWindSpeed, CurrentRPM, CurrentPower #Parameter.WindSpeed[Parameter.CurrentTime], Parameter.RPM[Parameter.CurrentTime], Parameter.Power[Parameter.CurrentTime]







#==============================================================================
# # Moae_ThreePhaseShortCircuit()
# def Cp_ThreePhaseShortCircuit(Tsr):
#     #Cp = getApproximation(Tsr, Parameter.Tsr_ThreePhaseShortCircuit, Parameter.Cp_ThreePhaseShortCircuit)
#     Cp = getApproximation(Tsr, Parameter.Tsr_ThreePhaseShortCircuit, Parameter.Cp_ThreePhaseShortCircuit)
#     return Cp
#     
# def Tg_ThreePhaseShortCircuit():
#     Tg = getApproximation(Parameter.RPM[Parameter.CurrentTime-1], Parameter.RPM_ThreePhaseShortCircuit, Parameter.Tg_ThreePhaseShortCircuit)
#     if Tg < 0:
#         Tg = 0
#     return Tg
# 
# def eff_g_ThreePhaseShortCircuit():
#     eff_g = getApproximation(Parameter.WindSpeed[Parameter.CurrentTime], Parameter.WindSpeed_ThreePhaseShortCircuit, Parameter.eff_g_ThreePhaseShortCircuit)
#     return eff_g
# 
# 
# 
# # Mode_MaxPower()
# def Cp_MaxPower(Tsr):
#     Cp = getApproximation(Tsr, Parameter.Tsr_MaxPower, Parameter.Cp_MaxPower)
#     #Cp = getApproximation(Parameter.WindSpeed[Parameter.CurrentTime-1], Parameter.WindSpeed_MaxPower, Parameter.Cp_MaxPower)
#     return Cp
# 
# def Tg_MaxPower():
#     Tg = getApproximation(Parameter.RPM[Parameter.CurrentTime-1], Parameter.RPM_MaxPower, Parameter.Tg_MaxPower)
#     if Tg < 0:
#         Tg = 0
#     return Tg
# 
# def eff_g_MaxPower():
#     eff_g = getApproximation(Parameter.WindSpeed[Parameter.CurrentTime], Parameter.WindSpeed_MaxPower, Parameter.eff_g_MaxPower)
#     return eff_g
# 
# 
# 
# 
# # Mode_MaxTorqueCurrent
# def Cp_MaxTorqueCurrent(Tsr):
#     Cp = getApproximation(Tsr, Parameter.Tsr__MaxTorqueCurrent, Parameter.Cp_MaxTorqueCurrent)
#     return Cp
#==============================================================================


#define public formulas for all mode.
def TotalTorque(TorqueBlade, TorqueGenerator, TorqueMachine = 0):  
    totaltorque = TorqueBlade - TorqueGenerator - TorqueMachine
    return totaltorque    

def CalculateRPM(TorqueTotal, LastRPM, TimeDelta, MonmentIntertia):
    #rpm = Parameter.RPM[Parameter.CurrentTime-1] + ( TorqueTotal * Parameter.TimeDelta / Parameter.MonmentIntertia ) * 60 / ( 2 * pi )
    rpm = LastRPM + ( TorqueTotal * TimeDelta / MonmentIntertia ) * 60 / ( 2 * pi )
    if rpm <= 0:
        rpm = 0.0000001
    Parameter.RPM.append(rpm)
    return rpm #Parameter.RPM[Parameter.CurrentTime]


def CalculatePower(CurrentRPM, eff_g, eff_e, TorqueGenerator):
    #power = 2 * pi * Parameter.RPM[Parameter.CurrentTime]/60 * TorqueGenerator * eff_g * eff_e
    power = 2 * pi * CurrentRPM/60 * TorqueGenerator * eff_g * eff_e
    if power < 0:
        power=0                              
    Parameter.Power.append(power)
    return power #Parameter.Power[Parameter.CurrentTime]


  
def TSR(LastWindSpeed, D , CurrentWindSpeed):
    #Tsr = 2 * pi * (Parameter.RPM[Parameter.CurrentTime-1] / 60) * (Parameter.D / 2) / Parameter.WindSpeed[Parameter.CurrentTime]
    Tsr = 2 * pi * (LastWindSpeed / 60) * (D / 2) / CurrentWindSpeed
    return Tsr

def CP(indexTsr, RefenerceTsr, RefenerceCp):
    Cp = getApproximation(indexTsr, RefenerceTsr, RefenerceCp)
    return Cp
    
def TorqueBlade(Cp, Rho, A, CurrentWindSpeed, LastRPM):
    #TorqueBlade = Cp * 0.5 * Parameter.Rho * Parameter.A * (Parameter.WindSpeed[Parameter.CurrentTime]**3) / (2 * pi * (Parameter.RPM[Parameter.CurrentTime-1] / 60))
    TorqueBlade = Cp * 0.5 * Rho * A * (CurrentWindSpeed**3) / (2 * pi * (LastRPM / 60))
    return TorqueBlade

def TorqueGenerator(indexLastRPM, refenceRPM, refenceTg):
    #EX:  Tg = getApproximation(Parameter.RPM[Parameter.CurrentTime-1], Parameter.RPM_ThreePhaseShortCircuit, Parameter.Tg_ThreePhaseShortCircuit)
    Tg = getApproximation(indexLastRPM, refenceRPM, refenceTg)
    return Tg

def EFF_g(indexCurrentWindSpeed, refencetWindSpeed, refenceeff_g):
    #EX: eff_g = getApproximation(Parameter.WindSpeed[Parameter.CurrentTime], Parameter.WindSpeed_ThreePhaseShortCircuit, Parameter.eff_g_ThreePhaseShortCircuit)
    eff_g = getApproximation(indexCurrentWindSpeed, refencetWindSpeed, refenceeff_g)
    return eff_g


#==============================================================================



# Find approximation
def getApproximation(index, domainlist, rangelist):
    indexleft, indexright = getMargin(index, domainlist)
    leftx    = domainlist[indexleft]
    lefty    = rangelist[indexleft]
    rightx   = domainlist[indexright]
    righty   = rangelist[indexright]
    value    = getpointinLinearEquation(leftx, lefty, rightx, righty, index)
    if value < 0:
       value = 0 
    #print(leftx, lefty, rightx, righty, index)   
    return value

def getMargin(index, domainlist):
    indexleft  = 0
    indexright = 0
    if index < domainlist[0]:
        indexleft  = 0
        indexright = 1
    elif index > domainlist[len(domainlist)-1]:
        indexleft  = len(domainlist)-2
        indexright = len(domainlist)-1
    else: 
        for i in range(0,len(domainlist)-1):
            if index == domainlist[i]:
                indexleft  = i
                indexright = i
                break;      
            if index > domainlist[i] and index < domainlist[i+1]:
                indexleft  = i
                indexright = i+1
                break; 
        if index == domainlist[len(domainlist)-1]:
            indexleft  = len(domainlist)-1
            indexright = len(domainlist)-1    
    return indexleft, indexright

def getpointinLinearEquation(startx, starty, endx, endy, pointx):
    if startx == endx: 
        pointy = starty
    else:
        pointy = (pointx-startx)*(endy-starty)/(endx-startx)+starty
    return pointy


# Check the value
def Check_MaxWindSpeed_ThreePhaseShortCircuit():
    return Parameter.WindSpeed[Parameter.CurrentTime] < Parameter.MaxWindSpeed_ThreePhaseShortCircuit


def Check_RPM_Increase():
    return Parameter.RPM[Parameter.CurrentTime] > Parameter.RPM[Parameter.CurrentTime-1]

def Check_MaxMagBrake():
    return Parameter.RPM[Parameter.CurrentTime] > Parameter.MaxMagBrake


def Check_CutOut():
    return (Parameter.RPM[Parameter.CurrentTime] > Parameter.CutOutRPM or Parameter.Power[Parameter.CurrentTime] > Parameter.CutOutPower)

#==============================================================================


#get the values
def IncreaseTime(LastTime):
    CurrentTime = LastTime + 1
    return CurrentTime

def sizeData():
    return len(Parameter.WindSpeed)

def CurrentWindSpeed(Time):
    return Parameter.WindSpeed[Time]

def CurrentRPM(Time):
    return Parameter.RPM[Time]

def CurrentPower(Time):
    return Parameter.Power[Time]



