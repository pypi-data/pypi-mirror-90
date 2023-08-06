try:
    from google.cloud import firestore
except ImportError:
    raise ImportError("Please ensure google-cloud-firestore version 2.0.2 is installed.")

__version__ = '0.0.1'
