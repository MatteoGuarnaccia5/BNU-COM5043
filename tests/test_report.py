

from src.orders.reportsHandler import ReportHandler
from tests.test_order import TEST_CUSTOMER_ORDER, TEST_SUPPLIER_ORDER

from unittest.mock import patch

# from src.api.order import OrderAPI

def test_calc_cost():
    with patch("src.api.order.OrderAPI.listSupplierOrders", return_value=[TEST_SUPPLIER_ORDER]*10):

        assert ReportHandler().calc_stock_costs() == 25

def test_calc_revenue():
    with patch("src.api.order.OrderAPI.listCustomerOrders", return_value=[TEST_CUSTOMER_ORDER]*10):

        assert ReportHandler().calc_sales_revenue() == 50