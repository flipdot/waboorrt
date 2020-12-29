using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

namespace Wabooorrt
{
	public class Startup
	{
		public void ConfigureServices(IServiceCollection services)
		{
			services.AddJsonRpc(config =>
			{
				config.JsonSerializerSettings = new JsonSerializerOptions
				{
					PropertyNameCaseInsensitive = true,
				};
			});

			services.AddSingleton<BotLogic>();
		}

		public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
		{
			if (env.IsDevelopment())
			{
				app.UseDeveloperExceptionPage();
			}

			app.UseRouting();

			app.UseJsonRpc();
		}
	}
}
