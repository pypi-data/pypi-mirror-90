"""
Configuration info for BLT Funcx Toolkit
"""


class BLTEndpoint:
    """
    BLT Endpoint wrapper class defining BLT endpoints
    """
    def __init__(self,
                 name=None,
                 uuid=None,
                 core_count=None,
                 gpu_count=None,
                 remarks=None):
        self.name = name
        self.core_count = core_count
        self.gpu_count = gpu_count
        self.remarks = remarks
        self.uuid = uuid

    def __repr__(self):
        return f"""FuncX Endpoint {self.name}: 
                   {self.core_count} cores,
                   {self.gpu_count} gpus,
                   uuid:{self.uuid},
                   remarks: {self.remarks}"""


blt_endpoints = {
    "blt_small":
    BLTEndpoint(name="blt_small",
                uuid="3c3f0b4f-4ae4-4241-8497-d7339972ff4a",
                core_count=1,
                gpu_count=0,
                remarks="Single Core"),
    "blt_medium":
    BLTEndpoint(name="blt_medium",
                uuid="a145aa44-abfa-4ff8-8131-2097dcdb90e9",
                core_count=4,
                gpu_count=0,
                remarks="4 Cores"),
    "blt_large":
    BLTEndpoint(name="blt_large",
                uuid="f197c41b-95c3-44ae-8218-35b682319a64",
                core_count=8,
                gpu_count=0,
                remarks="8 Cores"),
    "blt_xlarge":
    BLTEndpoint(name="blt_xlarge",
                uuid="b89de769-d0ce-446c-ae04-bdc19266b566",
                core_count=16,
                gpu_count=0,
                remarks="16 Cores"),
    "blt_wholenode":
    BLTEndpoint(name="blt_wholenode",
                uuid="d937af25-8a7e-46e7-a241-68ef4e86b576",
                core_count=48,
                gpu_count=0,
                remarks="Full node (48 core)"),
    "blt_wholenode":
    BLTEndpoint(name="blt_gpu",
                uuid="6d542cd1-140d-47c7-a26a-c0873ec15818",
                core_count=1,
                gpu_count=1,
                remarks="One core and one GPU")
}

# Sleep time in sec
FUNCX_SLEEP_TIME = 5

# Login node FQDN
BLT_LOGIN_ADDRESS = 'mayo.blt.lclark.edu'
