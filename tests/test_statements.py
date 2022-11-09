tests = [
    [ # Multiline comments, multiple ExpressionStatements
        """
            /* This is a
            multiline comment
            Yeah boi
            */
            ";yeah 42";
            32;
        """,
        {
            'type': 'Program',
            'body': [
                {
                    'type': 'ExpressionStatement',
                    'expression': {
                        'type': 'StringLiteral',
                        'value': ';yeah 42'
                    }
                },
                {
                    'type': 'ExpressionStatement',
                    'expression': {
                        'type': 'NumericLiteral',
                        'value': 32.0
                    }
                }
            ]
        }
    ],
    [ # BlockStatements
        """
            {
                42;
                "hello";
            }
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "BlockStatement",
                    "body": [
                        {
                            "type": "ExpressionStatement",
                            "expression": {
                                "type": "NumericLiteral",
                                "value": 42.0
                            }
                        },
                        {
                            "type": "ExpressionStatement",
                            "expression": {
                                "type": "StringLiteral",
                                "value": "hello"
                            }
                        }
                    ]
                }
            ]
        }
    ],
    [ # EmptyStatements
        """
            ;
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "EmptyStatement"
                }
            ]
        }
    ]
]
