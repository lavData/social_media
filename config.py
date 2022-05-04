import yaml
import consul

c = consul.Consul()


index, data = c.kv.get('config')
value = data['Value'].decode('utf-8')
config = yaml.safe_load(data['Value'])

TOKEN = config['token']

POSTGRES_HOST = config['postgresql']['host']
POSTGRES_PORT = config['postgresql']['port']
POSTGRES_USER = config['postgresql']['username']
POSTGRES_PASSWORD = config['postgresql']['password']
POSTGRES_DB = config['postgresql']['database']


