APP				=	itotest

all:
	make build

build:
	docker build -t $(APP) .

run:
	docker run --rm --name itotest $(APP)

clean:
	docker stop $(APP); docker rm $(APP)
	docker container prune --force
