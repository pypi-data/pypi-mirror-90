import esppy.espapi.connections as connections
import esppy.espapi.codec as codec
import esppy.espapi.tools as tools

def connect(session,k8s,delegate = None,**kwargs):

    conn = connections.ServerConnection(session,k8s,delegate,**kwargs)
    conn.start()
    return(conn)

def encode(o):
    encoder = codec.JsonEncoder(o)
    return(encoder.data)

def decode(data):
    decoder = codec.JsonDecoder(data)
    return(decoder.data)

def guid():
    return(tools.guid())
