using EdjCase.JsonRpc.Router;
using EdjCase.JsonRpc.Router.Abstractions;
using Wabooorrt.BotApi;
using System.Collections.Generic;

namespace Wabooorrt
{
	[RpcRoute("jsonrpc")]
	public class BotController : RpcController
	{
		private readonly IBotLogic _logic;

		public BotController(IBotLogic logic)
		{
			_logic = logic;
		}

		public IRpcMethodResult NextAction(Me me, Meta meta, List<Entity> entities)
		{
			return this.Ok(_logic.NextAction(me, meta, entities));
		}

		public IRpcMethodResult Health()
		{
			return this.Ok(true);
		}
	}
}