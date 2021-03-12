import pytest
from brownie import config, Wei, Contract


@pytest.fixture
def gov(accounts):
    # ychad.eth
    yield accounts.at('0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52', force=True)


@pytest.fixture
def rewards(gov):
    yield gov  # TODO: Add rewards contract


@pytest.fixture
def guardian(accounts):
    # dev.ychad.eth
    yield accounts.at('0x846e211e8ba920B353FB717631C015cf04061Cc9', force=True)


@pytest.fixture
def management(accounts):
    # dev.ychad.eth
    yield accounts.at('0x846e211e8ba920B353FB717631C015cf04061Cc9', force=True)


@pytest.fixture
def strategist(accounts):
    # You! Our new Strategist!
    yield accounts[3]


@pytest.fixture
def keeper(accounts):
    # This is our trusty bot!
    yield accounts[4]


@pytest.fixture
def token():
    token_address = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"
    yield Contract(token_address)


@pytest.fixture
def amount(accounts, token, whale):
    amount = 10 * 10 ** token.decimals()
    # In order to get some funds for the token you are about to use,
    # it impersonate an exchange address to use it's funds.
    reserve = whale
    token.transfer(accounts[0], amount, {"from": reserve})
    yield amount


@pytest.fixture
def weth(interface):
    yield interface.ERC20('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')


@pytest.fixture
def dai(interface):
    yield interface.ERC20('0x6B175474E89094C44Da98b954EedeAC495271d0F')


@pytest.fixture
def vault(pm, gov, rewards, guardian, management, token):
    Vault = pm(config["dependencies"][0]).Vault
    vault = guardian.deploy(Vault)
    vault.initialize(token, gov, rewards, "", "", guardian)
    vault.setDepositLimit(2 ** 256 - 1, {"from": gov})
    vault.setManagement(management, {"from": gov})
    yield vault


@pytest.fixture
def strategy(accounts, strategist, keeper, vault, Strategy, gov):
    strategy = strategist.deploy(Strategy, vault)
    strategy.setKeeper(keeper)
    vault.addStrategy(strategy, 9_000, 0, 2 ** 256 - 1, 1_000, {"from": gov})

    ## authorize oracle for strategy
    #osm = Contract('0x2953554810F73aD0498F6C948FB6eedf15747EE0')
    #o = Contract(osm.OSM())
    #o.set_user(osm, True, {"from": gov})
    #osm.setAuthorized(strategy, {"from": gov})

    yield strategy


@pytest.fixture
def whale(accounts):
    # binance7 wallet
    acc = accounts.at('0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8', force=True)

    # binance8 wallet
    #acc = accounts.at('0xf977814e90da44bfa03b6295a0616a897441acec', force=True)
    yield acc


@pytest.fixture
def dai_vault():
    yield Contract('0x19D3364A399d251E894aC732651be8B0E4e85001')
