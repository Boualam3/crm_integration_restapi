import os
from dotenv import load_dotenv
load_dotenv()

environment = os.environ.get('ENVIRONMENT', 'development')

# there is no prod/testing module yet
if environment == 'production':
    from .prod import *
elif environment == 'testing':
    # from .testing import *
    pass
else:
    from .dev import *
