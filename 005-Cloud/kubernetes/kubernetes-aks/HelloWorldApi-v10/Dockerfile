FROM registry.access.redhat.com/ubi9/dotnet-100:9.8-1790211954
WORKDIR /src

COPY ["HelloWorldApi.csproj", "."]
COPY . .
RUN dotnet publish -c Release -o /src/publish

WORKDIR /src/publish

ENV ASPNETCORE_URLS=http://+:8081
EXPOSE 8081

ENTRYPOINT ["dotnet", "HelloWorldApi.dll"]
