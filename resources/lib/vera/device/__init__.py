from vera.device import category 

# turn on/off a BinaryLight, arm/disarm a motion sensor etc.
def toggle(device, vera_controller):
    if device['category'] == category.BINARY_LIGHT:
        newTargetValue = '1'
        if int(device['status']):
            newTargetValue = '0'
        vera_controller.GET ( \
'/data_request?id=action&DeviceNum=' + str(device['id'])          + \
'&serviceId=urn:upnp-org:serviceId:SwitchPower1&action=SetTarget' + \
'&newTargetValue=' + newTargetValue                                 \
        )





