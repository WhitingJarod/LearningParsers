tests = [
    [ # Basic binary expression
        """
            5 + 10;
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "BinaryExpression",
                        "operator": "+",
                        "left": {
                            "type": "NumericLiteral",
                            "value": 5.0,
                        },
                        "right": {
                            "type": "NumericLiteral",
                            "value": 10.0
                        }
                    }
                }
            ]
        }
    ],
    [ # Chained binary expression
        """
            5 - 10 + 15;
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "BinaryExpression",
                        "operator": "+",
                        "left": {
                            "type": "BinaryExpression",
                            "operator": "-",
                            "left": {
                                "type": "NumericLiteral",
                                "value": 5.0
                            },
                            "right": {
                                "type": "NumericLiteral",
                                "value": 10.0
                            }
                        },
                        "right": {
                            "type": "NumericLiteral",
                            "value": 15.0
                        }
                    }
                }
            ]
        }
    ],
    [ # Left associative multiplication
        """
            2 * 3 * 4;
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "BinaryExpression",
                        "operator": "*",
                        "left": {
                            "type": "BinaryExpression",
                            "operator": "*",
                            "left": {
                                "type": "NumericLiteral",
                                "value": 2.0
                            },
                            "right": {
                                "type": "NumericLiteral",
                                "value": 3.0
                            }
                        },
                        "right": {
                            "type": "NumericLiteral",
                            "value": 4.0
                        }
                    }
                }
            ]
        }
    ],
    [ # Operator precedence
        """
            2 + 3 * 4;
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "BinaryExpression",
                        "operator": "+",
                        "left": {
                            "type": "NumericLiteral",
                            "value": 2.0
                        },
                        "right": {
                            "type": "BinaryExpression",
                            "operator": "*",
                            "left": {
                                "type": "NumericLiteral",
                                "value": 3.0
                            },
                            "right": {
                                "type": "NumericLiteral",
                                "value": 4.0
                            }
                        }
                    }
                }
            ]
        }
    ],
    [ # Parentheses
        """
            (2 + 3) * 4;
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "BinaryExpression",
                        "operator": "*",
                        "left": {
                            "type": "BinaryExpression",
                            "operator": "+",
                            "left": {
                                "type": "NumericLiteral",
                                "value": 2.0
                            },
                            "right": {
                                "type": "NumericLiteral",
                                "value": 3.0
                            }
                        },
                        "right": {
                            "type": "NumericLiteral",
                            "value": 4.0
                        }
                    }
                }
            ]
        }
    ]
]
