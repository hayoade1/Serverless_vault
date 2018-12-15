import os
import requests

vault_addr = os.environ['VAULT_ADDR']
vault_cacert = os.environ['VAULT_CACERT'] 
jwt = requests.get('http://metadata/computeMetadata/v1/instance/service-accounts/default/identity',
    headers={'Metadata-Flavor':'Google'},
    params={'audience':'http://vault/socialmedia', 'format':'full'})

auth = requests.post(vault_addr + '/v1/auth/gcp/login',
    json={'role':'socialmedia', 'jwt':jwt.text}, verify=vault_cacert)
token = auth.json()['auth']['client_token']

r = requests.get(vault_addr + '/v1/secret/apikeys/twitter',
    headers={'x-vault-token': token}, verify=vault_cacert)
apikey = r.json()['data']['value']

def F(request):
    return f'{apikey}'
