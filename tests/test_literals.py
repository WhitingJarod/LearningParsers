tests = [
    # Positive integers
    ["43;", {
        "type": "Program",
        "body": [{
            "type": "ExpressionStatement",
            "expression": {
                "type": "NumericLiteral",
                "value": 43.0
            }
        }]
    }],
    # Double quote strings
    ["\"hello\";", {
        "type": "Program",
        "body": [{
            "type": "ExpressionStatement",
            "expression": {
                "type": "StringLiteral",
                "value": "hello"
            }
        }]
    }],
    # Single quote strings
    ["\'hello\';", {
        "type": "Program",
        "body": [{
            "type": "ExpressionStatement",
            "expression": {
                "type": "StringLiteral",
                "value": "hello"
            }
        }]
    }],
]