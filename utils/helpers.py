import time
from datetime import datetime
from decimal import Decimal, ROUND_DOWN

import pytest
import requests
from web3 import Web3
from web3.exceptions import ContractLogicError

from src.contract_abi import contract_abi

w3 = Web3(Web3.HTTPProvider('https://haust-testnet-rpc.eu-north-2.gateway.fm'))


# Helper function for checking currency price in contracts
#1
def check_currency_price(currency, contract_address, tolerance, contract_abi):
    try:
        # Creating a Contract Object
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)

        # Getting the last round
        latest_round = contract.functions.latestRound().call()

        # Getting the price from the contract using the last round
        contract_price = contract.functions.getAnswer(latest_round).call()

        # Getting price with CoinGecko
        url = f'https://api.coingecko.com/api/v3/simple/price?ids={currency}&vs_currencies=usd'
        response = requests.get(url)
        price_data = response.json()

        # Checking that the key for the currency exists in the response
        if currency in price_data:
            market_price = Decimal(price_data[currency]['usd'])
            market_price = market_price.quantize(Decimal('1.00000000'), rounding=ROUND_DOWN)

            # Converting the contract price into a comparable format
            haust_contract_price = str(contract_price)
            if currency in ['bitcoin', 'ethereum']:
                # Round market_price to an integer and convert it to a string
                rounded_market_price_str = str(int(market_price))

                # Determine the length of the rounded market_price string
                len_int_part = len(rounded_market_price_str)

                # Insert a dot before the last len_int_part characters
                contract_price = Decimal(f"{haust_contract_price[:len_int_part]}.{haust_contract_price[len_int_part:]}")
            elif haust_contract_price.startswith('9'):
                correct_haust_contract_price = '0' + haust_contract_price
                contract_price = Decimal(f"{correct_haust_contract_price[0]}.{correct_haust_contract_price[1:]}")
            else:
                contract_price = Decimal(f"{haust_contract_price[0]}.{haust_contract_price[1:]}")
                print(contract_price)
                print(market_price)
            # Compare prices
            assert abs(market_price - contract_price) <= market_price * tolerance, (
                f"Price mismatch for {currency.upper()}: "
                f"Market price = {market_price}, Contract price = {contract_price}"
            )
        else:
            pytest.fail(f"Price for {currency.upper()} not found in CoinGecko response")

    except Exception as e:
        pytest.fail(f"Error checking {currency.upper()} price: {e}")

