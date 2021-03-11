from pathlib import Path
import click

from brownie import OSMedianizer, accounts, config, network, Wei
from eth_utils import is_checksum_address

def main():
    print(f"You are using the '{network.show_active()}' network")
    dev = accounts.load(click.prompt("Account", type=click.Choice(accounts.load())))
    print(f"You are using: 'dev' [{dev.address}]")

    osmedianizer = OSMedianizer.deploy({'from': dev, 'gas_price': Wei('80 gwei')})
