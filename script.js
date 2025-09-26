const lis = document.querySelector('#filmes');
 
fetch('http://localhost:8000/get_lista').then((res)=>{
    return res.json();
}).then((data)=> {
    data.map((lista)=> {
        console.log(lista)
        lis.innerHTML +=`
        <li>
            <strong>Nome do filme:</strong> ${lista.nome} <br></br>
            <strong>Atores:</strong> ${lista.atores} <br></br>
            <strong>Diretor:</strong> ${lista.diretor} <br></br>
            <strong>Ano:</strong> ${lista.ano} <br></br>
            <strong>Gênero:</strong> ${lista.genero} <br></br>
            <strong>Produtora:</strong> ${lista.produtora} <br></br>
            <strong>Sinopse:</strong> ${lista.sinopse} <br></br>
        </li>`
    })
})