# 2
def check_timestamp_interval_between_1_and_latest_rounds(currency, info, tolerance=0.005):
    # Creating a Contract Object
    contract = w3.eth.contract(address=info['address'], abi=contract_abi)

    # Getting the first round and its timestamp
    start_timestamp = contract.functions.getTimestamp(1).call()

    # Getting the latest round and its timestamp
    latest_round = contract.functions.latestRound().call()
    print(latest_round)
    latest_timestamp = contract.functions.getTimestamp(latest_round).call()
    print(latest_timestamp)

    # Debugging Output
    print(f"Currency: {currency.upper()}")
    print(f"Latest Round: {latest_round}, Latest Timestamp: {latest_timestamp}")

    # Expected intervals quantity
    expected_intervals = latest_round - 1

    # Expected time difference
    expected_time_difference = expected_intervals * 1800  # 30 minutes per round

    # Getting the previous round and its timestamp
    previous_round = latest_round - 1
    previous_timestamp = contract.functions.getTimestamp(previous_round).call()

    # Debugging Output
    print(f"Previous Round: {previous_round}, Previous Timestamp: {previous_timestamp}")

    # Calculate the time difference between the two rounds
    difference_latest_vs_previous_timestamp = latest_timestamp - previous_timestamp

    # Debugging Output
    print(f"Difference in Timestamps: {difference_latest_vs_previous_timestamp}")

    # Expected time difference between two neighboring rounds (e.g., 1800 seconds)
    expected_time_between_two_neighbour_rounds = 1800

    # Assert the time difference is within the expected range, considering the tolerance
    assert (expected_time_between_two_neighbour_rounds * (
            1 - tolerance)) <= difference_latest_vs_previous_timestamp <= (
                   expected_time_between_two_neighbour_rounds * (1 + tolerance)), (
        f"Timestamp error for {currency.upper()}: "
        f"Expected time difference around {expected_time_between_two_neighbour_rounds} seconds "
        f"with a tolerance of {tolerance * 100}%, "
        f"but received {difference_latest_vs_previous_timestamp} seconds."
    )

    if currency in ['bitcoin', 'ethereum', 'usd-coin']:
        # Actual time difference + add (int) an error in seconds in case of failure/stopping in transactions
        actual_time_difference = (latest_timestamp - start_timestamp) + 2940
    elif currency in ['tether']:
        actual_time_difference = (latest_timestamp - start_timestamp) + 50
    else:
        # Actual time difference
        actual_time_difference = latest_timestamp - start_timestamp

    print(f"Actual timestamp: {actual_time_difference}")
    print(f"Expected timestamp: {expected_time_difference}")
    # Calculate tolerance range
    lower_bound = expected_time_difference * (1 - tolerance)
    upper_bound = expected_time_difference * (1 + tolerance)

    # Checking within tolerance range
    # assert lower_bound <= actual_time_difference <= upper_bound, (
    #     f"Timestamp error for {currency.upper()}: "
    #     f"Expected time difference {expected_time_difference} seconds "
    #     f"with a tolerance of {tolerance * 100}%, "
    #     f"but received {actual_time_difference} seconds."
    # )

# 3
def check_aggregator_values_on_int(currency, info):
    # Creating a Contract Object
    contract = w3.eth.contract(address=info['address'], abi=contract_abi)

    # Checking if latestRound is of type int
    latest_round = contract.functions.latestRound().call()
    assert isinstance(latest_round, int), f"latestRound is not an int for {currency.upper()}"

    # Getting the price from the contract using the last round
    contract_price = contract.functions.getAnswer(latest_round).call()
    assert isinstance(contract_price, int), f"getAnswer is not an int for {currency.upper()}"

    # Checking if latestAnswer is of type int
    latest_answer = contract.functions.latestAnswer().call()
    assert isinstance(latest_answer, int), f"latestAnswer is not an int for {currency.upper()}"

    # Checking if latestTimestamp is of type int
    latest_timestamp = contract.functions.latestTimestamp().call()
    assert isinstance(latest_timestamp, int), f"latestTimestamp is not an int for {currency.upper()}"

    # Checking if getAnswer returns an int for a specific round (e.g., round 1)
    answer_for_round_1 = contract.functions.getAnswer(1).call()
    assert isinstance(answer_for_round_1, int), f"getAnswer(1) is not an int for {currency.upper()}"

