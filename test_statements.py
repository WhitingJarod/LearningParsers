tests = [
    # Positive integers
    ["""
    /* This is a
    multiline comment
    Yeah boi
    */
    ";yeah 42";
    32;
    """, {
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
]
