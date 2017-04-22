FROM microsoft/dotnet:1.1.1-sdk

WORKDIR /code

ADD src/Worker /code/src/Worker

ENV REDIS_HOST="redis" PGHOST="db"

RUN dotnet restore -v minimal src/Worker \
    && dotnet publish -c Release -o "./" "src/Worker/"

CMD dotnet src/Worker/Worker.dll
