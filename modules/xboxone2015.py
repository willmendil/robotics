import approxeng.input.controllers
from approxeng.input.xboxone import WiredXBoxOneSPad


VENDOR_ID = 1118
PRODUCT_ID = 733

approxeng.input.controllers.CONTROLLERS.append({'constructor': WiredXBoxOneSPad,
                                                'vendor_id': VENDOR_ID,
                                                'product_id': PRODUCT_ID})
