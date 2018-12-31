# Seki

[![PyPI version](https://badge.fury.io/py/seki.svg)](https://badge.fury.io/py/seki)
[![Known Vulnerabilities](https://snyk.io/test/github/oscarbc96/seki/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/oscarbc96/seki?targetFile=requirements.txt)
[![Supported python versions](https://img.shields.io/pypi/pyversions/seki.svg)](https://github.com/oscarbc96/seki)
[![License](https://img.shields.io/github/license/oscarbc96/seki.svg)](https://github.com/oscarbc96/seki)

Seki has been created to automatically generate `drone.yml` files to run security tools in the cloud.

## Related projects

- [Seki Server](https://github.com/oscarbc96/seki-server): example project to deploy drone server.
- [SecTools](https://github.com/oscarbc96/sectools): collections of public security related tools containerized.

## Installation

1. Install [Drone CLI](https://docs.drone.io/cli/install/)
2. Install seki
```bash
pip install seki
```

## Usage

Some seki functions use drone cli commands. To be able to use them, `DRONE_SERVER` and `DRONE_TOKEN` must be exported in terminal. You can find them in drone web ui inside account settings.

### Run

This command allows to run docker images on

```
Usage: seki run [OPTIONS] IMAGE
```

| Option     | Value                                   | Description                      |
|------------|-----------------------------------------|----------------------------------|
| --args     | TEXT                                    | Arguments for docker image.      |
| --telegram |                    -                    | Notify on telegram build result. |
| --cron     | @hourly,@daily,@weekly,@monthly,@yearly | Cron job                         |

#### Telegram

To use the telegram option the following [secrets](#Secrets) must be set:
`telegram_token`: telegram token from [telegram developer center](https://core.telegram.org/bots/api)
`telegram_to`: telegram user id (can be requested from the `@userinfobot` inside Telegram)

#### Examples

Find subdomains for `google.com` and get results back in telegram.
```bash
seki run oscarbc/subfinder.subfinder --args "subfinder -d google.com -o result.txt" --telegram
```

### Templates

```
Usage: seki template [OPTIONS] FILE
```

| Option | Value                                   | Description |
|--------|-----------------------------------------|-------------|
| --cron | @hourly,@daily,@weekly,@monthly,@yearly | Cron job    |

#### Parameters

Templates can have defined parameters. Parameters must be defined as a list in the first line of the template.

```yaml
# PARAMETERS: param1,param2,param3
```

And places to replace as follows:

```
  - echo $$PARAM1 $$PARAM2 $$PARAM3
```

#### Examples

Find subdomains for `google.com` and get results back in telegram. But this time using a template.
```bash
seki template test.yml
```
test.yml
```yml
# PARAMETERS: domain
clone:
  disable: true
kind: pipeline
name: default
steps:
- name: run
  image: oscarbc/subfinder.subfinder
  commands:
  - subfinder -d $$DOMAIN -o result.txt

- name: create tar
  image: alpine
  commands:
  - tar czf output.tar.gz .

- name: telegram notificaton
  image: appleboy/drone-telegram
  settings:
    document:
    - output.tar.gz
    format: markdown
    message: >
      {{#success build.status}}
          {{build.number}}: ✅ `{{commit.message}}` 🚁 [See build]({{build.link}})
      {{else}}
          {{build.number}}: ❌ `{{commit.message}}` 🚁 [See build]({{build.link}})
      {{/success}}
    to:
      from_secret: telegram_to
    token:
      from_secret: telegram_token
```

### Secrets

Secrets have to be registered inside seki drone project settings. Inside drone project settings [Drone docs](https://docs.drone.io/user-guide/pipeline/secrets/)

### Cron

To run pipelines periodically the system uses cron jobs from Drone. Seki creates a new branch and enables cron job for that new branch.

## Thanks

I would like to thank Drone to open source their project.

## License

seki is licensed under the MIT License. Take a look at the [LICENSE.md](LICENSE.md) for more information.
