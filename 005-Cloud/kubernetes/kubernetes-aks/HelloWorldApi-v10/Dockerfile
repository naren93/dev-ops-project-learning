FROM registry.access.redhat.com/ubi9/dotnet-100:9.8-1790211954
WORKDIR /opt/app-root/src

COPY --chown=1001:0 ["HelloWorldApi.csproj", "."]
COPY --chown=1001:0 . .
RUN dotnet publish -c Release -o /opt/app-root/publish

WORKDIR /opt/app-root/publish

ENV ASPNETCORE_URLS=http://+:8081
EXPOSE 8081

ENTRYPOINT ["dotnet", "HelloWorldApi.dll"]
