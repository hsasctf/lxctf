# pwstore REST-Api

- every request requires `Content-Type: application/json; charset=utf-8`
- every response returns `Content-Type: application/json; charset=utf-8`

## Workflow

### 1. Register at `/register`

- required arguments in http body

    ```JavaScript
    {
        'username': 'your_name',
        'masterpw': 'password used for authentication and encryption of your other passwords'
    }
    ```

- sample response

    ```JavaScript
    HTTP/1.1 201 Created
    ...
    {
        "user": "someuser"
    }
    ```

### 2. Store a password at `/addentry`

- required arguments in http body

    ```JavaScript
    {
        'username': 'your_name',
        'masterpw': 'password used for authentication and encryption of your other passwords',
        'pw_entry': 'you pw to store',
        'description' : 'description for your stored password'
    }
    ```

- sample response

    ```JavaScript
    HTTP/1.1 201 Created
    ...
    {
        "pw_entry": {
            "description": "paypal",
            "pw_id": 1548850335,
            "user": "someuser"
        }
    }
    ```

### 3. Get your saved password at `/getentry`

- required arguments in http body

    ```JavaScript
    {
        'username': 'your_name',
        'masterpw': 'password used for authentication and encryption of your other passwords',
        'pw_id': 'id of your saved password from response at password creation'
    }
    ```

- sample response

    ```JavaScript
    HTTP/1.1 200 OK
    ...
    {
        "pw_entry": {
            "creation_timestamp": "2019-11-20T18:00:09.367031",
            "description": "paypal",
            "pw": "4321",
            "pw_id": 1548850335,
            "username": "someuser"
        }
    }
    ```
