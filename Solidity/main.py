from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import address_contract, abi

w3= Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
contract = w3.eth.contract(address=address_contract, abi=abi)

print(w3.eth.get_balance('0xF3EEe078293694b10B81a373CEae3720da912B06'))
print(w3.eth.get_balance('0x45AFeee1Ce086a025c454b79Bc7D2832383ec4F6'))
print(w3.eth.get_balance('0x1CC9213bE732c82B53a7ECeE22624f5d54a32E22'))
print(w3.eth.get_balance('0xEA42d0b5F992f52CFf802Ef5263e5F7109433c67'))
print(w3.eth.get_balance('0x05F2E98f3E6d370b05673aC787910C3758A4c907'))



