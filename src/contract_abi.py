contract_abi = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "oracle",
                "type": "address"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "int256",
                "name": "current",
                "type": "int256"
            },
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "roundId",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "updatedAt",
                "type": "uint256"
            }
        ],
        "name": "AnswerUpdated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "roundId",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "startedBy",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "startedAt",
                "type": "uint256"
            }
        ],
        "name": "NewRound",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "roundId",
                "type": "uint256"
            }
        ],
        "name": "getAnswer",
        "outputs": [
            {
                "internalType": "int256",
                "name": "answer",
                "type": "int256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "roundId",
                "type": "uint256"
            }
        ],
        "name": "getTimestamp",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "timeStamp",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "latestAnswer",
        "outputs": [
            {
                "internalType": "int256",
                "name": "answer",
                "type": "int256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "latestRound",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "roundId",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "latestTimestamp",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "timeStamp",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "int256",
                "name": "price",
                "type": "int256"
            }
        ],
        "name": "setAnswer",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]


fallback_contract_abi = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "oracle_",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "ethereum_",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "haustPoolUSDT_",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "haustPoolUSDC_",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "usdt_",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "usdc_",
                "type": "address"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "asset",
                "type": "address"
            }
        ],
        "name": "getAssetPrice",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "price",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "asset",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "price",
                "type": "uint256"
            }
        ],
        "name": "setAssetPrice",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "hToken",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "token",
                "type": "address"
            }
        ],
        "name": "setHToken",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
