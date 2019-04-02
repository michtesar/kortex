#! /usr/bin/env python3

###
# KINOVA (R) KORTEX (TM)
#
# Copyright (c) 2018 Kinova inc. All rights reserved.
#
# This software may be modified and distributed
# under the terms of the BSD 3-Clause license.
#
# Refer to the LICENSE file for details.
#
###

from kortex_api.UDPTransport import UDPTransport
from kortex_api.RouterClient import RouterClient
from kortex_api.SessionManager import SessionManager

from kortex_api.autogen.client_stubs.DeviceConfigClientRpc import DeviceConfigClient
from kortex_api.autogen.client_stubs.BaseClientRpc import BaseClient

from kortex_api.autogen.messages import DeviceConfig_pb2, Session_pb2, Base_pb2, Errors_pb2

from kortex_api.Exceptions.KServerException import KServerException

def example_error_management(base_service):

    try:
        base_service.CreateUserProfile(Base_pb2.FullUserProfile())

    except KServerException as ex:
        # Get error and sub error codes
        error_code = ex.get_error_code()
        sub_error_code = ex.get_error_sub_code()
        print("error_code:{0} sub_error_code:{1} ".format(error_code, sub_error_code))

        # Error exception to string (here the try/except addresses an known issue that will be fixed in a future version)
        try:
            print("Error: {0}".format(ex))
        except Exception:
            print("Unknown error details for error_code:{0} sub_error_code:{1} ".format(error_code, sub_error_code))
    
    except Exception:
        import sys
        print("generic exception: {0}".format(sys.exc_info()[0]))


if __name__ == "__main__":

    DEVICE_IP = "192.168.1.10"
    DEVICE_PORT = 10000

    # Setup API
    errorCallback = lambda kException: print("_________ callback error _________ {}".format(kException))
    transport = UDPTransport()
    router = RouterClient(transport, errorCallback)
    transport.connect(DEVICE_IP, DEVICE_PORT)

    # Create session
    session_info = Session_pb2.CreateSessionInfo()
    session_info.username = 'admin'
    session_info.password = 'admin'
    session_info.session_inactivity_timeout = 60000   # (milliseconds)
    session_info.connection_inactivity_timeout = 2000 # (milliseconds)

    session_manager = SessionManager(router)
    session_manager.CreateSession(session_info)

    # Create required services
    base_service = BaseClient(router)

    # Example core
    example_error_management(base_service)

    # Close API session
    session_manager.CloseSession()

    # Deactivate the router and cleanly disconnect from the transport object
    router.SetActivationStatus(False)
    transport.disconnect()