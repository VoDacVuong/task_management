# Task Management

Task management api



```

## Create database
```
CREATE USER dev SUPERUSER;

ALTER USER dev WITH PASSWORD 'password';

CREATE DATABASE task_management_db WITH OWNER dev;
```

## Install Virtual environment
```
python3 -m venv venv
```

or

```
python3.8 -m venv venv
```

## Activate the virtual environment
```
source venv/bin/activate
```

## Install libraries
```
pip install -r requirements.txt
```

# Default admin account
Go to: http://localhost:8000/admin
Login with credentials
```
username: admin@example.com
password: admin
```
