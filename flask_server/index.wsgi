import sae
sae.add_vendor_dir('site-packages')
from app import app

application=sae.create_wsgi_app(app)