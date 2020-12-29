using System;
using Microsoft.Extensions.Logging;
using System.Text.Json;
using Wabooorrt.BotApi;
using System.Collections.Generic;

namespace Wabooorrt
{
	public class RandomBotLogic : IBotLogic
	{
		private readonly ILogger _logger;
		private Random _rnd = new Random();

		public RandomBotLogic(ILoggerFactory logger)
		{
			_logger = logger.CreateLogger(nameof(RandomBotLogic));
		}

		public IOperation NextAction(Me me, Meta meta, List<Entity> entities)
		{
			_logger.LogInformation("Next action requested.");
			_logger.LogInformation(JsonSerializer.Serialize(me));
			_logger.LogInformation(JsonSerializer.Serialize(meta));
			_logger.LogInformation(JsonSerializer.Serialize(entities));

			var noop = new NoOp();
			var walk = new WalkOp(Direction.North);
			var throww = new ThrowOp(_rnd.Next(0, 50), _rnd.Next(0, 50));
			var look = new LookOp(_rnd.Next(0, 50));

			var actions = new IOperation[] { noop, walk, throww, look };
			var result = actions[_rnd.Next(0, actions.Length)];

			_logger.LogInformation("Sending reply: {Result}", JsonSerializer.Serialize(result));

			return result;
		}
	}
}