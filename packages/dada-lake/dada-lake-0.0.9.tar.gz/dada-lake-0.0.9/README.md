# `dada-lake`

a `dada-lake` is an asset, metadata, and graph store, designed to ingest, transform, remix, and relate files of all kinds. Its API is built to serve the textures, images, videos, 3D objects, and sounds found on projects for [`globally.ltd`](https://globally.ltd).

## how is a dada-lake organized? 

a `dada-lake` is organized into a series of `entity_types` which can be related to each other. at its core is the `file` entity, which represents an individual file of any format. archive files (eg `zip`, `tar.gz`, etc) are also supported.


### files

`files` can have a `file_type` of `audio`, `image`, `video`, `data`, `code`, `doc`, `bundle` or simply `raw`. these types are inferred upon ingestion.
- `audio` files are `mp3`, `aiff`, `midi`, `flac`, etc. _(supported)_
- `image` files are `jpg`, `png`, `tiff`, `svg`, etc. _(supported)_
- `video` files are `mp4`, `webm`, `mov`, etc. _(supported)_
- `model` files are `gltf`, `obj`, `fbx`, etc. _(in progress)_
- `data` files are `csv`, `json`, `parquest`, `shp`, etc. _(in progress)_
- `code` files are `py`, `js`, `sh`, `html`, `css`, etc.  _(in progress)_
- `doc` files are `docx`, `txt`, `ppt`, `md`, etc.  _(in progress)_
- `bundle` files are `zip`, `tar.gz`, etc _(supported)_
    - the contents of `bundle` files are extracked and nested under the original archive file.
    - these contents can also be extracted as their own files, with the relationship between the parent and child retained. more on this below re: `macros`.
- `raw` files are those that don't fall into the above categories or whose types cannot be inferred.

### fields

for each `file` you can create a series of `fields` to associate with it. these `fields` can have their own `type`, representing the data value (eg `int`, `text`, `float`, etc) stored in the `field`. On ingestion, input data are validated against these `type`. You can also associate `fields` with any other `entity_type`. in this way, `fields` enable dada-lake's schema to be specified on a per-instance basis, or grow large to fit various use cases within a single instance. a dada-lake can be small: just a database and directory on your local machine, or a large cluster of databases and distributed file stores across many users and many machines. 

### folders + desktops

`files` can be related to `folders` and/or `desktops`. in each case, the `file` can have an associated `position` in the `folder` and/or `desktop`. `folders` can similarly be nested under `desktops`, with their own distinct `position`. `folders` and `desktops` can contain any combination of `files`. `fields` can also be associated with `file_folder` and `folder_desktop` relations, enabling the potential of relation-specific attributes. 

### themes + tags

every entity in the `dada-lake` can also have an associated `theme` and set of `tags`. A `theme` represents visual components associated with an `entity_type`. for a `image file`, this might include a thumbnail of that image, or a series of dominant colors contained within it. for a `folder`, this might include a representative emoji or a cover image. like other entities, `themes` can also have `fields`, so their schema is similarly flexible.

`tags` are global and can exist in a many-to-many relationship with any other `entity_type` (including other `tags`). `tags` allow you to easily create groups of related `entity_types`. for instance, we tag all `entity_types` related to `fifteen.pm` in order to keep track of all the assets related to that project. that being said, some of those `entity_types` can also be related to `globally.ltd`, a different `tag`.

### how is data queried?

data is queried via the a RESTful JSON API. each `entity_type` shares a similar search interface. full documentation (as well as an interactive api console) are available at [http://localhost:3030/docs] after starting a local server. (more on this below)

#### filter strings

`dada-lake` employs a DSL for constructing search filter statements we call "filter strings". filter strings are comprised of three elements: a field name, an operation, and a value. for instance, the filter string `name:lk:brian%` would translate to the SQL statement `WHERE name like 'brian%'`. `bpm:bt:100,120` would translate to `WHERE bpm BETWEEN 100 and 120` filters can be combined together via an `or` or `and` logic to build increasingly complex queries.

### how are files stored? 

When files are imported into a `dada-lake` they are first stored `locally` on any drive accessible to the API server (for instance, if running locally, on an external hard drive connected to your computer, or if on a cloud server, some network accessible drive. this parameter is set in the[.env](.env.sample) file). common metadata is extracted for all imported `files`, including a `check_sum`, which is used to create a unique `partition` for each file. underneath this partition, separate `version` partitions are created for each update to a `file`. in addition a `latest` version is set for each update.

an example of a `local` url might be: 
- `/Users/joora/.dada/stor/e=file/t=audio/s=track/x=mp3/y=20/m=5/d=22/h=10/i=1/v=dklfkasdflkdsajfalsdf-20052210/Screen Shot 2020-05-19 at 9.10.58 AM.png`
- here `e` is the `entity_type`, `t` is the `file_type`, `x` is the file `ext`, `y`, `m`, `d`, and `h` are the entity's created year, month, date, and hour, respectively. and `v` is the unique version identifier, consisting of the file `check_sum` and a `udpated_at` time.

in addition to this file, a `.dada` file is also created. a `.dada` file is a `json.gz` encoded representation of metadata associated with that file. this includes all assoicated `fields`, `folders`, `tags`, etc. `.dada` files live in the same directory as their associated files. for instance, the `.dada` path to the url above would be: `/Users/joora/.dada/stor/e=file/t=audio/s=track/x=mp3/y=20/m=5/d=22/h=10/i=1/v=dklfkasdflkdsajfalsdf-20052210/Screen Shot 2020-05-19 at 9.10.58 AM.dada`

each `dada-lake` can also be configured to distribute assets `globally`. this entails pushing a file currently stored locally to an amazon s3 bucket/digital ocean space with a similar directory structure. the only difference here, however, is that all files pushed to `s3`  / `digital-ocean` are automatically `gzipped` (unless they are already compressed (eg. `mp4` files)). each `file` can be set to `is_public`, which will make this url publically accessible on the web.

## how do i work on `dada-lake` on my computer?

### how is code organizeded?

the codebase for `data-lake` is split up into:
  - [the core module](dada/) for the API and data model
  - [multiple python libraries](lib/) which contain re-usable utilities used across the codebase
### docker build

You can start up an API cluster using [`docker-compose`](https://docs.docker.com/compose/).

first, copy [`.sample.env`](.sample.env) to `.env` and add your credentials. the most importat are the AWS access key and secret.

next run this command.:

```
docker-compose up -d 
```

You should now be able to access the following resources:

- [http://localhost:3031/docs](http://localhost:3031/docs)
    * API Documentation, Powered by [Swagger](https://swagger.io/)
- [http://localhost:3031/spec.json](http://localhost:3031/spec.json)
    * An [OpenAPI](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md) Specification
- [http://localhost:3031/users?api_key=dev](http://localhost:3031/users?api_key=dev)
    * An example API endpoint

### local development

to set up a local _MAC OS X_ dev environment, first install the `brew` dependencies:

```
brew bundle
```

Next, copy [`.sample.env`](.sample.env) to `.env` and add your credentials. the most importat are the AWS access key and secret.

Next create a virtual environment with using your tool of choice and install an editable version of the library:

```
make install
```

You should now be able to run the common [`Makefile`](./Makefile) commands. 

Most make commands accept the argument `env={}`. this value can either be `test`, `dev`, `prod`, or `docker`. 
each of these environments load different app configurations found in [`dada/config`](dada/config).

- `make db-upgrade`: run alembic migrations 
- `make db-migrate`: record a migration and create an updated [db schema diagram](migrations/db-schema.pdf)
- `make db-create-defaults`: create defaults as defined in [`dada/config/models/`](dada/config/models)
- `make serv-flask`: run a local development server 
- `make serv-gunicorn`: run a production gunicorn server 
- `make shell`: open a flask shell inside the application context with access to common models.

### start a local server 
- to start a local server, first open another shell and ensure that `redis-server` is running. 
- in another tab, start a `celery` helper by running `make celery-helper env={}`
- in another shell, start the api server by runnng `make serv-flask env={}`

you should be able to navigate to the api docs at [http://localhost:3030/docs]

### tests
- many tests require no other resources and can be run standalone via `make test_one t=path/to/test.py`
- tests that interact with the API and require `celery`  should be run by first starting a celery helper using the `env` of `test`:
  * `make celery-helper env=test`
- at which point you can run the full test suite via `make test` 

## TODOs

### PRIORITIES
- [ ] fix test modules
- [ ] move to digital ocean spaces for file storage.
- [ ] basic cli for uploading / downloading / searching files
- [ ] finalize local storage vs global storage?
- [ ] public / private controls file controls and tests for this functionality.

### DEV
- [ ] Abstracting all libraries out into separate, re-usable modules.
- [ ] Finishing writing out tests for all core api methods (`fields`, `files`, `users`, `desktops`, etc.)
- [ ] tests for tagging 
- [ ] tests for adding relationships
- [ ] tests for relationship filtering
- [ ] tests for removing relationships
- [ ] fix docker setup and finish modernizing to new `docker-compose` features 
### FEATURES
- [ ] Move to ltree model for file-file + tag-tag + folder-folder + desktop-desktop relationships
    - https://www.postgresql.org/docs/current/ltree.html
    - https://kite.com/blog/python/sqlalchemy/
- [ ] Support for `data` file type which stores data as parquet on S3.

### IMPORT via CLI
  - [ ] File
  - [ ] Archive
  - [ ] Implement bulk-editing API
  - [ ] Youtube DL 
  - [ ] Rekordbox
  - [ ] Itunes
  - [ ] Bandcamp
  - [ ] Mixcloud
  - [ ] Beatport
- Export
  - [ ] Folder Archive
  - [ ] Desktop Archive
  - [ ] Rekordbox
- Transform
  - [x] Exif-extraction for images 
  - [x] FFmpeg-extraction for video
  - [x] Rename + Update ID3 tags for audio
  - [ ] De-duping via fuzzy-string matching
  - [ ] Conversions, conversions, conversions!
