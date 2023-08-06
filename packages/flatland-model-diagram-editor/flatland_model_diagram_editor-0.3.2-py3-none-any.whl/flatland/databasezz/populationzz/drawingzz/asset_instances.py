"""
asset_instances.py
"""

population = [
    # xumlzz class diagram
    {'Name': 'class compartment', 'Form': 'shape', 'drawingzz type': 'xumlzz class diagram'},
    {'Name': 'binary association connectorzz', 'Form': 'shape', 'drawingzz type': 'xumlzz class diagram'},
    {'Name': 'generalization connectorzz', 'Form': 'shape', 'drawingzz type': 'xumlzz class diagram'},
    {'Name': 'label', 'Form': 'text', 'drawingzz type': 'xumlzz class diagram'},
    {'Name': 'binary association name', 'Form': 'text', 'drawingzz type': 'xumlzz class diagram'},
    {'Name': 'generalization name', 'Form': 'text', 'drawingzz type': 'xumlzz class diagram'},
    {'Name': 'class mult name', 'Form': 'text', 'drawingzz type': 'xumlzz class diagram'},
    {'Name': 'imported class compartment', 'Form': 'shape', 'drawingzz type': 'xumlzz class diagram'},
    {'Name': 'see also', 'Form': 'text', 'drawingzz type': 'xumlzz class diagram'},
    {'Name': 'class name', 'Form': 'text', 'drawingzz type': 'xumlzz class diagram'},
    {'Name': 'attributes', 'Form': 'text', 'drawingzz type': 'xumlzz class diagram'},
    {'Name': 'methods', 'Form': 'text', 'drawingzz type': 'xumlzz class diagram'},
    {'Name': 'associative mult stem', 'Form': 'shape', 'drawingzz type': 'xumlzz class diagram'},
    {'Name': 'grid', 'Form': 'shape', 'drawingzz type': 'xumlzz class diagram'},
    {'Name': 'margin', 'Form': 'shape', 'drawingzz type': 'xumlzz class diagram'},

    # Shlaer-Mellor class diagram
    {'Name': 'class compartment', 'Form': 'shape', 'drawingzz type': 'Shlaer-Mellor class diagram'},
    {'Name': 'binary association connectorzz', 'Form': 'shape', 'drawingzz type': 'Shlaer-Mellor class diagram'},
    {'Name': 'generalization connectorzz', 'Form': 'shape', 'drawingzz type': 'Shlaer-Mellor class diagram'},
    {'Name': 'label', 'Form': 'text', 'drawingzz type': 'Shlaer-Mellor class diagram'},
    {'Name': 'binary association name', 'Form': 'text', 'drawingzz type': 'Shlaer-Mellor class diagram'},
    {'Name': 'generalization name', 'Form': 'text', 'drawingzz type': 'Shlaer-Mellor class diagram'},
    {'Name': 'class mult name', 'Form': 'text', 'drawingzz type': 'Shlaer-Mellor class diagram'},
    {'Name': 'imported class compartment', 'Form': 'shape', 'drawingzz type': 'Shlaer-Mellor class diagram'},
    {'Name': 'see also', 'Form': 'text', 'drawingzz type': 'Shlaer-Mellor class diagram'},
    {'Name': 'class name', 'Form': 'text', 'drawingzz type': 'Shlaer-Mellor class diagram'},
    {'Name': 'attributes', 'Form': 'text', 'drawingzz type': 'Shlaer-Mellor class diagram'},
    {'Name': 'methods', 'Form': 'text', 'drawingzz type': 'Shlaer-Mellor class diagram'},
    {'Name': 'associative mult stem', 'Form': 'shape', 'drawingzz type': 'Shlaer-Mellor class diagram'},
    {'Name': 'grid', 'Form': 'shape', 'drawingzz type': 'Shlaer-Mellor class diagram'},
    {'Name': 'margin', 'Form': 'shape', 'drawingzz type': 'Shlaer-Mellor class diagram'},

    # Starr class diagram
    {'Name': 'class compartment', 'Form': 'shape', 'drawingzz type': 'Starr class diagram'},
    {'Name': 'binary association connectorzz', 'Form': 'shape', 'drawingzz type': 'Starr class diagram'},
    {'Name': 'generalization connectorzz', 'Form': 'shape', 'drawingzz type': 'Starr class diagram'},
    {'Name': 'label', 'Form': 'text', 'drawingzz type': 'Starr class diagram'},
    {'Name': 'binary association name', 'Form': 'text', 'drawingzz type': 'Starr class diagram'},
    {'Name': 'generalization name', 'Form': 'text', 'drawingzz type': 'Starr class diagram'},
    {'Name': 'class mult name', 'Form': 'text', 'drawingzz type': 'Starr class diagram'},
    {'Name': 'imported class compartment', 'Form': 'shape', 'drawingzz type': 'Starr class diagram'},
    {'Name': 'see also', 'Form': 'text', 'drawingzz type': 'Starr class diagram'},
    {'Name': 'class name', 'Form': 'text', 'drawingzz type': 'Starr class diagram'},
    {'Name': 'attributes', 'Form': 'text', 'drawingzz type': 'Starr class diagram'},
    {'Name': 'methods', 'Form': 'text', 'drawingzz type': 'Starr class diagram'},
    {'Name': 'associative mult stem', 'Form': 'shape', 'drawingzz type': 'Starr class diagram'},
    {'Name': 'grid', 'Form': 'shape', 'drawingzz type': 'Starr class diagram'},
    {'Name': 'margin', 'Form': 'shape', 'drawingzz type': 'Starr class diagram'},
    # For diagnostics only
    {'Name': 'shoot', 'Form': 'shape', 'drawingzz type': 'Starr class diagram'},

    # Symbols
    {'Name': 'solid arrow', 'Form': 'shape', 'drawingzz type': 'Starr class diagram'},
    {'Name': 'hollow arrow', 'Form': 'shape', 'drawingzz type': 'Starr class diagram'},
    {'Name': 'gen arrow', 'Form': 'shape', 'drawingzz type': 'Starr class diagram'},

    # xumlzz state machine diagram
    {'Name': 'transition', 'Form': 'shape', 'drawingzz type': 'xumlzz state machine diagram'},
    {'Name': 'event', 'Form': 'text', 'drawingzz type': 'xumlzz state machine diagram'},
    {'Name': 'activity', 'Form': 'text', 'drawingzz type': 'xumlzz state machine diagram'},
    {'Name': 'state name', 'Form': 'text', 'drawingzz type': 'xumlzz state machine diagram'},
    {'Name': 'state compartment', 'Form': 'shape', 'drawingzz type': 'xumlzz state machine diagram'},
    # Symbols
    {'Name': 'hollow large circle', 'Form': 'shape', 'drawingzz type': 'xumlzz state machine diagram'},
    {'Name': 'solid dot', 'Form': 'shape', 'drawingzz type': 'xumlzz state machine diagram'},

    # Domain diagram
    {'Name': 'domain nodezz', 'Form': 'shape', 'drawingzz type': 'Starr domain diagram'},
    {'Name': 'bridge', 'Form': 'shape', 'drawingzz type': 'Starr domain diagram'},

    {'Name': 'domain nodezz', 'Form': 'shape', 'drawingzz type': 'xumlzz domain diagram'},
    {'Name': 'bridge', 'Form': 'shape', 'drawingzz type': 'xumlzz domain diagram'},

    # Collaboration diagram
    {'Name': 'overview class', 'Form': 'shape', 'drawingzz type': 'Starr collaboration diagram'},
    {'Name': 'collaboration', 'Form': 'shape', 'drawingzz type': 'Starr collaboration diagram'},
    {'Name': 'message', 'Form': 'text', 'drawingzz type': 'Starr collaboration diagram'},
    {'Name': 'sync arrow', 'Form': 'shape', 'drawingzz type': 'Starr collaboration diagram'},

    {'Name': 'overview class', 'Form': 'shape', 'drawingzz type': 'xumlzz collaboration diagram'},
    {'Name': 'collaboration', 'Form': 'shape', 'drawingzz type': 'xumlzz collaboration diagram'},
    {'Name': 'message', 'Form': 'text', 'drawingzz type': 'xumlzz collaboration diagram'},
    {'Name': 'sync arrow', 'Form': 'shape', 'drawingzz type': 'xumlzz collaboration diagram'}
]