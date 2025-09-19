#from http.serve import SimpleHTTPRequestHandler, HTTPServe

# #definindo a porta
# port = 8000

# #definindo o gerenciador/manipulador de requisições
# handler = SimpleHTTPRequestHandler

# #criando a instancia servidor
# server = HTTPServer(("localhost", port), handler)

# #imprimindo mensagem de ok
# print(f"Server initiated in http://localhost:{port}")



# server.serve_forever()


import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

filmesCadastrados = []

class MyHandle (SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            f = open(os.path.join(path, 'index.html'), 'r')
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f.read().encode('utf-8'))
            f.close()
            return None
        except FileNotFoundError:
            pass
        return super().list_directory(path)
    

    def accont_user(self, login, senhaa):
        loga = "rebeca@gmail.com"
        senha = 1234

        if login == loga and senha == senhaa:
            return "Usuário logado"
        else:
            return "Usuário não existe"
        

    def do_GET(self):
        if self.path == '/login':
            try:
                with open(os.path.join(os.getcwd(), 'login.html'), 'r') as login:
                    content = login.read()

                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))

            except FileNotFoundError:
                self.send_error(404, 'file not found')
        elif self.path == '/cadastro':
            try:
                with open(os.path.join(os.getcwd(), 'cadastrofilmes.html'), 'r') as login:
                    content = login.read()

                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))

            except FileNotFoundError:
                self.send_error(404, 'file not found')

        elif self.path == '/filmes':
            try:
                with open(os.path.join(os.getcwd(), 'filmes.html'), 'r') as login:
                    content = login.read()

                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))

            except FileNotFoundError:
                self.send_error(404, 'file not found')
        else:
            super().do_GET()

        if self.path == '/filmes':
            html = "<html><body><h1>Filmes Cadastrados</h1><ul>"
            for filme in filmesCadastrados:
                html += f"<li><strong>{filme['Nome do filme']}</strong> - {filme['Diretor']} ({filme['Ano que foi lançado']})</li>"
            html += "</ul></body></html>"

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))

        else:
            super().do_GET()
                

    def do_POST(self):
        if self.path == '/send_login':
            content_length = int(self.headers['Content-length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            login = form_data.get('email', [''])[0]
            senha = int(form_data.get('senha', [''])[0])

            logou = self.accont_user(login,senha)

            print("Data form:")
            print("Email: ", form_data.get('email', [''])[0])
            print("Password: ", form_data.get('senha', [''])[0])


            self.send_response (200)
            self.send_header ("Content-type", "text/html")
            self.end_headers ()
            self.wfile.write ("Data Retrieving Sucess!".encode('utf-8'))
            self.wfile.write(logou.encode('utf-8'))

        elif self.path == '/send_cadastrofilmes':
            content_length = int(self.headers['Content-length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_datafilme = parse_qs(body)

            nomeFilme = form_datafilme.get('nome', [''])[0]
            atoresFilme = form_datafilme.get('atores', [''])[0]
            diretorFilme = form_datafilme.get('diretores', [''])[0]
            anoFilme = form_datafilme.get('ano', [''])[0]
            generoFilme = form_datafilme.get('genero', [''])[0]
            produtoraFilme = form_datafilme.get('produtora', [''])[0]
            sinopseFilme = form_datafilme.get('sinopse', [''])[0]

            filminhos = {
                'Nome do filme ' : nomeFilme,
                'Atores do filme ' : atoresFilme,
                'Diretor ' : diretorFilme,
                'Ano que foi lançado ' : anoFilme,
                'Genero do filme ' : generoFilme,
                'Produtora ' : produtoraFilme,
                'Sinopse do filme ' : sinopseFilme
            }

            filmesCadastrados.append(filminhos)
            

            self.send_response (200)
            self.send_header ('location', '/filmes')
            self.end_headers ()
            self.wfile.write("Filme cadastrado com sucesso!!!!!".encode('utf-8'))
            
        else:
            super(MyHandle, self).do_POST()
    
def main ():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandle)
    print('Server running in http://localhost:8000')
    httpd.serve_forever()

main()