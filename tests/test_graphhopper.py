# -*- coding: utf-8 -*-
# Copyright (C) 2019 GIS OPS UG
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#
"""Tests for the Graphhopper module."""

from routingpy import Graphhopper
from routingpy.direction import Direction, Directions
from routingpy.isochrone import Isochrones, Isochrone
from routingpy.matrix import Matrix

from tests.test_helper import *
import tests as _test

import json
import responses
from copy import deepcopy


class GraphhopperTest(_test.TestCase):
    name = 'graphhopper'

    def setUp(self):
        self.key = 'sample_key'
        self.client = Graphhopper(api_key=self.key)

    @responses.activate
    def test_full_directions(self):
        query = ENDPOINTS_QUERIES[self.name]['directions']

        responses.add(
            responses.GET,
            'https://graphhopper.com/api/1/route',
            status=200,
            json=ENDPOINTS_RESPONSES[self.name]['directions'],
            content_type='application/json')

        routes = self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://graphhopper.com/api/1/route?algorithm=alternative_route&alternative_route.max_paths=2&'
            'alternative_route.max_weight_factor=1.7&alternative_route_max_share_factor=0.7&avoid=tunnel%3Bford&'
            'block_area=48.23424%2C8.34234&calc_points=false&ch.disable=true&debug=true&details=time&details=tolls&'
            'elevation=true&heading=50%2C50%2C50&heading_penalty=100&instructions=false&key=sample_key&locale=en&'
            'optimize=true&pass_through=true&point=49.415776%2C8.680916&point=49.420577%2C8.688641&'
            'point=49.445776%2C8.780916&point_hint=false&points_encoded=true&profile=car&type=json&weighting=short_fastest',
            responses.calls[0].request.url)

    @responses.activate
    def test_directions_object_response(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['directions'])
        query['algorithm'] = None

        responses.add(
            responses.GET,
            'https://graphhopper.com/api/1/route',
            status=200,
            json=ENDPOINTS_RESPONSES[self.name]['directions'],
            content_type='application/json')

        routes = self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://graphhopper.com/api/1/route?avoid=tunnel%3Bford&'
            'block_area=48.23424%2C8.34234&calc_points=false&ch.disable=true&debug=true&details=time&details=tolls&'
            'elevation=true&heading=50%2C50%2C50&heading_penalty=100&instructions=false&key=sample_key&locale=en&'
            'optimize=true&pass_through=true&point=49.415776%2C8.680916&point=49.420577%2C8.688641&'
            'point=49.445776%2C8.780916&point_hint=false&points_encoded=true&profile=car&type=json&weighting=short_fastest',
            responses.calls[0].request.url)

        self.assertIsInstance(routes, Direction)
        self.assertIsInstance(routes.geometry, list)
        self.assertIsInstance(routes.duration, int)
        self.assertIsInstance(routes.distance, int)

    @responses.activate
    def test_directions_object_response_alternatives(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['directions'])

        responses.add(
            responses.GET,
            'https://graphhopper.com/api/1/route',
            status=200,
            json=ENDPOINTS_RESPONSES[self.name]['directions'],
            content_type='application/json')

        routes = self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://graphhopper.com/api/1/route?algorithm=alternative_route&alternative_route.max_paths=2&'
            'alternative_route.max_weight_factor=1.7&alternative_route_max_share_factor=0.7&avoid=tunnel%3Bford&'
            'block_area=48.23424%2C8.34234&calc_points=false&ch.disable=true&debug=true&details=time&details=tolls&'
            'elevation=true&heading=50%2C50%2C50&heading_penalty=100&instructions=false&key=sample_key&locale=en&'
            'optimize=true&pass_through=true&point=49.415776%2C8.680916&point=49.420577%2C8.688641&'
            'point=49.445776%2C8.780916&point_hint=false&points_encoded=true&profile=car&type=json&weighting=short_fastest',
            responses.calls[0].request.url)

        self.assertIsInstance(routes, Directions)
        self.assertIsInstance(routes[0], Direction)
        self.assertIsInstance(routes[1], Direction)
        self.assertIsInstance(routes[2], Direction)
        self.assertIsInstance(routes[0].geometry, list)
        self.assertIsInstance(routes[1].geometry, list)
        self.assertIsInstance(routes[2].geometry, list)

    @responses.activate
    def test_full_isochrones_response_object(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['isochrones'])
        query['buckets'] = 3

        responses.add(
            responses.GET,
            'https://graphhopper.com/api/1/isochrone',
            status=200,
            json=ENDPOINTS_RESPONSES[self.name]['isochrones'],
            content_type='application/json')

        isochrones = self.client.isochrones(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://graphhopper.com/api/1/isochrone?buckets=3&debug=false&key=sample_key&'
            'point=48.23424%2C8.34234&profile=car&reverse_flow=true&time_limit=1000',
            responses.calls[0].request.url)

        self.assertIsInstance(isochrones, Isochrones)
        self.assertIsInstance(isochrones[0], Isochrone)
        self.assertIsInstance(isochrones[1], Isochrone)
        self.assertIsInstance(isochrones[2], Isochrone)
        self.assertIsInstance(isochrones[0].geometry, object)
        self.assertIsInstance(isochrones[1].geometry, object)
        self.assertIsInstance(isochrones[2].geometry, object)

    @responses.activate
    def test_full_matrix(self):
        query = ENDPOINTS_QUERIES[self.name]['matrix']

        responses.add(
            responses.GET,
            'https://graphhopper.com/api/1/matrix',
            status=200,
            json=ENDPOINTS_RESPONSES[self.name]['matrix'],
            content_type='application/json')

        matrix = self.client.distance_matrix(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://graphhopper.com/api/1/matrix?key=sample_key&out_array=distances&out_array=times&out_array=weights&'
            'point=49.415776%2C8.680916&point=49.420577%2C8.688641&point=49.445776%2C8.780916&profile=car&debug=true',
            responses.calls[0].request.url)

        self.assertIsInstance(matrix, Matrix)
        self.assertIsInstance(matrix.durations, list)
        self.assertIsInstance(matrix.distances, list)

    @responses.activate
    def test_few_sources_destinations_matrix(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['matrix'])
        query['sources'] = [1]

        responses.add(
            responses.GET,
            'https://graphhopper.com/api/1/matrix',
            status=200,
            json={},
            content_type='application/json')
        resp = self.client.distance_matrix(**query)

        query['sources'] = None
        query['destinations'] = [1]

        responses.add(
            responses.GET,
            'https://graphhopper.com/api/1/matrix',
            status=200,
            json={},
            content_type='application/json')

        resp = self.client.distance_matrix(**query)

        self.assertEqual(2, len(responses.calls))
        self.assertURLEqual(
            'https://graphhopper.com/api/1/matrix?from_point=49.415776%2C8.680916&key=sample_key&out_array=distances'
            '&out_array=times&out_array=weights&profile=car&to_point=49.415776%2C8.680916&to_point=49.420577%2C8.688641&'
            '&to_point=49.445776%2C8.780916&debug=true',
            responses.calls[0].request.url)
        self.assertURLEqual(
            'https://graphhopper.com/api/1/matrix?from_point=49.415776%2C8.680916&from_point=49.420577%2C8.688641&'
            'from_point=49.445776%2C8.780916&key=sample_key&out_array=distances&out_array=times&out_array=weights&'
            'profile=car&to_point=49.415776%2C8.680916&debug=true',
            responses.calls[1].request.url)

    def test_index_sources_matrix(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['matrix'])
        query['sources'] = [100]

        self.assertRaises(
            IndexError, lambda: self.client.distance_matrix(**query))

    def test_index_destinations_matrix(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['matrix'])
        query['destinations'] = [100]

        self.assertRaises(
            IndexError, lambda: self.client.distance_matrix(**query))
