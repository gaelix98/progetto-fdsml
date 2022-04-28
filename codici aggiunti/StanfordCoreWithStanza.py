
from stanza.server import CoreNLPClient
import time, json

# Construct a CoreNLPClient with some basic annotators, a memory allocation of 4GB, and port number 9001
client = CoreNLPClient(
    annotators=['ner'], 
    memory='4G', 
    endpoint='http://localhost:9000',
    be_quiet=False)
print(client)

# Start the background server and wait for some time
# Note that in practice this is totally optional, as by default the server will be started when the first annotation is performed
client.start()
time.sleep(10)

js = open("C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset/kathleenemiller/bio.json")
sentence = json.load(js)
print(sentence)
document = client.annotate(sentence)
print(type(document))