<p align="center">
    <img alt="Tyran Logo" src="/static/img/logo.jpg" height="400" />
    <h3 align="center">Tyran</h3>
    <p align="center">A Vector Search as a Service.</p>
    <p align="center">
        <a href="https://github.com/Clivern/Tyran/actions/workflows/api.yml">
            <img src="https://github.com/Clivern/Tyran/actions/workflows/api.yml/badge.svg"/>
        </a>
        <a href="https://hub.docker.com/r/clivern/tyran">
            <img src="https://img.shields.io/badge/Docker-0.7.1-1abc9c.svg">
        </a>
    </p>
    <p align="center">
        <img alt="Tyran Chart" src="/static/img/chart.png" height="400" />
    </p>
</p>
<br/>

`Tyran` is a vector search as a service, designed to efficiently retrieve relevant context for large language models (`LLMs`). `Tyran` organizes documents alongside their associated metadata, such as topic, project or team, to enhance the search process.


## Quick Start

> [!IMPORTANT]
>
> Make sure you have docker and docker-compose installed for the quick start.


To run `Tyran` with `sqlite` and `qdrant` on port `8000` on docker.

```bash
$ wget https://raw.githubusercontent.com/Clivern/Tyran/main/docker-compose-sqlite.yml \
    -O docker-compose.yml

$ export OPENAI_API_KEY=~~key goes here~~

$ docker-compose up -d
```

To run `Tyran` with `mysql` and `qdrant` on port `8000` on docker.

```bash
$ wget https://raw.githubusercontent.com/Clivern/Tyran/main/docker-compose-mysql.yml \
    -O docker-compose.yml

$ export DB_USERNAME=tyran
$ export DB_PASSWORD=D1q9f0C2PEW
$ export OPENAI_API_KEY=~~key goes here~~

$ docker-compose up -d
```

To test the setup, create a simple document and then query it.

```bash
$ curl -X POST \
  http://127.0.0.1:8000/api/v1/document \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"content": "Hello World", "metadata": {"type":"testdata"}}'

{
  "id": "3d0ffff3-5d05-46e3-84c3-b805aad93a81",
  "content": "Hello World",
  "metadata": {
    "type": "testdata"
  },
  "createdAt": "2024-09-06T11:16:00",
  "updatedAt": "2024-09-06T11:16:00"
}

$ curl -X POST \
  http://127.0.0.1:8000/api/v1/document/search \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"text": "hi world", "limit": 1, "metadata": {"type":"testdata"}}'

[
  {
    "id": "3d0ffff3-5d05-46e3-84c3-b805aad93a81",
    "content": "Hello World",
    "metadata": {
      "type": "testdata"
    },
    "createdAt": "2024-09-06T11:13:27",
    "updatedAt": "2024-09-06T11:13:27",
    "score": 0.85183966
  }
]
```


## Versioning

For transparency into our release cycle and in striving to maintain backward compatibility, Tyran is maintained under the [Semantic Versioning guidelines](https://semver.org/) and release process is predictable and business-friendly.

See the [Releases section of our GitHub project](https://github.com/Clivern/Tyran/releases) for changelogs for each release version of Tyran. It contains summaries of the most noteworthy changes made in each release. Also see the [Milestones section](https://github.com/Clivern/Tyran/milestones) for the future roadmap.


## Bug tracker

If you have any suggestions, bug reports, or annoyances please report them to our issue tracker at https://github.com/Clivern/Tyran/issues


## Security Issues

If you discover a security vulnerability within Tyran, please send an email to [hello@clivern.com](mailto:hello@clivern.com)


## Contributing

We are an open source, community-driven project so please feel free to join us. see the [contributing guidelines](CONTRIBUTING.md) for more details.


## License

© 2024, Tyran. Released under [MIT License](https://opensource.org/licenses/mit-license.php).

**Tyran** is authored and maintained by [@Clivern](https://github.com/clivern).
