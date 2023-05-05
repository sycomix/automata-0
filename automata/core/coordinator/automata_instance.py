from typing import Dict, Optional, Type

from pydantic import BaseModel

from automata.configs.automata_agent_configs import AutomataAgentConfig
from automata.configs.config_enums import AgentConfigVersion
from automata.core.agent.automata_agent_builder import AutomataAgentBuilder
from automata.core.base.tool import Toolkit, ToolkitType


class AutomataInstance(BaseModel):
    config_version: AgentConfigVersion = AgentConfigVersion.DEFAULT
    description: str = ""
    builder: Type[AutomataAgentBuilder] = AutomataAgentBuilder
    llm_toolkits: Optional[Dict[ToolkitType, Toolkit]] = None

    def run(self, instructions: str) -> str:
        """
        Executes the specified instructions on an agent built from this instance's configuration
        and returns the result.

        Args:
            instructions (str): The instructions to be executed by the agent.

        Returns:
            str: The output produced by the agent.

        Raises:
            Exception: If any error occurs during agent execution.
        """
        config = AutomataAgentConfig.load(self.config_version)
        agent_builder = self.builder(config=config)
        if self.llm_toolkits:
            agent_builder = agent_builder.with_llm_toolkits(self.llm_toolkits)

        agent = agent_builder.with_instructions(instructions).build()
        result = agent.run()
        del agent
        return result

    class Config:
        arbitrary_types_allowed = True
