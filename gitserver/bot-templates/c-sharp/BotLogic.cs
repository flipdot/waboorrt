using System;
using Microsoft.Extensions.Logging;
using System.Text.Json;
using Wabooorrt.BotApi;
using System.Collections.Generic;

namespace Wabooorrt
{
	public class BotLogic
	{
		private readonly ILogger _logger;

		public BotLogic(ILoggerFactory logger)
		{
			_logger = logger.CreateLogger(nameof(BotLogic));
		}

		public IOperation NextAction(Me me, Meta meta, List<Entity> entities)
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

			return result;
		}
	}
}