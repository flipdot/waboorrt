using System;
using EdjCase.JsonRpc.Router;
using EdjCase.JsonRpc.Router.Abstractions;
using Microsoft.Extensions.Logging;
using System.Text.Json;

namespace Wabooorrt
{
	[RpcRoute("jsonrpc")]
	public class BotController : RpcController
	{
		private readonly ILogger _logger;

		public BotController(ILoggerFactory logger)
		{
			_logger = logger.CreateLogger(nameof(BotController));
		}

		public IRpcMethodResult NextAction(object gameState, string yourName)
		{
			_logger.LogInformation("Next action requested.");
			_logger.LogInformation(JsonSerializer.Serialize(gameState));

			var rnd = new Random();

			var noop = new BotNoOperation();
			var walk = new BotWalkOperation(BotWalkDirection.North);
			var throww = new BotThrowOperation(rnd.Next(0, 50), rnd.Next(0, 50));
			var look = new BotLookOperation(rnd.Next(0, 50));

			var actions = new IBotOperation[] { noop, walk, throww, look };
			var result = actions[rnd.Next(0, actions.Length)];

			_logger.LogInformation("Sending reply: {Result}", JsonSerializer.Serialize(result));

			return this.Ok(result);
		}

		public IRpcMethodResult Health()
		{
			return this.Ok(true);
		}
	}
}