# MyBook

_My Book_ é um projeto MVC desenvolvido em _Django_. Seu objetivo principal é cadastro de _audiobooks_.

As seguintes funcionalidades estão presentes no projeto:

- Controle de acesso por grupos de permissão (Administrador, Narrador e Ouvinte);
- CRUD de Usuários, Livros, _Audiobooks_;
- Reproduzir _audiobooks_;
- _Login_ e _logout_;

## Tecnologias utilizadas

- Python 3.8
- Django 3.2.5
- SQLite 3 (Ambiente DEV)
- MySQL (_Latest_) (Ambiente QAS/PRD)
- Nginx (_Latest_)
- uWSGI
- Docker 20.10.11
- Docker Compose 1.29.2

## Ferramentas utilizadas

- _Windows 10_
- _Ubuntu 20.04 LTS (WSL2)_
- _Visual Studio Code_

## Execução do projeto (_Docker Compose_)

Gerar o _build_ do projeto a partir do arquivo _docker-compose.yml_:

```sh
    docker-compose build
```

Iniciar os containers do _NGINX_, _MySQL_ e _Aplicação_:

```sh
    docker-compose up -d
```

O serviço estará disponível em [http://localhost/](http://localhost/).