FROM mcr.microsoft.com/dotnet/sdk:5.0-alpine AS build

WORKDIR /app

COPY *.sln *.csproj ./

RUN dotnet restore

COPY . ./

RUN dotnet publish -c Release -o out

FROM mcr.microsoft.com/dotnet/aspnet:5.0-alpine AS runtime
WORKDIR /app

EXPOSE 4000
ENV ASPNETCORE_URLS=http://+:4000
ENTRYPOINT ["dotnet", "Wabooorrt.dll"]
COPY --from=build /app/out ./