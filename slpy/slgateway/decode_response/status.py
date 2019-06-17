# -*- coding: cp850 -*-
from slgateway.decode_response.datautil import *
from slgateway.const import *

def decode_pool_status_response(buff, data):

    #{ name="", value= }
    if('sensors' not in data):
        data['sensors'] = {}
  
    ok, offset = getSome("I", buff, 0)

    freezeMode, offset = getSome("B", buff, offset)

    remotes, offset = getSome("B", buff, offset)

    poolDelay, offset = getSome("B", buff, offset)

    spaDelay, offset = getSome("B", buff, offset)

    cleanerDelay, offset = getSome("B", buff, offset)

    # fast forward 3 bytes. why? because.
    ff1, offset = getSome("B", buff, offset)
    ff2, offset = getSome("B", buff, offset)
    ff3, offset = getSome("B", buff, offset)

    if(data['config']['is_celcius']['value']):
        unittxt = '\xb0C'
    else:
        unittxt = '\xb0F'

    airTemp, offset = getSome("i", buff, offset)
    data['sensors']['air_temperature'] = dict(name="Air Temperature", \
                                            value=airTemp, \
                                            hassType="sensor", \
                                            unit=unittxt)

    bodiesCount, offset = getSome("I", buff, offset)
    bodiesCount = min(bodiesCount, 2)

    if('bodies' not in data):
        data['bodies'] = {} #[{} for x in range(bodiesCount)]

    for i in range(bodiesCount):
        bodyType, offset = getSome("I", buff, offset)
        if(bodyType not in range(2)): bodyType = 0

        if(i not in data['bodies']):
            data['bodies'][i] = {}
    
        data['bodies'][i]['body_type'] = dict(name="Type of body of water", \
                                                value=bodyType)

        currentTemp, offset = getSome("i", buff, offset)
        data['bodies'][i]['current_temperature'] = dict(name="Current {} Temperature"\
                                                .format(mapping.BODY_TYPE[bodyType]), \
                                                value=currentTemp, \
                                                hassType='sensor', \
                                                unit=unittxt)

        heatStatus, offset = getSome("i", buff, offset)
        data['bodies'][i]['heat_status'] = dict(name="{} Heater"\
                                                .format(mapping.BODY_TYPE[bodyType]), \
                                                value=heatStatus, \
                                                hassType='binary_sensor')

        heatSetPoint, offset = getSome("i", buff, offset)
        data['bodies'][i]['heat_set_point'] = dict(name="{} Heat Set Point"\
                                                .format(mapping.BODY_TYPE[bodyType]), \
                                                value=heatSetPoint, \
                                                hassType='sensor', \
                                                unit=unittxt)

        coolSetPoint, offset = getSome("i", buff, offset)
        data['bodies'][i]['cool_set_point'] = dict(name="{} Cool Set Point"\
                                                .format(mapping.BODY_TYPE[bodyType]), \
                                                value=coolSetPoint, \
                                                hassType='sensor', \
                                                unit=unittxt)

        heatMode, offset = getSome("i", buff, offset)
        data['bodies'][i]['heat_mode'] = dict(name="{} Heater Mode"\
                                                .format(mapping.BODY_TYPE[bodyType]), \
                                                value=heatMode,\
                                                hassType='sensor')
  
    circuitCount, offset = getSome("I", buff, offset)

    if('circuits' not in data):
        data['circuits'] = {}

    for i in range(circuitCount):
        circuitID, offset = getSome("I", buff, offset)

        if(circuitID not in data['circuits']):
            data['circuits'][circuitID] = {}

        if('id' not in data['circuits'][circuitID]):
            data['circuits'][circuitID]['id'] = circuitID

        circuitstate, offset = getSome("I", buff, offset)
        data['circuits'][circuitID]['value'] = circuitstate

        data['circuits'][circuitID]['hassType'] = 'switch'
 
        circuitColorSet, offset = getSome("B", buff, offset)
        circuitColorPos, offset = getSome("B", buff, offset)
        circuitColorStagger, offset = getSome("B", buff, offset)
        circuitDelay, offset = getSome("B", buff, offset)

    if('chemistry' not in data):
        data['chemistry'] = {}
    
    pH, offset = getSome("i", buff, offset)
    data['chemistry']['ph'] = dict(name="pH", \
                                    value=(pH / 100), \
                                    hassType='sensor')
  
    orp, offset = getSome("i", buff, offset)
    data['chemistry']['orp'] = dict(name="ORP", value=orp, \
                                    hassType='sensor')

    saturation, offset = getSome("i", buff, offset)
    data['chemistry']['saturation'] = dict(name="Saturation Index", \
                                            value=(saturation / 100), \
                                            hassType='sensor')

    saltPPM, offset = getSome("i", buff, offset)
    data['chemistry']['salt_ppm'] = dict(name="Salt", \
                                        value=saltPPM, \
                                        unit='ppm', \
                                        hassType='sensor')

    pHTank, offset = getSome("i", buff, offset)
    data['chemistry']['ph_tank_level'] = dict(name="pH Tank Level", \
                                            value=pHTank, \
                                            hassType='sensor')

    orpTank, offset = getSome("i", buff, offset)
    data['chemistry']['orp_tank_level'] = dict(name="ORP Tank Level", \
                                            value=orpTank, \
                                            hassType='sensor')

    alarms, offset = getSome("i", buff, offset)
    data['chemistry']['alarms'] = dict(name="Chemistry Alarm", \
                                        value=alarms, \
                                        hassType='binary_sensor')

