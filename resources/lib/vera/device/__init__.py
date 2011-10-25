import vera.device.category as category

# turn on/off a BinaryLight, arm/disarm a motion sensor etc.
def toggle(device, vera_controller):
    if device['category'] == category.BINARY_LIGHT:
        # TODO: move this to backend
        newTargetValue = '1'
        if device['status']:
            newTargetValue = '0'
        vera_controller.GET ( \
                '/data_request?id=action&DeviceNum=' + str(device['id']) +          \
                '&serviceId=urn:upnp-org:serviceId:SwitchPower1&action=SetTarget' + \
                '&newTargetValue=' + newTargetValue                                 \
        )




