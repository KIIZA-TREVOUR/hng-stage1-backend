from fastapi import FastAPI, Query, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import httpx
import math

app = FastAPI()

# Pydantic model for the response
class NumberResponse(BaseModel):
    number: int
    is_prime: bool
    is_perfect: bool
    properties: list[str]
    digit_sum: int
    fun_fact: str

# Helper functions
def is_prime(n: int) -> bool:
    """Check if a number is prime"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

def is_perfect(n: int) -> bool:
    """Check if a number is a perfect number"""
    if n <= 1:
        return False
    sum_divisors = 1
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            sum_divisors += i
            if i != n // i:
                sum_divisors += n // i
    return sum_divisors == n

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number"""
    if n < 0:
        return False
    num_str = str(n)
    length = len(num_str)
    return sum(int(digit) ** length for digit in num_str) == n

def get_parity(n: int) -> str:
    """Check if a number is even or odd"""
    return "even" if n % 2 == 0 else "odd"

async def get_fun_fact(n: int) -> str:
    """Fetch or generate a fun fact about a number"""
    if is_armstrong(n):
        # Manually construct the fun fact for Armstrong numbers
        digits = [int(d) for d in str(n)]
        length = len(digits)
        explanation = " + ".join([f"{d}^{length}" for d in digits])
        return f"{n} is an Armstrong number because {explanation} = {n}"
    else:
        # Fetch fun fact from Numbers API for non-Armstrong numbers
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"http://numbersapi.com/{n}/math", timeout=3.0)
                return response.text if response.status_code == 200 else "No fun fact available"
        except (httpx.RequestError, httpx.TimeoutException):
            return "No fun fact available"

# API endpoint
@app.get("/api/classify-number", response_model=NumberResponse)
async def classify_number(number: str = Query(..., description="Number to classify")):
    # Input validation
    if not number.lstrip('-').isdigit():
        return JSONResponse(
            content={"number": number, "error": True},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    num = int(number)
    
    # Determine properties
    properties = []
    if is_armstrong(num):
        properties.append("armstrong")
    properties.append(get_parity(num))
    
    # Fetch or generate fun fact
    fun_fact = await get_fun_fact(num)
    
    # Prepare response
    response = {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(abs(num))),
        "fun_fact": fun_fact
    }
    
    return response