```bash
git clone https://github.com/ikgron/Dash.git 
```

```bash
cd Dash
```

```bash
docker compose up
```
## Setup
1. Go to localhost:8080
2. Enter credentials:
    username: admin@email.com
    password: admin
3. Add server
    postgres | postgres
    username: admin
    password: admin
    create

## Finding / Creating Table
1. dropdown > servers > Databases > data (set in docker compose) > Schemas > public > tables > data

2. right click > create > table
    name it data

3. Add 3 columns : target_id (text); phase_timestamp (timestamp without timezone); phase (text)
    create

4. right click data table > import/export data > 3 dots > import > select your csv > click the top X > select csv > ok > import

5. go to localhost:8050 to view dashboard