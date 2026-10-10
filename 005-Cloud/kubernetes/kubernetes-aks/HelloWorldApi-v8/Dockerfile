FROM registry.access.redhat.com/ubi8/dotnet-80:8.0
WORKDIR /src

COPY ["HelloWorldApi.csproj", "."]
COPY . .
RUN dotnet publish -c Release -o /src/publish

WORKDIR /src/publish

ENV ASPNETCORE_HTTP_PORTS=8080
EXPOSE 8080

ENTRYPOINT ["dotnet", "HelloWorldApi.dll"]
