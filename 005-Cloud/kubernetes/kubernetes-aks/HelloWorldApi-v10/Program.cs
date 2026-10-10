var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => Results.Ok(new
{
    message = "Hello from the .NET 10 API",
    version = "v10"
}));

app.MapGet("/health", () => Results.Ok(new { status = "healthy" }));

app.Run();
