# Setup
Assuming you have `docker` installed and running as a system service(if your system uses `systemd`, run `sudo systemctl start docker.service`), run the following from the project's root directory:
```
# this creates the data directory where the database will live
$ mkdir data

# build the docker image
$ ./run build

# run the docker image as a deamon, exposing the port 5000
$ ./run run -d

# run the docker not as a deamon, while still exposing the port 5000
$ ./run run

# to enter the shell inside the docker
$ ./run run shell
# if you wish to view the database, you can than run from within the docker shell:
$ sqlite3 data/sqlite.db

# if you wish to kill the docker image, run:
$ ./run kill

# for use of the run command use
$ ./run -h 
```

Alternatively, if you wish to run without `docker`, just run the `src/main.py` and all should work the same as with `docker`.

Once this is done, you can check that the service works by going to: `http://localhost:5000/api/swagger.json` for a `Swagger` documentation about this service's API.

## Tests
You can try the API by running the `tests/all.py` Python file, which should finish without any errors.

# TODO
- [x] `/posts/add` - using the userId, if the userId is not valid, return bad auth, if all is well, save
- [x] `/posts/userId/<uid>` or `posts/id/<id>` or `posts/` - attempt to return a post as json data
    - if searching by id and the post is not found, fetch from external API and save
- [x] `/posts/remove/<id>` - remove a post given its id
- [x] `/posts/edit/<id>` - change to title and body, to the new title and body
- [x] swagger documentation available on endpoint `/api/swagger.json`


# WORK TIME
1. 19.07.
    - 17:25 - 18:54 | `01:29`
2. 20.07.
    - 10:22 - 12:33 | `02:11`
3. 21.07.
    - 10:22 - 11:08 | `00:46`
    - 16:17 - 19:45 | `03:28`
    - 20:00 - 20:30 | `00:30`
4. 23.07.:
    - 19:05 - 19:30 | `00:25`
