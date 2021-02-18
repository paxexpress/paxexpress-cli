# PAX Express

# Usage

```shell
poetry install

paxexpress --help
```

## CLI

### Authentication
>  virtual authentication
#### login
```shell
paxexpress authentication login
```
### logout
```shell
paxexpress authentication logout
```

### Repositories
#### Get all
> get all repositories of user
```shell
paxexpress repository all 
```
#### Get repository by name
```shell
paxexpress repository get -r [NAME]
```
#### Create a repository
```shell
paxexpress repository create -r [NAME]
```
#### Update a repository
```shell
paxexpress repository update -r [NAME]
```
#### Delete a repository
```shell
paxexpress repository delete -r [NAME]
```
#### Search 
```shell
paxexpress repository search -n [NAME] # search by name

paxexpress repository search -d [NAME] # search in descriptions
```