# 4
def compare_prices_between_fallback_market_contract(currency, info, contract_address, tolerance, contract_abi,
                                                    fallback_contract_abi):
    try:
        # Initialize the fallback contract
        oracle_address = Web3.to_checksum_address('0x8904fF78BAFDea87680e79eF1ccAF1ab6E7d0e0E')
        fallback_contract = w3.eth.contract(address=oracle_address, abi=fallback_contract_abi)

        # Asset address (assuming this asset's price is already set in the contract)
        # asset_address = Web3.to_checksum_address(info['address'])  # USDT

        # Retrieve the price from the fallback oracle
        fallback_price = fallback_contract.functions.getAssetPrice(info['address']).call()
        assert isinstance(fallback_price, int), f"Fallback oracle price should be int, got {type(fallback_price)}"
        print(fallback_price)

        # Initialize the main contract
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)

        # Get the latest round and the contract price from the aggregator
        latest_round = contract.functions.latestRound().call()
        contract_price = contract.functions.getAnswer(latest_round).call()

        # Retrieve market price using CoinGecko API
        url = f'https://api.coingecko.com/api/v3/simple/price?ids={currency}&vs_currencies=usd'
        response = requests.get(url)
        price_data = response.json()

        # Check that the key for the currency exists in the response
        if currency in price_data:
            market_price = Decimal(price_data[currency]['usd'])
            market_price = market_price.quantize(Decimal('1.00000000'), rounding=ROUND_DOWN)

            # Convert contract price into a comparable format
            haust_contract_price = str(contract_price)
            if currency in ['bitcoin', 'ethereum']:
                len_int_part = len(str(int(market_price)))
                contract_price = Decimal(f"{haust_contract_price[:len_int_part]}.{haust_contract_price[len_int_part:]}")
            elif haust_contract_price.startswith('9'):
                correct_haust_contract_price = '0' + haust_contract_price
                contract_price = Decimal(f"{correct_haust_contract_price[0]}.{correct_haust_contract_price[1:]}")
            else:
                contract_price = Decimal(f"{haust_contract_price[0]}.{haust_contract_price[1:]}")

            # Normalize fallback price for comparison if needed
            fallback_price_str = str(fallback_price)
            if fallback_price_str.startswith('9'):
                # If fallback price starts with 9, we assume it might have been a decimal
                correct_fallback_price_str = '0' + fallback_price_str
                fallback_price = Decimal(f"{correct_fallback_price_str[0]}.{correct_fallback_price_str[1:]}")
            elif len(fallback_price_str) > len(str(int(market_price))):
                # Fallback price might be in a larger scale, convert it similarly
                len_int_part = len(str(int(market_price)))
                fallback_price = Decimal(f"{fallback_price_str[:len_int_part]}.{fallback_price_str[len_int_part:]}")
            else:
                fallback_price = Decimal(f"{fallback_price_str[0]}.{fallback_price_str[1:]}")

            # Compare prices between market and fallback oracle
            assert abs(market_price - fallback_price) <= market_price * tolerance, (
                f"Price mismatch for {currency.upper()}: "
                f"Market price = {market_price}, Fallback price = {fallback_price}"
            )

            # Compare prices between fallback oracle and contract (aggregator)
            assert abs(fallback_price - contract_price) <= fallback_price * tolerance, (
                f"Price mismatch for {currency.upper()}: "
                f"Fallback price = {fallback_price}, Contract price = {contract_price}"
            )

    except ContractLogicError as e:
        print(f"ContractLogicError when getting price: {str(e)}")
        assert False, f"ContractLogicError when getting price: {str(e)}"

    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        assert False, f"Unexpected error: {str(e)}"

