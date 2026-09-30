import json
from collections.abc import Callable

from termcolor import colored
from flavor.colors import COLORS

from functions.browse import browse, schema_browse
from functions.read import read, schema_read
from functions.execute import execute, schema_execute
from functions.write import write, schema_write

available_functions = [
    schema_browse,
    schema_read,
    schema_execute,
    schema_write
]

function_map: dict[str, Callable[..., str]] = {
    "browse": browse,
    "read": read,
    "execute": execute,
    "write": write
}
def call_function(tool_call, working_directory:str, verbose: bool = False) -> dict:
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments or "{}")

    if not function_name in function_map:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"Error: Unknown function: {function_name}",
        }
    else:
        function_args["working_dir"] = working_directory
        result = function_map[function_name](**function_args)

        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        }
