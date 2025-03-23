import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 13337))  

s.listen(1)
conn, addr = s.accept()

while True:

    try:
        # Send un ptit hello
        conn.send("Hello".encode())

        # On attend de recevoir un calcul du client
        data = conn.recv(1024)
        data = data.decode().strip("\n")

        # Evaluation et envoi du résultat
        res = eval(data)
        conn.send(str(res).encode())
        print("Réponse envoyée au client.")

    except socket.error:
        print("Une erreur est survenue, déso.")
        break

conn.close()
