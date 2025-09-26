import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

filmes = []  # lista global para armazenar filmes

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/cadastro':
            self.serve_html('cadastrofilmes.html')
        elif self.path == '/filmes':
            self.serve_filmes()
        else:
            super().do_GET()

    def serve_html(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, f"Arquivo {filename} não encontrado")

    def serve_filmes(self):
        try:
            with open('filmes.html', 'r', encoding='utf-8') as f:
                html = f.read()
        except FileNotFoundError:
            self.send_error(404, "Arquivo filmes.html não encontrado")
            return

        linhas = ""
        for filme in filmes:
            linhas += f"""
            <tr>
                <td>{filme.get('nome','')}</td>
                <td>{filme.get('atores','')}</td>
                <td>{filme.get('diretor','')}</td>
                <td>{filme.get('ano','')}</td>
                <td>{filme.get('genero','')}</td>
                <td>{filme.get('produtora','')}</td>
                <td>{filme.get('sinopse','')}</td>
            </tr>
            """

        html = html.replace("<!-- LISTA_DE_FILMES -->", linhas)

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        if self.path == '/send_cadastrofilmes':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            form = parse_qs(body)

            filme = {
                'nome': form.get('nome', [''])[0],
                'atores': form.get('atores', [''])[0],
                'diretor': form.get('diretores', [''])[0],
                'ano': form.get('ano', [''])[0],
                'genero': form.get('genero', [''])[0],
                'produtora': form.get('produtora', [''])[0],
                'sinopse': form.get('sinopse', [''])[0]
            }

            filmes.append(filme)

            self.send_response(303)
            self.send_header('Location', '/filmes')
            self.end_headers()

def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print("Servidor rodando em http://localhost:8000")
    httpd.serve_forever()

if __name__ == '__main__':
    main()
