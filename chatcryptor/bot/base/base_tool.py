
import langchain.tools as BaseTool
from typing import Any, Awaitable, Callable, Dict, Optional, Tuple, Type, Union, List
from pydantic import (
    BaseModel)


class CustomeTool(BaseTool.Tool):
    groups: Optional[List[str]] = []

    def _to_args_and_kwargs(self, tool_input: Union[str, Dict]) -> Tuple[Tuple, Dict]:
        """Convert tool input to pydantic model."""
        # HACK: fix bugs params of Tool
        args, kwargs = BaseTool.BaseTool._to_args_and_kwargs(self, tool_input)
        # For backwards compatibility. The tool must be run with a single input
        all_args = list(args) + list(kwargs.values())
        if len(all_args) > 1:
            raise BaseTool.ToolException(
                f"Too many arguments to single-input tool {self.name}."
                f" Args: {all_args}"
            )
        return tuple(all_args), {}


class CustomeStructuredTool(BaseTool.StructuredTool):
    groups: Optional[List[str]] = []
