# Service requirements

This Document describes the requirements of a service to be used in this Framework

## Flags

This framework is for attack and defense ctf's. Each team is hosting one instance of each vulnerable service. These instances can be attacked by ther teams to get flags which can be exchanged for points. A team should also patch their own service instances so other teams can't exploit them

- Flags are placed into each service by the so-called `scorebot` every few minutes (-> new flags each round)
- Flags are *private* to the creator (either scorebot or other teams using the service)
- Flags will only give points for the round they were set in
- Flags look like `FLAG_RAAqLrPyMnIXQ`
- Each flag has a random `flag_id` (i.e. this could be used by scorebt as some kind of username)
- Trying to reedem the flags from a teams own services will not give any points
- Services have to be up and running all time (stopped services will cause a penalty)
- DoS'ing other teams' services is prohibited and will result in disqualification

## Vulnerabilities

- The goal is to exploit something, so retrieving flags should __not__ only be possible by bruteforcing
- Each service should have __several__ vulnerabilities
- Each vulnerability has to (directly or indirectly) lead to the __same__ flag

This leads to situations when team A fixed 3/4 vulnerabilities in their own service and team B can possibly still get points by exploiting the 4th one while team C only found one vulnerability but didn't patch it yet so team A and B can get 4 flags/round by team C while team C only gets one flag/team/round (or none, as the others patched it already)

## Networking functionality

Due to the nature of an attack and defense ctf, services have to somehow be reachable over the network by other teams. Also the scorebot keeps checking if the service is up and running correctly, so a service has to provide some way of interaction over the network for the scorebot to perform its checks.

### Setflag/Getflag scripts

The way scorebot determines if the service is running correctly is by interacting with it like a *normal user* would.

For an imaginary social network service this could be first to register a user (with name=`flag_id`), creating a private post (including the actual `flag`) and later logging back in to retrieve the flag. If the flag still matches the originally posted one, the service is considered to work correctly.

Each service has to provide the scripts the scorebot uses to perform these actions. Scorebot will first run the setflag and later the getflag script. It will invoke some methods that have to be provided by the scripts.
Due to the Scorebot being python 2, these scripts also have to be written in python 2

Setflag:

- script has to provide an `execute(ip, port, flag)` method (arguments provided by scorebot, return val unsed)
- script has to provide a `result()` method returning following dict:

    ```python
    {
        'FLAG_ID': 'unique string chosen by setflag script',  
        'TOKEN': 'something that needs to be passed to getflag scipt in order for it to work (type does not matter)',
        'ERROR': 0, # int
        'ERROR_MSG': 'string describing some error during script execution (may be empty)'
    }
    ```

Getflag:

- script has to provide an `execute(ip, port, flag_id, token)` method (arguments provided by scorebot, return val unused)
- script has to provide a `result()` method returning following dict:

    ```python
    {
        'FLAG': 'the flag that is successfully retrived again by the interaction between script and service',
        'ERROR': 0, # int
        'ERROR_MSG': 'string describing some error during script execution (may be empty)'
    }
    ```

Error scores:

Always return an error as integer

- negative integer: Service is down
- zero: Service is up und functional
- Positive integer: Service is up and not functional

Examples for both scripts can be found [here](https://github.com/hsasctf/lxctf/blob/master/services/2019/logserver/scripts/)

## OS

At the moment the team containers are running ubuntu 16.04, so services have to be able to run on this os. The language the service is written in is free to choose. Build instructions have to be included if neccessary (i.e. a CMakeLists.txt if the service is using cmake to build)

## Integration

In order to integrate the script into the framework, some information has to be provided by the script creator in form of `info.json` and `info.yml`.

The information provided by the creator of a service is marked with `//*` or `#*`

`info.json`:

```JavaScript
{
  "name" : "name of the service", //*
  "authors" : ["Your name"], //*
  "points": 100, 
  "flag_id_description": "brief description of what the flag_id is in context of the service (i.e. username)", //*
  "service_description": "brief description of your service", //*
  "port" : 5001,
  "getflag" : "scripts/getflag.py",
  "setflag" : "scripts/setflag.py",
  "is_working" : 1
}
```

`info.yml`:

```YML
architecture: x86_64
service_name: Attending teams can read this. #*
type: web
description: Attending teams can read this. #*
flag_id_description: Attending teams can read this #*
apt_dependencies: #*
    - libboost-all-dev
    - libssl-dev
    - g++
    - cmake
```


## Firewall integration

Open the vars/main.yml in role/firewall.
Add all the service's ports to this list, so the firewall is configured correctly (usually starting at port 5001).