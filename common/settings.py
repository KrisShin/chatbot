from environ import Env
import os

env = Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Set the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
Env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG = env('DEBUG')

OPENAI_API_KEY = env('OPENAI_API_KEY')
