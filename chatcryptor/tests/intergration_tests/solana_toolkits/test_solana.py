from chatcryptor.bot.agents.solana_toolkits.base import create_solana_onchain_agent


def test_load_agents():
    """Test that returns an answer""" 
    agent = create_solana_onchain_agent()
    a = agent.run(
        "I want to get balance of account on Solana blockchain: ASx1wk74GLZsxVrYiBkNKiViPLjnJQVGxKrudRgPir4A?")
    assert a != ''
