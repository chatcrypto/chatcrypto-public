"""Toolkit for interacting with a Solana."""
from typing import List

from pydantic import Field

from langchain.agents.agent_toolkits.base import BaseToolkit
from langchain.base_language import BaseLanguageModel
from langchain.tools import BaseTool
from chatcryptor.bot.tools.solana.solana_onchain_tool import *


class SolanaToolKit(BaseToolkit):
    """Toolkit for interacting with Solana data."""

    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    def get_tools(self) -> List[BaseTool]:
        return self.get_onchain_tools()

    def get_onchain_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return [
           
            
        ]
