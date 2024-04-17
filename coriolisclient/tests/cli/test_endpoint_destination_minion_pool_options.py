# Copyright 2024 Cloudbase Solutions Srl
# All Rights Reserved.

from cliff import lister
from unittest import mock

from coriolisclient.cli import endpoint_destination_minion_pool_options
from coriolisclient.cli import utils as cli_utils
from coriolisclient.tests import test_base


class EndpointDestinationMinionPoolOptionsFormatterTestCase(
        test_base.CoriolisBaseTestCase):
    """
    Test suite for the Coriolis Client Endpoint Destination Minion Pool
    Options Formatter.
    """

    def setUp(self):
        super(EndpointDestinationMinionPoolOptionsFormatterTestCase, self
              ).setUp()
        self.endpoint = (endpoint_destination_minion_pool_options.
                         EndpointDestinationMinionPoolOptionsFormatter)()

    def test_get_sorted_list(self):
        obj1 = mock.Mock()
        obj2 = mock.Mock()
        obj3 = mock.Mock()
        obj1.name = "app1"
        obj2.name = "app2"
        obj3.name = "app3"
        obj_list = [obj2, obj1, obj3]

        result = self.endpoint._get_sorted_list(obj_list)

        self.assertEqual(
            [obj1, obj2, obj3],
            result
        )

    @mock.patch.object(cli_utils, 'format_json_for_object_property')
    def test_get_formatted_data(self, mock_format_json_for_object_property):
        obj = mock.Mock()
        obj.name = mock.sentinel.name
        obj.to_dict = mock.Mock(
            return_value={"config_default": mock.sentinel.config_default}
        )

        result = self.endpoint._get_formatted_data(obj)

        self.assertEqual(
            (
                mock.sentinel.name,
                mock_format_json_for_object_property.return_value,
                mock.sentinel.config_default
            ),
            result
        )


class ListEndpointDestinationMinionPoolOptionsTestCase(
        test_base.CoriolisBaseTestCase):
    """
    Test suite for the Coriolis Client List Endpoint Destination Minion Pool
    Options.
    """

    def setUp(self):
        self.mock_app = mock.Mock()
        super(ListEndpointDestinationMinionPoolOptionsTestCase, self).setUp()
        self.endpoint = (endpoint_destination_minion_pool_options.
                         ListEndpointDestinationMinionPoolOptions)(
                             self.mock_app, mock.sentinel.app_args)

    @mock.patch.object(cli_utils, 'add_args_for_json_option_to_parser')
    @mock.patch.object(lister.Lister, 'get_parser')
    def test_get_parser(
        self,
        mock_get_parser,
        mock_add_args_for_json_option_to_parser
    ):
        result = self.endpoint.get_parser(mock.sentinel.prog_name)

        self.assertEqual(
            mock_get_parser.return_value,
            result
        )
        mock_get_parser.assert_called_once_with(mock.sentinel.prog_name)
        mock_add_args_for_json_option_to_parser.assert_called_once_with(
            mock_get_parser.return_value, 'environment')

    @mock.patch.object(endpoint_destination_minion_pool_options.
                       EndpointDestinationMinionPoolOptionsFormatter,
                       'list_objects')
    @mock.patch.object(cli_utils, 'get_option_value_from_args')
    def test_take_action(
        self,
        mock_get_option_value_from_args,
        mock_list_objects
    ):
        args = mock.Mock()
        args.options = mock.sentinel.options
        mock_endpoints = mock.Mock()
        mock_empdo = mock.Mock()
        self.mock_app.client_manager.coriolis.endpoints = mock_endpoints
        mock_empdo = (self.mock_app.client_manager.coriolis.
                      endpoint_destination_minion_pool_options)

        result = self.endpoint.take_action(args)

        self.assertEqual(
            mock_list_objects.return_value,
            result
        )
        mock_get_option_value_from_args.assert_called_once_with(
            args, 'environment', error_on_no_value=False)
        mock_empdo.list.assert_called_once_with(
            mock_endpoints.get_endpoint_id_for_name(args.endpoint),
            environment=mock_get_option_value_from_args.return_value,
            option_names=mock.sentinel.options
        )
        mock_list_objects.assert_called_once_with(mock_empdo.list.return_value)
