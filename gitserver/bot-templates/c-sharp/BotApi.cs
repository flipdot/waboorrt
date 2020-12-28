using System.Collections.Generic;
using System.Text.Json.Serialization;
using EdjCase.JsonRpc.Router;
using EdjCase.JsonRpc.Router.Abstractions;

namespace Wabooorrt.BotApi
{
	public enum Direction
	{
		North,
		East,
		South,
		West,
	}

	public interface IOperation
	{
		string Name { get; init; }
	}

	public class NoOp : IOperation
	{
		public string Name { get; init; } = "NOOP";
	}

	public class WalkOp : IOperation
	{
		public string Name { get; init; }

		public WalkOp(Direction direction)
		{
			Name = $"WALK_{direction.ToString().ToUpperInvariant()}";
		}
	}

	public class ThrowOp : IOperation
	{
		public string Name { get; init; } = "THROW";
		public int? X { get; set; }
		public int? Y { get; set; }

		public ThrowOp()
		{
		}

		public ThrowOp(int x, int y)
		{
			X = x;
			Y = y;
		}
	}

	public class LookOp : IOperation
	{
		public string Name { get; init; } = "LOOK";
		public double? Range { get; set; }

		public LookOp()
		{
		}

		public LookOp(double range)
		{
			Range = range;
		}
	}

	public enum EntityType
	{
		Bot,
	}

	public class Me
	{
		public int X { get; set; }
		public int Y { get; set; }
		public int Coins { get; set; }

		[JsonPropertyName("view_range")]
		public double ViewRange { get; set; }
	}

	public class Meta
	{
		public int W { get; set; }
		public int H { get; set; }
		public int Tick { get; set; }
		public string? Name { get; set; }
	}

	public class Entity
	{
		public int X { get; set; }
		public int Y { get; set; }
		public string? Type { get; set; }
	}
}