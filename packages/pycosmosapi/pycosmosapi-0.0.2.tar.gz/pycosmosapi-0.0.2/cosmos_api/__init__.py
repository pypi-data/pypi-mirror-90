#!/usr/bin/python
#
# Copyright 2020 - A.L.I Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
This is the API development for COSMOS-API.
"""
import requests
import json

class Telemetry():
    """
    Simple Request maker for cosmos communication:
    - generate EndPoint for server.
    - generate hearder.
    - method to post telemetry json to server.
    """
    cosmos_ip = "dmtest.cosmos.ali.jp"

    def __init__(self, api_token):
        # Generate EndPoint URL

        self.generate_EndPoint()

        # Generate hearders
        self.token = api_token
        self.default_header = self.generate_header()
        self.json_header = self.generate_json_header()

        # Print ED ~ Status
        self.print_ED()

    def generate_EndPoint(self):
        # Generate EndPoint for Remote Server.
        self.ED_telemetry = 'https://' + Telemetry.cosmos_ip + '/api/drone/updatetm'
        self.ED_operation = 'https://' + Telemetry.cosmos_ip + '/api/drone/myoperation'

    def generate_header(self):
        # Generate simple header with token.
        return({'X-Api-Key': '{0}'.format(self.token)})

    def generate_json_header(self):
        # Generate header with data specification.
        header = {'Content-Type': 'application/json',
                    'Accept':'application/json',
                    'X-Api-Key': '{0}'.format(self.token)}
        return(header)

    def print_ED(self):
        # Print out EndPoint for information.
        print("\nCOSMOS_Requests initialized with:")
        print("  Token: {}".format(self.default_header))
        print("  ED_telemetry: {}".format(self.ED_telemetry))
        print("  ED_operation: {}\n".format(self.ED_operation))

    def send_telemetry(self, vehicle_state_json):
        # Dumps vehicle_state and Post telemetry data to ED_telemetry:
        response = requests.post(self.ED_telemetry,
                                headers=self.json_header,
                                data=json.dumps(vehicle_state_json))
        return(response)

    def parse_operation(self, response):
        # Parse the operation json response
        operation = response.json()
        MOCA = int(operation["local_flight_alt"])
        waypoints = operation["waypoints"]
        mission = operation["missions"]
        return(MOCA, waypoints, mission)

    def get_operation(self):
        # Get request to extract operation details.
        response = requests.get(url=self.ED_operation, headers=self.default_header)
        if response.status_code == 200:
            try:
                MOCA, waypoints, missions = self.parse_operation(response)
                print("MOCA: {} meters.".format(MOCA))
                print("WayPoints:\n {}".format(waypoints))
                print("Missions:\n {}".format(missions))

            except Exception as e:
                print("Enable to parse operation: {}.".format(e))

        return(response)
