import rwth_nb.misc.notebook as nb
import rwth_nb.misc.share as share

from pprint import pprint

url = share.get_shareable_url(path='gdet3/GDET3 Äquivalenter Tiefpass.ipynb',
                              note='access for my colleage at IKS',
                              expires_in=24*60*60)
print(url)

# List all shareable tokens
tokens = share.get_shareable_tokens()
pprint(tokens)

# Revoke the new token
share.revoke_shareable_token(tokens[0]['id'])

# List all tokens again
tokens = share.get_shareable_tokens()
pprint(tokens)
