"""
shape_presentation_instances.py
"""

population = [
    # Starr class default
    {'Asset': 'class compartment', 'Presentation': 'default', 'drawingzz type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'binary association connectorzz', 'Presentation': 'default', 'drawingzz type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'generalization connectorzz', 'Presentation': 'default', 'drawingzz type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'imported class compartment', 'Presentation': 'default', 'drawingzz type': 'Starr class diagram', 'Line style': 'dashed'},
    {'Asset': 'associative mult stem', 'Presentation': 'default', 'drawingzz type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'grid', 'Presentation': 'default', 'drawingzz type': 'Starr class diagram', 'Line style': 'hide'},
    {'Asset': 'margin', 'Presentation': 'default', 'drawingzz type': 'Starr class diagram', 'Line style': 'hide'},
    {'Asset': 'solid arrow', 'Presentation': 'default', 'drawingzz type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'hollow arrow', 'Presentation': 'default', 'drawingzz type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'gen arrow', 'Presentation': 'default', 'drawingzz type': 'Starr class diagram', 'Line style': 'normal'},

    # xumlzz class default
    {'Asset': 'class compartment', 'Presentation': 'default', 'drawingzz type': 'xumlzz class diagram', 'Line style': 'normal'},
    {'Asset': 'binary association connectorzz', 'Presentation': 'default', 'drawingzz type': 'xumlzz class diagram', 'Line style': 'normal'},
    {'Asset': 'generalization connectorzz', 'Presentation': 'default', 'drawingzz type': 'xumlzz class diagram', 'Line style': 'normal'},
    {'Asset': 'imported class compartment', 'Presentation': 'default', 'drawingzz type': 'xumlzz class diagram', 'Line style': 'dashed'},
    {'Asset': 'associative mult stem', 'Presentation': 'default', 'drawingzz type': 'xumlzz class diagram', 'Line style': 'dashed'},
    {'Asset': 'grid', 'Presentation': 'default', 'drawingzz type': 'xumlzz class diagram', 'Line style': 'grid'},
    {'Asset': 'margin', 'Presentation': 'default', 'drawingzz type': 'xumlzz class diagram', 'Line style': 'margin'},

    # Shlaer-Mellor class default
    {'Asset': 'class compartment', 'Presentation': 'default', 'drawingzz type': 'Shlaer-Mellor class diagram', 'Line style': 'normal'},
    {'Asset': 'binary association connectorzz', 'Presentation': 'default', 'drawingzz type': 'Shlaer-Mellor class diagram', 'Line style': 'normal'},
    {'Asset': 'generalization connectorzz', 'Presentation': 'default', 'drawingzz type': 'Shlaer-Mellor class diagram', 'Line style': 'normal'},
    {'Asset': 'imported class compartment', 'Presentation': 'default', 'drawingzz type': 'Shlaer-Mellor class diagram', 'Line style': 'dashed'},
    {'Asset': 'associative mult stem', 'Presentation': 'default', 'drawingzz type': 'Shlaer-Mellor class diagram', 'Line style': 'normal'},
    {'Asset': 'grid', 'Presentation': 'default', 'drawingzz type': 'Shlaer-Mellor class diagram', 'Line style': 'grid'},
    {'Asset': 'margin', 'Presentation': 'default', 'drawingzz type': 'Shlaer-Mellor class diagram', 'Line style': 'margin'},

    # Starr class diagnostic
    {'Asset': 'class compartment', 'Presentation': 'diagnostic', 'drawingzz type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'binary association connectorzz', 'Presentation': 'diagnostic', 'drawingzz type': 'Starr class diagram',
     'Line style': 'normal'},
    {'Asset': 'generalization connectorzz', 'Presentation': 'diagnostic', 'drawingzz type': 'Starr class diagram',
     'Line style': 'normal'},
    {'Asset': 'imported class compartment', 'Presentation': 'diagnostic', 'drawingzz type': 'Starr class diagram', 'Line style': 'dashed'},
    {'Asset': 'associative mult stem', 'Presentation': 'diagnostic', 'drawingzz type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'grid', 'Presentation': 'diagnostic', 'drawingzz type': 'Starr class diagram', 'Line style': 'grid'},
    {'Asset': 'margin', 'Presentation': 'diagnostic', 'drawingzz type': 'Starr class diagram', 'Line style': 'margin'},
    {'Asset': 'solid arrow', 'Presentation': 'diagnostic', 'drawingzz type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'hollow arrow', 'Presentation': 'diagnostic', 'drawingzz type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'gen arrow', 'Presentation': 'diagnostic', 'drawingzz type': 'Starr class diagram', 'Line style': 'normal'},
    # Only for diagnostics
    {'Asset': 'shoot', 'Presentation': 'diagnostic', 'drawingzz type': 'Starr class diagram',
     'Line style': 'connectorzz highlight'},

    # xumlzz class diagnostic
    {'Asset': 'class compartment', 'Presentation': 'diagnostic', 'drawingzz type': 'xumlzz class diagram', 'Line style': 'normal'},
    {'Asset': 'binary association connectorzz', 'Presentation': 'diagnostic', 'drawingzz type': 'xumlzz class diagram',
     'Line style': 'connectorzz highlight'},
    {'Asset': 'generalization connectorzz', 'Presentation': 'diagnostic', 'drawingzz type': 'xumlzz class diagram',
     'Line style': 'connectorzz highlight'},
    {'Asset': 'imported class compartment', 'Presentation': 'diagnostic', 'drawingzz type': 'xumlzz class diagram', 'Line style': 'dashed'},
    {'Asset': 'associative mult stem', 'Presentation': 'diagnostic', 'drawingzz type': 'xumlzz class diagram', 'Line style': 'dashed'},
    {'Asset': 'grid', 'Presentation': 'diagnostic', 'drawingzz type': 'xumlzz class diagram', 'Line style': 'grid'},
    {'Asset': 'margin', 'Presentation': 'diagnostic', 'drawingzz type': 'xumlzz class diagram', 'Line style': 'margin'},

    {'Asset': 'class compartment', 'Presentation': 'diagnostic', 'drawingzz type': 'Shlaer-Mellor class diagram', 'Line style': 'normal'},
    {'Asset': 'binary association connectorzz', 'Presentation': 'diagnostic', 'drawingzz type': 'Shlaer-Mellor class diagram',
     'Line style': 'connectorzz highlight'},
    {'Asset': 'generalization connectorzz', 'Presentation': 'diagnostic', 'drawingzz type': 'Shlaer-Mellor class diagram',
     'Line style': 'connectorzz highlight'},
    {'Asset': 'imported class compartment', 'Presentation': 'diagnostic', 'drawingzz type': 'Shlaer-Mellor class diagram', 'Line style': 'dashed'},
    {'Asset': 'associative mult stem', 'Presentation': 'diagnostic', 'drawingzz type': 'Shlaer-Mellor class diagram', 'Line style': 'normal'},
    {'Asset': 'grid', 'Presentation': 'diagnostic', 'drawingzz type': 'Shlaer-Mellor class diagram', 'Line style': 'grid'},
    {'Asset': 'margin', 'Presentation': 'diagnostic', 'drawingzz type': 'Shlaer-Mellor class diagram', 'Line style': 'margin'},

    # xumlzz state default
    {'Asset': 'transition', 'Presentation': 'default', 'drawingzz type': 'xumlzz state machine diagram', 'Line style': 'normal'},
    {'Asset': 'state compartment', 'Presentation': 'default', 'drawingzz type': 'xumlzz state machine diagram', 'Line style': 'normal'},
    {'Asset': 'solid dot', 'Presentation': 'default', 'drawingzz type': 'xumlzz state machine diagram',
     'Line style': 'normal'},
    {'Asset': 'hollow large circle', 'Presentation': 'default', 'drawingzz type': 'xumlzz state machine diagram',
     'Line style': 'normal'},

]
