# coding: utf-8

"""
    Aliro Quantum App

    This is an api for the Aliro Quantum App  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: nick@aliroquantum.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import aliro_quantum
from aliro_quantum.models.device_details import DeviceDetails  # noqa: E501
from aliro_quantum.rest import ApiException

class TestDeviceDetails(unittest.TestCase):
    """DeviceDetails unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test DeviceDetails
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = aliro_quantum.models.device_details.DeviceDetails()  # noqa: E501
        if include_optional :
            return DeviceDetails(
                active_reset_fidelity = 1.337, 
                depth_one_circuit_time = 1.337, 
                device_id = '0', 
                display_name = '0', 
                gate_info = aliro_quantum.models.device_details_gate_info.DeviceDetails_gateInfo(
                    averages = {
                        'key' : aliro_quantum.models.device_details_gate_info_averages.DeviceDetails_gateInfo_averages(
                            current = 1.337, 
                            fidelity_change_per_day = 1.337, )
                        }, 
                    gate_list = [
                        aliro_quantum.models.gate.Gate(
                            aliro_computed = True, 
                            fidelity = 1.337, 
                            fidelity_change_per_day = 1.337, 
                            qubit_from = aliro_quantum.models.qubit.Qubit(
                                name = 56, 
                                pos_x = 1.337, 
                                pos_y = 1.337, 
                                real_qubit = 56, 
                                t1 = 1.337, 
                                t2 = 1.337, ), 
                            qubit_to = aliro_quantum.models.qubit.Qubit(
                                name = 56, 
                                pos_x = 1.337, 
                                pos_y = 1.337, 
                                real_qubit = 56, 
                                t1 = 1.337, 
                                t2 = 1.337, ), 
                            gate_type = '0', )
                        ], ), 
                gates = [
                    aliro_quantum.models.gate.Gate(
                        aliro_computed = True, 
                        fidelity = 1.337, 
                        fidelity_change_per_day = 1.337, 
                        qubit_from = aliro_quantum.models.qubit.Qubit(
                            name = 56, 
                            pos_x = 1.337, 
                            pos_y = 1.337, 
                            real_qubit = 56, 
                            t1 = 1.337, 
                            t2 = 1.337, ), 
                        qubit_to = aliro_quantum.models.qubit.Qubit(
                            name = 56, 
                            pos_x = 1.337, 
                            pos_y = 1.337, 
                            real_qubit = 56, 
                            t1 = 1.337, 
                            t2 = 1.337, ), 
                        gate_type = '0', )
                    ], 
                initialization_time = 1.337, 
                is_simulator = True, 
                jobs_queue_size = 56, 
                last_calibration = '0', 
                max_shots = 56, 
                next_available_time = '0', 
                price = 1.337, 
                quantum_volume = 56, 
                qubits = {
                    'key' : aliro_quantum.models.qubit.Qubit(
                        name = 56, 
                        pos_x = 1.337, 
                        pos_y = 1.337, 
                        real_qubit = 56, 
                        t1 = 1.337, 
                        t2 = 1.337, )
                    }, 
                supports_mid_circuit_measurement = True, 
                t1 = 1.337, 
                t2 = 1.337
            )
        else :
            return DeviceDetails(
        )

    def testDeviceDetails(self):
        """Test DeviceDetails"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
