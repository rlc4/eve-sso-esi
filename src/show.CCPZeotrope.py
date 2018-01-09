from API import swagger_client
from API.swagger_client.rest import ApiException

api = swagger_client.CharacterApi()
api.api_client.set_default_header('User-Agent', 'my-test-agent') # Set a relevant user agent so we know which software is actually using ESI
api.api_client.host = "https://esi.tech.ccp.is" # see [1]

try:
    response = api.get_characters_character_id(2112625428)
    print(response)
except  ApiException as e:
    print("Exception when calling CharacterApi->get_characters_character_id: %s\n" % e)
