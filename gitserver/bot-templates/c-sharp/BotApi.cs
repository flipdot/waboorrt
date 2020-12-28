using EdjCase.JsonRpc.Router;
using EdjCase.JsonRpc.Router.Abstractions;

namespace Wabooorrt
{
	public enum BotWalkDirection
	{
		North,
		East,
		South,
		West,
	}

	public interface IBotOperation
	{
		string Name { get; init; }
	}

	public class BotNoOperation : IBotOperation
	{
		public string Name { get; init; } = "NOOP";
	}

	public class BotWalkOperation : IBotOperation
	{
		public string Name { get; init; }

		public BotWalkOperation(BotWalkDirection direction)
		{
			Name = $"WALK_{direction.ToString().ToUpperInvariant()}";
		}
	}

	public class BotThrowOperation : IBotOperation
	{
		public string Name { get; init; } = "THROW";
		public int? X { get; set; }
		public int? Y { get; set; }

		public BotThrowOperation()
		{
		}

		public BotThrowOperation(int x, int y)
		{
			X = x;
			Y = y;
		}
	}

	public class BotLookOperation : IBotOperation
	{
		public string Name { get; init; } = "LOOK";
		public double? Range { get; set; }

		public BotLookOperation()
		{
		}

		public BotLookOperation(double range)
		{
			Range = range;
		}
	}
}