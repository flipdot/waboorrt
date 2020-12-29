using System;
using Microsoft.Extensions.Logging;
using System.Text.Json;
using Wabooorrt.BotApi;
using System.Collections.Generic;

namespace Wabooorrt
{
	public interface IBotLogic
	{
		IOperation NextAction(Me me, Meta meta, List<Entity> entities);
	}
}