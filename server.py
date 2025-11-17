"""
MCP Server for Basic Maths Operations

This MCP server provides tools for performing basic mathematical operations including addition,
multiplication, subtraction, and division. It also includes a tool to retrieve operation history.

Environment Variables:
- None required. The server runs locally without external dependencies.

Permissions:
- None required. All operations are read-only and performed locally.

Setup Instructions:
1. Install required packages: pip install fastmcp pydantic
2. Run the server: python this_file.py
3. Configure your MCP client to connect to this server.

Authentication Method:
- None required (local server).
"""

import os
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, field_validator, ValidationInfo, ConfigDict
from fastmcp import FastMCP

class Config:
    '''Configuration with environment variable validation'''
    # No environment variables required for this local server
    
    @classmethod
    def validate(cls) -> None:
        '''Validate required environment variables are set'''
        # No validations needed since no env vars are required
        pass

# Validate configuration on import
Config.validate()

# FastMCP initialization
mcp = FastMCP("MathsOperationsServer")

# Constants
CHARACTER_LIMIT = 1000  # Not strictly needed for maths, but included for completeness

# Pydantic Models
class MathOperationInput(BaseModel):
    model_config = ConfigDict(strict=True)
    
    num1: float
    num2: float
    
    @field_validator('num1', 'num2')
    @classmethod
    def validate_numeric(cls, v: float, info: ValidationInfo) -> float:
        """Ensure inputs are finite numbers"""
        if not isinstance(v, (int, float)) or not (float('-inf') < v < float('inf')):
            raise ValueError(f"{info.field_name} must be a finite number")
        return float(v)

class MathResult(BaseModel):
    model_config = ConfigDict(strict=True)
    
    result: float
    operation: str
    timestamp: str

class MathHistory(BaseModel):
    model_config = ConfigDict(strict=True)
    
    operations: List[MathResult]

# Global history storage (in-memory for this example)
_operation_history: List[MathResult] = []

# Helper functions
def _perform_operation(num1: float, num2: float, op: str) -> float:
    """Perform the specified mathematical operation"""
    if op == "addition":
        return num1 + num2
    elif op == "multiplication":
        return num1 * num2
    elif op == "subtraction":
        return num1 - num2
    elif op == "division":
        if num2 == 0:
            raise ValueError("Division by zero is not allowed")
        return num1 / num2
    else:
        raise ValueError(f"Unknown operation: {op}")

def _add_to_history(result: MathResult) -> None:
    """Add operation result to history"""
    _operation_history.append(result)

# Tools
@mcp.tool()
def add_numbers(num1: float, num2: float) -> MathResult:
    """
    Add two numbers.
    
    Args:
        num1: First number
        num2: Second number
    
    Returns:
        MathResult: The result of addition with metadata
    """
    try:
        result_value = _perform_operation(num1, num2, "addition")
        result = MathResult(
            result=result_value,
            operation="addition",
            timestamp=datetime.now().isoformat()
        )
        _add_to_history(result)
        return result
    except ValueError as e:
        raise ValueError(f"Addition failed: {e}")

@mcp.tool()
def multiply_numbers(num1: float, num2: float) -> MathResult:
    """
    Multiply two numbers.
    
    Args:
        num1: First number
        num2: Second number
    
    Returns:
        MathResult: The result of multiplication with metadata
    """
    try:
        result_value = _perform_operation(num1, num2, "multiplication")
        result = MathResult(
            result=result_value,
            operation="multiplication",
            timestamp=datetime.now().isoformat()
        )
        _add_to_history(result)
        return result
    except ValueError as e:
        raise ValueError(f"Multiplication failed: {e}")

@mcp.tool()
def subtract_numbers(num1: float, num2: float) -> MathResult:
    """
    Subtract second number from first number.
    
    Args:
        num1: First number (minuend)
        num2: Second number (subtrahend)
    
    Returns:
        MathResult: The result of subtraction with metadata
    """
    try:
        result_value = _perform_operation(num1, num2, "subtraction")
        result = MathResult(
            result=result_value,
            operation="subtraction",
            timestamp=datetime.now().isoformat()
        )
        _add_to_history(result)
        return result
    except ValueError as e:
        raise ValueError(f"Subtraction failed: {e}")

@mcp.tool()
def divide_numbers(num1: float, num2: float) -> MathResult:
    """
    Divide first number by second number.
    
    Args:
        num1: Dividend
        num2: Divisor (cannot be zero)
    
    Returns:
        MathResult: The result of division with metadata
    """
    try:
        result_value = _perform_operation(num1, num2, "division")
        result = MathResult(
            result=result_value,
            operation="division",
            timestamp=datetime.now().isoformat()
        )
        _add_to_history(result)
        return result
    except ValueError as e:
        raise ValueError(f"Division failed: {e}")

@mcp.tool()
def get_math_history() -> MathHistory:
    """
    Retrieve the history of all performed mathematical operations.
    
    Returns:
        MathHistory: List of all operation results
    """
    return MathHistory(operations=_operation_history)

if __name__ == "__main__":
    mcp.run()