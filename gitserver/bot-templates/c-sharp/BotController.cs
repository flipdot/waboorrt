using System;
using EdjCase.JsonRpc.Router;
using EdjCase.JsonRpc.Router.Abstractions;
using Microsoft.Extensions.Logging;
using System.Text.Json;
using Wabooorrt.BotApi;
using System.Collections.Generic;

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

		public IRpcMethodResult NextAction(Me me, Meta meta, List<Entity> entities)
		{
			_logger.LogInformation("Next action requested.");
			_logger.LogInformation(JsonSerializer.Serialize(me));
			_logger.LogInformation(JsonSerializer.Serialize(meta));
			_logger.LogInformation(JsonSerializer.Serialize(entities));

			var rnd = new Random();

			var noop = new NoOp();
			var walk = new WalkOp(Direction.North);
			var throww = new ThrowOp(rnd.Next(0, 50), rnd.Next(0, 50));
			var look = new LookOp(rnd.Next(0, 50));

			var actions = new IOperation[] { noop, walk, throww, look };
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