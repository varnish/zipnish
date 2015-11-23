import os

from app import create_app, db

# configuration file path
etc_config_path = '/etc/zipnish/ui.cfg'
config_path = os.path.dirname(os.path.abspath(__file__)) + '/ui.cfg'

if os.path.exists(etc_config_path):
	config_path = etc_config_path

app = create_app(config_path)

if __name__ == '__main__':
    app.run(host=app.config['HOST'], 
    		port=app.config['PORT'], 
    		debug=app.config['DEBUG'])