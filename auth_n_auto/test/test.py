from django.test import TestCase
from unittest.mock import patch
# from busines_app.views import external_api_view   #ProductListMock


class MyTestCase(TestCase):
    @patch('myapp.views.requests.get')  # Предположим, что requests.get используется в представлении для обращения к внешнему API
    def test_external_api(self, mock_get):
        # Настраиваем mock объект
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'key': 'value'}

        # response = external_api_view()

        # Проверяем, был ли вызван requests.get с определенным URL
        mock_get.assert_called_with('http://external.api/some/endpoint')

        # Проверяем ответ представления
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'key': 'value'})