from decimal import Decimal

from web3 import Web3

# Convert addresses to checksum format
currency_addresses_for_fallback = {
    'tether': {
        'address': Web3.to_checksum_address('0xb9fdfad79cd511bf5ad103174b396818cfd88f46'),  # USDT
        'tolerance': Decimal('0.01'),
    },
    'usd-coin': {
        'address': Web3.to_checksum_address('0x94a8efd7344cd4eb8ddbca213cb2bc4ee9fa5d91'),  # USDC
        'tolerance': Decimal('0.01'),
    },
    'bitcoin': {
        'address': Web3.to_checksum_address('0xa8ecbe9f78f9084c3978949c63eeb0091762a0f9'),  # BTC
        'tolerance': Decimal('0.1'),
    },
    'ethereum': {
        'address': Web3.to_checksum_address('0x6f1d95c5fa387045a653eb6ebaf4cba1501eeceb'),  # ETH
        'tolerance': Decimal('0.05'),
    },
}

contract_info = {
    'tether': {
        'address': '0x44ca92865B34a89F5e26E2ccAe0d9fd2F7B42b9c',  # USDT
        'tolerance': Decimal('0.01'),
    },
    'usd-coin': {
        'address': '0xec2a4fe923460af4148a20ffA1a7d85444AA52fd',  # USDC
        'tolerance': Decimal('0.01'),
    },
    'bitcoin': {
        'address': '0xcb976D54A3CE7CC5d039361fFAd9C260bf33D932',  # BTC
        'tolerance': Decimal('0.1'),
    },
    'ethereum': {
        'address': '0x9d1564A0f5C182757d19aB821A1de1F91B681779',  # ETH
        'tolerance': Decimal('0.05'),
    },
}
