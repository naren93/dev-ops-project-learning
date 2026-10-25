FROM registry.access.redhat.com/ubi8/dotnet-80:8.0
WORKDIR /opt/app-root/src

COPY --chown=1001:0 ["HelloWorldApi.csproj", "."]
COPY --chown=1001:0 . .
RUN dotnet publish -c Release -o /opt/app-root/publish

WORKDIR /opt/app-root/publish

ENV ASPNETCORE_HTTP_PORTS=8080
EXPOSE 8080

ENTRYPOINT ["dotnet", "HelloWorldApi.dll"]
