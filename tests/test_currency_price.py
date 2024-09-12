import allure
import pytest
from web3 import Web3

from src.contract_abi import contract_abi, fallback_contract_abi
from src.enums.contracts import contract_info, currency_addresses_for_fallback
from utils.helpers import check_currency_price, check_timestamp_interval_between_1_and_latest_rounds, \
    check_aggregator_values_on_int, compare_prices_between_fallback_market_contract, \
    checking_price_changes_after_1800_seconds, check_get_answer_price_vs_latest_answer, \
    check_round_updates_after_1800

# Connect to Haust-Oracle network-testnet  https://haust-testnet-rpc.eu-north-2.gateway.fm
w3 = Web3(Web3.HTTPProvider('https://haust-testnet-rpc.eu-north-2.gateway.fm'))


# Checking network connection
def test_check_connect():
    if not w3.is_connected():
        print("Failed to connect to the network")
    else:
        print("Connected to the network")


# Parameterized test for each currency
@pytest.mark.parametrize("currency,info", contract_info.items())
@allure.feature("Currency price comparison")
@allure.story("Checking the API Coingecko price VS Haust-Oracle aggregators")
def test_check_currency_price(currency, info):
    check_currency_price(currency, info['address'], info['tolerance'], contract_abi)


# Parameterized test for each currency
@pytest.mark.parametrize("currency,info", contract_info.items())
@allure.feature("Timestamp comparison")
@allure.story("Checking the difference between the first round timestamp and latest round timestamp")
def test_timestamp_interval(currency, info):
    # Call the helper function with the required arguments
    check_timestamp_interval_between_1_and_latest_rounds(currency, info)


# Parameterized test for each currency
@pytest.mark.parametrize("currency,info", contract_info.items())
@allure.feature("Aggregator Contract Value Formats")
@allure.story("Checking the formats of initial values returned by the contract")
def test_aggregator_return_values_type(currency, info):
    check_aggregator_values_on_int(currency, info)


@pytest.mark.parametrize("currency,info", currency_addresses_for_fallback.items())
def test_check_fallback_oracle_price_vs_aggregator_price(currency, info):
    contract_info_for_currency = contract_info[currency]
    compare_prices_between_fallback_market_contract(
        currency=currency,
        info=info,
        contract_address=Web3.to_checksum_address(contract_info_for_currency['address']),
        tolerance=contract_info_for_currency['tolerance'],
        contract_abi=contract_abi,
        fallback_contract_abi=fallback_contract_abi
    )


@pytest.mark.parametrize("currency,info", currency_addresses_for_fallback.items())
def test_check_price_changing_after_1800(currency, info):
    contract_info_for_currency = contract_info[currency]
    checking_price_changes_after_1800_seconds(
        currency=currency,
        info=info,
        contract_address=Web3.to_checksum_address(contract_info_for_currency['address']),
        contract_abi=contract_abi,
        fallback_contract_abi=fallback_contract_abi
    )


@pytest.mark.parametrize("currency,info", contract_info.items())
@allure.feature("Comparison latestAnswer price vs getAnswer(latestRound) price")
def test_comparison_latest_answer_price_vs_get_answer_price(currency, info):
    check_get_answer_price_vs_latest_answer(currency, info)


@pytest.mark.skip(reason="Skipping this test for now")
@pytest.mark.parametrize("currency,info", contract_info.items())
@allure.feature("Check price updates in new round")
def test_check_round_updates_after_1800(currency, info):
    check_round_updates_after_1800(currency, info)