# 5
def checking_price_changes_after_1800_seconds(currency, info, contract_address, contract_abi, fallback_contract_abi):
    # Convert oracle address
    oracle_address = Web3.to_checksum_address('0x8904fF78BAFDea87680e79eF1ccAF1ab6E7d0e0E')
    fallback_contract = w3.eth.contract(address=oracle_address, abi=fallback_contract_abi)

    # Create a contract Object
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    # Getting the latest price for an aggregator and latest Timestamp as start position for counting 30 minutes
    latest_price_aggregator = contract.functions.latestAnswer().call()

    # Getting the latest price for Fallback-Oracle
    latest_price_fallback_oracle = fallback_contract.functions.getAssetPrice(info['address']).call()

    print(f"Aggregator price: {currency}:{latest_price_aggregator}")
    print(f"Fallback-Oracle:{currency}:{latest_price_fallback_oracle}")

    start_timestamp = contract.functions.latestTimestamp().call()

    # Convert the provided timestamp (seconds since epoch) to a datetime object
    target_time = datetime.fromtimestamp(start_timestamp + 1800)
    print(f"Starting Time {start_timestamp}, Target Time: {target_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Poll the blockchain for new blocks until 30 minutes have passed
    while True:
        current_block = w3.eth.get_block('latest')
        current_time = datetime.now()

        # Check if 30 minutes have passed
        if current_time >= target_time:
            print("30 minutes have passed. Fetching latest data...")
            break

        # Wait a few seconds before checking the block again
        time.sleep(10)
    # Fetch latest price again after 30 minutes for aggregator and fallback oracle
    time.sleep(20)
    latest_price_aggregator_after_1800 = contract.functions.latestAnswer().call()
    latest_timestamp_after_1800 = contract.functions.latestTimestamp().call()

    latest_price_fallback_oracle_after_1800 = fallback_contract.functions.getAssetPrice(info['address']).call()

    print(f"Aggregator price after 30 minutes: {currency}:{latest_price_aggregator_after_1800}")
    print(f"Fallback-Oracle price after 30 minutes:{currency}:{latest_price_fallback_oracle_after_1800}")
    print(f"Latest timestamp after 30 min: {latest_timestamp_after_1800}")

    # Assert that the Timestamp has changed after 30 minutes. If the Timestamp hasn't changed, raise an error with a detailed message
    assert (1800 * (1 - 0.005)) <= (latest_timestamp_after_1800 - start_timestamp) <= (1800 * (1 + 0.005)),\
        f"Timestamp difference is less than 1800 seconds." \
        f" Start timestamp: {start_timestamp}," \
        f" Latest timestamp after 30 minutes: {latest_timestamp_after_1800}," \
        f" Difference: {latest_timestamp_after_1800 - start_timestamp} seconds"

    # Assert that the price has changed after 30 minutes. If the price hasn't changed, raise an error with a detailed message
    assert latest_price_aggregator != latest_price_aggregator_after_1800,\
        f"Aggregator price did not change after 30 minutes. Initial price: {latest_price_aggregator}," \
        f" Price after 30 minutes: {latest_price_aggregator_after_1800}"

    # Assert that the price has changed after 30 minutes. If the price hasn't changed, raise an error with a detailed message
    assert latest_price_fallback_oracle != latest_price_fallback_oracle_after_1800,\
        f"Fallback Oracle price did not change after 30 minutes. Initial price: {latest_price_fallback_oracle}," \
        f" Price after 30 minutes: {latest_price_fallback_oracle_after_1800}"


# 6
def check_get_answer_price_vs_latest_answer(currency, info):
    contract = w3.eth.contract(address=info['address'], abi=contract_abi)

    latest_round = contract.functions.latestRound().call()

    # Get price by using getAnswer
    actual_price = contract.functions.getAnswer(latest_round).call()
    latest_answer_price = contract.functions.latestAnswer().call()

    assert actual_price == latest_answer_price,\
        f"Error: Price mismatch! Expected price from aggregator: {latest_answer_price}, but got: {actual_price}"

# 7
def check_round_updates_after_1800(currency, info):
    contract = w3.eth.contract(address=info['address'], abi = contract_abi)

    latest_round = contract.functions.latestRound().call()

    # Get latest timestamp
    start_timestamp = contract.functions.latestTimestamp().call()
    # Convert the provided timestamp (seconds since epoch) to a datetime object
    target_time = datetime.fromtimestamp(start_timestamp + 1800)

    while True:
        current_time = datetime.now()

        # Check if 30 minutes have passed
        if current_time >= target_time:
            print("30 minutes have passed. Fetching latest data...")
            break

        # Wait a few seconds before checking the block again
        time.sleep(10)

    latest_round_after_1800 = contract.functions.latestRound().call()
    latest_round_timestamp = contract.functions.latestTimestamp().call()

    assert (latest_round_after_1800 - latest_round) == 1,\
        f"Error: Round mismatch! Expected the next round to be {latest_round + 1}," \
        f" but got {latest_round_after_1800}. Check if a new round has been initiated after the wait time."

    assert (latest_round_timestamp - (start_timestamp + 1800)) <= 30,\
        f"The previous round timestamp: {start_timestamp} is different from the latest round timestamp: {latest_round_timestamp}!"
