
from estrom.utils import DotDict

settings = DotDict({
    "crossbar": {
        "host": "localhost",
        "port": 7000,
        "realm": "estrom",
        "ns": "com.estrom",
    },

    "es": {
        "host": "localhost",
        "port": 9200,
        "percolator_type": ".percolator",
    },

    "beater": {
        "host": "localhost",
        "port": 8080,
    },

})
