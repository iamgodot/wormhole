# Wormhole

Wormhole is a URL shortener based on Django.

## Features

1. URL shortening
   - For the same URL, short links differ by users
   - Default expiration for short links
2. Link redirection
   - 302 redirection for short link access

## Configuration

An `.env` file should be provided, see `.env.template`.

`BASE_URL` should be the base url of short links.

## Usage

```bash
# Deploy wormhole at localhost:8000
# Shorten a URL, short link will be `localhost:8000/4S4U4o`
curl localhost:8000/api/v1/short_links -d '{"url":"https://github.com/iamgodot/wormhole"}' -H 'content-type:application/json' -v

# Try access it, will get a 302 redirection
curl localhost:8000/4S4U4o -v
```

## License

[MIT](docs/LICENSE)
